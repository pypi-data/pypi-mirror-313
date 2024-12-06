"""
Aplos Analytics

"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path
from dotenv import load_dotenv


class EnvironmentServices:
    """Environment Services"""

    def load_environment(
        self,
        *,
        starting_path: str | None = None,
        file_name: str = ".env.dev",
        override_vars: bool = True,
        raise_error_if_not_found: bool = True,
    ):
        """Loads the local environment"""

        if not starting_path:
            starting_path = __file__

        environment_file: str | None = self.find_file(
            starting_path=starting_path,
            file_name=file_name,
            raise_error_if_not_found=raise_error_if_not_found,
        )

        if environment_file:
            load_dotenv(dotenv_path=environment_file, override=override_vars)

    def load_event_file(self, full_path: str) -> Dict[str, Any]:
        """Loads an event file"""
        if not os.path.exists(full_path):
            raise RuntimeError(f"Failed to locate event file: {full_path}")

        event: Dict = {}
        with open(full_path, mode="r", encoding="utf-8") as json_file:
            event = json.load(json_file)

        if "message" in event:
            tmp = event.get("message")
            if isinstance(tmp, Dict):
                event = tmp

        if "event" in event:
            tmp = event.get("event")
            if isinstance(tmp, Dict):
                event = tmp

        return event

    def find_file(
        self, starting_path: str, file_name: str, raise_error_if_not_found: bool = True
    ) -> str | None:
        """Searches the project directory structor for a file"""
        parents = 10
        starting_path = starting_path or __file__

        paths: List[str] = []
        for parent in range(parents):
            path = Path(starting_path).parents[parent].absolute()

            tmp = os.path.join(path, file_name)
            paths.append(tmp)
            if os.path.exists(tmp):
                return tmp

        if raise_error_if_not_found:
            searched_paths = "\n".join(paths)
            raise RuntimeError(
                f"Failed to locate environment file: {file_name} in: \n {searched_paths}"
            )

        return None
