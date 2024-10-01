from typing import List

from .exporter import Exporter
from .json_exporter import JsonExporter
from .txt_exporter import TxtExporter
from .types import ExporterType


def get_exporter(exporter_type: ExporterType) -> Exporter:
    """
    Retorna uma instância do exportador especificado.

    Args:
        exporter_type (ExporterType): Tipo do exportador.

    Returns:
        Exporter: Instância do exportador.
    """

    match exporter_type:
        case ExporterType.none:
            return Exporter()
        case ExporterType.json:
            return JsonExporter()
        case ExporterType.txt:
            return TxtExporter()
        case _:
            raise ValueError("Tipo de exportador inválido")


def save_map(links: List[str], save: ExporterType) -> None:
    """
    Salva o mapa em um arquivo.

    Args:
        links (List[str]): Lista de links.
        save (ExporterType): Tipo de exportador.

    Returns:
        None
    """
    exporter = get_exporter(save)
    exporter.export(links)
