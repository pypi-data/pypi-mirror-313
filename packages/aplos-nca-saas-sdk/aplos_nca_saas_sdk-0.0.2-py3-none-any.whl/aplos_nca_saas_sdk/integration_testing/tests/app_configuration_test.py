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


class TestAppConfiguration(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__(name="app_configuration")

    def test(self) -> dict:
        """Test loading the application configuration"""

        config: NCAAppConfiguration = NCAAppConfiguration(self.env_vars.api_domain)
        response = config.get()

        if response.status_code != 200:
            raise RuntimeError("App configuration url is not working.")

        return response.json()
