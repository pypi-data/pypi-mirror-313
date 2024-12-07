import os
from pydantic import HttpUrl
from typing import Optional

from tfrunner.exceptions import EnvVarNotSet
from tfrunner.types import ConfigBaseModel


class GitLabProjectConfig(ConfigBaseModel):
    url: HttpUrl
    project_id: int
    token_var: str
    state_name: str

    def fetch_token(self) -> str:
        token: Optional[str] = os.environ.get(self.token_var)
        if token is None:
            raise EnvVarNotSet("Environment variable GITLAB_TOKEN is not set.")
        return token

