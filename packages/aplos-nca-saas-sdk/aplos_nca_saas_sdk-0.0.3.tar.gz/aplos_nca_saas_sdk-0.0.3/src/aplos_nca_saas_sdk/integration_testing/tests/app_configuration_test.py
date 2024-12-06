"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
    NCAAppConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)

from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)


class TestAppConfiguration(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__(name="app_configuration")

    def test(self) -> bool:
        """Test loading the application configuration"""

        self.results.clear()
        for domain in self.config.app_config.domains:
            config: NCAAppConfiguration = NCAAppConfiguration(domain)

            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.meta = {"domain": domain}
            try:
                response = config.get()
                test_response.response = response
                test_response.success = True
            except Exception as e:  # pylint: disable=W0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
