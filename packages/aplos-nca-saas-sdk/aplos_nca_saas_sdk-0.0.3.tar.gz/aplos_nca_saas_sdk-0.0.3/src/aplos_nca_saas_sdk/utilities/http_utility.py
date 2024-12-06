class Routes:
    """NCA Saas Routes"""

    NCA_EXECUTIONS = "nca/executions"
    NCA_GENERATE_UPLOAD = "nca/files"


class HttpUtilities:
    """Http Utilties"""

    @staticmethod
    def build_url(domain_name: str) -> str:
        """Build the url"""
        domain_name = domain_name.strip()
        if domain_name.startswith("http"):
            return domain_name
        else:
            return f"https://{domain_name}"

    @staticmethod
    def get_headers(jwt: str) -> dict:
        """Get the Http Headers"""
        headers = {
            "Content-Type": "application/json",
        }

        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"

        return headers
