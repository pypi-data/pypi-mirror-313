#!/usr/bin/python3


import random
import secrets
import string
from http import HTTPStatus

from requests import Response

from sk_schemas.certs import SSHPubKeyModel
from sk_schemas.users import (
    API_USERS_V1,
    SSHUserInfo,
    UserCreate,
    UserInfo,
)

from .client_base import HttpClient


def gen_rand_pw(password_length=14):
    pw = ""
    for required_char in [string.digits, "!@#$%^&*()-+?_=,<>/."]:
        pw += "".join(random.choice(required_char))
    return pw + secrets.token_urlsafe(password_length - len(pw))


class ClientUserMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def add_user(self, username="user", password="password", is_admin=False):
        user_register = UserCreate(
            username=username, password=password, is_admin=is_admin
        ).model_dump()

        return self.http_client.http_post(
            API_USERS_V1 + "/register", json=user_register
        )

    def get_users(self) -> tuple[Response, list[UserInfo]]:
        ret_list = []
        resp = self.http_client.http_get(API_USERS_V1 + "/all")
        if resp and resp.status_code == HTTPStatus.OK:
            json_list = resp.json()
            for dict in json_list:
                ret_list.append(UserInfo(**dict))

        return resp, ret_list

    def delete_user(self, username):
        return self.http_client.http_delete(API_USERS_V1 + "/" + username)

    def add_ssh_user(self, username: str, public_key: str):
        ssh_user = SSHUserInfo(
            username=username, public_key=SSHPubKeyModel(data=public_key)
        ).model_dump()

        return self.http_client.http_post(API_USERS_V1 + "/ssh", json=ssh_user)

    def delete_ssh_user(self, username: str):
        return self.http_client.http_delete(API_USERS_V1 + "/ssh/" + username)

    def get_ssh_users(self) -> tuple[Response, list[SSHUserInfo]]:
        resp = self.http_client.http_get(API_USERS_V1 + "/ssh/all")
        ret_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            json_list = resp.json()
            for dict in json_list:
                ret_list.append(SSHUserInfo(**dict))

        return resp, ret_list

    def get_user_me(self, token=None) -> tuple[Response, UserInfo | None]:
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            resp = self.http_client.http_get(API_USERS_V1 + "/me", headers=headers)
        else:
            resp = self.http_client.http_get(API_USERS_V1 + "/me")

        if resp and resp.status_code == HTTPStatus.OK:
            return resp, UserInfo(**resp.json())
        else:
            return resp, None
