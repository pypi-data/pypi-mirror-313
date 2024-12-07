#!/usr/bin/python3

import json
from http import HTTPStatus

from requests import Response

from sk_schemas.crypto import (
    API_CRYPTO_V1,
    CryptoSettings,
)

from .client_base import HttpClient


class ClientCryptoMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_crypto_settings(
        self,
    ) -> CryptoSettings | None:
        resp = self.http_client.http_get(API_CRYPTO_V1 + "/settings")
        if resp and resp.status_code == HTTPStatus.OK:
            return CryptoSettings(**resp.json())

        return None

    def set_crypto_settings(
        self,
        data: CryptoSettings,
    ) -> Response:
        response = self.http_client.http_put(
            API_CRYPTO_V1 + "/settings",
            json=json.loads(data.model_dump_json()),
        )

        return response
