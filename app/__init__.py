"""Application module"""
import pathlib
from logging import getLogger
import inject
from PyQt6.QtWidgets import QApplication

from .gui import Gui, settings
from .api_wrappers.kandinsky import KandinskyAPIWrapper
from .loggers import init_logger
from . import core


def config_injector(binder: inject.Binder):
    """Configure the injector"""
    binder.bind(QApplication, QApplication([]))
    binder.bind(KandinskyAPIWrapper, KandinskyAPIWrapper())
    binder.bind(Gui, Gui(settings_path=settings.default_settings_path()))


def run():
    """Run the application"""
    # Initialize the logger
    init_logger((pathlib.Path(settings.default_settings_path()) / "app.log").as_posix())
    getLogger("app").info("Starting the application")
    # Configure the dependency injector
    inject.configure(config_injector)
    # Build the GUI (second part of the constructor; after loading deps)
    inject.instance(Gui).build_requiring_deps()
    # Set the callbacks between the GUI and the core
    inject.instance(Gui).cb_generate.set_callable(core.generate_desktop_wallpaper)
    # Show the GUI
    inject.instance(Gui).show()
    # Run the application
    try:
        inject.instance(QApplication).exec()
    finally:
        getLogger("app").info("Application finished")
