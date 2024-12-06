"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from aplos_nca_saas_sdk.utilities.environment_services import EnvironmentServices
from aplos_nca_saas_sdk.integration_testing.integration_test_suite import (
    IntegrationTestSuite,
)
from aplos_nca_saas_sdk.integration_testing.configs.config import TestConfiguration


def main():
    """Run the tests"""

    evs: EnvironmentServices = EnvironmentServices()
    env_file = os.getenv("ENV_FILE")
    if env_file:
        # if we have an environment file defined, let's load it
        evs.load_environment(starting_path=__file__, file_name=env_file)

    its: IntegrationTestSuite = IntegrationTestSuite()
    config: TestConfiguration = TestConfiguration()
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")
    domain = os.getenv("TEST_DOMAIN")

    if not username or not password or not domain:
        raise RuntimeError(
            "TEST_USERNAME, TEST_PASSWORD, and TEST_DOMAIN must be set in the environment"
        )

    config.logins.add(username=username, password=password, domain=domain)
    config.app_config.domains.append(domain)

    its.test(test_config=config)


if __name__ == "__main__":
    main()
