from tftimeline.plot import LogParser
from tftimeline.models import OutputTypes
import typer
from typing import Optional


app = typer.Typer()

@app.command()
def main(
    output_path: Optional[str] = typer.Option(None, help="Filepath to write timeline to."),
    output_type: Optional[OutputTypes] = typer.Option(OutputTypes.html, help="File type to write.")
    ):
    logs = LogParser()
    logs.plot(output_path, output_type)

