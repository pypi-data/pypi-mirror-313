from pathlib import Path
import subprocess
import typer
from typing import Annotated, Optional

from tfrunner.projects.common import TfrunnerConfigLoader
from tfrunner.secrets.common import TfrunnerSecretFetcher

app = typer.Typer()

@app.command(context_settings={
    "allow_extra_args": True,
    "ignore_unknown_options": True,
})
def destroy(
    ctx: typer.Context,
    config_path: Annotated[Path, typer.Option(help="location of the config file to use for the tool's execution")],
    project: Annotated[Optional[str], typer.Option(help="name of the project to initialize")] = None,
) -> None:
    config = TfrunnerConfigLoader.from_yaml(config_path, project)
    _ = TfrunnerSecretFetcher.run(config)
    cmds: list[str] = ["terraform", "destroy"] + ctx.args
    subprocess.call(cmds, cwd=config.path)

