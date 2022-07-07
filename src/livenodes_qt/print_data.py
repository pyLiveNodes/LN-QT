from livenodes.viewer import View_QT
from PyQt5.QtWidgets import QFormLayout, QLabel

from livenodes.port import Port
from livenodes_core_nodes.ports import Ports_empty, Port_Data, Port_Vector_of_Strings
from typing import NamedTuple

class Port_stringable(Port):

    example_values = [
        ["EMG1", "EMG2"],
        [0, 1],
        [20, .1],
        20,
        "Bla"
    ]

    def __init__(self, name='stringable', optional=False):
        super().__init__(name, optional)

    @staticmethod
    def check_value(value):
        try: 
            str(value)
            return True, None
        except Exception as err:
            return False, err

class Ports_any(NamedTuple):
    any: Port_stringable = Port_stringable("Any")

class Print_data(View_QT):
    ports_in = Ports_any()
    ports_out = Ports_empty()

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
