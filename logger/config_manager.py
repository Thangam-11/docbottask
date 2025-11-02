"""
Configuration manager for loading and accessing config
"""
import yaml
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """Manages application configuration"""

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._auto_load_config()  # ✅ Automatically load on first creation
        return cls._instance

    def _auto_load_config(self):
        """Automatically load the default configuration file"""
        default_path = Path("configure/config.yaml")

        if not default_path.exists():
            raise FileNotFoundError(f"Default config file not found: {default_path.resolve()}")

        with open(default_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    def load_config(self, config_path: str = "configure/config.yaml") -> Dict[str, Any]:
        """Manually reload configuration from YAML file"""
        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_file, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports nested keys with dot notation)"""
        if self._config is None:
            self._auto_load_config()  # fallback

        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default

        return value

    def get_model_config(self) -> Dict[str, str]:
        """Get model configuration"""
        return self.get("models", {})

    def get_paths(self) -> Dict[str, str]:
        """Get path configuration"""
        return self.get("paths", {})

    def get_chunking_config(self) -> Dict[str, int]:
        """Get chunking configuration"""
        return self.get("chunking", {})

    def get_retrieval_config(self) -> Dict[str, int]:
        """Get retrieval configuration"""
        return self.get("retrieval", {})
