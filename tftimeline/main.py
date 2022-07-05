from tftimeline.plot import LogParser
from tftimeline.models import OutputTypes
import typer
from typing import Optional


app = typer.Typer()

@app.command()
def main(
    output_path: Optional[str] = typer.Option(None, help="Filepath to write timeline to."),
    output_type: Optional[OutputTypes] = typer.Option(OutputTypes.html, help="File type to write."),
    height: Optional[int] = typer.Option(1200, help="Height in pixel equivilent for image rendering."),
    width: Optional[int] = typer.Option(1600, help="Height in pixel equivilent for image rendering.")
    ):
    logs = LogParser()
    logs.plot(output_path, output_type, height, width)

