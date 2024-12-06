import sys
from PyQt5 import QtGui, QtCore, QtWidgets

import time, os, os.path, math
import numpy as np
from . import ui_dio_sensor, ui_dio_control, ui_dio_robot, ui_sensor_row, ui_micro_voltmeter, ui_thermometer

from .gauge import Gauge
from eyes17.SENSORS import ADS1115, BMP280, BMP180
from .advancedLoggerTools import LOGGER

import functools
from functools import partial
import pyqtgraph as pg

import numpy as np
import utils, shelve
from collections import OrderedDict

colors = ['#00ffff', '#008080', '#ff0000', '#800000', '#ff00ff', '#800080', '#00FF00', '#008000', '#ffff00',
          '#808000', '#0000ff', '#000080', '#a0a0a4', '#808080', '#ffffff', '#4000a0']


########### I2C : SENSOR AND CONTROL LAYOUTS ##################


class DIOSENSOR(QtWidgets.QDialog, ui_dio_sensor.Ui_Dialog):
    def __init__(self, parent, sensor, addr, mux_channel=None):
        super(DIOSENSOR, self).__init__(parent)
        name = sensor['name']
        self.initialize = sensor['init']
        self.address = addr
        self.mux_channel = mux_channel
        self.read = sensor['read']
        self.isPaused = False
        self.setupUi(self)
        colors = ['#00ffff', '#008080', '#ff0000', '#800000', '#ff00ff', '#800080', '#00FF00', '#008000', '#ffff00',
                  '#808000', '#0000ff', '#000080', '#a0a0a4', '#808080', '#ffffff', '#4000a0']
        self.currentPage = 0
        self.max = sensor.get('max', None)
        self.min = sensor.get('min', None)
        self.fields = sensor.get('fields', None)
        self.widgets = []
        self.buttonframe = None

        def initbuttonframe():
            if self.buttonframe is None:
                self.buttonframe = QtWidgets.QFrame()
                self.configLayout.addWidget(self.buttonframe)
                self.widgets.append(self.buttonframe)

        for a in sensor.get('config', []):  # Load configuration menus
            widgettype = a.get('widget', 'dropdown')
            if widgettype == 'button':
                l = QtWidgets.QPushButton(a.get('name', 'Button'))
                l.clicked.connect(a.get('function', None))
            elif widgettype == 'spinbox':
                l = QtWidgets.QLabel(a.get('name', ''))
                self.buttonLayout.addWidget(l);
                self.widgets.append(l)
                l = QtWidgets.QSpinBox()
                l.setMinimum(a.get('min', 0))
                l.setMaximum(a.get('max', 100))
                val = a.get('value', 0)
                if 'readbackfunction' in a:
                    val = a.get('readbackfunction')(address=addr)
                l.setValue(val)
                l.valueChanged.connect(a.get('function', None))
            elif widgettype == 'doublespinbox':
                l = QtWidgets.QLabel(a.get('name', ''))
                self.buttonLayout.addWidget(l);
                self.widgets.append(l)
                l = QtWidgets.QDoubleSpinBox()
                l.setMinimum(a.get('min', 0))
                l.setMaximum(a.get('max', 100))
                if 'readbackfunction' in a:
                    val = a.get('readbackfunction')()
                l.setValue(val)
                l.valueChanged.connect(a.get('function', None))
            elif widgettype == 'dropdown':
                l = QtWidgets.QLabel(a.get('name', ''))
                self.buttonLayout.addWidget(l);
                self.widgets.append(l)
                l = QtWidgets.QComboBox()
                l.addItems(a.get('options', []))
                l.currentIndexChanged['int'].connect(a.get('function', None))

            self.buttonLayout.addWidget(l)
            self.widgets.append(l)

        self.graph.setRange(xRange=[-5, 0])
        import pyqtgraph as pg
        self.region = pg.LinearRegionItem()
        self.region.setBrush([255, 0, 50, 50])
        self.region.setZValue(10)
        for a in self.region.lines: a.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor));
        self.graph.addItem(self.region, ignoreBounds=False)
        self.region.setRegion([-3, -.5])

        self.curves = {};
        self.curveData = {};
        self.fitCurves = {}
        self.cbs = {}
        self.gauges = {}
        self.datapoints = 0
        self.T = 0
        self.time = np.empty(300)
        self.start_time = time.time()
        row = 1;
        col = 1;
        MAXCOL = 4;
        if len(self.fields) >= 6: MAXCOL = 5
        for a, b, c in zip(self.fields, self.min, self.max):
            gauge = Gauge(self, a)
            gauge.setObjectName(a)
            gauge.set_MinValue(b)
            gauge.set_MaxValue(c)
            # listItem = QtWidgets.QListWidgetItem()
            # self.listWidget.addItem(listItem)
            # self.listWidget.setItemWidget(listItem, gauge)
            self.gaugeLayout.addWidget(gauge, row, col)
            col += 1
            if col == MAXCOL:
                row += 1
                col = 1
            self.gauges[a] = [gauge, a, b, c]  # Name ,min, max value

            curve = self.graph.plot(pen=colors[len(self.curves.keys())], connect="finite")
            fitcurve = self.graph.plot(pen=colors[len(self.curves.keys())], width=2, connect="finite")
            cbs = QtWidgets.QCheckBox(a)
            cbs.setStyleSheet('background-color:%s;' % (colors[len(self.curves.keys())]))
            self.parameterLayout.addWidget(cbs)
            cbs.setChecked(True)
            cbs.clicked.connect(self.toggled)

            self.curves[a] = curve
            self.curveData[a] = np.empty(300)
            self.fitCurves[a] = fitcurve
            self.cbs[a] = cbs

        self.setWindowTitle('Sensor : %s' % name)

    def toggled(self):
        for inp in self.fields:
            if self.cbs[inp].isChecked():
                self.curves[inp].setVisible(True)
                self.gauges[inp][0].set_NeedleColor()
                self.gauges[inp][0].set_enable_filled_Polygon()
            else:
                self.curves[inp].setVisible(False)
                self.gauges[inp][0].set_NeedleColor(255, 0, 0, 30)
                self.gauges[inp][0].set_enable_filled_Polygon(False)

    def setDuration(self):
        self.graph.setRange(xRange=[-1 * int(self.durationBox.value()), 0])

    def next(self):
        if self.currentPage == 1:
            self.currentPage = 0
            self.switcher.setText("Data Logger")
        else:
            self.currentPage = 1
            self.switcher.setText("Analog Gauge")

        self.monitors.setCurrentIndex(self.currentPage)

    def restartLogging(self):
        self.pauseLogging(False);
        self.pauseButton.setChecked(False)
        self.setDuration()
        for pos in self.fields:
            self.curves[pos].setData([], [])
            self.datapoints = 0
            self.T = 0
            self.curveData[pos] = np.empty(300)
            self.time = np.empty(300)
            self.start_time = time.time()

    def readValues(self):
        return self.read()

    def setValue(self, vals):
        if vals is None:
            print('check connections')
            return
        if self.currentPage == 0:  # Update Analog Gauges
            p = 0
            for a in self.fields:
                if (self.cbs[a].isChecked()):
                    self.gauges[a][0].update_value(vals[p])
                p += 1
        elif self.currentPage == 1:  # Update Data Logger
            if self.isPaused: return
            p = 0
            self.T = time.time() - self.start_time
            self.time[self.datapoints] = self.T
            if self.datapoints >= self.time.shape[0] - 1:
                tmp = self.time
                self.time = np.empty(self.time.shape[0] * 2)  # double the size
                self.time[:tmp.shape[0]] = tmp

            for a in self.fields:
                self.curveData[a][self.datapoints] = vals[p]
                if not p: self.datapoints += 1  # Increment datapoints once per set. it's shared

                if self.datapoints >= self.curveData[a].shape[0] - 1:
                    tmp = self.curveData[a]
                    self.curveData[a] = np.empty(self.curveData[a].shape[0] * 2)  # double the size
                    self.curveData[a][:tmp.shape[0]] = tmp
                self.curves[a].setData(self.time[:self.datapoints], self.curveData[a][:self.datapoints])
                self.curves[a].setPos(-self.T, 0)
                p += 1

    def sineFit(self):
        self.pauseButton.setChecked(True);
        self.isPaused = True;
        S, E = self.region.getRegion()
        start = (np.abs(self.time[:self.datapoints] - self.T - S)).argmin()
        end = (np.abs(self.time[:self.datapoints] - self.T - E)).argmin()
        print(self.T, start, end, S, E, self.time[start], self.time[end])
        res = 'Amp, Freq, Phase, Offset<br>'
        for a in self.curves:
            if self.cbs[a].isChecked():
                try:
                    fa = utils.fit_sine(self.time[start:end], self.curveData[a][start:end])
                    if fa is not None:
                        amp = abs(fa[0])
                        freq = fa[1]
                        phase = fa[2]
                        offset = fa[3]
                        s = '%5.2f , %5.3f Hz, %.2f, %.1f<br>' % (amp, freq, phase, offset)
                        res += s
                        x = np.linspace(self.time[start], self.time[end], 1000)
                        self.fitCurves[a].clear()
                        self.fitCurves[a].setData(x - self.T, utils.sine_eval(x, fa))
                        self.fitCurves[a].setVisible(True)

                except Exception as e:
                    res += '--<br>'
                    print(e.message)

        self.msgBox = QtWidgets.QMessageBox(self)
        self.msgBox.setWindowModality(QtCore.Qt.NonModal)
        self.msgBox.setWindowTitle('Sine Fit Results')
        self.msgBox.setText(res)
        self.msgBox.show()

    def dampedSineFit(self):
        self.pauseButton.setChecked(True);
        self.isPaused = True;
        S, E = self.region.getRegion()
        start = (np.abs(self.time[:self.datapoints] - self.T - S)).argmin()
        end = (np.abs(self.time[:self.datapoints] - self.T - E)).argmin()
        print(self.T, start, end, S, E, self.time[start], self.time[end])
        res = 'Amplitude, Freq, phase, Damping<br>'
        for a in self.curves:
            if self.cbs[a].isChecked():
                try:
                    fa = utils.fit_dsine(self.time[start:end], self.curveData[a][start:end])
                    if fa is not None:
                        amp = abs(fa[0])
                        freq = fa[1]
                        decay = fa[4]
                        phase = fa[2]
                        s = '%5.2f , %5.3f Hz, %.3f, %.3e<br>' % (amp, freq, phase, decay)
                        res += s
                        x = np.linspace(self.time[start], self.time[end], 1000)
                        self.fitCurves[a].clear()
                        self.fitCurves[a].setData(x - self.T, utils.dsine_eval(x, fa))
                        self.fitCurves[a].setVisible(True)
                except Exception as e:
                    res += '--<br>'
                    print(e.message)

        self.msgBox = QtWidgets.QMessageBox(self)
        self.msgBox.setWindowModality(QtCore.Qt.NonModal)
        self.msgBox.setWindowTitle('Damped Sine Fit Results')
        self.msgBox.setText(res)
        self.msgBox.show()

    def pauseLogging(self, v):
        self.isPaused = v
        for inp in self.fields:
            self.fitCurves[inp].setVisible(False)

    def saveRegion(self):
        self.__saveTraces__(True)

    def saveTraces(self):
        self.__saveTraces__(False)

    def __saveTraces__(self, considerRegion):
        print('saving region' if considerRegion else 'saving all data')
        self.pauseButton.setChecked(True);
        self.isPaused = True;
        fn = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", QtCore.QDir.currentPath(),
                                                   "Text files (*.txt);;CSV files (*.csv);;All files (*.*)",
                                                   "CSV files (*.csv)")
        if (len(fn) == 2):  # Tuple
            fn = fn[0]
        print(fn)

        if fn != '':
            f = open(fn, 'wt')
            f.write('time')
            for inp in self.fields:
                if self.cbs[inp].isChecked():
                    f.write(',%s' % (inp))
            f.write('\n')

            if considerRegion:
                S, E = self.region.getRegion()
                start = (np.abs(self.time[:self.datapoints] - self.T - S)).argmin()
                end = (np.abs(self.time[:self.datapoints] - self.T - E)).argmin()
                print(self.T, start, end, S, E, self.time[start], self.time[end])
                for a in range(start, end):
                    f.write('%.3f' % (self.time[a] - self.time[start]))
                    for inp in self.fields:
                        if self.cbs[inp].isChecked():
                            f.write(',%.3f' % (self.curveData[inp][a]))
                    f.write('\n')

            else:
                for a in range(self.datapoints):
                    f.write('%.3f' % (self.time[a] - self.time[0]))
                    for inp in self.fields:
                        if self.cbs[inp].isChecked():
                            f.write(',%.3f' % (self.curveData[inp][a]))
                    f.write('\n')
            f.close()

    def launch(self):
        if self.initialize is not None:
            self.initialize(address=self.address)
        self.restartLogging()
        self.show()


