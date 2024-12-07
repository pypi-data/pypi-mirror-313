#!/usr/bin/python3


import logging
import os
import time
from http import HTTPStatus
from typing import Callable

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter

from sk_client.cert_utils import CertUtils
from sk_schemas.sys import API_SYS_V1, JobNumber, JobStatus, JobStatusEnum

ADDRESS = "localhost"
HTTP_PORT = 8000
HTTPS_PORT = 443
API_ROOT = "/api"


def merge_dicts(dict_first: dict, dict_second: dict):
    merged_dict = dict_first.copy()
    merged_dict.update(dict_second)
    return merged_dict


class InitialUserRequiredError(Exception):
    pass


class OTPError(Exception):
    pass


class InvalidLoginError(Exception):
    pass


class PasswordExpiredError(Exception):
    pass


class UserLockedError(Exception):
    pass


class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return


class HttpClient:

    def __init__(
        self,
        address=ADDRESS,
        port=HTTPS_PORT,
        use_https=True,
        username=None,
        password=None,
        access_token=None,
        https_root_cert_file=None,
        use_hostname_ssl=False,
        hostname=None,
        cert_verify=True,
        client_key_file: str | None = None,
        client_cert_file: str | None = None,
        max_retries: int = 0,
        auto_relogin: bool = True,
        log_level: int = logging.DEBUG,
        raise_on_login_error=True,
        auto_password_update=False,
        pw_change_handler: Callable[[str], str] | None = None,
        otp_handler: Callable[[str], str] | None = None,
        initial_user_handler: Callable[[], tuple[str, str]] | None = None,
        wait_for_jobs: bool = True,
        timeout: int = 5,
        ssl_context=None,
    ):
        self.address = address
        self.port = port
        self.schema = None
        self.api_url = ""
        self.session = None
        self.kwargs: dict = {}
        self.max_retries = max_retries
        self.ssl_context = ssl_context

        self.auto_relogin = auto_relogin
        self.try_relogin = auto_relogin
        self.raise_on_login_error = raise_on_login_error
        self.otp_value: str | None = None

        self.access_token = access_token
        self.username = username
        self.password = password
        self.use_hostname_ssl = use_hostname_ssl
        self.hostname = hostname
        self.use_https = use_https
        self.wait_for_jobs = wait_for_jobs

        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        self.cert_verify = cert_verify
        self.root_cert_file = https_root_cert_file

        self.client_cert_file = client_cert_file
        self.client_key_file = client_key_file
        self.auto_password_update = auto_password_update
        self.pw_change_handler = pw_change_handler
        self.otp_handler = otp_handler
        self.initial_user_handler = initial_user_handler

        if client_key_file and client_cert_file:
            self.enable_mutual_auth(
                client_key_file, client_cert_file, refresh_session=False
            )

        if self.use_https:
            self.api_url += "https://"
            if self.root_cert_file:
                self.enable_cert_verify(self.root_cert_file, refresh_session=False)
            else:
                if not self.cert_verify:
                    self.disable_cert_verify()
                else:
                    raise ValueError(
                        "Root cert not provided - required for HTTPS verification"
                    )
        else:
            self.api_url += "http://"

        self.api_url += self.address + ":" + str(self.port)
        self.api_url += API_ROOT
        self.logger.debug("Using API URL:" + self.api_url)

        self.timeout = timeout
        self.set_kwargs(timeout=self.timeout)

    def __del__(self):
        self.close_session()

    def close_session(self):
        if self.session:
            self.session.close()
            self.session = None

    def open_session(self) -> Session:
        if self.session:
            return self.session
        self.session = Session()
        assert self.session

        if self.use_hostname_ssl:
            from requests_toolbelt.adapters import host_header_ssl

            if self.hostname is None:
                # discover the hostname from the server's HTTPS certificate
                try:
                    self.hostname = CertUtils.get_server_subject_alt_name(
                        address=self.address
                    )
                except Exception:
                    pass
                if self.hostname is None:
                    if not self.kwargs["verify"]:
                        self.hostname = "unknown"
                    else:
                        raise ValueError("Failed to discover hostname from server cert")
                self.logger.debug("Using hostname: " + self.hostname)

            self.session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
            self.set_hostname(self.hostname)
        if self.max_retries:
            from requests.adapters import HTTPAdapter, Retry

            retries = Retry(
                total=self.max_retries,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504],
            )

            self.session.mount("https://", HTTPAdapter(max_retries=retries))

        if self.ssl_context:

            # mount adapter with custom SSL context
            adapter = SSLAdapter(ssl_context=self.ssl_context)
            self.session.mount("https://", adapter)

        return self.session

    def get_hostname(self) -> str | None:
        return self.hostname

    def set_hostname(self, hostname: str):
        self.hostname = hostname
        self.logger.debug("Using HTTP header Hostname: " + self.hostname)
        self.kwargs["headers"] = merge_dicts(
            self.kwargs.get("headers", {}), {"Host": self.hostname}
        )
        return True

    def enable_mutual_auth(
        self, client_key_file: str, client_cert_file: str, refresh_session: bool = True
    ):
        if os.path.isfile(client_key_file) and os.path.isfile(client_cert_file):
            self.client_key_file = client_key_file
            self.client_cert_file = client_cert_file
            self.logger.debug("Using Client Cert: " + self.client_cert_file)
            self.logger.debug("Using Client Key: " + self.client_key_file)
            self.kwargs["cert"] = (client_cert_file, client_key_file)

            if refresh_session:
                self.close_session()
                self.open_session()
        else:
            raise ValueError("Client cert/key not provided - required for mutual auth")

    def disable_mutual_auth(self):
        self.kwargs["cert"] = None

    def disable_cert_verify(self):
        self.logger.debug("Disabled HTTPS Certificate Verification!!")
        self.kwargs["verify"] = False

    def enable_cert_verify(
        self, root_cert_file: str | None = None, refresh_session: bool = False
    ):
        if root_cert_file is None:
            root_cert_file = self.root_cert_file

        if root_cert_file and os.path.isfile(root_cert_file):
            self.logger.debug(
                "Enabled HTTPs Certificate Verification using " + root_cert_file
            )
            self.kwargs["verify"] = root_cert_file
            if refresh_session:
                self.close_session()
                self.open_session()
        else:
            raise ValueError("Root cert not provided - required for HTTPS verification")

    def set_max_retries(self, max_retries: int = 5):
        self.max_retries = max_retries
        self.close_session()
        self.open_session()

    def set_kwargs(self, **kwargs):
        self.kwargs = merge_dicts(self.kwargs, kwargs) if self.kwargs else kwargs
        self.logger.debug("Requests Kwargs: " + repr(self.kwargs))

    def do_http(self, action, endpoint, retries=3, **kwargs) -> Response:
        self.open_session()
        combined_kwargs = merge_dicts(self.kwargs, kwargs)

        if action not in ["get", "post", "patch", "delete", "put"]:
            raise ValueError("Invalid action: " + action)

        exception = None
        # get the session attribute and run it with the combined args
        try:
            resp = getattr(self.session, action)(
                self.api_url + endpoint, **combined_kwargs
            )
        except requests.exceptions.SSLError as e:
            self.logger.debug(f"SSL Exception {e}")
            exception = e
            if "self-signed certificate" in str(e):
                self.disable_cert_verify()
        except Exception as e:
            self.logger.debug(f"Exception {e} - Reconnecting and retrying operation")
            exception = e

        if exception is not None:
            if retries > 0:
                self.close_session()
                self.open_session()
                return self.do_http(action, endpoint, retries=retries - 1, **kwargs)
            else:
                raise exception

        if resp.status_code == HTTPStatus.UNAUTHORIZED and self.try_relogin:
            # auth Token expired - need to get a new auth token
            self.try_relogin = False
            if "auth" in endpoint and "token" in endpoint:
                resp = self.parse_login_failure(resp)
                self.try_relogin = self.auto_relogin
                return resp
            else:
                # get new auth token
                self.relogin()
                # retry the request
                resp = self.do_http(action, endpoint, **kwargs)
                if resp.status_code != HTTPStatus.UNAUTHORIZED:
                    self.try_relogin = self.auto_relogin

        return resp

    def http_get(self, endpoint, **kwargs) -> Response:
        return self.do_http("get", endpoint, **kwargs)

    def http_post(self, endpoint, **kwargs) -> Response:
        return self.do_http("post", endpoint, **kwargs)

    def http_put(self, endpoint, **kwargs) -> Response:
        return self.do_http("put", endpoint, **kwargs)

    def http_patch(self, endpoint, **kwargs) -> Response:
        return self.do_http("patch", endpoint, **kwargs)

    def http_delete(self, endpoint, **kwargs) -> Response:
        return self.do_http("delete", endpoint, **kwargs)

    def check_job_response(
        self, response: Response, timeout=10, ignore_job_failure=False
    ) -> bool:
        if response.status_code == HTTPStatus.ACCEPTED:
            job = JobNumber(**response.json())
            if not self.wait_for_jobs:
                print("Not waiting for jobs")
                return True

            status = self.wait_for_job_done(job, timeout)
            if status and status.status == JobStatusEnum.COMPLETED:
                return True
            else:
                if ignore_job_failure:
                    print("Ignore job failure")
                    return True
                else:
                    if status is None:
                        print(
                            f"{self.address} Job {job.id} failed reading status -  ({job.descritpion}) - {response.text} "
                        )
                    return False
        print(f"{self.address} Failed job response: " + response.text)
        return False

    def wait_for_job_done(self, job: JobNumber, timeout=10) -> JobStatus | None:
        start = time.time()
        status = None
        while time.time() - start < timeout:
            response = self.http_get(API_SYS_V1 + f"/job-status/{job.id}")
            if response and response.status_code == HTTPStatus.OK:
                status = JobStatus(**response.json())
                if status.status != JobStatusEnum.RUNNING:
                    print(
                        f"{self.address} Job {job.id} status: {status.status.value} - ({job.descritpion})"
                    )
                    return status
            # print(f"Job {job_number.id} status: {status}")
            time.sleep(0.1)

        return status

    def upload_file(self, endpoint: str, file_name: str) -> Response:
        files = {"file": open(file_name, "rb")}

        resp = self.http_post(endpoint, files=files)
        return resp

    def parse_login_failure(self, resp) -> Response:
        """Handle login failures. Based on the response status code and text
        call handler functions that have been provided or raise exception."""

        exception: Exception | None = None

        # parse the response status code and text to determine the cause of the failure
        if resp.status_code == HTTPStatus.UNAUTHORIZED:
            if "invalid otp" in resp.text.lower():
                # get OTP and retry login
                if self.otp_handler and self.username and self.password:
                    self.otp_value = self.otp_handler(self.username)
                    resp = self.login(self.username, self.password, otp=self.otp_value)
                    return resp
                else:
                    exception = OTPError("One Time Password Incorrect")
            else:
                exception = InvalidLoginError("Invalid Login")
        elif resp.status_code == HTTPStatus.LOCKED and "Password Expired" in resp.text:
            if self.auto_password_update:
                # change password and try again
                return self.change_password()
            else:
                exception = PasswordExpiredError("Password Expired")

        elif resp.status_code == HTTPStatus.LOCKED:
            exception = UserLockedError("User is Locked")
        elif resp.status_code == HTTPStatus.FORBIDDEN and "No users exist" in resp.text:
            if self.initial_user_handler is not None:
                self.logger.debug("Calling Initial User Handler")
                username, password = self.initial_user_handler()
                return self.initial_user_add(username, password)
            else:
                exception = InitialUserRequiredError("Initial User Required")

        else:
            self.logger.debug("General Login Failure: " + repr(resp.status_code))
            exception = ConnectionError(
                "Failed with status code: " + repr(resp.status_code)
            )

        if self.raise_on_login_error and exception is not None:
            raise exception
        else:
            return resp

    def get_connection_details(self):
        # get the current Session and return the SSL connection details
        assert self.session
        with self.session.get(
            self.api_url + "api/users/v1/me", stream=True, **self.kwargs
        ) as response:
            if (
                response.raw._connection is None
                or response.raw._connection.sock is None
            ):
                raise Exception("No SSL Socket")
            sock = response.raw._connection.sock
            cipher = sock.cipher()  # type: ignore
            # peer_cert = sock.getpeercert()  # type: ignore
            # shared_ciphers = sock.shared_ciphers()  # type: ignore
        return cipher

    def change_password(
        self, new_password: str | None = None, relogin: bool = True
    ) -> Response:
        assert self.username and self.password
        from sk_client.client_auth import ClientAuthMgr
        from sk_client.client_users import gen_rand_pw

        if new_password is None:
            if self.pw_change_handler is not None:
                self.logger.debug(
                    "Calling Password Change Handler for user " + self.username
                )
                new_password = self.pw_change_handler(self.username)
            else:
                new_password = gen_rand_pw()
                self.logger.debug(f"Generated New Password for user {self.username}")

        resp = ClientAuthMgr(self).user_change_password(
            username=self.username,
            old_password=self.password,
            new_password=new_password,
        )
        if resp.status_code == HTTPStatus.OK:
            self.password = new_password
            if relogin:
                return self.relogin()
            else:
                return resp
        else:
            self.logger.debug("Failed Changing Password: " + repr(resp.status_code))
            return self.parse_login_failure(resp)

    def relogin(
        self,
    ) -> Response:
        if self.username is None or self.password is None:
            raise Exception("Cannot relogin with no username or password")
        return self.login(self.username, self.password, otp=self.otp_value)

    def login(
        self,
        username: str,
        password: str,
        otp: str | None = None,
        update_user: bool = False,
    ) -> Response:
        self.otp_value = otp
        resp = self.auth_token(
            username=username, password=password, client_secret=self.otp_value
        )
        if resp.status_code == HTTPStatus.OK:
            self.access_token = resp.json()["access_token"]
            kwargs = {"headers": {"Authorization": f"Bearer {self.access_token}"}}
            if update_user:
                self.username = username
                self.password = password
            # add the headers to future sessions
            self.set_kwargs(**kwargs)
            return resp
        else:
            self.logger.debug("Failed Login: " + repr(resp.status_code))
            return self.parse_login_failure(resp)

    def initial_user_add(self, username: str, password: str, is_admin=True) -> Response:
        from sk_schemas.users import API_USERS_V1, UserCreate

        user_register = UserCreate(
            username=username, password=password, is_admin=is_admin
        ).model_dump()

        resp = self.http_post(API_USERS_V1 + "/initial", json=user_register)
        if resp.status_code == HTTPStatus.CREATED:
            # store the username/password
            self.username = username
            self.password = password
            return self.login(username=self.username, password=self.password)
        else:
            self.logger.debug("Failed adding initial user: " + repr(resp.status_code))
            return self.parse_login_failure(resp)

    def auth_token(
        self,
        username: str,
        password: str,
        scope: str | None = "",
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> Response:
        login = {
            "username": username,
            "password": password,
            "scope": scope,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        from sk_schemas.auth import API_AUTH_V1_TOKEN

        return self.http_post(API_AUTH_V1_TOKEN, data=login)
