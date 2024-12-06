import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import List

import toml
from aws_lambda_powertools import Logger
from devops.code_artifacts.environment_vars import envrionment_vars

logger = Logger()


class AWSCodeArtifactsService:
    """AWS Code Artifactis"""

    def __init__(self) -> None:
        self.domain = envrionment_vars.code_artifact_domain
        self.repository = envrionment_vars.code_artifact_repository_name
        self.account = envrionment_vars.code_artifact_account_number
        self.profile = envrionment_vars.code_artifact_repository_profile

    def build(self):
        """Build the artifacts"""

        project_root = Path(__file__).parents[2]

        # extact the version
        pyproject_toml = os.path.join(project_root, "pyproject.toml")

        if not os.path.exists(pyproject_toml):
            raise RuntimeError(
                f"The pyproject.toml file ({pyproject_toml}) not found. "
                "Please check the path and try again."
            )

        # get the "packages" from the toml file
        packages_path: str | None = None
        with open(pyproject_toml, "r", encoding="utf-8") as file:
            pyproject_data = toml.load(file)
            packages_path = pyproject_data.get("project", {}).get("source")

        if not packages_path:
            raise RuntimeError(
                "The packages path is not defined in the pyproject.toml file."
            )
        version_file = os.path.join(project_root, packages_path, "version.py")

        self.extract_version_and_write_to_file(pyproject_toml, version_file)
        # do the build
        self.__run_local_clean_up(project_root)
        self.__run_login()
        self.__run_build()

    def publish(self):
        """Publish the artifacts"""
        self.__run_publish()

    def __run_local_clean_up(self, project_root: str):
        """run a local clean up and remove older items in the dist directory"""

        dist_dir = os.path.join(project_root, "dist")
        if os.path.exists(dist_dir):
            # clear it out
            shutil.rmtree(dist_dir)

    def run_remote_clean_up(self):
        """
        Clean out older versions
        """
        logger.warning("warning/info: older versions are not being cleaned out.")

    def extract_version_and_write_to_file(self, pyproject_toml: str, version_file: str):
        """
        extract the version number from the pyproject.toml file and write it
        to the version.py file
        """
        if not os.path.exists(pyproject_toml):
            raise FileNotFoundError(
                f"The pyproject.toml file ({pyproject_toml}) not found. "
                "Please check the path and try again."
            )

        with open(pyproject_toml, "r", encoding="utf-8") as file:
            pyproject_data = toml.load(file)
            version = pyproject_data["project"]["version"]
            with open(version_file, "w", encoding="utf-8") as f:
                f.write(f"__version__ = '{version}'\n")

    def __run_login(self):
        """log into code artifact"""
        profile_flag: str = ""

        if self.profile:
            profile_flag = f"--profile {self.profile}"
        commands = f"aws codeartifact login --tool pip --domain {self.domain} --repository {self.repository} {profile_flag}".split()
        self.run_commands(commands=commands)

    def __run_build(self):
        """Run python build commands"""
        self.run_commands(["python", "-m", "build"])

    def __run_publish(self):
        """publish to code artifact"""
        self.connect_artifact_to_twine()
        repo_url = self.get_repo_url()

        token = self.get_auth_token()
        # Set up the environment variables for the upload command
        env = os.environ.copy()
        env["TWINE_USERNAME"] = "aws"
        env["TWINE_PASSWORD"] = token

        commands = [
            "python",
            "-m",
            "twine",
            "upload",
            "--repository-url",
            repo_url,
        ]

        # if self.profile:
        #     commands.extend(["--profile", f"{self.profile}"])

        commands.extend(["dist/*"])

        self.run_commands(
            commands=commands,
            env=env,
        )

    def connect_artifact_to_twine(self) -> None:
        """Connect twine to codeartifact"""
        profile_flag = ""
        if self.profile:
            profile_flag = f"--profile {self.profile}"
        commands = f"aws codeartifact login {profile_flag} --tool twine --domain {self.domain} --repository {self.repository}".split()
        self.run_commands(commands=commands, capture_output=True)

    def get_repo_url(self) -> str:
        """get the artifact repo url"""
        get_url_command = [
            "aws",
            "codeartifact",
            "get-repository-endpoint",
            "--domain",
            self.domain,
            "--domain-owner",
            self.account,
            "--repository",
            self.repository,
            "--format",
            "pypi",
        ]

        if self.profile:
            get_url_command.extend(["--profile", self.profile])

        repo_url = self.run_commands(get_url_command, capture_output=True)

        if not repo_url:
            raise RuntimeError("Unable to get the repository url")
        repo_url = self.get_url(repo_url)
        return repo_url

    def get_auth_token(self) -> str:
        """get the auth token"""
        commands = [
            "aws",
            "codeartifact",
            "get-authorization-token",
            "--domain",
            self.domain,
            "--domain-owner",
            self.account,
            "--query",
            "authorizationToken",
            "--output",
            "text",
        ]

        token = self.run_commands(commands=commands, capture_output=True)

        return token

    def get_url(self, payload: str):
        """get the url from the payload"""
        value: dict = json.loads(payload)
        url = value.get("repositoryEndpoint")

        return url

    def run_commands(
        self, commands: List[str], capture_output: bool = False, env=None
    ) -> str | None:
        """centralized area for running process commands"""
        try:
            # Run the publish command
            result = subprocess.run(
                commands,
                check=True,
                capture_output=capture_output,
                env=env,  # pass any environment vars
            )

            if capture_output:
                output = result.stdout.decode().strip()
                return output

        except subprocess.CalledProcessError as e:
            logger.exception(f"An error occurred: {e}")


def main():
    """build the artifacts"""
    artifacts: AWSCodeArtifactsService = AWSCodeArtifactsService()
    artifacts.build()
    artifacts.publish()


if __name__ == "__main__":
    main()
