#!/usr/bin/python3


from http import HTTPStatus

from requests import Response

from sk_schemas.auth import (
    API_AUTH_V1,
    OtpUriModel,
    SysSecuritySettings,
)

from .client_base import HttpClient


class ClientAuthMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def user_login(self, username="user", password="string", otp_value=None):
        login = {
            "username": username,
            "password": password,
            "scope": "",
            "client_id": None,
            "client_secret": otp_value,
        }

        return self.http_client.http_post(API_AUTH_V1 + "/token", data=login)

    def user_change_password(
        self,
        username="user",
        old_password="string",
        otp_value=None,
        new_password="string",
    ):
        from sk_schemas.users import UserChangePassword, UserPassword

        login = UserChangePassword(
            username=username,
            password=old_password,
            scope="",
            client_id=None,
            client_secret=otp_value,
            new_password=UserPassword(password=new_password),
        ).model_dump()

        return self.http_client.http_post(API_AUTH_V1 + "/change-password", json=login)

    def get_auth_settings(self) -> tuple[Response, SysSecuritySettings | None]:
        resp = self.http_client.http_get(API_AUTH_V1 + "/settings")
        if resp and resp.status_code == HTTPStatus.OK:
            return resp, SysSecuritySettings(**resp.json())

        return resp, None

    def set_auth_settings(
        self,
        otp_enforce=False,
        token_timeout_sec=30 * 60,
        password_timeout_sec=86400 * 90,
    ) -> Response:
        data = SysSecuritySettings(
            otp_enforce=otp_enforce,
            token_timeout_sec=token_timeout_sec,
            password_timeout_sec=password_timeout_sec,
        ).model_dump()

        resp = self.http_client.http_post(API_AUTH_V1 + "/settings", json=data)
        return resp

    def user_otp_enable(self) -> Response:
        return self.http_client.http_post(API_AUTH_V1 + "/otp/enable")

    def user_otp_disable(self) -> Response:
        return self.http_client.http_post(API_AUTH_V1 + "/otp/disable")

    def user_otp_generate_qrcode(self) -> Response:
        return self.http_client.http_post(API_AUTH_V1 + "/otp/generate-qrcode")

    def user_otp_generate_qrcode_b64(self) -> Response:
        return self.http_client.http_post(API_AUTH_V1 + "/otp/generate-qrcode-b64")

    def user_otp_generate_uri(self) -> tuple[Response, OtpUriModel | None]:
        resp = self.http_client.http_post(API_AUTH_V1 + "/otp/generate-uri")
        if resp and resp.status_code == HTTPStatus.OK:
            return resp, OtpUriModel(**resp.json())
        else:
            return resp, None
