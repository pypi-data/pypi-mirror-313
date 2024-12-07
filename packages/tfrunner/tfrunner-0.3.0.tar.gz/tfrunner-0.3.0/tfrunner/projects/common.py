from enum import Enum
from pathlib import Path
from typing import Optional, Self
import yaml

from tfrunner.types import ConfigBaseModel
from .gitlab import GitLabProjectConfig

class ProjectKind(Enum):
    GITLAB = "gitlab"

class ProjectConfig(ConfigBaseModel):
    kind: ProjectKind
    spec: ConfigBaseModel
    path: Path

    @classmethod
    def from_config_path(cls, config_path: Path, **kwargs) -> Self:
        kwargs['path'] = (config_path / ".." / Path(kwargs['path'])).resolve()
        return cls(**kwargs)


PROJECT_KIND_MAPPER: dict[ProjectKind, type[ConfigBaseModel]] = {
    ProjectKind.GITLAB: GitLabProjectConfig
}

class TfrunnerConfigLoader:
    @classmethod
    def from_yaml(cls, config_path: Path, project_name: Optional[str]) -> ProjectConfig | dict[str, ProjectConfig]:
        with open(config_path, "r") as f:
            config: dict = yaml.safe_load(f)

        if project_name is not None:
            return cls.__get_project_config(config_path, config[project_name])

        return {k: cls.__get_project_config(config_path, v) for k, v in config.items()}

    @staticmethod
    def __get_project_config(config_path: Path, project_spec: dict) -> ProjectConfig:
        kind: ProjectKind = ProjectKind(project_spec['kind'])
        spec: ConfigBaseModel = PROJECT_KIND_MAPPER[kind](**project_spec['spec'])
        return ProjectConfig.from_config_path(
            kind=kind,
            spec=spec,
            config_path=config_path,
            path=project_spec['path'],
        )


