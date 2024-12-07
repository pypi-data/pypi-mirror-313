from tfrunner.projects.gitlab import GitLabProjectConfig
from tfrunner.types import StateBackend, TerraformStateInitializer


class GitLabStateBackend:
    """
    Return terraform init command for a gitlab backed terraform state.
    """
    @classmethod
    def run(
        cls,
        config: GitLabProjectConfig,
    ) -> list[str]:
        state: StateBackend = cls.__get_state_backend(config)
        init_cmd: list[str] = TerraformStateInitializer.run(state)
        return init_cmd

    @staticmethod
    def __get_state_backend(
        config: GitLabProjectConfig
    ) -> StateBackend:
        return StateBackend(
            address="{}/api/v4/projects/{}/terraform/state/{}".format(
                config.url, config.project_id, config.state_name
            ),
            username="dummy",
            password=config.fetch_token(),
        )

