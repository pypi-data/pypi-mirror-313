from typing import Any

import yaml
import os
import codecs
from .env_loader import EnvLoader


class Config:
    def __init__(self, *config_dirs: str) -> None:
        self.config = dict[str, Any]()

        for config_dir in config_dirs:
            self.config.update(self.load_config(config_dir))

        if not self.config:
            raise ValueError(f"Config is empty! Check {config_dirs=}")

    def get(self) -> dict[str, Any]:
        return self.config

    @staticmethod
    def load_config(path: str | None = None) -> dict[str, Any]:
        if not path:
            return {}
        if path.endswith("/"):
            path = path[:-1]
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config is not present! {path=}")
        with codecs.open(f"{path}/config.yaml", encoding="utf-8") as file:
            config: dict[str, Any] = yaml.load(file, EnvLoader)
            return config
