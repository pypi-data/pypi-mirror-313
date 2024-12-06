# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
'''
Code for science experiments using expEYES-17 interface
Logs data from thermocouple sensor MAX6675

And EMF from ADS1115

for thermoelectric experiment

'''

import sys, time, math, os.path
import shelve

import utils
from QtVersion import *

import sys, time, functools
from utils import pg
import numpy as np

from .layouts import ui_thermoelectric

from .layouts.gauge import Gauge

import eyes17.eyemath17 as em
from .layouts.advancedLoggerTools import LOGGER
from eyes17.SENSORS import ADS1115
from .layouts.sensor_utilities import MICRO_VOLTMETER, THERMOMETER


class Expt(QtWidgets.QWidget, ui_thermoelectric.Ui_Form):
    TIMER = 10  #Every 10 mS
    running = True
    TMAX = 120
    RESET = 0
    ACTIVE = 1
    PAUSED = 2
    ADC = None

    def __init__(self, device=None):
        super(Expt, self).__init__()
        self.setupUi(self)

        self.p = device  # connection to the device hardware
        self.logger = LOGGER(self.p.I2C)

        self.latestEmf = 0
        self.latestTemp = 0

        self.datapoints = 0
        self.state = self.RESET
        self.recording = False

        self.voltmeter = MICRO_VOLTMETER(self, device, self.confVMeter)
        self.thermometerWidget = THERMOMETER(self, device, self.confVMeter)
        self.thermometerLayout.addWidget(self.thermometerWidget)



        colors = ['#00ffff', '#008080', '#ff0000', '#800000', '#ff00ff', '#800080', '#00FF00', '#008000', '#ffff00',
                  '#808000', '#0000ff', '#000080', '#a0a0a4', '#808080', '#ffffff', '#4000a0']
        labelStyle = {'color': 'rgb(200,250,200)', 'font-size': '12pt'}
        self.graph.setLabel('left', 'Thermo EMF -->', units='V', **labelStyle)
        self.graph.setLabel('bottom', 'Hot Junction Temperature -->', units='C', **labelStyle)

        self.valueTable.setHorizontalHeaderLabels(['Temperature', 'EMF(uV)'])
        '''
		item = QtWidgets.QTableWidgetItem()
		self.valueTable.setItem(0, pos, item)
		item.setText('')
		'''
        self.start_time = time.time()
        row = 1;
        col = 1;

        self.Tgauge = Gauge(self, 'Temp')
        self.Tgauge.setObjectName('T')
        self.Tgauge.set_MinValue(0)
        self.Tgauge.set_MaxValue(100)
        self.gaugeLayout.addWidget(self.Tgauge, 1, 1)

        self.emfgauge = Gauge(self, 'EMF(uV)')
        self.emfgauge.setObjectName('EMF')
        self.emfgauge.set_MinValue(0)
        self.emfgauge.set_MaxValue(6000)
        self.gaugeLayout.addWidget(self.emfgauge, 1, 2)

        self.curve = self.graph.plot(pen=colors[0], connect="finite")
        self.fitcurve = self.graph.plot(pen=colors[1], width=2, connect="finite")

        self.graph.setRange(xRange=[0, 100])
        self.region = pg.LinearRegionItem()
        self.region.setBrush([255, 0, 50, 50])
        self.region.setZValue(10)
        for a in self.region.lines: a.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor));
        self.graph.addItem(self.region, ignoreBounds=False)
        self.region.setRegion([30, 80])

        self.TData = np.empty(500)
        self.EMFData = np.empty(500)

        self.lastT = 200

        self.startTime = time.time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateEverything)
        self.timer.start(self.TIMER)
        self.setTheme("default")

    def setTheme(self, theme):
        self.setStyleSheet("")
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'layouts', 'themes')
        self.setStyleSheet(open(os.path.join(path, theme + ".qss"), "r").read())

    def recover(self):
        self.logger = LOGGER(self.p.I2C)
        print('recover', self.p.connected)
        self.voltmeter.set_device(self.p)

    def configureVoltmeter(self):
        self.voltmeter.launch()


    def updateEverything(self):
        emf = 0
        if not self.p.connected:
            return
        emf = self.voltmeter.fetch()
        errmsg = ''
        if emf <= 0:  #Up to 1mV negative is allowed
            self.emfgauge.set_enable_filled_Polygon(False)
        else:
            self.emfgauge.set_enable_filled_Polygon()
        self.emfgauge.update_value(emf)

        #self.setTheme("default")
        #Temperature
        ok = True
        errmsg = ''
        temp = self.thermometerWidget.fetch()
        if temp == False:
            errmsg += self.tr('PT1000 not connected between SEN and GND')
            self.Tgauge.update_value(0)
            self.Tgauge.set_enable_filled_Polygon(False)
            ok = False
        elif temp > 500:
            errmsg += self.tr('PT1000 value too high. check connections')
            self.Tgauge.update_value(100)
            self.Tgauge.set_enable_filled_Polygon(False)
            ok = False
        else:
            self.Tgauge.set_enable_filled_Polygon()
            self.Tgauge.update_value(temp)

        if not ok:
            self.msg(errmsg)
            return

        if self.ADC is not None:
            self.msg(self.tr('Temp: ') + '%.2f' % (temp) + ', ' + self.tr('EMF: ') + '%.3f' % (emf))

        if self.state == self.ACTIVE:
            if abs(temp - self.lastT) >= self.intervalBox.value() and (-10 < temp < 200):
                self.lastT = temp
                self.addPoint(temp,emf)

        self.latestTemp=temp
        self.latestEmf=emf

    def addPoint(self,x,y):
        self.valueTable.setRowCount(self.datapoints + 1)
        # Temperature
        item = self.valueTable.item(self.datapoints, 0)
        if item is None:
            item = QtWidgets.QTableWidgetItem()
            self.valueTable.setItem(self.datapoints, 0, item)
        item.setText('%.3f' % x)

        # EMF
        item = self.valueTable.item(self.datapoints, 1)
        if item is None:
            item = QtWidgets.QTableWidgetItem()
            self.valueTable.setItem(self.datapoints, 1, item)
        item.setText('%.3f' % (y))
        self.valueTable.scrollToBottom()

        self.TData[self.datapoints] = x
        self.EMFData[self.datapoints] = y*1e-6 #Convert to volts
        self.datapoints += 1
        self.curve.setData(self.TData[:self.datapoints], self.EMFData[:self.datapoints])

    def addDatapoint(self):
        self.addPoint(self.latestTemp,self.latestEmf)

    def toggleLogging(self):
        icon = QtGui.QIcon()

        if self.state == self.RESET:  #Was off. start recording data
            self.lastT = 200
            self.state = self.ACTIVE
            self.logButton.setText(self.tr('PAUSE MEASUREMENTS'))
            icon.addPixmap(QtGui.QPixmap(":/control/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        elif self.state == self.ACTIVE:
            self.state = self.PAUSED
            self.logButton.setText(self.tr('RESET DATA'))
            self.msg(self.tr('Paused recording'))
            icon.addPixmap(QtGui.QPixmap(":/control/reset.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif self.state == self.PAUSED:
            self.state = self.RESET
            self.graph.setXRange(0, 100)
            self.curve.setData([], [])
            self.curve.clear()
            self.fitcurve.clear()
            self.datapoints = 0
            self.valueTable.scrollToTop()
            self.TData = np.empty(500)
            self.EMFData = np.empty(500)
            self.logButton.setText(self.tr('START MEASUREMENTS'))
            self.msg(self.tr('Clear Traces and Data'))
            icon.addPixmap(QtGui.QPixmap(":/control/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.logButton.setIcon(icon)

    def setInterval(self):
        self.intervalBox.setValue(2)

    def linearFit(self):
        res = ''
        self.isPaused = True;
        S, E = self.region.getRegion()
        start = (np.abs(self.TData[:self.datapoints] - S)).argmin()
        end = (np.abs(self.TData[:self.datapoints] - E)).argmin()
        if start>end: #FLip
            x = end
            end = start
            start = x

        try:
            fa = em.fit_line(self.TData[start:end], self.EMFData[start:end])
            if fa is not None:
                self.fitcurve.clear()
                self.fitcurve.setData(self.TData[start:end], fa[0])
                print('fit',fa[1])
                res += '%.3f uV/C, %.3f\nApprox Room Temp: %.1f' % (fa[1][0]*1e6, fa[1][1]*1e6, (-1*fa[1][1]/fa[1][0]))

        except Exception as e:
            res += '--<br>'
            print(e)
            pass

        self.msgBox = QtWidgets.QMessageBox(self)
        self.msgBox.setWindowTitle('Linear Fit Results')
        self.msgBox.setText(res)
        self.msgBox.show()

    def updateHandler(self, device):
        if (device.connected):
            self.p = device

    def msg(self, m):
        self.msgwin.setText(self.tr(m))

    def saveData(self):
        self.timer.stop()
        fn = QFileDialog.getSaveFileName(self, "Save file", "Thermoelectric_data.csv",
                                         "Text files (*.txt);;CSV files (*.csv)", "CSV files (*.csv)")
        if (len(fn) == 2):  #Tuple
            fn = fn[0]
        if '.' not in fn:
            fn += '.csv'
        print(fn)
        if fn != '':
            f = open(fn, 'wt')
            f.write('time')
            f.write('Temperature(C),EMF(uV)\n')
            for a in range(self.datapoints):
                f.write('%.3f,%d\n' % (self.TData[a], self.EMFData[a]*1e6))
            f.close()
            self.msg(self.tr('Traces saved to ') + fn)
        self.timer.start(self.TIMER)


if __name__ == '__main__':
    import eyes17.eyes

    dev = eyes17.eyes.open()
    app = QApplication(sys.argv)

    # translation stuff
    lang = QLocale.system().name()
    t = QTranslator()
    t.load("lang/" + lang, os.path.dirname(__file__))
    app.installTranslator(t)
    t1 = QTranslator()
    t1.load("qt_" + lang,
            QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(t1)

    mw = Expt(dev)
    mw.show()
    sys.exit(app.exec_())
