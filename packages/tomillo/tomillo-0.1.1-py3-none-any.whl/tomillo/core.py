from tomillo.log_prep import config as logconf
from bshlib.utils import super_touch

from pathlib import Path
from loguru import logger
import tomlkit
import os

logconf()

class Configuration(object):

    stgfile: Path
    map: dict

    def __new__(cls, project: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    def __init__(self, project: str):
        self.stgfile = Path(os.environ["HOME"]) / '.config' / project / 'settings.toml'
        logger.debug('parsing settings file..')
        self.map = self.parse_settings()

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        self.map[key] = value
        self.save_settings()

    def parse_settings(self):
        try:
            with open(self.stgfile, 'rt') as f:
                stg = tomlkit.load(f)
            logger.success('settings applied')
        except FileNotFoundError:
            super_touch(self.stgfile)
            stg = {}
            logger.success('settings initialized')
        return stg

    def save_settings(self):
        with open(self.stgfile, 'wt') as f:
            tomlkit.dump(self.map, f)
        logger.success('settings saved')
