import os
from pathlib import Path
from pydantic import HttpUrl
from typing import Optional, Self
import yaml

from tfrunner.exceptions import EnvVarNotSet
from tfrunner.types import ConfigBaseModel


class GitLabProjectConfig(ConfigBaseModel):
    url: HttpUrl
    project_id: int
    token_var: str
    state_name: str
    path: Path

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
            config['path'] = (path / ".." / Path(config['path'])).resolve()
            return cls(**config)

    def fetch_token(self) -> str:
        token: Optional[str] = os.environ.get(self.token_var)
        if token is None:
            raise EnvVarNotSet("Environment variable GITLAB_TOKEN is not set.")
        return token

