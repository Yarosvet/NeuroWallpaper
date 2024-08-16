"""Application module"""
import inject
from PyQt6.QtWidgets import QApplication

from .gui import Gui, settings
from .api_wrappers.kandinsky import KandinskyAPIWrapper


def config_injector(binder: inject.Binder):
    """Configure the injector"""
    binder.bind(KandinskyAPIWrapper, KandinskyAPIWrapper())


def run():
    """Run the application"""
    inject.configure(config_injector)

    app = QApplication([])
    graphics = Gui(settings_path=settings.default_settings_path())
    graphics.show()
    app.exec()
