#!/usr/bin/python3

import json
from http import HTTPStatus
from typing import List

from requests import Response

from sk_schemas.inet import IpModel, IpSubnetModel, RouteModel
from sk_schemas.intf import (
    API_INTERFACES_V1,
    IfaceRoleSet,
    IfaceRoleTypes,
    IfaceSettings,
)
from sk_schemas.stats import StatsStringModel

from .client_base import HttpClient


class ClientIntfMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def get_interface_settings(
        self,
    ) -> tuple[Response, List[IfaceSettings]]:
        resp = self.http_client.http_get(API_INTERFACES_V1 + "/settings")
        if resp and resp.status_code == HTTPStatus.OK:
            ret_list = []
            intf_list = resp.json()
            for dict in intf_list:
                ret_list.append(IfaceSettings(**dict))
            return resp, ret_list

        return resp, []

    def get_lan_interface(self):
        resp, if_list = self.get_interface_by_role("lan")
        if if_list is not None and len(if_list) > 0:
            return if_list[0]
        else:
            return None

    def get_wan_interface(self):
        resp, if_list = self.get_interface_by_role("wan")
        if if_list is not None and len(if_list) > 0:
            return if_list[0]
        else:
            return None

    def get_interface_by_role(self, role: str) -> tuple[Response, List[IfaceSettings]]:
        role = IfaceRoleTypes(role).value

        resp = self.http_client.http_get(API_INTERFACES_V1 + "/role/" + str(role))
        if resp and resp.status_code == HTTPStatus.OK:
            ret_list = []
            intf_list = resp.json()
            for dict in intf_list:
                ret_list.append(IfaceSettings(**dict))
            return resp, ret_list

        return resp, []

    def set_interface_roles(self, wan_mac_addr: str, lan_mac_addr: str) -> Response:

        subnet_data = json.loads(
            IfaceRoleSet(
                wan_mac_addr=wan_mac_addr, lan_mac_addr=lan_mac_addr
            ).model_dump_json()
        )
        return self.http_client.http_post(API_INTERFACES_V1 + "/role", json=subnet_data)

    def get_interface_by_name(
        self, iface_name: str
    ) -> tuple[Response, IfaceSettings | None]:
        resp = self.http_client.http_get(API_INTERFACES_V1 + "/" + str(iface_name))
        if resp and resp.status_code == HTTPStatus.OK:
            intf = resp.json()
            if intf:
                return resp, IfaceSettings(**intf)

        return resp, None

    def set_interface_ip(self, interface_name: str, addr: str) -> Response:

        subnet_data = json.loads(IpSubnetModel(subnet=addr).model_dump_json())  # type: ignore
        return self.http_client.http_post(
            API_INTERFACES_V1 + f"/{interface_name}/ip", json=subnet_data
        )

    def get_interface_ips(
        self,
        iface_name: str,
    ) -> tuple[Response, List[IpSubnetModel]]:
        ret_list = []

        response = self.http_client.http_get(API_INTERFACES_V1 + f"/{iface_name}/ip")

        if response and response.status_code == HTTPStatus.OK:
            response_list = response.json()
            for resp_json in response_list:
                ret_list.append(IpSubnetModel(**resp_json))

        return response, ret_list

    def del_interface_ip(self, interface_name: str, ip_subnet: str) -> Response:

        subnet_data = json.loads(IpSubnetModel(subnet=ip_subnet).model_dump_json())  # type: ignore
        return self.http_client.http_delete(
            API_INTERFACES_V1 + f"/{interface_name}/ip", json=subnet_data
        )

    def get_ip_routes(
        self,
    ) -> tuple[Response, StatsStringModel | None]:
        resp = self.http_client.http_get(API_INTERFACES_V1 + "/ip/routes")
        if resp and resp.status_code == HTTPStatus.OK:
            json_resp = resp.json()
            return resp, StatsStringModel(**json_resp)

        return resp, None

    def get_ip_routes_saved(
        self,
    ) -> tuple[Response, list[RouteModel] | None]:
        resp = self.http_client.http_get(API_INTERFACES_V1 + "/ip/routes-saved")
        ret_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            for resp_json in resp.json():
                ret_list.append(RouteModel(**resp_json))

            return resp, ret_list

        return resp, None

    def add_ip_route(
        self, ip_subnet: str, interface_name: str | None, gateway_ip: str | None
    ) -> Response:

        gw_ip = IpModel(ip=gateway_ip) if gateway_ip else None  # type: ignore
        ip_sub = IpSubnetModel(subnet=ip_subnet) if ip_subnet else None  # type: ignore

        data = json.loads(
            RouteModel(
                if_name=interface_name,
                ip_subnet=ip_sub,  # type: ignore
                gateway_ip=gw_ip,  # type: ignore
            ).model_dump_json()
        )

        return self.http_client.http_post(API_INTERFACES_V1 + "/ip/route", json=data)

    def delete_ip_route(
        self, ip_subnet: str, interface_name: str | None, gateway_ip: str | None
    ) -> Response:

        gw_ip = IpModel(ip=gateway_ip) if gateway_ip else None  # type: ignore
        ip_sub = IpSubnetModel(subnet=ip_subnet) if ip_subnet else None  # type: ignore

        data = json.loads(
            RouteModel(
                if_name=interface_name,
                ip_subnet=ip_sub,  # type: ignore
                gateway_ip=gw_ip,  # type: ignore
            ).model_dump_json()
        )

        return self.http_client.http_delete(API_INTERFACES_V1 + "/ip/route", json=data)
