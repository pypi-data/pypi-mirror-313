"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Dict, Any
from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars
from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class IntegrationTestBase:
    """
    Integration Test Base Class
    """

    def __init__(self, name: str, index: int = 0):
        self.name = name
        self.index = index
        self.env_vars: EnvironmentVars = EnvironmentVars()

        if not self.env_vars.api_domain:
            raise RuntimeError(
                "APLOS_API_DOMAIN environment variable is not set. "
                "This is required to run the tests"
            )

        self.endpoints: NCAEndpoints = NCAEndpoints(
            aplos_saas_domain=self.env_vars.api_domain,
        )

    def test(self) -> Dict[str, Any] | None:
        """Run the Test"""
        raise RuntimeError("This should be implemented by the subclass.")
