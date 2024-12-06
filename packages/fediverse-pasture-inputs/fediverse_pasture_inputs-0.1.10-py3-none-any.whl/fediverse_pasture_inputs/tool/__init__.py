import tempfile
import zipfile

from typing import Generator
from contextlib import contextmanager
from urllib.request import urlretrieve

from fediverse_pasture_inputs.version import __version__


def make_url(tag):
    return f"https://codeberg.org/api/packages/funfedidev/generic/fediverse_pasture_assets/{tag}/fediverse_pasture_assets.zip"


@contextmanager
def current_asset_archive(
    tag: str = __version__,
) -> Generator[zipfile.ZipFile, None, None]:
    """
    Provides the zipfile for `tag` as a generator.

    ```pycon
    >>> with current_asset_archive("0.1.8") as assets:
    ...     assets.namelist()
        ['assets/', 'assets/note2.jsonap', ...]

    ```
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = f"{tmpdirname}/assets.zip"
        urlretrieve(make_url(tag), filename)
        with zipfile.ZipFile(filename) as fp:
            yield fp


def extract(tag: str = __version__):
    """Extracts the zipfile"""
    with current_asset_archive(tag) as archive:
        archive.extractall()
