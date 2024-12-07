#!/usr/bin/python3

import json
import tempfile
import time
from datetime import datetime
from http import HTTPStatus
from typing import List

from pydantic.networks import IPv4Address
from requests import Response

from sk_schemas.certs import SSLVerifClientEnum, TLSConfigModel
from sk_schemas.intf import HostnameModel
from sk_schemas.stats import (
    FileDataModel,
    MachineIDModel,
    StatusModel,
    SystemReportModel,
    SystemVersionModel,
    SysTimeModel,
)
from sk_schemas.sys import (
    API_SYS_V1,
    DEFAULT_DNS_SERVERS,
    DNSConfigModel,
    DNSServer,
    SwupdateStatus,
    SwupdateStatusEnum,
    SyslogConfigModel,
)

from .client_base import HttpClient


class ClientSysMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def system_reboot(self) -> Response | None:
        try:
            resp = self.http_client.http_post(API_SYS_V1 + "/reboot")
            return resp
        except Exception:
            return None

    def check_for_swupdate(self) -> Response:
        resp = self.http_client.http_post(API_SYS_V1 + "/swupdate-check")
        return resp

    def get_swupdate_status(self) -> SwupdateStatus | None:
        response = self.http_client.http_get(API_SYS_V1 + "/swupdate-check-status")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return SwupdateStatus(**data)

        return None

    def wait_swupdate_complete(self, timeout=60) -> SwupdateStatusEnum | None:
        start = time.time()
        swupdate_status = self.get_swupdate_status()
        assert swupdate_status is not None

        while time.time() - start < timeout:
            swupdate_status = self.get_swupdate_status()
            assert swupdate_status is not None
            if (
                swupdate_status.status == SwupdateStatusEnum.IN_PROGRESS
                or swupdate_status.status == SwupdateStatusEnum.INSTALLING
            ):
                print(
                    f"{self.http_client.address} SWupdate status {swupdate_status.status}"
                )
                time.sleep(1)
                continue
            else:
                break

        return swupdate_status.status

    def upload_swupdate_file(self, file_name: str) -> Response:
        resp = self.http_client.upload_file(API_SYS_V1 + "/swupdate", file_name)
        return resp

    def install_swupdate(self) -> Response:
        resp = self.http_client.http_post(API_SYS_V1 + "/swupdate-install")
        return resp

    def delete_swupdate(self) -> Response:
        resp = self.http_client.http_delete(API_SYS_V1 + "/swupdate")
        return resp

    def get_sys_crypto_logs(self) -> tuple[Response, List[FileDataModel]]:
        response = self.http_client.http_get(API_SYS_V1 + "/logs/crypto")
        resp_list = []
        if response and response.status_code == HTTPStatus.OK:
            data_list = response.json()
            for data in data_list:
                resp_list.append(FileDataModel(**data))

        return response, resp_list

    def get_logfile(self, endpoint: str) -> tuple[Response, FileDataModel | None]:
        response = self.http_client.http_get(endpoint)
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, FileDataModel(**data)

        return response, None

    def get_all_sys_logs(self) -> None:
        # get all logs and save to the output directory
        # make a temp directory and save the logs there
        temp_dir = tempfile.mkdtemp(
            prefix=f"vm_{self.http_client.address.replace('.', '_')}_"
        )
        for endpoint in [
            API_SYS_V1 + "/logs/http-access",
            API_SYS_V1 + "/logs/rest-api",
            API_SYS_V1 + "/logs/swupdate",
            API_SYS_V1 + "/logs/ipsec",
            API_SYS_V1 + "/logs/ssh",
            API_SYS_V1 + "/logs/user-auth",
        ]:
            resp, logs = self.get_logfile(endpoint)
            if resp.status_code == HTTPStatus.OK and logs is not None:
                with open(temp_dir + "/" + endpoint.split("/")[-1], "w") as f:
                    print(f"Saving log data to {f.name}")
                    f.write(logs.data.decode("utf-8"))

        print(f"Saved all logs for {self.http_client.address} to {temp_dir}")

    def get_sys_http_access_log(self):
        return self.get_logfile(API_SYS_V1 + "/logs/http-access")

    def get_sys_rest_api_log(self):
        return self.get_logfile(API_SYS_V1 + "/logs/rest-api")

    def get_swupdate_log(self):
        return self.get_logfile(API_SYS_V1 + "/logs/swupdate")

    def get_ipsec_log(self):
        return self.get_logfile(API_SYS_V1 + "/logs/ipsec")

    def get_ssh_log(self):
        return self.get_logfile(API_SYS_V1 + "/logs/ssh")

    def get_sys_user_auth_log(self):
        return self.get_logfile(API_SYS_V1 + "/logs/user-auth")

    def get_sys_report(self) -> tuple[Response, List[SystemReportModel]]:
        response = self.http_client.http_get(API_SYS_V1 + "/system-report")
        resp_list = []
        if response and response.status_code == HTTPStatus.OK:
            data_list = response.json()
            for data in data_list:
                resp_list.append(SystemReportModel(**data))

        return response, resp_list

    def get_system_report_field(self, field_name: str) -> str | None:
        resp, system_report = self.get_sys_report()
        if system_report is None:
            return None
        match = [report.data for report in system_report if report.name == field_name]
        if len(match) == 0:
            return None
        else:
            return match[0]

    def get_sys_status(self) -> tuple[Response, List[StatusModel]]:
        response = self.http_client.http_get(API_SYS_V1 + "/status")
        resp_list = []
        if response and response.status_code == HTTPStatus.OK:
            data_list = response.json()
            for data in data_list:
                resp_list.append(StatusModel(**data))

        return response, resp_list

    def get_sys_time(self) -> tuple[Response, SysTimeModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/time")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, SysTimeModel(**data)

        return response, None

    def get_sys_datetime(
        self,
    ) -> datetime:
        resp, sys_time = self.get_sys_time()
        assert sys_time
        return datetime.fromisoformat(sys_time.time)

    def get_sys_machine_id(self) -> tuple[Response, MachineIDModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/machine-id")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, MachineIDModel(**data)

        return response, None

    def get_sys_version(self) -> tuple[Response, SystemVersionModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/version")

        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, SystemVersionModel(**data)

        return response, None

    def get_hostname(self) -> tuple[Response, HostnameModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/hostname")

        if response and response.status_code == HTTPStatus.OK:
            hostname_model = response.json()
            return response, HostnameModel(**hostname_model)

        return response, None

    def set_hostname(self, hostname: str) -> Response:
        data = json.loads(HostnameModel(hostname=hostname).model_dump_json())
        return self.http_client.http_post(API_SYS_V1 + "/hostname", json=data)

    def get_tls_settings(self) -> tuple[Response, TLSConfigModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/tls_settings")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, TLSConfigModel(**data)

        return response, None

    def set_tls_settings(
        self, enable_ssl_verify_client: bool, ssl_verify_depth: int
    ) -> Response:
        ssl_verify_client = (
            SSLVerifClientEnum.VERIFY_ON
            if enable_ssl_verify_client
            else SSLVerifClientEnum.VERIFY_OFF
        )

        data = json.loads(
            TLSConfigModel(
                ssl_verify_client=ssl_verify_client, ssl_verify_depth=ssl_verify_depth
            ).model_dump_json()
        )
        return self.http_client.http_post(API_SYS_V1 + "/tls_settings", json=data)

    def get_syslog_settings(self) -> tuple[Response, SyslogConfigModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/syslog/settings")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, SyslogConfigModel(**data)

        return response, None

    def set_syslog_settings(
        self,
        enabled: bool,
        server_address: str | None = None,
        server_port: int = 514,
        enable_authentication: bool = False,
    ) -> bool:
        data = json.loads(
            SyslogConfigModel(
                enable_remote_syslog=enabled,
                server_address=IPv4Address(address=server_address) if enabled else None,
                server_port=server_port,
                enable_authentication=enable_authentication,
            ).model_dump_json()
        )
        response = self.http_client.http_post(
            API_SYS_V1 + "/syslog/settings", json=data
        )
        return self.http_client.check_job_response(response)

    def get_dns_settings(self) -> tuple[Response, DNSConfigModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/dns/settings")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, DNSConfigModel(**data)

        return response, None

    def get_dns_status(self) -> tuple[Response, SystemReportModel | None]:
        response = self.http_client.http_get(API_SYS_V1 + "/dns/status")
        if response and response.status_code == HTTPStatus.OK:
            data = response.json()
            return response, SystemReportModel(**data)

        return response, None

    def set_dns_settings(
        self,
        servers: List[DNSServer],
        fallback_servers: List[DNSServer] = DEFAULT_DNS_SERVERS,
        dnssec: bool = False,
    ) -> bool:
        data = json.loads(
            DNSConfigModel(
                servers=servers, fallback_servers=fallback_servers, dnssec=dnssec
            ).model_dump_json()
        )
        response = self.http_client.http_post(API_SYS_V1 + "/dns/settings", json=data)
        return self.http_client.check_job_response(response)
