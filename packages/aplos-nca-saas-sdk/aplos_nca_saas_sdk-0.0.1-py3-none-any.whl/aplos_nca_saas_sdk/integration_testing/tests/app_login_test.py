"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin


from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class TestAppLogin(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__("app-login")

    def test(self) -> dict:
        """Test a login"""

        user_name = self.env_vars.username
        password = self.env_vars.password

        login = NCALogin(aplos_saas_domain=self.env_vars.api_domain)
        token = login.authenticate(username=user_name, password=password)
        if not token:
            raise RuntimeError("Failed to authenticate")
        else:
            return {"token": token}
