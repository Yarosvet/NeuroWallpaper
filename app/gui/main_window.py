"""Main window of the application"""
import sys
from typing import Literal
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon
from PyQt6.QtCore import Qt, pyqtSlot

from app.types import QtCallback
from .view.ui_main_window import Ui_MainWindow
from .api_widgets import ApiWidget, KandinskyWidget


class MainWindow(QMainWindow):
    """Main window of the GUI"""

    def __init__(self):
        super().__init__()
        self.close_cb = QtCallback()
        self.params_edited_cb = QtCallback()
        self.generate_now_cb = QtCallback()
        self.api_changed_cb = QtCallback()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.interval_spinbox.valueChanged.connect(self.params_edited_cb.void_slot)
        self.ui.kandinsky_radiobtn.toggled.connect(self.api_changed_cb.void_slot)
        self.ui.auto_change_checkbox.checkStateChanged.connect(self.params_edited_cb.void_slot)
        self.ui.generate_button.clicked.connect(self.generate_now_cb.void_slot)

        # Build the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon()  # TODO: Set the icon
        self.tray_icon.activated.connect(self._tray_icon_activated)  # noqa  # Why IDE doesn't see connect() method?

    @pyqtSlot()
    def _tray_icon_activated(self):
        """Show the window"""
        self.tray_icon.hide()
        self.show()
        self.setWindowState(Qt.WindowState.WindowActive)

    def closeEvent(self, a0):  # pylint: disable=invalid-name
        """Close event"""
        if self.ui.hide_to_tray_checkbox.isChecked():
            # Hide to tray
            a0.ignore()
            self.tray_icon.show()
            self.hide()
        else:
            self.close_cb()
            super().closeEvent(a0)
            sys.exit(0)

    def set_interval_value(self, value: int):
        """Set the interval value in minutes"""
        self.ui.interval_spinbox.setValue(value)

    def set_auto_generate_enabled(self, enabled: bool):
        """Set the auto generate enabled"""
        self.ui.auto_change_checkbox.setChecked(enabled)

    @property
    def auto_generate_enabled(self) -> bool:
        """Return the auto generate enabled"""
        return self.ui.auto_change_checkbox.isChecked()

    def set_radio_selected_api(self, api: Literal['kandinsky']):
        """Set the radio button for the selected API"""
        if api == 'kandinsky':
            self.ui.kandinsky_radiobtn.setChecked(True)

    @property
    def selected_api(self) -> Literal['kandinsky']:
        """Return the selected API"""
        if self.ui.kandinsky_radiobtn.isChecked():
            return 'kandinsky'
        return 'kandinsky'  # Default

    def set_api_widget_scheme(self, widget: type[ApiWidget]):
        """Set the API parameters widget"""
        # Clear the layout
        for i in reversed(range(self.ui.api_parameters_layout.count())):
            self.ui.api_parameters_layout.itemAt(i).widget().deleteLater()
        # Add the widget
        self.ui.api_parameters_layout.addWidget(widget())

    def api_widget(self) -> ApiWidget | None:
        """Return the API parameters widget"""
        item = self.ui.api_parameters_layout.itemAt(0)
        return item.widget() if item is not None else None

    def kandinsky_widget_or_none(self) -> KandinskyWidget | None:
        """Return the Kandinsky widget if it's selected or None"""
        widget = self.api_widget()
        return widget if isinstance(widget, KandinskyWidget) else None

    @property
    def interval_value(self) -> int:
        """Return the interval value in minutes"""
        return self.ui.interval_spinbox.value()

    def set_last_gen_state(self, time_str: str, is_ok: bool):
        """Set the last generation state"""
        self.ui.generation_time_label.setText(time_str)
        self.ui.generation_state_label.setText("OK" if is_ok else "FAILED")  # TODO: use icons

    def set_hide_to_tray_enabled(self, enabled: bool):
        """Set the hide to tray enabled"""
        self.ui.hide_to_tray_checkbox.setChecked(enabled)

    @property
    def hide_to_tray_enabled(self) -> bool:
        """Return the hide to tray enabled"""
        return self.ui.hide_to_tray_checkbox.isChecked()
