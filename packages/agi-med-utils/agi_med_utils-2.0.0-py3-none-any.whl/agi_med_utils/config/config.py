import yaml
import os
import codecs
from .env_loader import EnvLoader
from ..extentions.signleton_meta import SingletonMeta


class ConfigSingleton(metaclass=SingletonMeta):
    def __init__(self, *config_dirs):
        self.config = dict()

        for config_dir in config_dirs:
            self.config.update(self.load_config(config_dir))

        assert len(self.config), "Error: empty config!"

    def get(self):
        return self.config

    @staticmethod
    def load_config(path=None):
        if path is not None:
            if path.endswith("/"):
                path = path[:-1]
            assert os.path.exists(path), "Error: config unavailable!"
            with codecs.open(f"{path}/config.yaml", encoding="utf-8") as file:
                return yaml.load(file, EnvLoader)
        return {}
