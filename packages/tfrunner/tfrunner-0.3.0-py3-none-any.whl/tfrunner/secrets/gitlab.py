import os
import requests

from tfrunner.projects.gitlab import GitLabProjectConfig

class GitLabSecretFetcher:
    """
    Fetches GitLab CI variables inside of a GitLab project.
    """
    @classmethod
    def run(
        cls,
        config: GitLabProjectConfig,
    ) -> dict[str, str]:
        """
        Return GitLab CI variables for the given GitLab project.

        Additionally, loads each of them as environment variables.
        """
        response: list[dict] = cls.__make_gitlab_request(config)
        vars: dict[str, str] = cls.__extract_vars_from_response(response)
        cls.__load_vars_to_env(vars)
        return vars

    @staticmethod
    def __make_gitlab_request(config: GitLabProjectConfig) -> list[dict]:
        api_url: str = "{}/api/v4/projects/{}/variables".format(
            config.url, config.project_id
        )
        headers: dict[str, str] = {"PRIVATE-TOKEN": config.fetch_token()}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"""
            Failed to fetch CI variables.
            Gitlab url: {config.url}
            Project: {config.project_id}
            Status code: {response.status_code}
            Response: {response.text}
            """)

    @staticmethod
    def __extract_vars_from_response(response: list[dict]) -> dict[str, str]:
        return {
            item['key']: item['value']
            for item in response
        }

    @staticmethod
    def __load_vars_to_env(vars: dict[str, str]) -> None:
        for k, v in vars.items():
            os.environ[f"TF_VAR_{k.lower()}"] = v

