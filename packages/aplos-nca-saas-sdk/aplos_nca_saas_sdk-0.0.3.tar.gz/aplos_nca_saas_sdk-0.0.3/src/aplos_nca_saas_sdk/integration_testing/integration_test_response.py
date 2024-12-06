"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Dict, Any, Optional


class IntegrationTestResponse:
    """Integration Test Response"""

    def __init__(self):
        self.name: str = ""
        self.meta: Dict[str, Any] = {}
        self.response: Dict[str, Any] = {}
        self.error: Optional[str] = None
        self.success: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """JSON Dictionary Object"""
        return {
            "name": self.name,
            "meta": self.meta,
            "response": self.response,
            "error": self.error,
            "success": self.success,
        }
