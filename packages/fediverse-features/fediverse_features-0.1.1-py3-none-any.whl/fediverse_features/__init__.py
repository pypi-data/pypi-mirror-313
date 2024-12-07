import tempfile
import zipfile
import tomllib
import pathlib

from dataclasses import dataclass, field
from contextlib import contextmanager
from urllib.request import urlretrieve
from typing import List


def make_url(tag):
    return f"https://codeberg.org/api/packages/helge/generic/fediverse-features/{tag}/fediverse_features.zip"


@contextmanager
def fediverse_features_archive(tag):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = f"{tmpdirname}/features.zip"
        urlretrieve(make_url(tag), filename)
        with zipfile.ZipFile(filename) as fp:
            yield fp


@dataclass
class Config:
    tag: str = "0.1.6"
    features: List[str] = field(default_factory=list)
    target: str = "features/fediverse-features/"


def load_config(filename: str = "fediverse-features.toml") -> Config:
    data = {}
    if pathlib.Path(filename).exists():
        with open(filename, "rb") as fp:
            data = tomllib.load(fp)
    return Config(**data)
