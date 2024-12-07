from tfrunner.projects.common import ProjectKind, ProjectConfig
from .gitlab import GitLabSecretFetcher

SECRET_FETCHER_KIND_MAPPER = {
    ProjectKind.GITLAB: GitLabSecretFetcher
}

class TfrunnerSecretFetcher:
    @staticmethod
    def run(config: ProjectConfig) -> dict[str, str]:
      kind: ProjectKind = config.kind
      fetcher = SECRET_FETCHER_KIND_MAPPER[kind]
      return fetcher.run(config.spec)
