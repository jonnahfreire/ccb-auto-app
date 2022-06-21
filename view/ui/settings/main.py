from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *

from app.main import get_driver_settings, set_driver_path
from app.config.paths import syslocal_path
from ..alertLoading.main import AlertLoading

from ..styles import *


class SettingsScreen(QDialog):

    def __init__(self, parent, ui_path) -> None:
        super().__init__()
        self.parent = parent
        loadUi(ui_path, self)

        self.back = self.backBtn
        self.back.mousePressEvent = self.handle_back_click

        self.info.setStyleSheet(settings_info_style)

        set_element_shadow(self.info)
        self.selectDriverPathBtn.setMinimumSize(135, 30)
        self.selectDriverPathBtn.setStyleSheet(btn_success + "QPushButton{font-size: 10pt;}")
        self.selectDriverPathBtn.clicked.connect(self.handle_set_driver_path)

        set_element_shadow(self.selectDriverPathBtn)

        self.set_driver_settings()
        self.driverPath.setMinimumSize(500, 30)
        self.driverPath.setMaximumSize(500, 30)
        self.selectDriverPathBtn.move(self.driverPath.width() + 25, self.selectDriverPathBtn.y())

        self.alert_loading = AlertLoading(self, p_w=800, p_h=600,
                                          infinity=False, duration=2000,
                                          container_w=340,
                                          message="Salvando configurações, aguarde..",
                                          on_animation_end=self.set_driver_settings)

    def handle_back_click(self, event):
        self.parent.setCurrentIndex(self.parent.currentIndex() - 1)

    def set_driver_settings(self):
        drive_settings = get_driver_settings()
        driver_path = drive_settings["path"]
        driver_version = drive_settings["version"]

        if len(driver_path) > 50:
            driver_path = driver_path[:50] + "..."

        if not driver_version == "Versão: Não definido":
            self.driverVersion.setText("ChromeDriver - " + driver_version)
        else:
            self.driverVersion.setText(driver_version)
        self.driverPath.setText(driver_path)

    def handle_set_driver_path(self):
        filepath = QFileDialog.getOpenFileName(
            self, 'Selecione o driver', syslocal_path, "Pdf files (*.exe *.bin)")[0]

        if filepath is not None or len(filepath) > 0:
            self.alert_loading.start_animation()
            set_driver_path(filepath)
