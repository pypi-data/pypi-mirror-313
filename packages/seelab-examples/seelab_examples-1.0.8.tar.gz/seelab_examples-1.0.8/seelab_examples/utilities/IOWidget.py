import platform
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

from ..layouts.gauge import Gauge
from ..layouts import ui_miniInputSelector
from functools import partial

class MINIINPUT(QtWidgets.QDialog, ui_miniInputSelector.Ui_Form):
    SLIDER_SCALING = 1000.

    def __init__(self, parent, device, name, **kwargs):
        super(MINIINPUT, self).__init__(parent)
        self.setupUi(self)
        self.p = device
        if name in ['A1','A2']:
            self.p.select_range(name,8)
        widgets={ # [Input, min, max, read_function]
            'RES':[True,0,100e3,self.p.get_resistance],
            'A1':[True,-5,5,partial(self.p.get_average_voltage,'A1')],
            'A2':[True,-5,5,partial(self.p.get_average_voltage,'A2')],
            'A3':[True,-3,3,partial(self.p.get_average_voltage,'A3')],
            'PV1':[False,-5,5,self.p.set_pv1],
            'PV2':[False,-3,3,self.p.set_pv2],
        }

        self.gauge_widget = Gauge(self, name)
        self.gauge_widget.title_fontsize = 28
        self.gauge_widget.setMinimumWidth(200)
        self.readFunction = None
        self.writeFunction = None
        self.last_value = 0
        if name in widgets:
            prop = widgets[name]
            self.gauge_widget.setObjectName(name)
            self.gauge_widget.set_MinValue(widgets[name][1])
            self.max_value = widgets[name][2]
            self.gauge_widget.set_MaxValue(widgets[name][2])
            if prop[0]:
                self.readFunction = prop[3]
            else:
                self.writeFunction = prop[3]
                self.gauge_widget.value_needle_snapzone = 1
                self.gauge_widget.valueChanged.connect(self.update_write_value)

        self.gaugeLayout.addWidget(self.gauge_widget)

    def update_write_value(self, value):
        if self.writeFunction:
            self.gauge_widget.value = value
            self.gauge_widget.update()
            self.last_value = value

    def update_vals(self):
        if self.readFunction:
            value = self.readFunction()
            self.last_value = value
            self.gauge_widget.update_value(value)
        elif self.writeFunction:
            self.writeFunction(self.last_value)
            self.gauge_widget.realvalue = self.last_value

    def reconnect(self, device):
        self.p = device


