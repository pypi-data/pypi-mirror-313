import os


class EnvironmentVars:
    """Loading Environment Vars or replace them with runtime values"""

    def __init__(self) -> None:
        # load defaults
        self.api_domain = os.getenv("APLOS_API_DOMAIN", "")

        self.aws_region = os.getenv("COGNITO_REGION")
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.username = os.getenv("COGNITO_USER_NAME")
        self.password = os.getenv("COGNITO_PASSWORD")

        self.config_file = os.getenv("CONFIG_FILE")
        self.metadata_file = os.getenv("METADATA_FILE")
        self.analysis_file = os.getenv("ANALYSIS_FILE")

        if self.api_domain is not None and "https://" in self.api_domain:
            self.api_domain = self.api_domain.replace("https://", "")

        self.aplos_api_url = f"https://{self.api_domain}"
