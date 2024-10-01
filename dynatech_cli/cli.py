from rich.console import Console
from typer import Context, Exit, Option, Typer
from typing_extensions import Annotated

from dynatech_cli import __version__
from dynatech_cli.commands import mapper_app

console = Console()
app = Typer()

app.add_typer(mapper_app, name="mapper", help="Mapeamento de paginas web.")


def version_func(flag: bool):
    if flag:
        console.print(f"Dynatech CLI version: {__version__}")
        raise Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    _: Annotated[
        bool,
        Option(
        "--version",
        "-v",
        callback=version_func,
        is_flag=True,
        help="Mostre a versão do Dynatech CLI."
        ),
    ] = False
):
    message = """
    Bem-vindo ao Dynatech CLI! 🚀

    Para ver a lista de comandos disponíveis, execute:

    $ dynatech --help
    """

    if ctx.invoked_subcommand:
        return

    console.print(message)
    raise Exit()
