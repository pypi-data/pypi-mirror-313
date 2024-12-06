import asyncio
import click
import zipfile

from pathlib import Path
from fediverse_pasture_inputs import available

from .format import page_from_inputs, add_samples_to_zip


async def run_for_path(path):
    for inputs in available.values():
        with open(f"{path}/{inputs.filename}", "w") as fp:
            await page_from_inputs(fp, inputs)


@click.group()
def main(): ...


@main.command()
def docs():
    path = "docs/inputs/"
    Path(path).mkdir(parents=True, exist_ok=True)
    asyncio.run(run_for_path(path))


@main.command()
def zip_file():
    path = "docs/assets/"
    Path(path).mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(f"{path}/samples.zip", "w") as zipcontainer:
        for inputs in available.values():
            asyncio.run(add_samples_to_zip(zipcontainer, inputs))


if __name__ == "__main__":
    main()
