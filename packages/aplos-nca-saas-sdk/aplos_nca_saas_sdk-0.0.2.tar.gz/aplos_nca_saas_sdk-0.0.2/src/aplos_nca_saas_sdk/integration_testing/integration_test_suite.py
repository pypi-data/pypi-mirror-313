"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Dict, Any
from datetime import datetime, UTC
from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
    IntegrationTestFactory,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)


class IntegrationTestSuite:
    """Runs Tests against an active instance"""

    def __init__(self):
        self.test_results: List[Dict[str, Any]] = []
        self.verbose: bool = False
        self.raise_on_failure: bool = False

    def test(self) -> bool:
        """Run a full suite of integration tests"""
        start_time: datetime = datetime.now(UTC)
        factory: IntegrationTestFactory = IntegrationTestFactory()
        test_class: IntegrationTestBase | None = None
        for test_class in factory.test_classes:
            test_instance: IntegrationTestBase = test_class
            test: Dict[str, Any] = {
                "test_name": test_instance.name,
                "success": True,
                "error": None,
                "start_time_utc": datetime.now(UTC),
                "end_time_utc": None,
            }
            if self.verbose:
                print(f"Running test class {test_instance.name}")
            try:
                results = test_instance.test()
                test["results"] = results

            except Exception as e:  # pylint: disable=broad-except
                test["success"] = False
                test["error"] = str(e)

            test["end_time_utc"] = datetime.now(UTC)
            self.test_results.append(test)

            if self.verbose:
                if test["success"]:
                    print(f"Test {test_instance.name} succeeded")
                else:
                    print(
                        f"Test {test_instance.name} failed with error {test['error']}"
                    )
        # find the failures
        failures = [test for test in self.test_results if not test["success"]]

        # print the results

        print("Test Results:")
        for test in self.test_results:
            duration = test["end_time_utc"] - test["start_time_utc"]
            print(
                f"  {test['test_name']} {'succeeded' if test['success'] else 'failed'} duration: {duration}"
            )
            if not test["success"]:
                print(f"    Error: {test['error']}")

        print(f"Test Suite completed in {datetime.now(UTC) - start_time}")

        print(f"Total Tests: {len(self.test_results)}")
        print(f"Successful Tests: {len(self.test_results) - len(failures)}")
        print(f"Failed Tests: {len(failures)}")

        if self.raise_on_failure and len(failures) > 0:
            count = len(failures)
            print(f"{count} tests failed. Raising exception.")
            raise RuntimeError(f"{count} tests failed")

        return len(failures) == 0
