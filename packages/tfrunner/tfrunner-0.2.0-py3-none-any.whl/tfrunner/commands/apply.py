from pathlib import Path
import subprocess
import typer
from typing import Annotated

from tfrunner.projects.gitlab import GitLabProjectConfig
from tfrunner.secrets.gitlab import GitLabSecretFetcher

app = typer.Typer()

@app.command(context_settings={
    "allow_extra_args": True,
    "ignore_unknown_options": True,
})
def apply(
    ctx: typer.Context,
    config_path: Annotated[Path, typer.Option(help="location of the config file to use for the tool's execution")]
) -> None:
    config: GitLabProjectConfig = GitLabProjectConfig.from_yaml(config_path)
    _ = GitLabSecretFetcher.run(config)
    cmds: list[str] = ["terraform", "apply"] + ctx.args
    subprocess.call(cmds, cwd=config.path)

