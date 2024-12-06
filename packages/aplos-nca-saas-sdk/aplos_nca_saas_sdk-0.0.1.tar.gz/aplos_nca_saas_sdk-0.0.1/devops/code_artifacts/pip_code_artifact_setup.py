import os
import subprocess
from aws_lambda_powertools import Logger
from devops.code_artifacts.environment_vars import envrionment_vars

logger = Logger()


def setup_codeartifact_pip(
    account_number: str,
    domain: str,
    repository: str,
    region: str,
    profile: str | None = None,
):
    # Get the AWS account ID
    # sts_client = boto3.client('sts')
    # account_id = sts_client.get_caller_identity().get('Account')

    # Authenticate pip with CodeArtifact
    login_command = [
        "aws",
        "codeartifact",
        "login",
        "--tool",
        "pip",
        "--domain",
        domain,
        "--domain-owner",
        account_number,
        "--repository",
        repository,
        "--region",
        region,
    ]
    if profile:
        login_command.extend(["--profile", profile])

    result = subprocess.run(login_command, capture_output=True, text=True, check=True)

    if result.returncode != 0:
        logger.error("Failed to authenticate pip with CodeArtifact.")
        logger.error("Command output:", result.stdout)
        logger.error("Error output:", result.stderr)
        raise RuntimeError("CodeArtifact login failed")

    logger.info("Successfully authenticated pip with CodeArtifact.")
    logger.info("Command output:", result.stdout)

    logger.info(
        f"Configured pip to use CodeArtifact repository {repository} in domain {domain}."
    )


def main():
    setup_codeartifact_pip(
        account_number=envrionment_vars.code_artifact_account_number,
        domain=envrionment_vars.code_artifact_domain,
        repository=envrionment_vars.code_artifact_repository_name,
        region=envrionment_vars.code_artifact_repository_region,
        profile=envrionment_vars.code_artifact_repository_profile,
    )


if __name__ == "__main__":
    main()
