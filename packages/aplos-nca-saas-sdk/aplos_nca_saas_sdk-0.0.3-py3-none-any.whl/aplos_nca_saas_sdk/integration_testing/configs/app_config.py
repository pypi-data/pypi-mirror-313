"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List


class TestApplicationConfiguration:
    """
    Application Configuration: Defines the domains that the application configuration tests will check against

    """

    def __init__(self):
        self.__domains: List[str] = []

    @property
    def domains(self) -> List[str]:
        return self.__domains

    @domains.setter
    def domains(self, value: List[str]):
        self.__domains = value
