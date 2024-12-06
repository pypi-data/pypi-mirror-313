from flask import Blueprint, render_template, request, session, send_from_directory, current_app, jsonify
import os, tempfile, subprocess, json, glob
from PyQt5 import QtCore

bly = Blueprint('blockly', __name__)

showStatusSignal = None
kpyPath = 'kpy'
blockly_ip = ''
blocklyPath = ''



@bly.route('/')
def homeindex():
	return render_template('index.html')


p = None
def setBlocklyPath(pth, ip):
    global blocklyPath, local_ip
    blocklyPath = pth
    print('blockly at',pth)
    blockly_ip = ip

def setShowStatusSignal(sig):
    global showStatusSignal
    showStatusSignal = sig

def setP(dev):
    global p
    p = dev

@bly.route('/visual')
def index():
    return render_template('visual.html')

@bly.route('/editor')
def javaeditor():
    return render_template('editor.html')


@bly.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'logo.png', mimetype='image/png')

@bly.route('/loadxml', methods=['GET'])
def load_xml():
    file = request.args.get('file')
    # Do something with the file (e.g., load it, process it, etc.)
    # For now, return a dummy response
    print(file, blocklyPath)
    f =  open(os.path.join(blocklyPath,'samples',file+'.xml')).read()
    return jsonify({'status': 'success', 'message': f'Loaded {file}','xml':f})



@bly.route('/get_device_status', methods=['GET'])
def get_device_status():
    if p is not None:
        return jsonify({'connected': p.connected})
    else:
        return jsonify({'connected': False})



