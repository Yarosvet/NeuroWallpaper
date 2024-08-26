"""Kandinsky API wrapper"""
import json
import functools
from dataclasses import dataclass

import httpx


@dataclass
class Style:
    """Data class for a style"""
    name: str
    title: str
    title_en: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Style":
        """Create a Style object from a dictionary"""
        return cls(data["name"], data["title"], data["titleEn"])


DEFAULT_STYLES = [
    Style("KANDINSKY", "Кандинский", "Kandinsky"),
    Style("UHD", "Детальное фото", "Detailed photo"),
    Style("ANIME", "Аниме", "Anime"),
    Style("DEFAULT", "Свой стиль", "No style"),
]

STATUS_INITIAL = "INITIAL"
STATUS_PROCESSING = "PROCESSING"
STATUS_DONE = "DONE"
STATUS_FAIL = "FAIL"


@dataclass
class Text2ImageStatus:
    """Data class for a task of `GENERATE` type"""
    uuid: str
    status: str
    images: list[str] | None
    error_description: str | None
    censored: bool | None

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Text2ImageStatus":
        """Create a TaskGenerate object from a dictionary"""
        return cls(
            data.get("uuid"),
            data.get("status"),
            data.get("images", None),
            data.get("errorDescription", None),
            data.get("censored", None)
        )


class KandinskyAPIWrapper:
    """Wrapper for the Kandinsky API"""

    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.auth_headers = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}"
        }
        self.base_url = "https://api-key.fusionbrain.ai/key/api/v1"

    def set_credentials(self, api_key: str, secret_key: str):
        """Set the API key and secret key"""
        self.auth_headers.update({
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}"
        })

    def text2image(  # pylint: disable=too-many-arguments
            self,
            model_id: int,
            style: str,
            prompt: str,
            neg_prompt: str,
            width: int,
            height: int
    ) -> Text2ImageStatus:
        """Run a text-2-image task"""
        url = f"{self.base_url}/text2image/run"
        params = {
            "type": "GENERATE",
            "style": style,
            "width": width,
            "height": height,
            "num_images": 1,
            "negativePromptUnclip": neg_prompt,
            "generateParams": {
                "query": prompt,
            }
        }
        data = {
            'model_id': (None, str(model_id)),
            'params': (None, json.dumps(params), 'application/json')
        }
        r = httpx.request('POST', url, files=data, headers=self.auth_headers)
        r.raise_for_status()  # Raise an exception if the request failed
        return Text2ImageStatus.from_dict(r.json())

    @functools.cached_property
    def text2image_model_id(self) -> int:
        """Get the ID of the text-2-image model (the first one)"""
        url = f"{self.base_url}/models"
        r = httpx.request("GET", url, headers=self.auth_headers)
        r.raise_for_status()  # Raise an exception if the request failed
        return r.json()[0]['id']

    def check_status(self, uuid: str) -> Text2ImageStatus:
        """Check the status of a text-2-image task"""
        url = f"{self.base_url}/text2image/status/{uuid}"
        r = httpx.request("GET", url, headers=self.auth_headers)
        r.raise_for_status()
        return Text2ImageStatus.from_dict(r.json())
