import time
from typing import NamedTuple

import cv2
import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QColor
# from PyQt5 import Qt
from PyQt5 import QtCore

from livenodes.sender import Sender
from livenodes.viewer import View_QT

from livenodes_core_nodes.ports import Ports_data_channels, Ports_empty


class Video_Render(View_QT):
    ports_in =  Ports_data_channels()
    ports_out = Ports_empty()

    category = "Annotation"
    description = ""

    example_init = {
        "name": "Video Render",
    }

    def __init__(self,
                name="Video Render",
                 **kwargs):
        super().__init__(name=name, **kwargs)
        self.name = name


    def _settings(self):
        """
        Get the Nodes setup settings.
        Primarily used for serialization from json files.
        """
        return { \
            "name": self.name
        }
    
    

    def convert_cv_to_qt(self, cv_img):
        """
        Convert from an opencv image to QPixmap.
        Code source: https://github.com/docPhil99/opencvQtdemo/blob/master/staticLabel2.py
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)

    def process(self, data, **kwargs):
        self._emit_draw(data=data)

    def _init_draw(self, parent):
        """
        Visualize video framewise.
        """
        self.frame_label = QLabel()
        
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame_label)
        self.frame_label.setAlignment(QtCore.Qt.AlignCenter)

        def update(data=[]):
            playback_colormap = self.convert_cv_to_qt(data[0])
            self.frame_label.setPixmap(playback_colormap)

        return update