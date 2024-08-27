# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 600))
        MainWindow.setMaximumSize(QtCore.QSize(600, 35500))
        MainWindow.setStyleSheet("QWidget {  /*QMainWindow etc.*/\n"
"    background-color: rgb(33, 33, 33);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: white;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QRadioButton{\n"
"    color: white;\n"
"    font: 10pt \"Inter\";\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    background-color: #46A229;\n"
"    color: white;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:!enabled {\n"
"    background-color: #8FD17B;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #467935;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #23690D;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width:                  10px;\n"
"    height:                 10px;\n"
"    border:                 2px solid white;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color:       #46A229;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color:       rgb(48, 48, 48);\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: white\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width:                  10px;\n"
"    height:                 10px;\n"
"    border-radius:          7px;\n"
"    border:                 2px solid white;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color:       #46A229;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    background-color:       rgb(48, 48, 48);\n"
"}\n"
"\n"
"QSpinBox {\n"
"    color: white;\n"
"    background-color: rgb(48, 48, 48);\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"#frame, #api_params_frame {\n"
"    background: none;\n"
"    border: 1px solid rgb(44, 44, 44);\n"
"    border-radius: 3px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.interval_label = QtWidgets.QLabel(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interval_label.sizePolicy().hasHeightForWidth())
        self.interval_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(12)
        font.setBold(False)
        self.interval_label.setFont(font)
        self.interval_label.setObjectName("interval_label")
        self.horizontalLayout_4.addWidget(self.interval_label)
        spacerItem = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.interval_spinbox = QtWidgets.QSpinBox(parent=self.frame)
        self.interval_spinbox.setMinimumSize(QtCore.QSize(70, 0))
        self.interval_spinbox.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono")
        font.setPointSize(11)
        self.interval_spinbox.setFont(font)
        self.interval_spinbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.interval_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.interval_spinbox.setKeyboardTracking(True)
        self.interval_spinbox.setMinimum(5)
        self.interval_spinbox.setMaximum(43200)
        self.interval_spinbox.setObjectName("interval_spinbox")
        self.horizontalLayout_4.addWidget(self.interval_spinbox)
        self.min_label = QtWidgets.QLabel(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.min_label.sizePolicy().hasHeightForWidth())
        self.min_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(False)
        self.min_label.setFont(font)
        self.min_label.setObjectName("min_label")
        self.horizontalLayout_4.addWidget(self.min_label)
        spacerItem1 = QtWidgets.QSpacerItem(160, 17, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.auto_change_checkbox = QtWidgets.QCheckBox(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(False)
        self.auto_change_checkbox.setFont(font)
        self.auto_change_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.auto_change_checkbox.setObjectName("auto_change_checkbox")
        self.horizontalLayout_4.addWidget(self.auto_change_checkbox)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.hide_to_tray_checkbox = QtWidgets.QCheckBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        font.setBold(False)
        self.hide_to_tray_checkbox.setFont(font)
        self.hide_to_tray_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.hide_to_tray_checkbox.setObjectName("hide_to_tray_checkbox")
        self.verticalLayout_4.addWidget(self.hide_to_tray_checkbox)
        self.run_at_startup_checkbox = QtWidgets.QCheckBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        self.run_at_startup_checkbox.setFont(font)
        self.run_at_startup_checkbox.setObjectName("run_at_startup_checkbox")
        self.verticalLayout_4.addWidget(self.run_at_startup_checkbox)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.api_groupbox = QtWidgets.QGroupBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(12)
        font.setBold(False)
        self.api_groupbox.setFont(font)
        self.api_groupbox.setObjectName("api_groupbox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.api_groupbox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.kandinsky_radiobtn = QtWidgets.QRadioButton(parent=self.api_groupbox)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.kandinsky_radiobtn.setFont(font)
        self.kandinsky_radiobtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.kandinsky_radiobtn.setChecked(True)
        self.kandinsky_radiobtn.setAutoExclusive(True)
        self.kandinsky_radiobtn.setObjectName("kandinsky_radiobtn")
        self.verticalLayout_3.addWidget(self.kandinsky_radiobtn)
        self.verticalLayout_2.addWidget(self.api_groupbox)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.api_params_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.api_params_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.api_params_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.api_params_frame.setObjectName("api_params_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.api_params_frame)
        self.verticalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.api_parameters_layout = QtWidgets.QGridLayout()
        self.api_parameters_layout.setObjectName("api_parameters_layout")
        self.verticalLayout_5.addLayout(self.api_parameters_layout)
        self.verticalLayout.addWidget(self.api_params_frame)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.generation_time_label = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Roboto Mono")
        font.setBold(False)
        self.generation_time_label.setFont(font)
        self.generation_time_label.setScaledContents(True)
        self.generation_time_label.setObjectName("generation_time_label")
        self.horizontalLayout_2.addWidget(self.generation_time_label)
        self.generation_state_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.generation_state_label.setMinimumSize(QtCore.QSize(16, 16))
        self.generation_state_label.setMaximumSize(QtCore.QSize(16, 16))
        self.generation_state_label.setText("")
        self.generation_state_label.setScaledContents(True)
        self.generation_state_label.setObjectName("generation_state_label")
        self.horizontalLayout_2.addWidget(self.generation_state_label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.loading_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.loading_label.setText("")
        self.loading_label.setObjectName("loading_label")
        self.horizontalLayout_2.addWidget(self.loading_label)
        self.generate_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.generate_button.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(12)
        font.setBold(False)
        self.generate_button.setFont(font)
        self.generate_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout_2.addWidget(self.generate_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Neuro Wallpaper"))
        self.interval_label.setText(_translate("MainWindow", "Interval"))
        self.min_label.setText(_translate("MainWindow", "min"))
        self.auto_change_checkbox.setText(_translate("MainWindow", "Enable auto-change picture"))
        self.hide_to_tray_checkbox.setText(_translate("MainWindow", "Always hide to tray"))
        self.run_at_startup_checkbox.setText(_translate("MainWindow", "Run at system startup"))
        self.api_groupbox.setTitle(_translate("MainWindow", "Select API"))
        self.kandinsky_radiobtn.setText(_translate("MainWindow", "Kandinsky"))
        self.label.setText(_translate("MainWindow", "Last generation:"))
        self.generation_time_label.setText(_translate("MainWindow", "None"))
        self.generate_button.setText(_translate("MainWindow", "Generate now"))