class DIOCONTROL(QtWidgets.QDialog, ui_dio_control.Ui_Dialog):
    def __init__(self, parent, sensor, addr):
        super(DIOCONTROL, self).__init__(parent)
        name = sensor['name']
        self.initialize = sensor['init']
        self.address = addr
        self.setupUi(self)
        self.isPaused = False
        self.currentPage = 0  # Only one page exists.
        self.val = 0

        self.widgets = []
        self.gauges = {}
        self.functions = {}

        for a in sensor.get('write', []):  # Load configuration menus
            l = QtWidgets.QSlider(self);
            l.setMinimum(a[1]);
            l.setMaximum(a[2]);
            l.setValue(a[3]);
            l.setOrientation(QtCore.Qt.Orientation(0x1))  # Qt.Horizontal
            l.valueChanged['int'].connect(functools.partial(self.write, l))
            self.configLayout.addWidget(l);
            self.widgets.append(l)

            gauge = Gauge(self)
            gauge.setObjectName(a[0])
            gauge.set_MinValue(a[1])
            gauge.set_MaxValue(a[2])
            gauge.update_value(a[3])
            self.gaugeLayout.addWidget(gauge)
            self.gauges[l] = gauge  # Name ,min, max value,default value, func
            self.functions[l] = a[4]

        self.setWindowTitle('Control : %s' % name)

    def readValues(self):
        return None

    def write(self, w, val):
        self.val = val
        self.gauges[w].update_value(val)
        self.functions[w](val)

    def launch(self):
        self.initialize(address=self.address)
        self.show()


