import typer
from typer.models import CommandInfo

from tfrunner.commands import (
    init, plan, validate,
    fmt, destroy, apply
)


######################
# DEFINE APPLICATION #
######################

app = typer.Typer()

# Add commands from all files in
# the commands module to the app
all_commands: list[list[CommandInfo]] = [
    init.app.registered_commands,
    plan.app.registered_commands,
    validate.app.registered_commands,
    fmt.app.registered_commands,
    destroy.app.registered_commands,
    apply.app.registered_commands,
]
flattened_commands: list[CommandInfo] = [
    c for cs in all_commands for c in cs
]
app.registered_commands += flattened_commands


#######################
# CLI TOOL ENTRYPOINT #
#######################

def cli() -> None:
    app()


if __name__ == "__main__":
    cli()

