from pathlib import Path
import subprocess
import typer
from typing import Annotated

from tfrunner.projects.gitlab import GitLabProjectConfig

app = typer.Typer()

@app.command(context_settings={
    "allow_extra_args": True,
    "ignore_unknown_options": True,
})
def fmt(
    ctx: typer.Context,
    config_path: Annotated[Path, typer.Option(help="location of the config file to use for the tool's execution")]
) -> None:
    config: GitLabProjectConfig = GitLabProjectConfig.from_yaml(config_path)
    cmds: list[str] = ["terraform", "fmt"] + ctx.args
    subprocess.call(cmds, cwd=config.path)

