"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Dict

import requests

from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class NCAAppConfiguration:
    """
    NCA Application Configuration



    "idp": {
        "Auth": {
        "Cognito": {
            "region": "<region>",
            "userPoolId": "<user-pool-id>",
            "userPoolClientId": "<user-pool-client-id>",
            "authenticationFlowType": "<auth-flow-type>"
        }
        }
    },

    """

    def __init__(self, aplos_saas_domain: str):
        self.endpoints: NCAEndpoints = NCAEndpoints(aplos_saas_domain=aplos_saas_domain)
        self.__response: requests.Response | None = None

    def get(self) -> requests.Response:
        """Executes a HTTP Get request"""

        if self.__response is not None:
            return self.__response

        url = self.endpoints.app_configuration()
        self.__response = requests.get(url, timeout=30)
        if self.__response.status_code != 200:
            raise RuntimeError("App configuration url is not working.")

        return self.__response

    @property
    def cognito_client_id(self) -> str:
        """Returns the cognito client id"""
        data: Dict[str, Any] = self.get().json()
        cognito_client_id = (
            data.get("idp", {})
            .get("Auth", {})
            .get("Cognito", {})
            .get("userPoolClientId")
        )
        return cognito_client_id

    @property
    def cognito_region(self) -> str:
        """Returns the cognito region"""
        data: Dict[str, Any] = self.get().json()
        cognito_client_id = (
            data.get("idp", {}).get("Auth", {}).get("Cognito", {}).get("region")
        )
        return cognito_client_id
