from tfrunner.projects.common import ProjectConfig, ProjectKind
from .gitlab import GitLabStateBackend

StateKindMapper = {
    ProjectKind.GITLAB: GitLabStateBackend
}

class TfrunnerBackendLoader:
    @staticmethod
    def run(config: ProjectConfig) -> list[str]:
        state_backend = StateKindMapper[config.kind]
        return state_backend.run(config.spec)

