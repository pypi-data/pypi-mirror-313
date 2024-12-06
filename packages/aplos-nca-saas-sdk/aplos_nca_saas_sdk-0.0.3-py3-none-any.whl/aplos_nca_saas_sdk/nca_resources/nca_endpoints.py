"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""


class NCAEndpoints:
    """Aplos NCA SaaS Endpoints"""

    def __init__(self, *, aplos_saas_domain: str):
        self.__domain: str = aplos_saas_domain
        self.__protocal: str = "https://"

    def __base(self, tenant_id: str | None = None, user_id: str | None = None) -> str:
        """Returns the base endpoint"""
        route = f"{self.__protocal}{self.__domain}"

        if tenant_id:
            route = f"{route}/tenants/{tenant_id}"
        if user_id:
            if not tenant_id:
                raise ValueError("Tenant ID is required on the users path")
            route = f"{route}/users/{user_id}"

        return route

    def tenant(self, tenant_id: str) -> str:
        """Returns the tenant endpoint"""
        return f"{self.__base(tenant_id=tenant_id)}"

    def app_configuration(self) -> str:
        """Returns the configuration endpoint"""
        return f"{self.__base()}/app/configuration"

    def user(self, tenant_id: str, user_id: str) -> str:
        """Returns the user endpoint"""
        return f"{self.__base(tenant_id=tenant_id, user_id=user_id)}"

    def executions(self, tenant_id: str, user_id: str) -> str:
        """Returns the executions endpoint"""
        return f"{self.__base(tenant_id=tenant_id, user_id=user_id)}/nca/executions"

    def execution(self, tenant_id: str, user_id: str, execution_id: str) -> str:
        """Returns the executions endpoint"""
        return f"{self.executions(tenant_id=tenant_id, user_id=user_id)}/{execution_id}"

    def files(self, tenant_id: str, user_id: str) -> str:
        """Returns the files endpoint"""
        return f"{self.__base(tenant_id=tenant_id, user_id=user_id)}/nca/files"

    def file(self, tenant_id: str, user_id: str, file_id: str) -> str:
        """Returns the file endpoint"""
        return f"{self.files(tenant_id=tenant_id, user_id=user_id)}/{file_id}"
