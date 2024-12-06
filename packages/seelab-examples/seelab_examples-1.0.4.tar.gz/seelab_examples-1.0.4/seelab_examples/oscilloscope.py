'''
A four channel Oscilloscope with basic features

'''
import sys
import time
import numpy as np
from functools import partial
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from queue import Queue
from dataclasses import dataclass
from enum import Enum, auto

class CommandType(Enum):
    TRIGGER_LEVEL = auto()
    TRIGGER_SOURCE = auto()
    TRIGGER_ENABLE = auto()
    SINE_FREQ = auto()
    PV1_VOLTAGE = auto()
    PV2_VOLTAGE = auto()
    SELECT_RANGE = auto()
    # Add more command types as needed

@dataclass
class Command:
    type: CommandType
    args: dict

class OscilloscopeThread(QtCore.QThread):
    data_ready = QtCore.pyqtSignal(object, object)
    finished = QtCore.pyqtSignal()
    
    def __init__(self, device, input_selector):
        super().__init__()
        self.device = device
        self.running = True
        self.paused = False
        self.input_selector = input_selector
        self.enabled_channels = [True] * 4  # All channels enabled by default
        self.trigger_enabled = True
        self.command_queue = Queue()
        self.timebase_value = 2  # Initialize timebase_value with a default value
        self.NP = 1000
        
    def run(self):
        while self.running:
            # Process any pending commands
            self.process_commands()
            
            if not self.paused:
                # Get indices of enabled channels (0 for A1, 1 for A2, etc.)
                active_channels = [i for i, enabled in enumerate(self.enabled_channels) if enabled]
                if not active_channels:
                    time.sleep(0.01)
                    continue
                
                # Determine number of channels to capture
                if 2 in active_channels or 3 in active_channels:  # If A3 or MIC is enabled
                    num_channels = 4  # Must capture all channels
                elif len(active_channels) == 2 and 0 in active_channels and 1 in active_channels:
                    num_channels = 2  # Only A1 and A2
                else:
                    num_channels = 1  # Single channel case
                
                # Determine input mapping for first channel
                first_active = active_channels[0]
                if first_active == 3:
                    channel_input = 'MIC'
                else:
                    channel_input = self.input_selector if first_active == 0 else f'A{first_active + 1}'
                #print(f"Capturing {num_channels} channels with input {channel_input}")
                # Start capture
                self.device.capture_traces(num_channels,self.NP, self.timebase_value, channel_input, trigger=self.trigger_enabled)
                
                # Wait for capture to complete
                while True:
                    if not self.running:
                        return
                    
                    status = self.device.oscilloscope_progress()
                    if status[0]:  # Conversion done
                        break
                    time.sleep(0.01)
                
                # Fetch data only for enabled channels
                x = []
                y = []
                for i in range(4):
                    if self.enabled_channels[i]:
                        channel_num = i + 1
                        x_data, y_data = self.device.fetch_trace(channel_num)
                        x.append(x_data/1e6) #uS to Seconds
                        y.append(y_data)
                    else:
                        x.append([])
                        y.append([])
                
                # Emit the data
                self.data_ready.emit(x, y)
                self.finished.emit()


    def process_commands(self):
        """Process all pending commands in the queue"""
        while not self.command_queue.empty():
            try:
                cmd = self.command_queue.get_nowait()
                self.execute_command(cmd)
                self.command_queue.task_done()
            except Queue.Empty:
                break
    
    def execute_command(self, cmd: Command):
        """Execute a single command"""
        try:
            if cmd.type == CommandType.TRIGGER_LEVEL:
                self.device.configure_trigger(
                    cmd.args['channel'],
                    cmd.args['source'],
                    cmd.args['level']
                )
            elif cmd.type == CommandType.TRIGGER_ENABLE:
                self.trigger_enabled = cmd.args['enabled']
            elif cmd.type == CommandType.SINE_FREQ:
                self.device.set_sine(cmd.args['frequency'])
            elif cmd.type == CommandType.PV1_VOLTAGE:
                self.device.set_pv1(cmd.args['voltage'])
            elif cmd.type == CommandType.PV2_VOLTAGE:
                self.device.set_pv2(cmd.args['voltage'])
            elif cmd.type == CommandType.SELECT_RANGE:
                self.device.select_range(cmd.args['channel'],cmd.args['value'])
            # Add more command handlers as needed
            
        except Exception as e:
            print(f"Error executing command {cmd.type}: {e}")

    
    def pause(self):
        """Pause data acquisition"""
        self.paused = True
    
    def resume(self):
        """Resume data acquisition"""
        self.paused = False
    
    def stop(self):
        """Stop the thread"""
        self.running = False
        self.wait()
    
    def update_channels(self, enabled_list):
        """Update which channels are enabled"""
        self.enabled_channels = enabled_list


class QCollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        
        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)
        
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content_area.setWidgetResizable(True)
        
        self.content_widget = QtWidgets.QWidget()
        self.content_area.setWidget(self.content_widget)
        
        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)
        
        self.content_area.setMaximumHeight(0)  # Start collapsed
        self.content_area.setMinimumHeight(0)
        
        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )
    
    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow
        )
        
        if checked:
            self.content_area.setMaximumHeight(0)  # Collapse
            self.content_area.setMinimumHeight(0)
        else:
            self.content_area.setMaximumHeight(max(self.content_widget.sizeHint().height(), 1000))  # Expand
            self.content_area.setMinimumHeight(max(self.content_widget.sizeHint().height(), 120))

    
    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = layout.sizeHint().height()
        
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(100)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)
        
        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

class Expt(QtWidgets.QMainWindow):
    def __init__(self, dev):
        super().__init__()
        self.device = dev
        #self.device.set_sine(1000)

        self.amplification_options = [16.0, 8.0, 4.0, 2.5, 1.5, 1.0, 0.5]
        self.setWindowTitle("Four Channel Oscilloscope")
        self.setGeometry(100, 100, 1000, 600)
        
        # Create main layout with trigger controls on right
        main_layout = QtWidgets.QHBoxLayout()
        left_layout = QtWidgets.QVBoxLayout()
        trigger_layout = QtWidgets.QVBoxLayout()
        
        # Create central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        
        # Create single plot widget
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.plot_widget.setBackground('w')
        left_layout.addWidget(self.plot_widget)
        

        # Create timebase slider
        self.tbvals = [0.100, 0.200, 0.500, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]  # allowed mS/div values
        self.timebase_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.timebase_slider.setMinimum(0)  # Set minimum value
        self.timebase_slider.setMaximum(len(self.tbvals)-1)  # Set maximum value
        self.timebase_slider.setValue(1)  # Set default value
        self.timebase_slider.valueChanged.connect(self.update_timebase)

        # Add the timebase slider to the layout below the plot
        self.timebase_label = QtWidgets.QLabel("Timebase (ms):")
        left_layout.addWidget(self.timebase_label)
        left_layout.addWidget(self.timebase_slider)

        # Create single plot with 4 curves
        self.plot = self.plot_widget.addPlot(row=0, col=0)
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel('left', 'Voltage', units='V')
        self.plot.setLabel('bottom', 'Time', units='s')
        self.plot.setYRange(-5, 5)

        # Create arrow item for trigger level
        self.trigger_arrow = pg.ArrowItem(angle=180, tipAngle=30, baseAngle=30, pen='g', brush='#333')
        self.plot.addItem(self.trigger_arrow)
        self.trigger_arrow.setPos( 0.,0. )  # Set initial position to 0 volts
        self.trigger_arrow.hide()  # Hide initially

        # Create 4 curves with different colors
        self.curves = []
        self.channel_names = ['A1', 'A2', 'A3', 'MIC']
        colors = ['b', 'r', 'g', 'y']
        
        # Create legend
        self.plot.addLegend()
        self.current_input = 'A1'
        
        for name, color in zip(self.channel_names, colors):
            curve = self.plot.plot(pen=pg.mkPen(color, width=2), name=name)
            self.curves.append(curve)
        
        # Add controls layout
        controls_layout = QtWidgets.QHBoxLayout()
        
        
        # Add visibility toggles for each channel
        self.channel_toggles = []
        for name in self.channel_names:
            frame = QtWidgets.QFrame()
            frame.setFrameShape(QtWidgets.QFrame.Box)
            frame_layout = QtWidgets.QVBoxLayout()
            frame.setLayout(frame_layout)
            controls_layout.addWidget(frame)
            
            checkbox = QtWidgets.QCheckBox(name)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.update_channel_visibility)
            self.channel_toggles.append(checkbox)
            frame_layout.addWidget(checkbox)

            if name == 'A1':
                #checkbox.setText("")
                # Add channel input selector for A1
                self.input_selector = QtWidgets.QComboBox()
                self.input_selector.addItems(['A1', 'A2', 'A3', 'MIC', 'IN1', 'SEN'])
                self.input_selector.currentTextChanged.connect(self.input_changed)
                frame_layout.addWidget(self.input_selector)

                self.amplification_combobox_a1 = QtWidgets.QComboBox()
                self.amplification_combobox_a1.addItems([f"{v}V" for v in self.amplification_options])
                self.amplification_combobox_a1.currentIndexChanged.connect(partial( self.select_amplification,name))
                frame_layout.addWidget(self.amplification_combobox_a1)
            elif name == 'A2':                
                self.amplification_combobox_a2 = QtWidgets.QComboBox()
                self.amplification_combobox_a2.addItems([f"{v}V" for v in self.amplification_options])
                self.amplification_combobox_a1.currentIndexChanged.connect(partial( self.select_amplification,name))
                frame_layout.addWidget(self.amplification_combobox_a2)


        # Create button group for oscilloscope control
        self.play_pause_btn = QtWidgets.QPushButton("⏸️")  # Unicode pause symbol
        self.play_pause_btn.setCheckable(True)
        self.play_pause_btn.clicked.connect(self.toggle_capture)
        controls_layout.addWidget(self.play_pause_btn)
        
        self.single_btn = QtWidgets.QPushButton("SINGLE")
        self.single_btn.clicked.connect(self.single_capture)
        self.single_btn.hide()  # Hidden by default in run mode
        controls_layout.addWidget(self.single_btn)
        
        left_layout.addLayout(controls_layout)
        
        # Add collapsible control sections
        controls_layout = QtWidgets.QVBoxLayout()
        
        # Voltage Controls Section
        voltage_box = QCollapsibleBox("▶ Voltage Controls")
        voltage_layout = QtWidgets.QHBoxLayout()
        
        # PV1 Controls
        pv1_group = QtWidgets.QGroupBox("PV1")
        pv1_layout = QtWidgets.QVBoxLayout()
        self.pv1_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pv1_slider.setMinimum(-500)  # -5V
        self.pv1_slider.setMaximum(500)   # +5V
        self.pv1_slider.setValue(0)
        self.pv1_label = QtWidgets.QLabel("0 V")
        self.pv1_slider.valueChanged.connect(lambda v: self.update_pv1(v/100))
        pv1_layout.addWidget(self.pv1_label)
        pv1_layout.addWidget(self.pv1_slider)
        pv1_group.setLayout(pv1_layout)
        voltage_layout.addWidget(pv1_group)
        
        # PV2 Controls
        pv2_group = QtWidgets.QGroupBox("PV2")
        pv2_layout = QtWidgets.QVBoxLayout()
        self.pv2_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.pv2_slider.setMinimum(-330)  # -3.3V
        self.pv2_slider.setMaximum(330)   # +3.3V
        self.pv2_slider.setValue(0)
        self.pv2_label = QtWidgets.QLabel("0 V")
        self.pv2_slider.valueChanged.connect(lambda v: self.update_pv2(v/100))
        pv2_layout.addWidget(self.pv2_label)
        pv2_layout.addWidget(self.pv2_slider)
        pv2_group.setLayout(pv2_layout)
        voltage_layout.addWidget(pv2_group)
        
        voltage_widget = QtWidgets.QWidget()
        voltage_widget.setLayout(voltage_layout)
        voltage_box.setContentLayout(voltage_layout)
        controls_layout.addWidget(voltage_box)
        
        # Wave Generator Section
        wave_box = QCollapsibleBox("▶ Wave Generator")
        wave_layout = QtWidgets.QHBoxLayout()
        
        # Sine Wave Controls
        sine_group = QtWidgets.QGroupBox("Sine Wave")
        sine_layout = QtWidgets.QVBoxLayout()
        self.wg_freq = QtWidgets.QSpinBox()
        self.wg_freq.setMinimum(1)
        self.wg_freq.setMaximum(5000)
        self.wg_freq.setValue(1000)
        self.wg_freq.setSuffix(" Hz")
        self.wg_freq.valueChanged.connect(self.update_wg)
        sine_layout.addWidget(QtWidgets.QLabel("Frequency"))
        sine_layout.addWidget(self.wg_freq)
        sine_group.setLayout(sine_layout)
        wave_layout.addWidget(sine_group)
        
        # Square Wave Controls
        sq1_group = QtWidgets.QGroupBox("Square Wave (SQ1)")
        sq1_layout = QtWidgets.QGridLayout()
        
        self.sq1_freq = QtWidgets.QSpinBox()
        self.sq1_freq.setMinimum(1)
        self.sq1_freq.setMaximum(50000)
        self.sq1_freq.setValue(1000)
        self.sq1_freq.setSuffix(" Hz")
        self.sq1_freq.valueChanged.connect(self.update_sq1)
        
        self.sq1_duty = QtWidgets.QSpinBox()
        self.sq1_duty.setMinimum(0)
        self.sq1_duty.setMaximum(100)
        self.sq1_duty.setValue(50)
        self.sq1_duty.setSuffix(" %")
        self.sq1_duty.valueChanged.connect(self.update_sq1)
        
        sq1_layout.addWidget(QtWidgets.QLabel("Frequency"), 0, 0)
        sq1_layout.addWidget(self.sq1_freq, 0, 1)
        sq1_layout.addWidget(QtWidgets.QLabel("Duty Cycle"), 1, 0)
        sq1_layout.addWidget(self.sq1_duty, 1, 1)
        sq1_group.setLayout(sq1_layout)
        wave_layout.addWidget(sq1_group)
        
        wave_widget = QtWidgets.QWidget()
        wave_widget.setLayout(wave_layout)
        wave_box.setContentLayout(wave_layout)
        controls_layout.addWidget(wave_box)
        
        # Add controls layout to main layout
        left_layout.addLayout(controls_layout)
        
        # Set stretch factors
        left_layout.setStretch(0, 4)  # Plot gets most space
        left_layout.setStretch(1, 0)  # Channel controls minimum space
        left_layout.setStretch(2, 0)  # Collapsible controls minimum space
        
        # Create trigger controls
        trigger_group = QtWidgets.QGroupBox("Trigger")
        trigger_layout_inner = QtWidgets.QVBoxLayout()
        
        # Trigger Enable Checkbox
        self.trigger_enable = QtWidgets.QCheckBox("Enable Trigger")
        self.trigger_enable.setChecked(True)
        self.trigger_enable.stateChanged.connect(self.update_trigger)
        trigger_layout_inner.addWidget(self.trigger_enable)
        
        # Trigger Source Selector
        trigger_layout_inner.addWidget(QtWidgets.QLabel("Source:"))
        self.trigger_source = QtWidgets.QComboBox()
        self.trigger_source.currentTextChanged.connect(self.update_trigger)
        trigger_layout_inner.addWidget(self.trigger_source)
        
        # Trigger Level Slider
        self.trigger_level = QtWidgets.QSlider(QtCore.Qt.Vertical)
        self.trigger_level.setMinimum(-500)  # -5V
        self.trigger_level.setMaximum(500)   # +5V
        self.trigger_level.setValue(0)        # 0V
        self.trigger_level.valueChanged.connect(self.update_trigger)
        
        # Show value as tooltip continuously while dragging
        self.trigger_level.sliderMoved.connect(self.update_trigger_tooltip)
        
        trigger_layout_inner.addWidget(self.trigger_level)  # Add slider directly
        
        # Trigger level display (optional, can be removed)
        self.trigger_level_label = QtWidgets.QLabel("0 V")
        trigger_layout_inner.addWidget(self.trigger_level_label)
        
        trigger_group.setLayout(trigger_layout_inner)
        trigger_layout.addWidget(trigger_group)
        
        # Add layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(trigger_layout)
        
        # Initialize device and thread
        try:
            self.scope_thread = OscilloscopeThread(self.device, self.input_selector.currentText())
            self.scope_thread.data_ready.connect(self.update_plot)
            self.scope_thread.finished.connect(self.single_capture_complete)
            
            # Update trigger source options based on enabled channels
            self.update_trigger_sources()
            
            # Start capture immediately
            self.start_capture()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to initialize device: {str(e)}")
            sys.exit(1)
    
    def toggle_capture(self):
        if self.play_pause_btn.isChecked():
            self.stop_capture()
            self.play_pause_btn.setText("▶️")  # Unicode play symbol
            self.single_btn.show()
        else:
            self.start_capture()
            self.play_pause_btn.setText("⏸️")  # Unicode pause symbol
            self.single_btn.hide()
    
    def single_capture(self):
        """Capture a single trace and then stop"""
        # Disable the button while capturing
        self.single_btn.setEnabled(False)
        
        # Resume the thread for one capture
        self.scope_thread.resume()
        # Stop after one measurement
        QtCore.QTimer.singleShot(100, self.scope_thread.pause)
    
    def single_capture_complete(self):
        """Re-enable the single button after capture is complete"""
        if self.scope_thread.paused:  # Only re-enable if we're in single-shot mode
            self.single_btn.setEnabled(True)
    
    def start_capture(self):
        """Start continuous capture"""
        self.scope_thread.resume()
        if not self.scope_thread.isRunning():
            self.scope_thread.start()
    
    def stop_capture(self):
        """Stop capture"""
        self.scope_thread.pause()
    
    def update_plot(self, x, y):
        for i, curve in enumerate(self.curves):
            curve.setData(x[i], y[i])
    
    def update_channel_visibility(self, state):
        """Update which channels are enabled and visible"""
        enabled_channels = [toggle.isChecked() for toggle in self.channel_toggles]
        for toggle, curve in zip(self.channel_toggles, self.curves):
            curve.setVisible(toggle.isChecked())
        
        # Update thread with enabled channels
        if hasattr(self, 'scope_thread'):
            self.scope_thread.update_channels(enabled_channels)
        
        # Update trigger sources
        self.update_trigger_sources()
    
    def closeEvent(self, event):
        if hasattr(self, 'scope_thread'):
            self.scope_thread.stop()
            self.scope_thread.wait()
        event.accept()
    
    def input_changed(self, new_input):
        """Handle input selection change"""
        if hasattr(self, 'scope_thread'):
            self.scope_thread.input_selector = new_input
            self.current_input = new_input
            # If we're running, restart capture with new input
            if not self.play_pause_btn.isChecked():
                self.stop_capture()
                self.start_capture()
    
    def update_trigger_sources(self):
        """Update trigger source dropdown based on enabled channels"""
        current = self.trigger_source.currentText()
        self.trigger_source.clear()
        
        # Always add CH1 (mapped input)
        self.trigger_source.addItem(self.current_input)
        
        # Add other enabled channels
        if self.channel_toggles[1].isChecked():
            self.trigger_source.addItem("A2")
        if self.channel_toggles[2].isChecked():
            self.trigger_source.addItem("A3")
        if self.channel_toggles[3].isChecked():
            self.trigger_source.addItem("MIC")
            
        # Try to restore previous selection if still valid
        index = self.trigger_source.findText(current)
        if index >= 0:
            self.trigger_source.setCurrentIndex(index)
    
    def update_trigger(self):
        """Queue trigger update command"""
        if not hasattr(self, 'scope_thread'):
            return
            
        enabled = self.trigger_enable.isChecked()
        source = self.trigger_source.currentText()
        level = self.trigger_level.value() / 100.0
        

        # Update the position of the trigger arrow
        self.trigger_arrow.setPos(0., level)  # Update arrow position to the current trigger level
        self.trigger_arrow.setVisible(enabled)  # Show or hide based on trigger enable state

        # Update level display
        self.trigger_level_label.setText(f"{level:.2f} V")
        
        # Map CH1 to actual input if needed
        if source == self.current_input:
            source = self.input_selector.currentText()
        #print(self.current_input, self.trigger_source.currentText())
        # Get channel number
        chan_map = {self.current_input: 0, "A2": 1, "A3": 2, "MIC": 3}
        chan = chan_map[self.trigger_source.currentText()]
        
        # Queue commands
        self.scope_thread.command_queue.put(Command(
            type=CommandType.TRIGGER_ENABLE,
            args={'enabled': enabled}
        ))
        
        if enabled:
            self.scope_thread.command_queue.put(Command(
                type=CommandType.TRIGGER_LEVEL,
                args={
                    'channel': chan,
                    'source': source,
                    'level': level
                }
            ))
    
    def update_pv1(self, voltage):
        """Update PV1 voltage"""
        self.pv1_label.setText(f"{voltage:.2f} V")
        if hasattr(self, 'scope_thread'):
            self.scope_thread.command_queue.put(Command(
                type=CommandType.PV1_VOLTAGE,
                args={'voltage': voltage}
            ))
    
    def update_pv2(self, voltage):
        """Update PV2 voltage"""
        self.pv2_label.setText(f"{voltage:.2f} V")
        if hasattr(self, 'scope_thread'):
            self.scope_thread.command_queue.put(Command(
                type=CommandType.PV2_VOLTAGE,
                args={'voltage': voltage}
            ))
    
    def update_wg(self):
        """Update wave generator frequency"""
        if hasattr(self, 'scope_thread'):
            self.scope_thread.command_queue.put(Command(
                type=CommandType.SINE_FREQ,
                args={
                    'frequency': self.wg_freq.value(),
                    'wave_type': 'sine'
                }
            ))
    
    def update_sq1(self):
        """Update SQ1 frequency and duty cycle"""
        if hasattr(self, 'scope_thread'):
            self.scope_thread.command_queue.put(Command(
                type=CommandType.SQR1,
                args={
                    'frequency': self.sq1_freq.value(),
                    'duty_cycle': self.sq1_duty.value()
                }
            ))
    
    def update_timebase(self):
        """Update the timebase value for capture"""
        NP = 1000
        tb = self.timebase_slider.value()
        msperdiv = self.tbvals[int(tb)]  # millisecs / division
        totalusec = msperdiv * 1000 * 10.0  # total 10 divisions
        timebase_value = int(totalusec / NP) #NP = 1000
        print(totalusec/1.e6)
        self.plot.setXRange(0, totalusec/1.e6)
        self.plot.setYRange(-5, 5)

        self.scope_thread.timebase_value = timebase_value
        self.scope_thread.NP = NP
        self.timebase_label.setText("TimeBase: %d (mS)/div  | Duration: %d mS"%(msperdiv, msperdiv*10))

    def update_trigger_tooltip(self):
        """Update the tooltip for the trigger level slider continuously while dragging"""
        level = self.trigger_level.value() / 100.0  # Convert to volts
        tooltip_text = f"Level: {level:.2f} V"
        self.trigger_level.setToolTip(tooltip_text)

    def select_amplification(self, channel, value):
        """Select amplification for the specified channel"""
        # Call the function to set the range
        self.scope_thread.command_queue.put(Command(
            type=CommandType.SELECT_RANGE,
            args={
                'channel': channel,
                'value': self.amplification_options[value]
            }
        ))


if __name__ == "__main__":
    from eyes17.eyes import open as eyes17_open
    app = QtWidgets.QApplication(sys.argv)
    device = eyes17_open()
    window = Expt(device)
    window.show()
    sys.exit(app.exec_())