from pathlib import Path
from pydantic import BaseModel, HttpUrl
from typing import Self
import yaml


class ConfigBaseModel(BaseModel):
    """
    A pydantic base model that can be imported from a yaml file.
    """
    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        with open(path, "r") as f:
            return cls(**yaml.safe_load(f))


class StateBackend(BaseModel):
    """
    Define a generic terraform remote state backend.
    """
    address: HttpUrl
    username: str
    password: str
    lock_method: str = "POST"
    unlock_method: str = "DELETE"
    retry_wait_min: int = 5


class TerraformStateInitializer:
    """
    Generates a terraform init command using a remote state backend.
    """
    @staticmethod
    def run(backend: StateBackend) -> list[str]:
        return [
            "terraform",
            "init",
            f"-backend-config=address={backend.address}",
            f"-backend-config=lock_address={backend.address}/lock",
            f"-backend-config=unlock_address={backend.address}/lock",
            f"-backend-config=username={backend.username}",
            f"-backend-config=password={backend.password}",
            f"-backend-config=lock_method={backend.lock_method}",
            f"-backend-config=unlock_method={backend.unlock_method}",
            f"-backend-config=retry_wait_min={backend.retry_wait_min}",
        ]

