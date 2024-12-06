"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Optional


class TestLogin:
    """
    Application Login: Defines the login that the application configuration tests will check against

    """

    def __init__(
        self,
        username: Optional[str] = None,
        passord: Optional[str] = None,
        domain: Optional[str] = None,
    ):
        self.__username: Optional[str] = username
        self.__password: Optional[str] = passord
        self.__domain: Optional[str] = domain

    @property
    def username(self) -> str:
        if self.__username is None:
            raise RuntimeError("Username is not set")
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def password(self) -> str:
        if self.__password is None:
            raise RuntimeError("Password is not set")
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    @property
    def domain(self) -> str:
        if self.__domain is None:
            raise RuntimeError("Domain is not set")
        return self.__domain

    @domain.setter
    def domain(self, value: str):
        self.__domain = value


class TestLogins:
    """
    Application Logins: Defines the logins that the application configuration tests will check against

    """

    def __init__(self):
        self.__logins: List[TestLogin] = []

    @property
    def list(self) -> List[TestLogin]:
        """List the logins"""
        return self.__logins

    def add(self, *, username: str, password: str, domain: str):
        """Add a loging"""
        login = TestLogin()
        login.username = username
        login.password = password
        login.domain = domain
        self.__logins.append(login)
