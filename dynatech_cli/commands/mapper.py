from typing import List

from rich.console import Console
from typer import Argument, Exit, Option, Typer
from typing_extensions import Annotated

from dynatech_cli.exporters import ExporterType, save_map
from dynatech_cli.scrapers import Mapper

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
    save: Annotated[
        ExporterType,
        Option(
            "--save",
            "-s",
            help='Salvar o mapa em um arquivo',
            ),
        ] = ExporterType.none,
) -> None:
    """
    Mapeamento de páginas web.

    Exemplo de uso:

    $ dynatech mapper map https://example.com

    Para mapear recursivamente:

    $ dynatech mapper map https://example.com --recursive

    ou

    $ dynatech mapper map https://example.com -r

    Para definir a profundidade do mapeamento:

    $ dynatech mapper map https://example.com --max-depth 3

    ou

    $ dynatech mapper map https://example.com -m 3

    Para definir o intervalo entre requisições:

    $ dynatech mapper map https://example.com --rate-limit 1

    ou

    $ dynatech mapper map https://example.com -l 1

    Para salvar o mapa em um arquivo:

    $ dynatech mapper map https://example.com --save json

    ou

    $ dynatech mapper map https://example.com -s json

    Para mais informações, execute:

    $ dynatech mapper map --help
    """

    try:
        if recursive:
            mapper = Mapper(domain, max_depth=max_depth, rate_limit=rate_limit)
        else:
            mapper = Mapper(domain, max_depth=1, rate_limit=rate_limit)

        console.print(
            f"[green]Iniciando o mapeamento de:[/green] [bold]{domain}[/bold]"
            )
        links: List[str] = mapper.map_web_site()

        console.print(
            f"\n[bold yellow]Encontrados:[/bold yellow] {len(links)}\n"
            )

        if save != ExporterType.none:
            console.print(
                f"[green]Salvando o mapa em:[/green] [bold]{save.value}[/bold]"
                )
            save_map(links, save)

    except ValueError as ve:
        console.print(f"[red]Erro:[/red] {ve}")
        Exit(1)
    except Exception as e:
        console.print(f"[red]Ocorreu um erro inesperado:[/red] {e}")
        Exit(1)
