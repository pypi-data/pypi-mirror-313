import typer

from importlib.metadata import entry_points
from pathlib import Path
from ._settings import Settings, paths

settings = Settings()

app = typer.Typer()

for plugin in entry_points(group="tubescience.cli"):
    plugin_app = plugin.load()
    if not isinstance(plugin_app, typer.Typer):
        continue
    app.add_typer(plugin_app, name=plugin.name)


@app.command()
def show_settings():
    from rich.console import Console
    console = Console()
    console.print(settings.model_dump_json(indent=4))


if __name__ == "__main__":  # pragma: no cover
    app()
