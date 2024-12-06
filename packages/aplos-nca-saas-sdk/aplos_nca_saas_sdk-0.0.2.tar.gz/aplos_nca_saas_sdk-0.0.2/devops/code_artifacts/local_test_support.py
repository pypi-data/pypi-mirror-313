import os
import json
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from aws_lambda_powertools import Logger

logger = Logger()


class LocalTestingSupport:
    def __init__(self) -> None:
        pass

    def load_local_environment(
        self, *, path: Optional[str] = None, file_name: str = ".env.development"
    ):
        """Loads the local environment"""
        environment_file: str | None = None
        if path:
            environment_file = os.path.join(path, file_name)
        else:
            environment_file = self.__find_env_file(file_name)

        if environment_file is None:
            raise RuntimeError(f"Failed to locate evnrionment file: {file_name}")

        if os.path.exists(environment_file):
            logger.debug(f"loading profile: {environment_file}")
            load_dotenv(environment_file, override=True)

            aws_profile = os.getenv("AWS_PROFILE")
            logger.debug(f"aws_profile: {aws_profile}")
        else:
            raise RuntimeError(
                f"Failed to locate evnrionment file: {file_name} at {environment_file}"
            )

    def __find_env_file(self, file_name: str) -> Optional[str]:
        """Finds the environment file"""
        for i in range(10):
            path = str(Path(__file__).parents[i].absolute())
            env_file = os.path.join(path, file_name)
            if os.path.exists(env_file):
                return env_file

        return None

    def load_event_file(self, full_path: str) -> dict:
        """Loads an event file"""
        if not os.path.exists(full_path):
            raise RuntimeError(f"Failed to locate event file: {full_path}")

        event: dict = {}
        with open(full_path, mode="r", encoding="utf-8") as json_file:
            event = json.load(json_file)

        if "message" in event:
            tmp = event.get("message")
            if isinstance(tmp, dict):
                event = tmp

        if "event" in event:
            tmp = event.get("event")
            if isinstance(tmp, dict):
                event = tmp

        return event
