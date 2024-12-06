"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Optional
from aplos_nca_saas_sdk.aws_resources.aws_cognito import CognitoAuthenication
from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
    NCAAppConfiguration,
)


class NCALogin:
    """NCA Login"""

    def __init__(
        self,
        *,
        cognito_client_id: Optional[str] = None,
        cognito_region: Optional[str] = None,
        aplos_saas_domain: Optional[str] = None,
    ) -> None:
        """
        NCA SaaS Login

        Args:
            cognito_client_id (Optional[str], optional): Cognito Client Id. Defaults to None.
            cognito_region (Optional[str], optional): Cognito Region. Defaults to None.
            aplos_saas_domain (Optional[str], optional): Aplos NCA SaaS domain. Defaults to None.

        Requirements:
            Either pass in the cognito_client_id and cognito_region.
            or set the aplos_saas_domain to automatically get the client_id and region.
        """
        self.jwt: str
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.__cognito_client_id = cognito_client_id
        self.__region = cognito_region
        self.__domain: Optional[str] = aplos_saas_domain
        self.__cognito: Optional[CognitoAuthenication] = None
        self.__config: Optional[NCAAppConfiguration] = None

    @property
    def cognito(self) -> CognitoAuthenication:
        """
        Cognito Authentication
        Returns:
            CognitoAuthenication: object to handle cognito authentication
        """
        if self.__cognito is None:
            self.__cognito = CognitoAuthenication(
                client_id=self.__cognito_client_id,
                region=self.__region,
                aplos_domain=self.__domain,
            )

        return self.__cognito

    @property
    def domain(self) -> str | None:
        """
        Domain
        Returns:
            str: the domain
        """
        return self.__domain

    @property
    def config(self) -> NCAAppConfiguration:
        """
        NCA App Configuration
        Returns:
            NCAAppConfiguration: object to handle the NCA App Configuration
        """
        if self.__config is None:
            if self.__domain is None:
                raise RuntimeError(
                    "Failed to get Aplos Configuration.  The Domain is not set."
                )

            self.__config = NCAAppConfiguration(
                aplos_saas_domain=self.__domain,
            )

        return self.__config

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> str:
        """_summary_

        Args:
            username (str): the username
            password (str): the users password

        """

        self.jwt = self.cognito.login(username=username, password=password)

        return self.jwt
