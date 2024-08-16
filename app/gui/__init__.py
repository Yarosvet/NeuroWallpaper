"""This module contains the main GUI class for the application"""
import inject
from PyQt6.QtCore import QTimer

from app.types import SimpleCallback, PendingCallback
from app.api_wrappers.kandinsky import KandinskyAPIWrapper
from .main_window import MainWindow
from .api_widgets import KandinskyWidget
from .settings import SettingsManager


class Gui:
    """Graphical user interface for the application"""

    def __init__(self, settings_path: str):
        self.cb_generate = SimpleCallback()  # It'll be triggered when it's time to generate a new picture (all cases)
        self.cb_fetch_styles = PendingCallback()  # It'll be triggered when it's time to fetch the styles for Kandinsky

        # Load settings
        self.settings = SettingsManager(settings_path)
        self.settings.load()

        # Create the main window
        self.main_window = MainWindow()

        # Configure timer
        self.timer_generate = QTimer(parent=self.main_window)
        self.timer_generate.timeout.connect(self.cb_generate)  # noqa  # Why IDE doesn't see connect() method?

        # Build from settings
        self.timer_generate.setInterval(self.settings.params.interval * 60 * 1000)  # Convert minutes to milliseconds
        self.main_window.set_interval_value(self.settings.params.interval)
        self.main_window.set_auto_generate_enabled(self.settings.params.auto_generate)
        self.build_api_widget_from_settings()  # pylint: disable=no-value-for-parameter

        # Set callbacks
        self.main_window.close_cb.set_callable(self.settings.save)  # Save settings on close
        self.main_window.params_edited_cb.set_callable(self.update_model)  # Update settings on UI params change
        self.main_window.generate_now_cb.set_callable(self.cb_generate)  # Generate now callback
        self.main_window.api_changed_cb.set_callable(self._update_and_save_selected_api)  # Update selected API

    def build_api_widget_from_settings(self, kandinsky_api: KandinskyAPIWrapper = inject.attr(KandinskyAPIWrapper)):
        """Build the API widget parameters from settings"""
        if self.settings.params.selected_api == 'kandinsky':
            self.main_window.set_radio_selected_api('kandinsky')
            self.main_window.set_api_widget_scheme(KandinskyWidget)
            if (kandinsky := self.main_window.kandinsky_widget_or_none()) is not None:
                kandinsky.set_styles([self.settings.params.kandinsky_config.selected_style])
                kandinsky.set_api_key(self.settings.params.kandinsky_config.api_key)
                kandinsky.set_secret(self.settings.params.kandinsky_config.api_secret)
                kandinsky.set_negative_prompt(self.settings.params.kandinsky_config.negative_prompt)
                kandinsky.set_prompt(self.settings.params.kandinsky_config.prompt)
                # Configure the wrapper
                kandinsky_api.set_credentials(
                    self.settings.params.kandinsky_config.api_key,
                    self.settings.params.kandinsky_config.api_secret
                )
                # Now send a callback to fetch the styles
                self.cb_fetch_styles()  # It's a pending callback, will be executed when the function is set
                # Set callback for parameters change
                kandinsky.params_edited_cb.set_callable(self.update_settings)

    def update_model(self):
        """Update the internal model from the GUI"""
        self.update_settings()
        # Update interval
        self.timer_generate.setInterval(self.settings.params.interval * 60 * 1000)  # Convert minutes to milliseconds
        # Update auto generate timer state
        if self.settings.params.auto_generate and not self.timer_generate.isActive():
            # If auto generate is enabled and timer is not active
            self.timer_generate.start()
        elif not self.settings.params.auto_generate and self.timer_generate.isActive():
            # If auto generate is disabled and timer is active
            self.timer_generate.stop()

    def update_settings(self, kandinsky_api: KandinskyAPIWrapper = inject.attr(KandinskyAPIWrapper)):
        """Update the settings from the GUI"""
        self.settings.params.interval = self.main_window.get_interval_value()
        self.settings.params.auto_generate = self.main_window.get_auto_generate_enabled()
        self.settings.params.selected_api = self.main_window.get_selected_api()
        if self.settings.params.selected_api == 'kandinsky':
            if (kandinsky := self.main_window.kandinsky_widget_or_none()) is not None:
                self.settings.params.kandinsky_config.selected_style = kandinsky.get_selected_style()
                self.settings.params.kandinsky_config.api_key = kandinsky.get_api_key()
                self.settings.params.kandinsky_config.api_secret = kandinsky.get_secret()
                self.settings.params.kandinsky_config.negative_prompt = kandinsky.get_negative_prompt()
                self.settings.params.kandinsky_config.prompt = kandinsky.get_prompt()
                # Configure the wrapper
                kandinsky_api.set_credentials(
                    self.settings.params.kandinsky_config.api_key,
                    self.settings.params.kandinsky_config.api_secret
                )

    def show(self):
        """Show the GUI"""
        self.main_window.show()

    def _update_and_save_selected_api(self):
        """Update the selected API"""
        self.update_settings()
        self.build_api_widget_from_settings()  # pylint: disable=no-value-for-parameter

    def set_kandinsky_styles(self, styles: list[tuple[str, str]]):
        """Set the Kandinsky styles in the widget if it's selected"""
        if (kandinsky := self.main_window.kandinsky_widget_or_none()) is not None:
            kandinsky.set_styles(styles)
            kandinsky.set_selected_style(self.settings.params.kandinsky_config.selected_style[0])