class DIOROBOT(QtWidgets.QDialog, ui_dio_robot.Ui_Dialog):
    def __init__(self, parent, sensor, addr):
        super(DIOROBOT, self).__init__(parent)
        name = sensor['name']
        self.initialize = sensor['init']
        self.address = addr
        self.setupUi(self)
        self.widgets = []
        self.gauges = OrderedDict()
        self.lastPos = OrderedDict()
        self.functions = OrderedDict()
        self.positions = []

        for a in sensor.get('write', []):  # Load configuration menus
            l = QtWidgets.QSlider(self);
            l.setMinimum(a[1]);
            l.setMaximum(a[2]);
            l.setValue(a[3]);
            l.setOrientation(QtCore.Qt.Orientation(0x1))  # Qt.Horizontal
            l.valueChanged['int'].connect(functools.partial(self.write, l))
            self.configLayout.addWidget(l);
            self.widgets.append(l)

            gauge = Gauge(self)
            gauge.setObjectName(a[0])
            gauge.set_MinValue(a[1])
            gauge.set_MaxValue(a[2])
            gauge.update_value(a[3])
            self.lastPos[l] = a[3]
            self.gaugeLayout.addWidget(gauge)
            self.gauges[l] = gauge  # Name ,min, max value,default value, func
            self.functions[l] = a[4]

        self.setWindowTitle('Control : %s' % name)

    def write(self, w, val):
        self.gauges[w].update_value(val)
        self.lastPos[w] = val
        self.functions[w](val)

    def add(self):
        self.positions.append([a.value() for a in self.lastPos.keys()])
        item = QtWidgets.QListWidgetItem("%s" % str(self.positions[-1]))
        self.listWidget.addItem(item)
        print(self.positions)

    def play(self):
        mypos = [a.value() for a in self.lastPos.keys()]  # Current position
        sliders = list(self.gauges.keys())
        for nextpos in self.positions:
            dx = [(x - y) for x, y in zip(nextpos, mypos)]  # difference between next position and current
            distance = max(dx)
            for travel in range(20):
                for step in range(4):
                    self.write(sliders[step], int(mypos[step]))
                    mypos[step] += dx[step] / 20.
                time.sleep(0.01)

    def launch(self):
        self.initialize(address=self.address)
        self.show()


