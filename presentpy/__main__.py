from pathlib import Path

import click

from presentpy.parser import process_notebook


@click.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--theme", type=click.Choice(["light", "dark"], case_sensitive=False), default="light")
def process(file, theme):
    path = Path(file)
    presentation = process_notebook(path, theme)
    presentation.save(f"{path.stem}.pptx")


if __name__ == "__main__":
    process()
