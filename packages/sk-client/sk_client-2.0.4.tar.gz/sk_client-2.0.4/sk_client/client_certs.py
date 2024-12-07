#!/usr/bin/python3
import json
import os
from http import HTTPStatus
from tempfile import NamedTemporaryFile
from typing import List

from requests import Response

from sk_schemas.certs import (
    API_CERTS_V1,
    CertDetailModel,
    CertInfoModel,
    CertSigningRequestModel,
    CertUsageEnum,
    CsrResponseModel,
    CsrSignedRequestModel,
    CsrUuidModel,
    HexString,
    KeyInfoModel,
    KeyLoadedInfoModel,
)

from .client_base import HttpClient


class ClientCertMgr:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def upload_ca_cert_raw(self, raw_data) -> tuple[Response, CertInfoModel | None]:
        cert_file = NamedTemporaryFile(
            prefix="test_cert", suffix=".pem", dir="/tmp/"
        ).name

        with open(cert_file, "w") as fd:
            fd.write(raw_data)
        ret = self.upload_ca_cert_file(cert_file)

        # remove tmp file:
        os.unlink(cert_file)

        return ret

    def upload_key_file(
        self, endpoint, cert_file
    ) -> tuple[Response, KeyInfoModel | None]:
        resp = self.http_client.upload_file(endpoint, cert_file)
        if resp and resp.status_code == HTTPStatus.ACCEPTED:
            resp_json = resp.json()
            return resp, KeyInfoModel(**resp_json)
        else:
            return resp, None

    def upload_cert_file(
        self, endpoint, cert_file
    ) -> tuple[Response, CertInfoModel | None]:
        resp = self.http_client.upload_file(endpoint, cert_file)
        if resp and resp.status_code == HTTPStatus.ACCEPTED:
            resp_json = resp.json()
            return resp, CertInfoModel(**resp_json)
        else:
            return resp, None

    def upload_ca_cert_file(self, cert_file) -> tuple[Response, CertInfoModel | None]:
        return self.upload_cert_file(API_CERTS_V1 + "/ca", cert_file)

    def upload_user_cert_file(self, cert_file) -> tuple[Response, CertInfoModel | None]:
        return self.upload_cert_file(API_CERTS_V1 + "/user", cert_file)

    def handle_cert_list_response(self, resp) -> list[CertInfoModel]:
        ret_list = []
        json_list = resp.json()
        for resp_json in json_list:
            ret_list.append(CertInfoModel(**resp_json))
        return ret_list

    def get_all_certs(self) -> tuple[Response, list[CertInfoModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/all")
        if resp and resp.status_code == HTTPStatus.OK:
            return resp, self.handle_cert_list_response(resp)
        else:
            return resp, None

    def get_loaded_certs(self) -> tuple[Response, list[CertDetailModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/loaded")
        ret_list = []
        if resp and resp.status_code == HTTPStatus.OK:
            json_list = resp.json()
            for resp_json in json_list:
                ret_list.append(CertDetailModel(**resp_json))
            return resp, ret_list
        else:
            return resp, None

    def get_cas(self) -> tuple[Response, list[CertInfoModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/ca")
        if resp and resp.status_code == HTTPStatus.OK:
            return resp, self.handle_cert_list_response(resp)
        else:
            return resp, None

    def get_user_certs(self) -> tuple[Response, list[CertInfoModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/user")
        if resp and resp.status_code == HTTPStatus.OK:
            return resp, self.handle_cert_list_response(resp)
        else:
            return resp, None

    def delete_private_keys(self, key_fingerprints: List[str]) -> bool:
        json_data = []
        for fingerprint in key_fingerprints:
            model = KeyInfoModel(fingerprint=HexString(fingerprint), algorithm=None)
            json_data.append(json.loads(model.model_dump_json()))

        response = self.http_client.http_delete(
            API_CERTS_V1 + "/private_keys", json=json_data
        )
        return self.http_client.check_job_response(response, ignore_job_failure=False)

    def upload_user_private_key_file(
        self, file
    ) -> tuple[Response, KeyInfoModel | None]:
        return self.upload_key_file(API_CERTS_V1 + "/private_key", file)

    def delete_certs(self, cert_fingerprints: List[str], timeout: int = 10) -> bool:
        json_data = []
        for cert_fingerprint in cert_fingerprints:

            json_data.append(
                json.loads(
                    CertInfoModel(
                        fingerprint=cert_fingerprint, is_ca=None
                    ).model_dump_json()
                )
            )

        response = self.http_client.http_delete(API_CERTS_V1 + "/certs", json=json_data)

        return self.http_client.check_job_response(
            response, ignore_job_failure=False, timeout=timeout
        )

    def delete_all_credentials(self, timeout: int = 10) -> bool:

        response = self.http_client.http_delete(API_CERTS_V1 + "/all_credentials")

        return self.http_client.check_job_response(
            response, ignore_job_failure=False, timeout=timeout
        )

    def get_all_cert_details(self) -> tuple[Response, list[CertDetailModel]]:
        response = self.http_client.http_get(API_CERTS_V1 + "/all/details")
        resp_list = []
        if response and response.status_code == HTTPStatus.OK:
            for model_data in response.json():
                resp_list.append(CertDetailModel(**model_data))

        return response, resp_list

    def get_cert_details(
        self, cert_fingerprint: str
    ) -> tuple[Response, CertDetailModel | None]:
        model = CertInfoModel(fingerprint=cert_fingerprint, is_ca=None)
        json_data = json.loads(model.model_dump_json())
        response = self.http_client.http_get(API_CERTS_V1 + "/details", json=json_data)
        if response and response.status_code == HTTPStatus.OK:
            return response, CertDetailModel(**response.json())
        else:
            return response, None

    def get_cert_details_by_id(
        self, cert_id: str
    ) -> tuple[Response, CertDetailModel | None]:
        response = self.http_client.http_get(API_CERTS_V1 + "/details/id/" + cert_id)
        if response and response.status_code == HTTPStatus.OK:
            return response, CertDetailModel(**response.json())
        else:
            return response, None

    def get_cert_details_by_fingerprint(
        self, fingerprint: str
    ) -> tuple[Response, CertDetailModel | None]:
        response = self.http_client.http_get(
            API_CERTS_V1 + "/details/fingerprint/" + fingerprint
        )
        if response and response.status_code == HTTPStatus.OK:
            return response, CertDetailModel(**response.json())
        else:
            return response, None

    def get_https_cert_details(self) -> tuple[Response, CertDetailModel | None]:
        response = self.http_client.http_get(API_CERTS_V1 + "/tls/server-cert")
        if response and response.status_code == HTTPStatus.OK:
            return response, CertDetailModel(**response.json())
        else:
            return response, None

    def get_https_cert_info(self) -> tuple[Response, CertInfoModel | None]:
        response = self.http_client.http_get(API_CERTS_V1 + "/tls/server-cert/info")
        if response and response.status_code == HTTPStatus.OK:
            if response.json() is None:
                return response, None
            return response, CertInfoModel(**response.json())
        else:
            return response, None

    def get_syslog_ca_cert_details(self) -> tuple[Response, CertDetailModel | None]:
        response = self.http_client.http_get(API_CERTS_V1 + "/syslog/ca")
        if response and response.status_code == HTTPStatus.OK:
            if response.json() is None:
                return response, None
            return response, CertDetailModel(**response.json())
        else:
            return response, None

    def get_syslog_client_cert_details(self) -> tuple[Response, CertDetailModel | None]:
        response = self.http_client.http_get(API_CERTS_V1 + "/syslog/client-cert")
        if response and response.status_code == HTTPStatus.OK:
            if response.json() is None:
                return response, None
            return response, CertDetailModel(**response.json())
        else:
            return response, None

    def delete_https_server_cert(self) -> Response:
        response = self.http_client.http_delete(API_CERTS_V1 + "/tls/server-cert")
        return response

    def get_user_private_keys(self) -> tuple[Response, list[KeyInfoModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/private_keys")
        if resp and resp.status_code == HTTPStatus.OK:
            ret_list = []
            json_list = resp.json()
            for resp_json in json_list:
                ret_list.append(KeyInfoModel(**resp_json))
            return resp, ret_list
        else:
            return resp, None

    def get_loaded_private_keys(
        self,
    ) -> tuple[Response, list[KeyLoadedInfoModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/private_keys/loaded")
        if resp and resp.status_code == HTTPStatus.OK:
            ret_list = []
            json_list = resp.json()
            for resp_json in json_list:
                ret_list.append(KeyLoadedInfoModel(**resp_json))
            return resp, ret_list
        else:
            return resp, None

    def get_open_csrs(
        self,
    ) -> tuple[Response, list[CsrResponseModel] | None]:

        resp = self.http_client.http_get(API_CERTS_V1 + "/signing_requests")
        ret = []

        if resp and resp.status_code == HTTPStatus.OK:
            for csr in resp.json():
                ret.append(CsrResponseModel(**csr))
            return resp, ret
        else:
            return resp, None

    def gen_new_csr(
        self, csr: CertSigningRequestModel
    ) -> tuple[Response, CsrResponseModel | None]:

        data = json.loads(csr.model_dump_json())
        resp = self.http_client.http_post(API_CERTS_V1 + "/signing_request", json=data)

        if resp and resp.status_code == HTTPStatus.OK:
            resp_data = resp.json()
            return resp, CsrResponseModel(**resp_data)
        else:
            return resp, None

    def delete_open_csr(self, csr_id: CsrUuidModel) -> Response:

        data = json.loads(csr_id.model_dump_json())
        resp = self.http_client.http_delete(
            API_CERTS_V1 + "/signing_request", json=data
        )

        return resp

    def upload_signed_csr_file(
        self,
        cert_file: str,
        fingerprint: str,
        id: str,
        usage=CertUsageEnum.IPSEC,
    ) -> tuple[Response, CertInfoModel | None]:
        with open(cert_file, "r") as fd:
            cert_data = fd.read()

        data = json.loads(
            CsrSignedRequestModel(
                id=id, cert_data=cert_data, fingerprint=fingerprint, usage=usage
            ).model_dump_json()
        )

        resp = self.http_client.http_post(API_CERTS_V1 + "/signed_csr", json=data)
        if resp and resp.status_code == HTTPStatus.ACCEPTED:
            resp_json = resp.json()
            return resp, CertInfoModel(**resp_json)
        else:
            return resp, None

    def get_tls_client_certs(self) -> tuple[Response, list[CertInfoModel] | None]:
        resp = self.http_client.http_get(API_CERTS_V1 + "/tls/client-cert")
        if resp and resp.status_code == HTTPStatus.OK:
            return resp, self.handle_cert_list_response(resp)
        else:
            return resp, None

    def upload_tls_cert_file(
        self, cert_file: str
    ) -> tuple[Response, CertInfoModel | None]:
        return self.upload_cert_file(API_CERTS_V1 + "/tls/client-cert", cert_file)

    def delete_tls_cert(self, cert_fingerprint: str):
        model = CertInfoModel(fingerprint=cert_fingerprint, is_ca=None)
        json_data = json.loads(model.model_dump_json())
        return self.http_client.http_delete(
            API_CERTS_V1 + "/tls/client-cert", json=json_data
        )

    def upload_syslog_ca_cert_file(
        self, cert_file
    ) -> tuple[Response, CertInfoModel | None]:
        return self.upload_cert_file(API_CERTS_V1 + "/syslog/ca", cert_file)

    def delete_syslog_ca_cert(self) -> Response:
        return self.http_client.http_delete(API_CERTS_V1 + "/syslog/ca")

    def delete_syslog_client_certs(self) -> Response:
        return self.http_client.http_delete(API_CERTS_V1 + "/syslog/client-cert")