@bly.route('/set_pv1/<float:value>', methods=['POST'])
def set_pv1(value):
    if p is not None:
        actual_voltage = p.set_pv1(value)  # Set voltage on PV1
        return jsonify({'status': 'success', 'message': f'Set voltage on PV1 to {actual_voltage}V'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_pv2/<float:value>', methods=['POST'])
def set_pv2(value):
    if p is not None:
        actual_voltage = p.set_pv2(value)  # Set voltage on PV2
        return jsonify({'status': 'success', 'message': f'Set voltage on PV2 to {actual_voltage}V'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_voltage/<string:channel>', methods=['GET'])
def get_voltage(channel):
    if p is not None:
        voltage = p.get_voltage(channel)  # Measure voltage from specified channel
        return jsonify({'status': 'success', 'channel': channel, 'voltage': voltage})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_voltage_time/<string:channel>', methods=['GET'])
def get_voltage_time(channel):
    if p is not None:
        t, v = p.get_voltage_time()  # Measure voltage with timestamp
        return jsonify({'status': 'success', 'channel': channel, 'timestamp': t, 'voltage': v})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_average_voltage', methods=['GET'])
def get_average_voltage():
    if p is not None:
        v = p.get_average_voltage(samples=50)  # Default to 50 samples
        return jsonify({'status': 'success', 'average_voltage': v})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/capture1/<string:channel>/<int:ns>/<int:tg>', methods=['GET'])
def capture1(channel, ns, tg):
    if p is not None:
        x, y = p.capture1(channel, ns, tg)  # Single channel oscilloscope
        return jsonify({'status': 'success', 'timestamps': x, 'voltages': y})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/capture2/<int:ns>/<int:tg>', methods=['GET'])
def capture2(ns, tg):
    if p is not None:
        t1, v1, t2, v2 = p.capture2(ns, tg)  # Two channel oscilloscope
        return jsonify({'status': 'success', 'channel1': {'timestamps': t1, 'voltages': v1}, 'channel2': {'timestamps': t2, 'voltages': v2}})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/capture4/<int:ns>/<int:tg>', methods=['GET'])
def capture4(ns, tg):
    if p is not None:
        t1, v1, t2, v2, t3, v3, t4, v4 = p.capture4(ns, tg)  # Four channel oscilloscope
        return jsonify({'status': 'success', 'channel1': {'timestamps': t1, 'voltages': v1}, 'channel2': {'timestamps': t2, 'voltages': v2}, 'channel3': {'timestamps': t3, 'voltages': v3}, 'channel4': {'timestamps': t4, 'voltages': v4}})
    return jsonify({'status': 'error', 'message': 'Device not connected'})



@bly.route('/set_sine/<float:frequency>', methods=['POST'])
def set_sine(frequency):
    if p is not None:
        p.set_sine(frequency)  # Set sine wave frequency
        return jsonify({'status': 'success', 'message': f'Sine wave set to {frequency} Hz'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_wave/<float:frequency>/<string:type>', methods=['POST'])
def set_wave(frequency, type):
    if p is not None:
        p.set_wave(frequency, type)  # Set frequency and type of waveform
        return jsonify({'status': 'success', 'message': f'Waveform set to {type} at {frequency} Hz'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_sine_amp/<int:value>', methods=['POST'])
def set_sine_amp(value):
    if p is not None:
        p.set_sine_amp(value)  # Set sine wave amplitude
        return jsonify({'status': 'success', 'message': f'Sine wave amplitude set to {value}'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/load_equation', methods=['POST'])
def load_equation():
    function = request.json.get('function')
    if p is not None and function:
        p.load_equation(function)  # Load an arbitrary shape to WG using an equation
        return jsonify({'status': 'success', 'message': f'Loaded equation: {function}'})
    return jsonify({'status': 'error', 'message': 'Device not connected or function not provided'})

@bly.route('/set_sq1/<float:frequency>/<int:duty_cycle>', methods=['POST'])
def set_sq1(frequency, duty_cycle=50):
    if p is not None:
        p.set_sq1(frequency, duty_cycle)  # Set square wave frequency for SQ1
        return jsonify({'status': 'success', 'message': f'Square wave SQ1 set to {frequency} Hz with {duty_cycle}% duty cycle'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/set_sq2/<float:frequency>/<int:duty_cycle>', methods=['POST'])
def set_sq2(frequency, duty_cycle=50):
    if p is not None:
        p.set_sq2(frequency, duty_cycle)  # Set square wave frequency for SQ2
        return jsonify({'status': 'success', 'message': f'Square wave SQ2 set to {frequency} Hz with {duty_cycle}% duty cycle'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})


@bly.route('/get_resistance', methods=['GET'])
def get_resistance():
    if p is not None:
        resistance = p.get_resistance()  # Measure resistance between SEN and GND
        return jsonify({'status': 'success', 'resistance': resistance})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_capacitance', methods=['GET'])
def get_capacitance():
    if p is not None:
        capacitance = p.get_capacitance()  # Measure capacitance between IN1 and GND
        return jsonify({'status': 'success', 'capacitance': capacitance})
    return jsonify({'status': 'error', 'message': 'Device not connected'})



@bly.route('/set_state', methods=['POST'])
def set_state():
    data = request.json
    if p is not None:
        p.set_state(SQR1=data.get('SQR1', False), OD1=data.get('OD1', False))  # Set digital states
        return jsonify({'status': 'success', 'message': 'Digital states set successfully'})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_states', methods=['GET'])
def get_states():
    if p is not None:
        states = p.get_states()  # Get logic levels on digital input pins
        return jsonify({'status': 'success', 'states': states})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_state/<string:channel>', methods=['GET'])
def get_state(channel):
    if p is not None:
        state = p.get_state(channel)  # Get logic level on specified digital input pin
        return jsonify({'status': 'success', 'channel': channel, 'state': state})
    return jsonify({'status': 'error', 'message': 'Device not connected'})

@bly.route('/get_freq/<string:channel>', methods=['GET'])
def get_freq(channel):
    if p is not None:
        frequency = p.get_freq(channel)  # Measure frequency on specified input channel
        return jsonify({'status': 'success', 'channel': channel, 'frequency': frequency})
    return jsonify({'status': 'error', 'message': 'Device not connected'})




@bly.route('/get_sensor/<string:sensor>/<string:param>', methods=['GET'])
def get_sensor(sensor, param):
    result = p.get_sensor(sensor, int(param))
    return jsonify({'value': result})


@bly.route('/get_all_sensors', methods=['GET'])
def get_all_sensors():
    sensors = []
    if p is not None:
        for addr in p.addressmap:
            sensors.append(f'[{addr}]{p.addressmap[addr]}')
    print('getAllSensors', p.addressmap, sensors)
    return jsonify({'sensors': sensors})

@bly.route('/scan_i2c', methods=['GET'])
def scan_i2c():
    global p
    sensors = []
    p.active_sensors = {}  # Empty sensors list
    x = p.I2CScan()
    print('Responses from:', x)
    for a in x:
        possiblesensors = p.sensormap.get(a, [])
        for sens in possiblesensors:
            s = p.namedsensors.get(sens)
            sensors.append(f'[{a}]{s["name"].split(" ")[0]}')
    print('found', sensors)
    return jsonify({'sensors': sensors})


@bly.route('/get_sensor_parameters/<string:name>', methods=['GET'])
def get_sensor_parameters(name):
    print('found sensor params for', name, p.namedsensors)
    if name in p.namedsensors:
        return jsonify({'fields': p.namedsensors[name]["fields"]})
    else:
        return jsonify({'fields': ['0']})


@bly.route('/get_generic_sensor/<string:name>/<int:addr>', methods=['GET'])
def get_generic_sensor(name, addr):
    if name not in p.active_sensors:
        p.active_sensors[name] = p.namedsensors[name]
        p.namedsensors[name]['init'](address=addr)
    vals = p.active_sensors[name]['read']()
    #print(vals, type(vals))
    if vals is not None:
        return jsonify({'data': [float(a) for a in vals]})
    else:
        return jsonify({'data': None})


