"""Main window of the application"""
from typing import Literal
from PyQt6.QtWidgets import QMainWindow

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

    def closeEvent(self, a0):  # pylint: disable=invalid-name
        """Close event"""
        self.close_cb()
        super().closeEvent(a0)

    def set_interval_value(self, value: int):
        """Set the interval value in minutes"""
        self.ui.interval_spinbox.setValue(value)

    def set_auto_generate_enabled(self, enabled: bool):
        """Set the auto generate enabled"""
        self.ui.auto_change_checkbox.setChecked(enabled)

    def get_auto_generate_enabled(self) -> bool:
        """Return the auto generate enabled"""
        return self.ui.auto_change_checkbox.isChecked()

    def set_radio_selected_api(self, api: Literal['kandinsky']):
        """Set the radio button for the selected API"""
        if api == 'kandinsky':
            self.ui.kandinsky_radiobtn.setChecked(True)

    def get_selected_api(self) -> Literal['kandinsky']:
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

    def get_interval_value(self) -> int:
        """Return the interval value in minutes"""
        return self.ui.interval_spinbox.value()
