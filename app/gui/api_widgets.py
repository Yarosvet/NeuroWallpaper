"""Module of API widgets for the GUI."""
from PyQt6.QtWidgets import QWidget, QRadioButton, QVBoxLayout

from app.types import QtCallback
from .view.ui_kandinsky_widget import Ui_KandinskyWidget


class ApiWidget(QWidget):  # pylint: disable=too-few-public-methods
    """Base class for API widgets"""


class KandinskyWidget(ApiWidget):
    """Widget for the Kandinsky API"""

    def __init__(self):
        super().__init__()
        self.params_edited_cb = QtCallback()

        self.ui = Ui_KandinskyWidget()
        self.ui.setupUi(self)
        self.ui.styles_group_box.setLayout(QVBoxLayout())  # Set the layout for the radio buttons

        self.ui.apikey_lineedit.textChanged.connect(self.params_edited_cb.void_slot)
        self.ui.apisecret_lineedit.textChanged.connect(self.params_edited_cb.void_slot)
        self.ui.negative_prompt_lineedit.textChanged.connect(self.params_edited_cb.void_slot)
        self.ui.prompt_lineedit.textChanged.connect(self.params_edited_cb.void_slot)

    def set_styles(self, styles: list[tuple[str, str]]):
        """Set the list of styles"""
        # Delete all the children of the group box
        for c in self.ui.styles_group_box.children():
            c.deleteLater()
        # Add a radio button for each style
        for name, title in styles:
            radio_button = QRadioButton(title, parent=self.ui.styles_group_box)
            radio_button.setObjectName(f"radio_{name}")
            # Set data to the radio button
            radio_button.setProperty('style_name', name)
            self.ui.styles_group_box.layout().addWidget(radio_button)
            # Connect to the callback
            radio_button.toggled.connect(  # noqa  # Why IDE doesn't see connect() method?
                self.params_edited_cb.void_slot)
        # Select the first radio button
        radio = [c for c in self.ui.styles_group_box.children() if isinstance(c, QRadioButton)]
        radio[0].setChecked(True)

    def set_selected_style(self, style_name: str):
        """Set the selected style"""
        for c in self.ui.styles_group_box.children():
            if isinstance(c, QRadioButton) and c.property('style_name') == style_name:
                c.setChecked(True)
                break

    def get_selected_style(self) -> tuple[str, str]:
        """Return the selected style"""
        for c in self.ui.styles_group_box.children():
            if isinstance(c, QRadioButton) and c.isChecked():
                return c.property('style_name'), c.text()
        return 'DEFAULT', 'No style'  # Default

    def set_api_key(self, api_key: str):
        """Set the API key"""
        self.ui.apikey_lineedit.setText(api_key)

    def get_api_key(self) -> str:
        """Return the API key"""
        return self.ui.apikey_lineedit.text()

    def set_secret(self, secret_key: str):
        """Set the secret key"""
        self.ui.apisecret_lineedit.setText(secret_key)

    def get_secret(self) -> str:
        """Return the secret key"""
        return self.ui.apisecret_lineedit.text()

    def set_negative_prompt(self, text: str):
        """Set the negative prompt"""
        self.ui.negative_prompt_lineedit.setText(text)

    def get_negative_prompt(self) -> str:
        """Return the negative prompt"""
        return self.ui.negative_prompt_lineedit.text()

    def set_prompt(self, text: str):
        """Set the prompt"""
        self.ui.prompt_lineedit.setPlainText(text)

    def get_prompt(self) -> str:
        """Return the prompt"""
        return self.ui.prompt_lineedit.toPlainText()
