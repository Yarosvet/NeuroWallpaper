"""Settings module for the application"""
import json
import platform
import os
from dataclasses import dataclass, field
from typing import Literal
from pathlib import Path

from app.types import DataDictMixin


@dataclass
class KandinskyConfig(DataDictMixin):
    """Kandinsky API configuration"""
    api_key: str = ''
    api_secret: str = ''
    selected_style: tuple[str, str] = ('DEFAULT', 'No style')
    negative_prompt: str = ""
    prompt: str = "Котики"  # Let's have some cats by default :)


@dataclass
class Parameters(DataDictMixin):
    """Settings parameters"""
    interval: int = 5
    auto_generate: bool = False
    selected_api: Literal['kandinsky'] = 'kandinsky'
    kandinsky_config: KandinskyConfig = field(default_factory=KandinskyConfig)


def default_settings_path() -> str:
    """Return the default settings path"""
    data_path = Path("data/")
    if platform.system() == "Windows":
        data_path = Path(os.getenv("APPDATA"), "NeuroWallpaper/")
    return data_path.joinpath("settings.json").absolute().as_posix()


class SettingsManager:
    """Class providing load and save settings with JSON"""

    def __init__(self, path: str):
        self.params = Parameters()
        self.file_path = path

    def load(self):
        """Update settings from saved file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.params = Parameters.from_dict(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            pass

    def save(self):
        """Save settings to file"""
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.params.to_dict(), f)