class SENSORROW(QtWidgets.QWidget, ui_sensor_row.Ui_Form):
    def __init__(self, parent, **kwargs):
        super(SENSORROW, self).__init__(parent)
        self.setupUi(self)
        self.title.setText(kwargs.get('name'))
        self.description.setText(kwargs.get('description'))
        self.address = kwargs.get('address')
        self.addressNumber.display(self.address)
        self.scene = QtWidgets.QGraphicsScene()
        self.image.setScene(self.scene)
        self.image_qt = QtGui.QImage(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blockly', 'media', kwargs.get('name') + '.jpeg'))
        print(os.path.join('blockly', 'media', kwargs.get('name') + '.jpeg'))
        pic = QtWidgets.QGraphicsPixmapItem()
        pic.setPixmap(QtGui.QPixmap.fromImage(self.image_qt))
        # self.scene.setSceneRect(0, 0, 100, 100)
        self.scene.addItem(pic)


##### microvoltmeter


class MICRO_VOLTMETER(QtWidgets.QDialog, ui_micro_voltmeter.Ui_Dialog):
    p = None
    logger = None

    def __init__(self, parent, device, button):
        super(MICRO_VOLTMETER, self).__init__(parent)
        self.setupUi(self)
        self.parentButton = button
        self.emfgauge = Gauge(self, 'EMF(uV)')
        self.emfgauge.setObjectName('EMF')
        self.emfgauge.set_MinValue(0)
        self.emfgauge.set_MaxValue(6000)
        self.gaugeLayout.addWidget(self.emfgauge, 1, 1)

        self.ADSOPTION = 0
        self.A3OPTION = 1
        self.voltmeterOption = self.ADSOPTION
        self.A3offset = 0
        self.A3gain = 1000
        #Load previous config values
        try:
            s = shelve.open('eyes_shelf.db', flag='r')
            try:
                self.A3gain = s['A3gain']
                self.A3offset = s['A3offset']
            finally:
                s.close()
        except:
            pass
        self.gainLabel.setText('%.2f x' % self.A3gain)
        self.offsetLabel.setText("%d uV" % (self.A3offset * 1e6))

        self.set_device(device)

        self.resAverage = 10

        self.setVoltmeter(self.voltmeterOption)

    def setVoltmeter(self, t):
        print('setVoltmeter tab changed:', t)
        if t == 0:
            self.locateADS1115()
            if self.ADC is None:
                self.msg('ADS1115 Not Found')
                self.errdg = ErrorDialog('Missing ADS1115',
                                         'Could not find ADS1115 connected on I2C port\nCheck the connections')
                self.errdg.launch(2500)
                self.voltmeterOption = self.A3OPTION
                self.voltmeterTab.setCurrentIndex(self.voltmeterOption)
                self.setVoltmeter(self.voltmeterOption)  #Go set A3
                return
            self.voltmeterOption = self.ADSOPTION
            self.emfgauge.title_text = 'ADS1115\nEmf(mV)'
            self.parentButton.setText(
                'VOLTMETER: ADS1115 %s,%s' % (self.adsBox.currentText(), self.gainBox.currentText()))
        elif t == 1:
            self.msg('Measuring with A3')
            self.emfgauge.set_enable_filled_Polygon(True)
            self.voltmeterOption = self.A3OPTION
            self.emfgauge.title_text = 'A3\nEmf(mV)'
            self.parentButton.setText('VOLTMETER: A3 @ %.1fx' % self.A3gain)

    def set_device(self, p):
        self.p = p
        self.logger = LOGGER(self.p.I2C)
        self.setVoltmeter(self.voltmeterOption)

    def A3Zero(self):
        self.A3offset = self.p.get_average_voltage('A3', samples=20)  #in Volts
        self.offsetLabel.setText("%d uV" % (self.A3offset * 1e6))
        s = shelve.open('eyes_shelf.db', 'c')
        try:
            s['A3offset'] = self.A3offset
        finally:
            s.close()

    def setA3Gain(self):
        r = self.p.get_resistance()
        if r == np.Inf:
            self.A3gain = 1
        elif r < 50:
            self.A3gain = np.Inf
        else:
            r = np.average([self.p.get_resistance() for a in range(self.resAverage)])
            self.A3gain = 1 + (10000 / r)
        self.gainLabel.setText('%.2f x' % self.A3gain)
        s = shelve.open('eyes_shelf.db', 'c')
        try:
            s['A3gain'] = self.A3gain
        finally:
            s.close()

    def locateADS1115(self):
        ## Search for ADS1115
        self.ADC = None
        x = self.logger.I2CScan()
        self.msg('ADS1115 not found')
        self.msgwin.setStyleSheet('color:darkred;')
        for a in x:
            possiblesensors = self.logger.sensormap.get(a, None)
            if 'ADS1115' in possiblesensors:
                self.msg('ADS1115 located at: %s' % a)
                self.msgwin.setStyleSheet('color:black;')
                self.ADC = ADS1115.connect(self.p.I2C)  # Measure the ADC
                self.ADC.setGain(
                    'GAIN_SIXTEEN')  # options : 'GAIN_TWOTHIRDS','GAIN_ONE','GAIN_TWO','GAIN_FOUR','GAIN_EIGHT','GAIN_SIXTEEN'
                self.ADC.setGain(['GAIN_TWOTHIRDS', 'GAIN_ONE', 'GAIN_TWO', 'GAIN_FOUR', 'GAIN_EIGHT', 'GAIN_SIXTEEN'][
                                     self.gainBox.currentIndex()])
                self.ADC.setDataRate([8, 16, 32, 64, 128, 250, 475, 860][self.rateBox.currentIndex()])

    def rateChanged(self, r):
        self.ADC.setDataRate([8, 16, 32, 64, 128, 250, 475, 860][r])
        self.ADC.readADC_SingleEnded(self.adsBox.currentIndex())

    def gainChanged(self, g):
        self.ADC.setGain(['GAIN_TWOTHIRDS', 'GAIN_ONE', 'GAIN_TWO', 'GAIN_FOUR', 'GAIN_EIGHT', 'GAIN_SIXTEEN'][g])
        self.ADC.readADC_SingleEnded(self.adsBox.currentIndex())

    def msg(self, m):
        self.msgwin.setText(self.tr(m))

    def fetch(self):
        if not self.p.connected:
            return 0
        errmsg = ''
        if self.voltmeterOption == self.A3OPTION:
            if self.isVisible():
                # Resistance Monitor
                r = self.p.get_resistance()
                if r == np.Inf:
                    self.resLabel.setText('Resistance(SEN-GND): Open')
                elif r < 50:
                    self.resLabel.setText('Resistance(SEN-GND): < 50 Ohms')
                else:
                    self.resLabel.setText('Resistance(SEN-GND): %.2f' % (
                        np.average([self.p.get_resistance() for a in range(self.resAverage)])))
            v = self.p.get_average_voltage('A3', samples=50)
            emf = 1e6 * (v - self.A3offset) / self.A3gain
            #print(v,emf,self.A3offset,self.A3gain)

        elif self.voltmeterOption == self.ADSOPTION:  #ADS1115 Voltmeter
            if self.ADC is None:
                self.locateADS1115()
                errmsg += self.tr(', ADS1115 not found. chan:' + str(self.adsBox.currentIndex()))
                emf = 0
                ok = False
            else:
                if self.adsBox.currentIndex() < 4:
                    emf = self.ADC.readADC_SingleEnded(self.adsBox.currentIndex())  # ADC reading in Channel Ax
                elif self.adsBox.currentIndex() == 4:
                    emf = self.ADC.readADC_Differential('01')  # ADC reading differential b/w 0 and 1
                else:
                    emf = self.ADC.readADC_Differential('23')  # ADC between 2 and 3

        if self.isVisible():
            if emf <= 0:
                self.emfgauge.set_enable_filled_Polygon(False)
            else:
                self.emfgauge.set_enable_filled_Polygon()
            self.emfgauge.update_value(emf)
        return emf

    def launch(self):
        #self.initialize(address=self.address)
        self.show()


class THERMOMETER(QtWidgets.QWidget, ui_thermometer.Ui_Form):
    p = None
    logger = None

    def __init__(self, parent, device, button):
        super(THERMOMETER, self).__init__(parent)
        self.setupUi(self)
        self.parentButton = button
        self.resAverage = 10
        self.PT1000_OPTION = 0
        self.PT100_OPTION = 1
        self.MAX6675_OPTION = 2
        self.BMP180_OPTION = 3
        self.BMP280_OPTION = 4
        self.LM35_OPTION = 5
        self.THERMOMETER_MISSING_OPTION = 6
        self.thermometer = self.PT1000_OPTION
        self.calibration_points = OrderedDict()
        self.poly = np.poly1d([1, 0])

        try:
            s = shelve.open('eyes_shelf.db', 'r')
            try:
                self.thermometer = s['thermometer']
            finally:
                s.close()
            self.temperatureSensorBox.setCurrentIndex(self.thermometer)
        except:
            self.guessThermometer()
        self.set_device(device)

    def set_device(self, p):
        self.p = p
        self.logger = LOGGER(self.p.I2C)
        self.setThermometer(self.thermometer)

    def guessThermometer(self):
        self.p.SPI.start('CS1')
        maxval = self.p.SPI.send16(0xFFFF)
        self.p.SPI.stop('CS1')
        maxtemp = (maxval >> 3) * 0.25

        if not maxval & 0x4 and 2 < maxtemp < 150:
            self.thermometer = self.MAX6675_OPTION
        elif 2 < self.temperaturePT1000() < 150:
            self.thermometer = self.PT1000_OPTION
        elif 2 < self.temperaturePT100() < 150:
            self.thermometer = self.PT100_OPTION
        else:
            # Search for I2C sensors
            opts = self.p.I2C.scan()
            if 118 in opts:  #BME280/BMP280
                self.thermometer = self.BMP280_OPTION
                self.BMP = BMP280.connect(self.p.I2C)
            elif 119 in opts:  #BMP180
                self.thermometer = self.BMP180_OPTION
                self.BMP = BMP180.connect(self.p.I2C)
            else:
                self.thermometer = self.THERMOMETER_MISSING_OPTION
        self.temperatureSensorBox.setCurrentIndex(self.thermometer)
        s = shelve.open('eyes_shelf.db', 'c')
        try:
            s['thermometer'] = self.thermometer
        finally:
            s.close()

    def setThermometer(self, m):
        print('thermoemeter set', m)
        #s = BMP280.connect(p.I2C)
        #s.readTemperature()
        self.thermometer = m

        if m == self.BMP280_OPTION or m == self.BMP180_OPTION:  # Scan and verify
            opts = self.p.I2C.scan()
            if m == self.BMP280_OPTION:
                self.BMP = BMP280.connect(self.p.I2C)
                if 118 not in opts:  # BME280/BMP280
                    self.errdg = ErrorDialog('Missing Sensor?',
                                             'Scan Only Found :%s\nCheck the connections' % opts)
                    self.errdg.launch(2000)

            elif m == self.BMP180_OPTION:
                self.BMP = BMP180.connect(self.p.I2C)
                if 119 not in opts:  # BME280/BMP280
                    self.errdg = ErrorDialog('Missing Sensor?',
                                             'Scan Only Found :%s\nCheck the connections' % opts)
                    self.errdg.launch(2000)

    def temperature(self,calibrate = True):
        self.titleLabel.setText('Temperature Sensor')
        t = 0
        if self.thermometer == self.PT1000_OPTION:
            t =  self.temperaturePT1000()
        elif self.thermometer == self.PT100_OPTION:
            t =  self.temperaturePT100()
        elif self.thermometer == self.MAX6675_OPTION:
            self.p.SPI.start('CS1')
            val = self.p.SPI.send16(0xFFFF)
            self.p.SPI.stop('CS1')
            t = (val >> 3) * 0.25
            if (val & 0x4):
                self.titleLabel.setText(self.tr('thermocouple not attached. : ') + str(val))
                t =  0
        elif (
                self.thermometer == self.BMP180_OPTION or self.thermometer == self.BMP280_OPTION) and self.BMP is not None:
            t =  self.BMP.readTemperature()
        else:
            t =  0
        if calibrate:
            return self.poly(t)
        else:
            return t

    def temperaturePT1000(self):
        r = np.average([self.p.get_resistance() for a in range(self.resAverage)])  # Measure the resistance in ohm
        if r == np.inf:
            return False
        return -1*(np.sqrt(-0.00232*r+17.59246) - 3.908) / 0.00116

        '''
        #Written by Ujjwal Nikam, NSHE
        """Function to measure the instanteneous temperature"""
        R0 = 1000  # PT1000 (RTD Name)
        Alpha = 3.85 / 1000  # Temperature coefficient
        t0 = time.time()  # Time initialization
        n = 1  # NO of measurements for averaging
        Rsum = 0
        for x in range(0, n):  # Loop for averaging
            r = np.average([self.p.get_resistance() for a in range(self.resAverage)])  # Measure the resistance in ohm
            if r == np.inf:
                return False
            Rsum = Rsum + r  # Sum of resistance
        R = Rsum / n  # Average resistance
        T = (1 / Alpha) * ((R / R0) - 1)  # Calculate Temperature from Resistance
        return T
        '''

    def temperaturePT100(self):
        r = np.average([self.p.get_resistance() for a in range(self.resAverage)])
        r0 = 100.0  # PT100 parameters r0, A and B
        A = 3.9083e-3
        B = -5.7750e-7
        c = 1 - r / r0
        try:
            b4ac = math.sqrt(A * A - 4 * B * c)
            temp = (-A + b4ac) / (2.0 * B)
            return temp
        except:
            return 0

    def fetch(self):
        temp = self.temperature()
        if temp == False or temp > 500:
            self.tempLabel.setText('Err')
            ok = False
        else:
            self.tempLabel.setText('%.2f C' % temp)
        return temp

    def addCalibrationPoint(self):
        try:
            t = float(self.manualTemperature.value())
        except:
            self.manualTemperature.setValue(25)
            t = 25
        self.__addCalibrationPoint__(t)

    def addCalibration0(self):
        reply = QtWidgets.QMessageBox.question(self, 'Calibration Warning',
                                               'Is the sensor in an ice bath (0C)?',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return
        self.__addCalibrationPoint__(0)

    def addCalibration100(self):
        reply = QtWidgets.QMessageBox.question(self, 'Calibration Warning',
                                               'Is the sensor in boiling water (100 C)?',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return

        self.__addCalibrationPoint__(100)

    def __addCalibrationPoint__(self, t):
        temp = self.temperature(False)
        var = abs(temp - t)
        if var > 10:
            reply = QtWidgets.QMessageBox.question(self, 'Calibration Warning',
                                                   'Temperature difference exceeds %d.\nApply calibration?' % var,
                                                   QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return
        if temp == False:
            reply = QtWidgets.QMessageBox.information(self, 'Calibration Error',
                                                   'Temperature read error')
            return

        print(temp,t)
        self.calibration_points[t] = temp
        if len(self.calibration_points) == 1: # Single Point
            self.poly = np.poly1d([1, t-temp])
        elif len(self.calibration_points) == 2: # 2 Point
            pts = list(self.calibration_points.items())
            slope = (pts[1][0] - pts[0][0])/(pts[1][1] - pts[0][1]) # Y2 - Y1, X2 - X1
            offset = pts[0][0] - slope * pts[0][1] # y1 - slope* x1
            self.poly = np.poly1d([slope, offset])
        else:
            pts = list(self.calibration_points.items())
            x = np.array(pts)[:, 1]  # X axis
            y = np.array(pts)[:, 0]  # Y Axis
            # Degree of the polynomial. Linear fitting
            degree = 1
            X = np.vander(x, degree + 1)  # Set up the Vandermonde matrix
            # Solve the linear system using least squares method
            coefficients = np.linalg.lstsq(X, y, rcond=None)[0]
            coefficients = coefficients[::-1]  # Change order from ascending  to descending.
            self.poly = np.poly1d(coefficients)
            # Display the polynomial coefficients
            print("Coefficients:", coefficients, self.poly)
        self.displayCalibrationPolynomial()

    def resetCalibration(self):
        self.calibration_points = OrderedDict()
        self.poly = np.poly1d([1, 0]) #m,c
        self.displayCalibrationPolynomial()

    def displayCalibrationPolynomial(self):
        self.calibrationLabel.setText('Y = %.2f*X + %.2f'%(self.poly[1],self.poly[0]))

class ErrorDialog(QtWidgets.QMessageBox):
    def __init__(self, title, message, parent=None):
        super(ErrorDialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.setGeometry(450, 300, 300, 200)

    def launch(self, timeout=2000):
        self.show()
        self.autoclosetimer = QtCore.QTimer()
        self.autoclosetimer.setSingleShot(True)
        self.autoclosetimer.timeout.connect(self.fade_out)
        self.autoclosetimer.start(timeout)

    def fade_out(self):
        self.anim = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(200)  # duration in milliseconds
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.finished.connect(self.close)
        self.anim.start()
