from rich.console import Console
from typer import Typer, Argument, Option, Exit
from typing_extensions import Annotated
from dynatech_cli.core import Mapper
from typing import List

console = Console()
app = Typer()


@app.command(name="map")
def map_web_page(
    domain: Annotated[str, Argument(help='URL do domínio a ser mapeado')],
    recursive: Annotated[
        bool,
        Option(
            "--recursive",
            "-r",
            help='Mapear recursivamente',
            ),
        ] = False,
    max_depth: Annotated[
        int,
        Option(
            "--max-depth",
            "-m",
            help='Profundidade do mapeamento',
            rich_help_panel='Customization',
            show_default=False,
            ),
        ] = 2,
    rate_limit: Annotated[
        float,
        Option(
            "--rate-limit",
            "-l",
            help='Intervalo entre requisições',
            rich_help_panel='Customization',
            show_default=False,
            ),
        ] = 0.5,
) -> None:
    """
    Mapeamento de páginas web.

    Exemplo de uso:

    $ dynatech mapper map https://example.com

    Para mapear recursivamente:

    $ dynatech mapper map https://example.com --recursive

    Para definir a profundidade do mapeamento:

    $ dynatech mapper map https://example.com --max-depth 3

    Para definir o intervalo entre requisições:

    $ dynatech mapper map https://example.com --rate-limit 1

    Para mais informações, execute:

    $ dynatech mapper map --help
    """

    try:
        if recursive:
            mapper = Mapper(domain, max_depth=max_depth, rate_limit=rate_limit)
        else:
            mapper = Mapper(domain, max_depth=1, rate_limit=rate_limit)

        console.print(f"[green]Iniciando o mapeamento de:[/green] [bold]{domain}[/bold]")
        links: List[str] = mapper.map_web_site()

        console.print(f"\n[bold yellow]Total de links encontrados:[/bold yellow] {len(links)}\n")
        for link in links:
            console.print(f"[blue]{link}[/blue]")

    except ValueError as ve:
        console.print(f"[red]Erro:[/red] {ve}")
        Exit(1)
    except Exception as e:
        console.print(f"[red]Ocorreu um erro inesperado:[/red] {e}")
        Exit(1)