"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Optional

import boto3
import jwt as jwt_lib
from mypy_boto3_cognito_idp.client import CognitoIdentityProviderClient
from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
    NCAAppConfiguration,
)


class CognitoAuthenication:
    """
    Cognito Authentication

    """

    def __init__(
        self,
        *,
        client_id: Optional[str] = None,
        region: Optional[str] = None,
        aplos_domain: Optional[str] = None,
    ) -> None:
        # setup the client id
        self.__client_id: Optional[str] = client_id
        self.__jwt: Optional[str] = None
        self.__access_token: Optional[str] = None
        self.__refresh_token: Optional[str] = None
        self.__region: str = region or "us-east-1"
        self.__client: Optional[CognitoIdentityProviderClient] = None
        self.__user_id: Optional[str] = None
        self.__tenant_id: Optional[str] = None
        self.__config: Optional[NCAAppConfiguration] = None
        self.__aplos_domain: Optional[str] = aplos_domain

        self.__validate_parameters()

    @property
    def client(self) -> CognitoIdentityProviderClient:
        """
        Get the boto3 client

        Returns:
            boto3.client: the boto3 client
        """
        if self.__client is None:
            self.__client = boto3.client("cognito-idp", region_name=self.region)

        return self.__client

    @property
    def client_id(self) -> str | None:
        """
        Client Id
        Returns:
            str: the client id
        """
        return self.__client_id

    @property
    def region(self) -> str | None:
        """
        Region
        Returns:
            str: the region
        """
        return self.__region

    def __validate_parameters(self) -> None:
        if self.__client_id is None and self.__aplos_domain is not None:
            self.__config = NCAAppConfiguration(aplos_saas_domain=self.__aplos_domain)
            self.__client_id = self.__config.cognito_client_id
            self.__region = self.__config.cognito_region

        if self.__client_id is None:
            raise RuntimeError(
                "Missing Cognito Client Id. "
                "Pass in a client_id as a command arg or set the COGNITO_CLIENT_ID enviornment var. "
                "Alternatively, set the aplos_domain to automatically get the client_id and region."
            )

        if self.__region is None:
            raise RuntimeError(
                "Missing Cognito Region"
                "Pass in a region as a command arg or set the COGNITO_REGION enviornment var. "
                "Alternatively, set the aplos_domain to automatically get the client_id and region."
            )

    def login(self, username: str, password: str) -> str:
        """
        Get a JWT (JSON Web Token)

        Args:
            username (str): username (email address)
            password (str): password
            client_id (str): cognito client/application id

        Returns:
            str | None: json web token (jwt)
        """

        if not self.client_id:
            raise RuntimeError("Missing Cognito Client Id")

        auth_response = self.client.initiate_auth(
            ClientId=self.client_id,
            # user USER_PASSWORD_AUTH flow for this type of login
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )

        if "ChallengeName" in auth_response:
            # depending on your setup, it's possible you will get challenged for a
            # password change. contact support if this happens
            raise RuntimeError(
                "New password required before a token can be provided. Please contact support or your Aplos Administrator."
            )

        # Extract the session tokens
        # id_token is the JWT token
        # typical tokens last for 30 minutes to 1 hour by default
        self.__jwt = auth_response["AuthenticationResult"]["IdToken"]
        # access token is if you have direct access to aws resources
        # you probably won't ever need this
        self.__access_token = auth_response["AuthenticationResult"]["AccessToken"]  # noqa: F814, F841, pylint: disable=W0612
        # refresh token if needed
        # you can use refresh tokens to "refresh" your jwt or simply login again
        # refresh tokens are typically good for 30 days by default
        self.__refresh_token = auth_response["AuthenticationResult"]["RefreshToken"]  # noqa: F814, F841, pylint: disable=w0612

        # return the jwt token
        if isinstance(self.__jwt, str):
            self.__parse_jwt(self.__jwt)
            return self.__jwt

        raise RuntimeError("Failed to get a JWT token")

    def __parse_jwt(self, encoded_jwt: str) -> None:
        # Decode the payload (second part) from Base64
        decoded_jwt: dict = jwt_lib.decode(
            encoded_jwt, options={"verify_signature": False}
        )
        self.__user_id = decoded_jwt.get("custom:aplos_user_id")
        self.__tenant_id = decoded_jwt.get("custom:aplos_user_tenant_id")

    @property
    def jwt(self) -> str:
        """Get the JWT JSON Web Token"""
        if isinstance(self.__jwt, str):
            return self.__jwt

        raise RuntimeError("Failed to get a JWT token")

    @property
    def user_id(self) -> str:
        """Get the authenticated User Id"""
        if isinstance(self.__user_id, str):
            return self.__user_id

        raise RuntimeError("Failed to get a user id")

    @property
    def tenant_id(self) -> str:
        """Get the authenticated Tenant Id"""
        if isinstance(self.__tenant_id, str):
            return self.__tenant_id

        raise RuntimeError("Failed to get a tenant id")

    @property
    def access_token(self) -> str:
        """Get the AWS Access Token"""
        if isinstance(self.__access_token, str):
            return self.__access_token

        raise RuntimeError("Failed to get an access token")

    @property
    def refresh_token(self) -> str:
        """Get the AWS Cognito Refresh Token"""
        if isinstance(self.__refresh_token, str):
            return self.__refresh_token

        raise RuntimeError("Failed to get a refresh token")
