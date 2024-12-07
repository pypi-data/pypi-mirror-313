#!/usr/bin/python3

import json
import time
from http import HTTPStatus
from typing import List

from requests import Response

from sk_schemas.ipsec import (
    API_IPSEC_V1,
    ConnCreateModel,
    ConnectionModel,
    ConnectionSaModel,
    NameModel,
    SAModel,
)

from .client_base import HttpClient


class ClientIpsecMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_loaded_connections(
        self,
    ) -> List[ConnectionModel] | None:
        resp = self.http_client.http_get(API_IPSEC_V1 + "/connections/loaded")
        if resp and resp.status_code == HTTPStatus.OK:
            ret_list = []
            conn_list = resp.json()
            for sa_dict in conn_list:
                ret_list.append(ConnectionModel(**sa_dict))
            return ret_list

        return None

    def get_saved_connections(
        self,
    ) -> List[ConnCreateModel] | None:
        resp = self.http_client.http_get(API_IPSEC_V1 + "/connections")
        if resp and resp.status_code == HTTPStatus.OK:
            ret_list = []
            conn_list = resp.json()
            for sa_dict in conn_list:
                ret_list.append(ConnCreateModel(**sa_dict))
            return ret_list

        return None

    def get_conn_in_list(
        self, conn_list: List[ConnectionModel], conn_name: str
    ) -> ConnectionModel | None:
        for conn in conn_list:
            if conn.name == conn_name:
                return conn
        return None

    def get_sas(
        self,
    ) -> List[SAModel]:
        ret_list: List[SAModel] = []

        resp = self.http_client.http_get(API_IPSEC_V1 + "/sas")
        if resp and resp.status_code == HTTPStatus.OK:
            sa_list = resp.json()
            if not sa_list:
                return ret_list
            for sa_dict in sa_list:
                ret_list.append(SAModel(**sa_dict))
            return ret_list
        else:
            print(
                f"Failed to get SA list on {self.http_client.address} response: {resp}"
            )
            return ret_list

    def add_connection(
        self,
        conn_model: ConnCreateModel,
        load_conn=True,
        wait_activate_time: float | None = None,
    ) -> tuple[bool, Response]:
        # first upload the connection so its saved
        response = self.http_client.http_post(
            API_IPSEC_V1 + "/connections", json=json.loads(conn_model.model_dump_json())
        )
        ret = self.http_client.check_job_response(response)

        if ret and response.status_code == HTTPStatus.ACCEPTED and load_conn:
            print(f"Loading {conn_model.name}")
            ret, response = self.load_connection(conn_model.name)
            if wait_activate_time:
                time.sleep(wait_activate_time)
        return ret, response

    def modify_connection(
        self,
        conn_name: str,
        conn_model: ConnCreateModel,
        activate=True,
        wait_activate_time: float | None = None,
    ) -> tuple[bool, Response]:
        response = self.http_client.http_put(
            API_IPSEC_V1 + "/connections/" + conn_name,
            json=json.loads(conn_model.model_dump_json()),
        )
        ret = self.http_client.check_job_response(response)

        if ret and response.status_code == HTTPStatus.ACCEPTED and activate:
            print(f"Activating {conn_model.name}")
            ret, response = self.load_connection(conn_model.name)
            if wait_activate_time:
                time.sleep(wait_activate_time)
        return ret, response

    def initiate_child_sa(self, conn_name: str, child_name: str) -> bool:
        data = ConnectionSaModel(
            connection_name=NameModel(name=conn_name),
            sa_name=NameModel(name=child_name),
        )
        json_data = json.loads(data.model_dump_json())
        response = self.http_client.http_post(
            API_IPSEC_V1 + "/sas/initiate-child", json=json_data
        )
        return self.http_client.check_job_response(response)

    def terminate_child_sa(self, conn_name: str, child_name: str) -> bool:
        data = ConnectionSaModel(
            connection_name=NameModel(name=conn_name),
            sa_name=NameModel(name=child_name),
        )
        json_data = json.loads(data.model_dump_json())
        response = self.http_client.http_post(
            API_IPSEC_V1 + "/sas/terminate-child", json=json_data
        )
        return self.http_client.check_job_response(response, ignore_job_failure=True)

    def initiate_ike_conn(self, conn_name: str) -> bool:
        model = NameModel(name=conn_name)
        json_data = json.loads(model.model_dump_json())
        response = self.http_client.http_post(
            API_IPSEC_V1 + "/sas/initiate-ike", json=json_data
        )
        return self.http_client.check_job_response(response)

    def terminate_ike_conn(self, conn_name: str) -> bool:
        model = NameModel(name=conn_name)
        json_data = json.loads(model.model_dump_json())
        response = self.http_client.http_post(
            API_IPSEC_V1 + "/sas/terminate-ike", json=json_data
        )
        return self.http_client.check_job_response(response, ignore_job_failure=True)

    def load_connection(self, name: str) -> tuple[bool, Response]:
        response = self.http_client.http_post(
            API_IPSEC_V1 + "/connections/loaded/" + str(name)
        )
        return self.http_client.check_job_response(response), response

    def unload_connection(self, name: str) -> tuple[bool, Response]:
        response = self.http_client.http_delete(
            API_IPSEC_V1 + "/connections/loaded/" + str(name)
        )
        return self.http_client.check_job_response(response), response

    def delete_connection(self, conn_name: str) -> bool:
        model = NameModel(name=conn_name)
        json_data = json.loads(model.model_dump_json())
        response = self.http_client.http_delete(
            API_IPSEC_V1 + "/connections", json=json_data
        )
        return self.http_client.check_job_response(response)
