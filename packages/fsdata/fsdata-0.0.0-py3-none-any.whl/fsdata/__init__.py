"""fsspec data mapper"""

import os
import re

import pandas as pd

from functools import lru_cache
from configparser import ConfigParser, Interpolation

from upath import UPath



class ExpandVars(Interpolation):
    """Interpolation to expand environment variables"""

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


def config_dirs():
    """list of config dirs from environment or defaults"""
    config_dirs = os.getenv("FSDATA_CONFIG_DIRS", None)
    if config_dirs:
        return config_dirs.split(os.pathsep)
    
    config_home = os.getenv("XDG_CONFIG_HOME", "~/.config")
    config_dirs = os.getenv("XDG_CONFIG_DIRS", "/etc/xdg").split(os.pathsep)

    config_dirs = [config_home, *config_dirs]
    config_dirs = [os.path.expanduser(p) for p in config_dirs if len(p)]

    return config_dirs


@lru_cache
def read_config():
    """read configuration files"""
    config = ConfigParser(interpolation=ExpandVars())

    for folder in config_dirs():
        file = os.path.join(folder, "fsdata.ini")      
        if os.path.exists(file):
            config.read(file)

    return config


def check_path(path):
    """check and normalize path"""
    if re.match(r"^([a-z]):", path):
        prefix = ""
    else:
        prefix, _, path = path.rpartition(":")

    if prefix == "":
        prefix = "local"

    if path.startswith("~"):
        path = os.path.expanduser(path)

    if not path.startswith(("/", "\\")):
        raise ValueError(f"Path {path!r} is not absolute!")
    
    return prefix + ":" + path


class Collection:
    """collection of data files"""

    def __init__(self, name: str, path: str = None):
        path = check_path(path)
        self.name = name
        self.path = UPath(path)

    def __repr__(self):
        return f"Collection({self.name!r}, {self.path!r})"

    def items(self):
        return [p.stem for p in self.path.glob("*")]

    def load(self, name):
        file = self.path.joinpath(f"{name}.parquet")
        return pd.read_parquet(file.as_uri())
    
    def save(self, name, data):
        file = self.path.joinpath(f"{name}.parquet")
        data.to_parquet(file.as_uri())

    def remove(self, name):
        file = self.path.joinpath(f"{name}.parquet")
        if file.exists():
            file.unlink()
        else:
            raise FileNotFoundError(file)

@lru_cache
def __getattr__(name: str):
    """get collection by name"""
    config = read_config()

    if name.islower() and name in config:
        path = config.get(name, "path")
        return Collection(name, path)
    else:
        raise AttributeError(f"module 'fsdata' has no attribute '{name}'")


def __dir__():
    """list of collections"""
    config = read_config()

    result = [name.lower() for name in config.sections()]

    return result


