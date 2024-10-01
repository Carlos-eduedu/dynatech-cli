import re

from typer.testing import CliRunner

from dynatech_cli import __version__
from dynatech_cli.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    output = ansi_escape.sub('', result.stdout)
    assert output == f"Dynatech CLI version: {__version__}\n"


def test_no_args():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Bem-vindo ao Dynatech CLI! 🚀" in result.stdout


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--version" in result.stdout
    assert "-v" in result.stdout
