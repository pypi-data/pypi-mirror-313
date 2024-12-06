import json
from pathlib import Path

CWD = Path(".")
JSON_CONFIG = CWD / "config.json"


class Config:
    """Configuration class for torrent worker."""

    KEY_DOWNLOAD = "download_dir"
    KEY_TORRENTS_SOURCE = "torrents_source"

    def __init__(self):
        self._config = self._load_config()

    @property
    def download_dir(self) -> str | None:
        return self._config.get(self.KEY_DOWNLOAD)

    @download_dir.setter
    def download_dir(self, value: str) -> None:
        self._config[self.KEY_DOWNLOAD] = value
        self._save_config()

    @property
    def torrents_source(self) -> str | None:
        return self._config.get(self.KEY_TORRENTS_SOURCE)

    @torrents_source.setter
    def torrents_source(self, value: str) -> None:
        self._config[self.KEY_TORRENTS_SOURCE] = value
        self._save_config()

    @property
    def app_data(self) -> Path:
        return Path("bittorrent") / "appdata"

    def _load_config(self) -> dict:
        """Load config from JSON file."""
        if JSON_CONFIG.exists():
            with open(JSON_CONFIG, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_config(self) -> None:
        """Save config to JSON file."""
        with open(JSON_CONFIG, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=4)
