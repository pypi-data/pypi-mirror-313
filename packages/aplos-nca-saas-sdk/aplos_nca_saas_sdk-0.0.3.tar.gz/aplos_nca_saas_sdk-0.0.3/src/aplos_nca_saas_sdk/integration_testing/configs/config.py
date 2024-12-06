"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.integration_testing.configs.app_config import (
    TestApplicationConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.configs.login import TestLogins


class TestConfiguration:
    """
    Testing Suite Configuration: Provides a way to define the testing configuration for the Aplos Analytics SaaS SDK

    """

    def __init__(self):
        self.app_config: TestApplicationConfiguration = TestApplicationConfiguration()
        self.logins: TestLogins = TestLogins()
