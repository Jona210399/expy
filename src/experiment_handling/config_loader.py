from omegaconf import OmegaConf, DictConfig, SCMode
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_yaml_path: Path) -> None:
        self.config_yaml_path = config_yaml_path
        self.config = self._load_config()

    def _load_config(self) -> DictConfig:
        return OmegaConf.load(self.config_yaml_path)

    def get_config(self) -> DictConfig:
        return self.config

    def get_config_as_dataclass(self, dataclass: type) -> object:
        schema = OmegaConf.structured(dataclass)
        config = OmegaConf.merge(self.config, schema)
        OmegaConf.set_readonly(config, False)
        return OmegaConf.to_container(
            config,
            resolve=True,
            throw_on_missing=True,
            structured_config_mode=SCMode.INSTANTIATE,
        )

    def get_config_as_dict(self) -> dict:
        return OmegaConf.to_container(self.config)
