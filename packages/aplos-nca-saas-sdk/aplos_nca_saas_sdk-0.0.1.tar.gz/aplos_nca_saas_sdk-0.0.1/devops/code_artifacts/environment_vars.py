import os


class EnvironmentVars:
    """Environment variables"""

    def __init__(self):
        pass

    @property
    def code_artifact_account_number(self):
        """Gets thd code artifacti account number"""
        return os.getenv("CODEARTIFACT_AWS_ACCCOUNT_NUMBER")  # "974817967438"

    @property
    def code_artifact_domain(self):
        """Gets the code artifact domain"""
        return os.getenv("CODEARTIFACT_DOMAIN")  # "aplos-nca"

    @property
    def code_artifact_repository_name(self):
        """Gets the code artifact repository name"""
        return os.getenv("CODEARTIFACT_REPOSITORY_NAME")  # "python"

    @property
    def code_artifact_repository_region(self):
        """Gets the code artifact repository region"""
        return os.getenv("CODEARTIFACT_REPOSITORY_REGION")  # "us-east-1"

    @property
    def code_artifact_repository_profile(self):
        """Gets the code artifact repository profile"""
        return os.getenv("CODEARTIFACT_REPOSITORY_PROFILE")


envrionment_vars = EnvironmentVars()
