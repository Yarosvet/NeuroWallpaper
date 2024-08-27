"""Main application logic"""
import threading
import time
import base64
import os
import platform
import ctypes
import sys
from pathlib import Path
from typing import Any, Literal
from collections.abc import Callable
from logging import getLogger
import inject
from PyQt6.QtWidgets import QApplication
from httpx import RequestError

from app.gui import Gui
from app.api_wrappers.kandinsky import KandinskyAPIWrapper, STATUS_DONE, STATUS_FAIL


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


# TODO: Refactor this (too complex algorithm)
@inject.autoparams()
def generate_kandinsky_desktop_wallpaper(  # pylint: disable=too-many-arguments,too-complex
        style: str,
        prompt: str,
        neg_prompt: str,
        app: QApplication,
        kandinsky_api: KandinskyAPIWrapper,
        on_finish: Callable[[bool], None] = None
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
        success = False
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
            if image_status.status == STATUS_DONE:
                if image_status.censored:
                    # Just log a warning if the image was censored
                    getLogger("app").warning("Generated image was censored")
                    return  # Do not set the wallpaper 0_o
                # Set the desktop wallpaper if the image is ready
                image_bytes = base64.b64decode(image_status.images[0])
                _set_desktop_wallpaper(image_bytes, f='jpeg')
                success = True  # Set the flag which will be passed to the callback
            else:
                # Show an error message if the image failed to generate
                getLogger("app").error("Failed to generate image: %s", image_status.error_description)
        except RequestError:
            getLogger("app").exception("Failed to generate image")
            return
        finally:
            if on_finish is not None:
                on_finish(success)

    t = threading.Thread(target=_generate_and_set, name="Kandinsky-generate-image", daemon=True)
    t.start()


@inject.autoparams()
def generate_desktop_wallpaper(api: Literal['kandinsky'], parameters: dict[str, Any], gui: Gui):
    """Generate a desktop wallpaper"""

    def _on_finish_generation(is_ok: bool):
        """Callback for when the generation finishes"""
        gui.bridge_gen_state(time.time(), is_ok)  # Set state in the GUI via QtBridge
        gui.bridge_set_loading(False)  # Hide the loading spinner

    if api == 'kandinsky':
        gui.bridge_set_loading(True)  # Show the loading spinner
        generate_kandinsky_desktop_wallpaper(**parameters, on_finish=_on_finish_generation)
    else:
        getLogger("app").error("Unsupported API: %s", api)


def _update_startup_entry_windows(run_at_startup: bool):
    """Update the startup entry on Windows"""
    import winreg  # pylint: disable=import-outside-toplevel
    # TODO: Test it on Windows
    app_name = "NeuroWallpaper"
    if not hasattr(sys, '_MEIPASS'):
        getLogger("app").warning(
            "Cannot add startup entry in non-frozen mode (available with compiled executable only)"
        )
        return
    exe_path_with_arg = f'"{sys.executable}" --startup'
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
            if run_at_startup:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path_with_arg)
                getLogger("app").info("Startup entry added successfully")
            else:
                winreg.DeleteValue(key, app_name)
                getLogger("app").info("Startup entry removed successfully")
    except FileNotFoundError:
        getLogger("app").error("Registry key not found: %s", key_path)
    except PermissionError:
        getLogger("app").error("Permission denied while accessing the registry. Try running as administrator.")
    except Exception as e:  # pylint: disable=broad-except
        getLogger("app").exception("Failed to update startup entry: %s", e)


def _update_startup_entry_linux(run_at_startup: bool):
    """Update the startup entry on Linux"""
    # TODO: add support for other desktop environments
    app_name = "NeuroWallpaper"
    if hasattr(sys, '_MEIPASS'):  # If we are running in a frozen environment
        exec_str = Path(sys.executable).as_posix()
    else:
        exec_str = f"{Path(sys.executable).as_posix()} {Path(sys.argv[0]).as_posix()}"  # Python and script path
    desktop_entry = f"""[Desktop Entry]
Type=Application
Exec={exec_str} --startup
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name={app_name}
Comment=Start {app_name} at login"""
    autostart_dir = Path.home().joinpath(".config", "autostart")
    autostart_dir.mkdir(parents=True, exist_ok=True)
    desktop_file = autostart_dir.joinpath(f"{app_name}.desktop")

    try:
        if run_at_startup:
            with open(desktop_file, "w", encoding='utf-8') as f:
                f.write(desktop_entry)
            getLogger("app").info("Startup entry added successfully")
        else:
            if desktop_file.exists():
                desktop_file.unlink()
            getLogger("app").info("Startup entry removed successfully")
    except Exception as e:  # pylint: disable=broad-except
        getLogger("app").exception("Failed to update startup entry: %s", e)


def update_startup_entry(run_at_startup: bool):
    """Update the startup entry"""
    if platform.system().lower() == 'linux':
        _update_startup_entry_linux(run_at_startup)
    elif platform.system().lower() == 'windows':
        _update_startup_entry_windows(run_at_startup)
    else:
        getLogger("app").error("Unsupported OS: %s", platform.system())
