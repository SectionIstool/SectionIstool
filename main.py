import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import * # type: ignore

from app.common.config import cfg
from app.view.SectionIstool import Window

if cfg.get(cfg.dpiScale) == "Auto": # type: ignore
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) # type: ignore
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale)) # type: ignore

app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()