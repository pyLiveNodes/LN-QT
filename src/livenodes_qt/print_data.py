from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QFormLayout, QLabel


class Print_data(View_QT):
    channels_in = ['Data']
    channels_out = []

    category = "Debug"
    description = ""

    example_init = {
        "name": "Display Channel Data",
    }


    def process(self, data, **kwargs):
        self._emit_draw(data=data)

    def _init_draw(self, parent):

        label = QLabel("")

        layout = QFormLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addRow(label)

        def update(data=None):
            nonlocal label
            label.setText(str(data))
        return update
