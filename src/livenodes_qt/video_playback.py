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
# TODO Change this import if livenodes_core_nodes is the correct location for this node
from livenodes_core_nodes.ports import Ports_empty, Port_Data, Port_Vector_of_Strings

from livenodes_core_nodes.ports import Port_Dict, Port_Vector_of_Ints, Port_Data, Port_Single_Channel_Number, Port_Vector_of_Strings, Ports_empty

class Ports_out(NamedTuple):
    annot: Port_Vector_of_Strings = Port_Vector_of_Strings("Annotation")
    data: Port_Data = Port_Data('Data')


class Video_Playback(Sender, View_QT):
    ports_in = Ports_empty()
    ports_out = Ports_out()

    category = "Annotation"
    description = ""

    #TODO Change paths when the actual repo etc. is known
    example_init = {
        "name": "Video Playback",
        "path_to_video": "/home/fabian-rechner/Arbeit/CSL/Repos/example-project/sample_projects/bub/data/bub/test_video.mp4",
        "path_to_annotation": "/home/fabian-rechner/Arbeit/CSL/Repos/example-project/sample_projects/bub/data/bub/test_non_empty.csv"
    }

    def __init__(self,
                path_to_video,
                path_to_annotation,
                name="Video Playback",
                framerate=60,
                block=False,
                 **kwargs):
        super().__init__(name=name, block=block, **kwargs)
        self.name = name
        self.path_to_video = path_to_video
        self.path_to_annotation = path_to_annotation
        self.framerate = framerate


    def _settings(self):
        """
        Get the Nodes setup settings.
        Primarily used for serialization from json files.
        """
        return { \
            "name": self.name,
            "path_to_video": self.path_to_video,
            "path_to_annotation": self.path_to_annotation
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


    #TODO Play and pause
    #TODO Sound is not needed, correct?
    def _run(self):
        """
        Play video with framewise annotation.
        """
        annotation_data = pd.read_csv(self.path_to_annotation)
        video_capture = cv2.VideoCapture(self.path_to_video)
        self.framerate = video_capture.get(cv2.CAP_PROP_FPS)  # Set as attribute because it might be useful later on

        for _, frame_annotation in annotation_data.iterrows():
            playback_annotation = frame_annotation.to_numpy()
            frame_available, playback_frame = video_capture.read()
            if not frame_available:
                continue

            self._emit_data(playback_annotation, channel=self.ports_out.annot)
            self._emit_data(playback_frame, channel=self.ports_out.data)
            self._emit_draw(data=[playback_frame])
                
            yield True

            time.sleep(1./self.framerate)  # Wait for next loop execution, otherwise it would be way too fast


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