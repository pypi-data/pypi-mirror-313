"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Dict, Any, List

from aplos_nca_saas_sdk.integration_testing.configs.config import TestConfiguration
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)


class IntegrationTestBase:
    """
    Integration Test Base Class
    """

    def __init__(self, name: str | None = None, index: int = 0):
        self.name = name
        self.index = index
        self.__config: TestConfiguration | None = None
        self.__results: List[IntegrationTestResponse] = []

    @property
    def config(self) -> TestConfiguration:
        """
        Get the configuration for the test
        """
        if self.__config is None:
            raise RuntimeError(
                "Test configuration not set. "
                "A configuration is required to run integration tests."
            )
        return self.__config

    @config.setter
    def config(self, value: TestConfiguration):
        """
        Set the configuration for the test
        """
        self.__config = value

    @property
    def results(self) -> List[IntegrationTestResponse]:
        """
        Get the results of the test
        """
        return self.__results

    def success(self) -> bool:
        """
        Returns True if all tests in the suite were successful
        """
        return all([result.success for result in self.results])

    def test(self) -> bool:
        """
        Run the Test
        Args:
            config: The Test Configuration
        Returns:
            True if the test was successful, False otherwise.  If any
            of the tests fail, it will be false.  Execeptions are only
            raised if the raise_on_failure flag is set to True.
        """
        raise RuntimeError("This should be implemented by the subclass.")
