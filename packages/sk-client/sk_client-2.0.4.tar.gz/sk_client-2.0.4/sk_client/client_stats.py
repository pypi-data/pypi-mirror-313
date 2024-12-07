#!/usr/bin/python3

from http import HTTPStatus
from typing import List

from requests import Response

from sk_schemas.stats import (
    API_STATS_V1,
    API_STATS_V2,
    DpStats,
    FileDataModel,
    StatsStringModel,
)

from .client_base import HttpClient


class ClientStatsMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_stats_string(
        self, api_endpoint: str
    ) -> tuple[Response, StatsStringModel | None]:
        resp = self.http_client.http_get(api_endpoint)

        if resp and resp.status_code == HTTPStatus.OK:
            stats_json = resp.json()
            return resp, StatsStringModel(**stats_json)

        return resp, None

    def get_dp_stats(self, api_endpoint: str) -> tuple[Response, DpStats | None]:
        resp = self.http_client.http_get(api_endpoint)

        if resp and resp.status_code == HTTPStatus.OK:
            stats_json = resp.json()
            return resp, DpStats(**stats_json)

        return resp, None

    def get_history_api(self, api_endpoint: str) -> tuple[Response, list[DpStats]]:

        resp = self.http_client.http_get(api_endpoint)

        ret = []
        if resp and resp.status_code == HTTPStatus.OK:
            for k in resp.json():
                ret.append(DpStats(**k))
            return resp, ret
        return resp, ret

    def get_hw_stats(self, iface_name=None) -> tuple[Response, StatsStringModel | None]:

        iface_ep = ""
        if iface_name:
            iface_ep = f"/{iface_name}"

        return self.get_stats_string(API_STATS_V1 + "/hw" + iface_ep)

    def get_ipsec_stats(self) -> tuple[Response, StatsStringModel | None]:

        return self.get_stats_string(API_STATS_V1 + "/ipsec")

    def get_ipsec_counter_history(
        self,
    ) -> tuple[Response, list[DpStats]]:
        return self.get_history_api(API_STATS_V1 + "/history/ipsec")

    def get_error_counter_history(
        self,
    ) -> tuple[Response, list[DpStats]]:
        return self.get_history_api(API_STATS_V1 + "/history/errors")

    def get_iface_counter_history(
        self,
    ) -> tuple[Response, list[DpStats]]:
        return self.get_history_api(API_STATS_V1 + "/history/iface")

    def get_sa_counter_history(
        self,
    ) -> tuple[Response, list[DpStats]]:
        return self.get_history_api(API_STATS_V1 + "/history/sas")

    def get_runtime_stats(self) -> tuple[Response, StatsStringModel | None]:
        return self.get_stats_string(API_STATS_V1 + "/runtime")

    def get_error_stats(
        self,
    ) -> tuple[Response, StatsStringModel | None]:
        return self.get_stats_string(API_STATS_V1 + "/errors")

    def get_error_stats_v2(
        self,
    ) -> tuple[Response, DpStats | None]:
        return self.get_dp_stats(API_STATS_V2 + "/errors")

    def get_iface_stats(self) -> tuple[Response, DpStats | None]:
        return self.get_dp_stats(API_STATS_V1 + "/iface")

    def get_crypto_stats(self) -> tuple[Response, List[FileDataModel]]:

        resp = self.http_client.http_get(API_STATS_V1 + "/crypto")

        resp_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            data = resp.json()
            for k in data:
                resp_list.append(FileDataModel(**k))
        return resp, resp_list

    def get_acl_session_stats(self) -> tuple[Response, DpStats | None]:
        return self.get_dp_stats(API_STATS_V1 + "/acl-session")

    def get_acl_session_details(self) -> tuple[Response, StatsStringModel | None]:
        return self.get_stats_string(API_STATS_V1 + "/acl-session-details")

    def get_acl_session_history(
        self,
    ) -> tuple[Response, list[DpStats]]:
        return self.get_history_api(API_STATS_V1 + "/history/acl-session")
