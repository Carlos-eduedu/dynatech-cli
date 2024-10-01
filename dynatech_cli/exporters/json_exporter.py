from json import dumps
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.prompt import Prompt

from .exporter import Exporter

console = Console()


class JsonExporter(Exporter):
    FILE_NAME_DEFAULT = "map.json"
    FILE_PATH_DEFAULT = "."

    @classmethod
    def _convert_to_json(cls, data: Any) -> str:
        return dumps(data, indent=4, ensure_ascii=False)

    def _ask_for_file_name(self) -> str:
        return Prompt.ask(
            "Digite o nome do arquivo", default=self.FILE_NAME_DEFAULT
            )

    def _ask_for_file_path(self) -> Path:
        file_path = Path(Prompt.ask(
            "Digite o caminho do arquivo", default=self.FILE_PATH_DEFAULT
            )
        )

        if not file_path.exists():
            console.print(f"[red]O caminho {file_path} não existe![/red]")
            return self._ask_for_file_path()

        return file_path

    def export(self, data: Any) -> None:
        json_data = self._convert_to_json(data)
        file_name = self._ask_for_file_name()
        file_path = self._ask_for_file_path()

        with open(file_path / file_name, "w", encoding="utf-8") as file:
            file.write(json_data)
            console.print(
                f"[green]Arquivo {file_name} salvo com sucesso![/green]"
                )
