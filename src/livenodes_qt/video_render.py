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
#TODO Change this import if livenodes_core_nodes is the correct location for this node
# from livenodes_core_nodes.ports import Ports_empty, Port_Data, Port_Vector_of_Strings


#TODO Integrate Ports later on
# class Ports_out(NamedTuple):
#     data: Port_Data = Port_Data("Data")
#     annot: Port_Vector_of_Strings = Port_Vector_of_Strings("Annotation")


class RenderVideo(View_QT):
    channels_in =  ["Data"] # Ports_empty()
    channels_out = ["Annotation"] # Ports_out()

    category = "Annotation"
    description = ""

    #TODO Change paths when the actual repo etc. is known
    example_init = {
        "name": "Video Playback",
    }

    def __init__(self,
                name="Video Playback",
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
    
    
    #TODO Scale according to windowsize? For now the video is centered
    def convert_cv_to_qt(self, cv_img):  # img_height, img_width
        """
        Convert from an opencv image to QPixmap.
        Code source: https://github.com/docPhil99/opencvQtdemo/blob/master/staticLabel2.py
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        # p = convert_to_Qt_format.scaled(img_width, img_height, Qt.KeepAspectRatio)
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