import typing

import numpy as np
from flask import Flask, request, Blueprint, jsonify
import logging
from flask_cors import CORS
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QEventLoop
from PyQt5.QtWidgets import QApplication

# blueprint for socket comms parts of app
from .blockly_routes import bly as blockly_blueprint
from .blockly_routes import setBlocklyPath, setShowStatusSignal, setP
from werkzeug.serving import make_server, WSGIRequestHandler
import threading, webbrowser

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


print('starting the compile server...')

flask_thread = None
server_ip = ''
device = None


def create_server(showStatusSignal, serverSignal, path, local_ip, dev):
	global flask_thread, server_ip, device
	server_ip = local_ip
	setShowStatusSignal(showStatusSignal)
	setBlocklyPath(path, local_ip)
	device = dev
	setP(dev)
	flask_thread = FlaskThread()
	flask_thread.setShowStatusSignal(showStatusSignal)
	flask_thread.setServerSignal(serverSignal)
	# flask_thread.finished.connect(QApplication.quit)

	# Start the thread
	flask_thread.start()
	return flask_thread



class FlaskThread(QThread):
	finished = pyqtSignal()
	serverSignal = None
	MPSlots= None


	def __init__(self, parent=None):
		super().__init__(parent)
		self.cameraReadySignal = None
		self.coords = None
		self.server = None


	def setServerSignal(self, sig):
		self.serverSignal = sig
		self.QuietRequestHandler.serverSignal = self.serverSignal

	def setShowStatusSignal(self, sig):
		self.showStatusSignal = sig
		self.QuietRequestHandler.showStatusSignal = self.showStatusSignal


	class QuietRequestHandler(WSGIRequestHandler):
		serverSignal = None
		showStatusSignal = None
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

		def log(self, type, message, *args):
			# Emit the log message using the serverSignal
			if self.showStatusSignal:
				self.showStatusSignal.emit(type+':'+message%args,False)


	def run(self):
		# Run the Flask app in a separate thread
		print('starting the flask app...')
		self.app = Flask(__name__, template_folder='flask_templates', static_folder='static', static_url_path='/')
		self.app.logger.setLevel(logging.WARNING)
		CORS(self.app)
		self.app.register_blueprint(blockly_blueprint)
		try:
			#self.app.run(host='0.0.0.0', port=5000)
			self.server = make_server('0.0.0.0', 8888, self.app, request_handler=self.QuietRequestHandler)
			self.server.serve_forever()
		except Exception as e:
			import traceback
			self.serverSignal.emit(traceback.format_exc())

	def updateCoords(self,c):
		self.coords = c
		#print(c)

	def stop_flask_app(self):
		if hasattr(self, 'server') and self.server:
			self.server.shutdown()

		self.delMPSignal.emit()
		# Perform any necessary cleanup before stopping the app
		# Stop the Flask app

