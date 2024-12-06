from pathlib import Path
import subprocess
import typer
from typing import Annotated

from tfrunner.projects.gitlab import GitLabProjectConfig
from tfrunner.state_backend.gitlab import GitLabStateBackend

app = typer.Typer()

@app.command(context_settings={
    "allow_extra_args": True,
    "ignore_unknown_options": True,
})
def init(
    ctx: typer.Context,
    config_path: Annotated[Path, typer.Option(help="location of the config file to use for the tool's execution")],
) -> None:
    config: GitLabProjectConfig = GitLabProjectConfig.from_yaml(config_path)
    init_cmd: list[str] = GitLabStateBackend.run(config)
    init_cmd += ctx.args
    subprocess.call(init_cmd, cwd=config.path)

