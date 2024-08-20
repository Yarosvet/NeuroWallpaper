"""Main application logic"""
import threading
import time
import base64
import os
import platform
import ctypes
from pathlib import Path
from typing import Any, Literal
from logging import getLogger
import inject
from PyQt6.QtWidgets import QApplication
from httpx import RequestError

from app.gui import Gui
from app.api_wrappers.kandinsky import KandinskyAPIWrapper, STATUS_DONE, STATUS_FAIL


@inject.autoparams()
def set_styles_to_gui_kandinsky(gui: Gui, kandinsky_api: KandinskyAPIWrapper):
    """Fetch from API and set the kandinsky styles to the GUI"""

    def _fetch_styles():
        try:
            getLogger("app").debug("Fetching styles...")
            styles = kandinsky_api.styles()
        except RequestError:
            getLogger("app").exception("Failed to fetch styles")
            return
        getLogger("app").debug("Styles fetched successfully")
        gui.bridge_set_styles([(style.name, style.title) for style in styles])

    t = threading.Thread(target=_fetch_styles, name="Kandinsky-fetch-styles", daemon=True)
    t.start()


@inject.autoparams()
def _set_desktop_wallpaper(image: bytes, f: str = 'jpeg', gui: Gui = None):
    """Set the desktop wallpaper"""
    # Save it to settings folder
    path = Path(gui.settings.base_path).joinpath(f"wallpaper.{f}")
    with open(path, "wb") as _f:
        _f.write(image)
    # Set as wallpaper
    # TODO: Add support for other OS and different desktop environments (or maybe create a library for that? mm?)
    if platform.system().lower() == 'linux':
        command = "gsettings set org.gnome.desktop.background picture-uri " + path.as_uri()
        command_dark = "gsettings set org.gnome.desktop.background picture-uri-dark " + path.as_uri()
        os.system(command)
        os.system(command_dark)
    elif platform.system().lower() == 'windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path.as_posix(), 0)
    else:
        getLogger("app").error("Unsupported OS: %s", platform.system())
        return
    getLogger("app").info("Wallpaper set successfully")


@inject.autoparams()
def generate_kandinsky_desktop_wallpaper(  # pylint: disable=too-many-arguments
        style: str,
        prompt: str,
        neg_prompt: str,
        app: QApplication,
        kandinsky_api: KandinskyAPIWrapper
):
    """Generate a desktop wallpaper using the Kandinsky API"""
    # Get dimensions of the screen
    w, h = app.primaryScreen().size().width(), app.primaryScreen().size().height()
    # By 19.08.2024, Kandinsky has limitation of (w + h) <= 3072
    wh_limit = 3072
    if w + h > wh_limit:
        # Let's make image smaller and keep the aspect ratio
        ratio = w / h
        h = int(wh_limit / (1 + ratio))
        w = int(ratio * h)

    def _generate_and_set():
        # Start generating the image
        getLogger("app").info("Generating image (%dx%d) using Kandinsky API...", w, h)
        try:
            image_status = kandinsky_api.text2image(
                model_id=kandinsky_api.text2image_model_id,
                style=style,
                prompt=prompt,
                neg_prompt=neg_prompt,
                width=w,
                height=h,
            )
            # Wait until the image is ready
            while image_status.status not in (STATUS_DONE, STATUS_FAIL):
                time.sleep(1)
                image_status = kandinsky_api.check_status(image_status.uuid)
                getLogger("app").debug("Status: %s", image_status.status)
        except RequestError:
            getLogger("app").exception("Failed to generate image")
            return
        if image_status.status == STATUS_DONE:
            if image_status.censored:
                # Just log a warning if the image was censored
                getLogger("app").warning("Generated image was censored")
                return  # Do not set the wallpaper 0_o
            # Set the desktop wallpaper if the image is ready
            image_bytes = base64.b64decode(image_status.images[0])
            _set_desktop_wallpaper(image_bytes, f='jpeg')
        else:
            # Show an error message if the image failed to generate
            getLogger("app").error("Failed to generate image: %s", image_status.error_description)

    t = threading.Thread(target=_generate_and_set, name="Kandinsky-generate-image", daemon=True)
    t.start()


def generate_desktop_wallpaper(api: Literal['kandinsky'], parameters: dict[str, Any]):
    """Generate a desktop wallpaper"""
    if api == 'kandinsky':
        generate_kandinsky_desktop_wallpaper(**parameters)
    else:
        getLogger("app").error("Unsupported API: %s", api)
