"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin


from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)


class TestAppLogin(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__("app-login")

    def test(self) -> bool:
        """Test a login"""

        self.results.clear()

        for login in self.config.logins.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            try:
                nca_login = NCALogin(aplos_saas_domain=login.domain)
                token = nca_login.authenticate(
                    username=login.username, password=login.password
                )
                test_response.response = token
                if not token:
                    test_response.error = "Failed to authenticate"

                else:
                    test_response.success = True
            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
