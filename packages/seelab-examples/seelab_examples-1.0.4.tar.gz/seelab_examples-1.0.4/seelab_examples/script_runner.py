import os, time
import sys, json, serial, platform
import tempfile,importlib
import pyqtgraph as pg
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore
try:
    from .utilities.syntax import PythonHighlighter
except:
    from utilities.syntax import PythonHighlighter

from eyes17.eyes import open as eyes17_open

import importlib.util  # Added import for importlib



def listPorts():
    '''
    Make a list of available serial ports. For auto scanning and connecting
    '''
    import glob
    system_name = platform.system()
    if system_name == "Windows":
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial('COM%d'%i)
                available.append('COM%d'%i)
                s.close()
            except serial.SerialException:
                pass
        return available
    elif system_name == "Darwin":
        # Mac
        return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
    else:
        # Assume Linux or something else
        return glob.glob('/dev/ttyACM*')

def isPortFree(portname):
    try:
        fd = serial.Serial(portname, 500000, stopbits=1, timeout = 1.0)
        if fd.isOpen():
            if 'inux' in platform.system(): #Linux based system
                import fcntl    
                try:
                    fcntl.flock(fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fd.close()
                    return True #Port is available
                except IOError:
                    fd.close()
                    return False #Port is not available

            else:
                fd.close()
                return True #Port is available
        else:
            fd.close()
            return False #Port is not available

    except serial.SerialException as ex:
        return False #Port is not available

def getFreePorts(openPort=None):
    '''
    Find out which ports are currently free 
    '''
    portlist={}
    for a in listPorts():
        if a != openPort:
            portlist[a] = isPortFree(a)
        else:
            portlist[a] = False
    return portlist


class HoverToolbar(QtWidgets.QToolBar):
    def __init__(self, text, hideFunc, parent=None):
        super().__init__(text, parent)
        self.hideFunc = hideFunc
        self.timer = QtCore.QTimer(self)  # Create a timer
        self.timer.setSingleShot(True)  # Set the timer to be single shot
        self.timer.timeout.connect(self.hideFunc)  # Connect the timer to hideFunc

    def leaveEvent(self, event):
        self.timer.start(2000)  # Start the timer

    def enterEvent(self, event):
        self.timer.stop()  # Stop the timer if the user re-enters


class HoverOpenBtn(QtWidgets.QPushButton):
    def __init__(self, text, openOtionsFunc, parent=None):
        super().__init__(text, parent)
        self.openFunc = openOtionsFunc

    def enterEvent(self, event):
        self.openFunc()


class ZoomableTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFontPointSize(12)  # Set an initial font size

    def wheelEvent(self, event):
        # Check if the Ctrl key is pressed
        if event.modifiers() == QtCore.Qt.ControlModifier:
            # Zoom in or out based on the scroll direction
            delta = event.angleDelta().y()
            if delta > 0:
                self.setFontPointSize(self.fontPointSize() + 1)  # Zoom in
            else:
                self.setFontPointSize(self.fontPointSize() - 1)  # Zoom out
            event.accept()  # Accept the event
        else:
            super().wheelEvent(event)  # Call the base class implementation

    def fontPointSize(self):
        # Get the current font point size
        return self.font().pointSize()

    def setFontPointSize(self, size):
        # Set the font point size
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

class ScriptRunner(QtWidgets.QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.showMaximized()
        layouts_path = os.path.join(os.path.dirname(__file__), 'layouts')
        sys.path.append(layouts_path)  # Add layouts directory to sys.path

        self.createFileMenu()
        self.createPipMenu()
        self.device = None
        self.setWindowTitle("SEELab3/ExpEYES Sample Programs")
        self.setGeometry(100, 100, 800, 600)
        self.editMode = True
        self.module = None
        self.ipyConsole = None
        self.selected_script = None
        self.help_file = None
        self.help_server = None


        # Create a central widget
        self.central_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        self.sbar = self.statusBar()

        # Add a button to run/edit the code
        self.run_code_button = QtWidgets.QPushButton("Run Code", self)
        self.run_code_button.setIcon(QtGui.QIcon(os.path.join("icons","play_icon.png")))  # Set play icon
        self.run_code_button.clicked.connect(self.run_code)
        
        self.sbar.addPermanentWidget(self.run_code_button)


        self.help_button = QtWidgets.QPushButton("Show Help", self)
        self.help_button.setIcon(QtGui.QIcon(os.path.join("icons","help.svg")))  # Set play icon
        self.help_button.clicked.connect(self.show_help)
        self.sbar.addPermanentWidget(self.help_button)


        #self.toolbar.addWidget(self.run_code_button)

        self.createExperimentsToolbar()

        # Store the currently loaded script
        self.current_script = None

        # Add the QTextEdit to the central widget
        self.source_code_edit = QtWidgets.QTextEdit(self)
        self.central_widget.addWidget(self.source_code_edit)
        self.central_widget.setCurrentWidget(self.source_code_edit)  # Show the source code editor


        # Load available scripts
        self.create_experiments_menu()

        self.createThemeMenu()

        # Remove tmp.py
        tmp_file_path = os.path.join(os.path.dirname(__file__), 'tmp.py')
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)



        self.setTheme("default")

        self.selected_script = args.script if args.script else 'oscilloscope'
        self.initializeCommunications()

        #Auto-Detector
        self.deviceSelector = self.portSelectionDialog()
        self.shortlist=[]

        self.startTime = time.time()
        self.timer = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.locateDevices)
        self.timer.start(1500)

    def selectDevice(self):

        self.locateDevices(True)        
        if self.deviceSelector.exec_():
            if self.device.H.portname != self.deviceSelector.getSelection():
                if self.current_script:
                    try:
                        self.current_script.timer.stop()  # Stop the timer loop of current widget
                    except:
                        pass
                self.current_script.close()  # Close the current script if it's open

                self.initializeCommunications(port = self.deviceSelector.getSelection())
            else:
                self.showStatus('Device already connected',False)

    def initializeCommunications(self,port=False):
        if self.device:
            self.device.H.disconnect()
            self.device.H.portname=None
        if port:
            self.device = eyes17_open(port = port)
        else:
            self.device = eyes17_open()
        
        if self.device.connected:
            self.showStatus('Device Connected',False)

        self.load_script(self.selected_script if self.selected_script is not None else 'oscilloscope')


    def locateDevices(self, force = False):
        if self.device and not force:
            if self.device.H.connected:
                return

        try:
            L = getFreePorts(self.device.H.portname)
        except Exception as e:
            print(e)
            return
        total = len(L)
        menuChanged = False
        print(total, menuChanged)
        if L != self.shortlist:
            menuChanged = True

            self.deviceSelector.setList(L,self.device.H)
            #Check for, and handle disconnect event
            if self.device.connected:
                if platform.system() == "Windows": return #Ignore disconnect event on windows
                if self.device.H.portname not in L and not force:
                        self.showStatus('Device Disconnected',True)
                        self.setWindowTitle('Error : Device Disconnected')
                        QtWidgets.QMessageBox.warning(self, 'Connection Error', 'Device Disconnected. Please check the connections')
                        try:
                            self.device.H.disconnect()
                            self.device.H.portname = None
                        except:pass
                        self.device.connected = False

            elif True in L.values():
                reply = QtWidgets.QMessageBox.question(self, 'Connection', 'Device Available. Connect?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    self.initializeCommunications()

            #update the shortlist
            self.shortlist=L


    class portSelectionDialog(QtWidgets.QDialog):
        def __init__(self,parent=None):
            super(ScriptRunner.portSelectionDialog, self).__init__(parent)
            self.button_layout = QtWidgets.QVBoxLayout()
            self.setLayout(self.button_layout)
            self.btns=[]
            self.doneButton = QtWidgets.QPushButton("Done")
            self.button_layout.addWidget(self.doneButton)
            self.doneButton.clicked.connect(self.finished)


        def setList(self,L,handler):
            for a in self.btns:
                a.setParent(None)
                del a
            self.btns=[]

            self.button_group = QtWidgets.QButtonGroup()

            #moods[0].setChecked(True)
            pos=0
            for i in L:
                # Add each radio button to the button layout
                btn = QtWidgets.QRadioButton(i)
                self.button_layout.addWidget(btn)
                self.btns.append(btn)
                if handler:
                    if handler.connected:
                        if handler.portname == i:
                            btn.setStyleSheet("color:green;")
                if not L[i]: #Port in use
                    btn.setEnabled(False)
                    btn.setChecked(True)

                self.button_group.addButton(btn, pos)
                pos+=1

            # Set the layout of the group box to the button layout

        #Print out the ID & text of the checked radio button
        def finished(self):
            if self.button_group.checkedId()!= -1:
                self.done(QtWidgets.QDialog.Accepted)
        def getSelection(self):
            if self.button_group.checkedId()!= -1:
                return self.button_group.checkedButton().text()
            else:
                return False

    def checkConnectionStatus(self,dialog=False):
        if self.p.connected:return True
        else:
            if dialog: QtWidgets.QMessageBox.warning(self, 'Connection Error', 'Device not connected. Please connect an MCA to the USB port')
            return False

    def showStatus(self,msg,error=None):
        if error: self.sbar.setStyleSheet("color:#F77")
        else: self.sbar.setStyleSheet("color:#000000")
        self.sbar.showMessage(msg)

    def createExperimentsToolbar(self):
        BW = 40
        BH = 40
        H = 50

        # Create a toolbar for script selection
        self.toolbar = QtWidgets.QToolBar("ExptMenus")
        self.toolbar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.toolbar)

        # Add square icon buttons to the toolbar
        with open(os.path.join(os.path.dirname(__file__),'experiments.json'), 'r') as file:
            data = json.load(file)  # Load the JSON data
        #print(data)
        for name in data:
            button = HoverOpenBtn(f"{name}",partial(self.updateExperimentsSubmenuToolbar,data[name]),self)
            button.setIcon(QtGui.QIcon(os.path.join("icons", name+'.png')))  # Set icon
            button.setFixedHeight(H)  # Set fixed height
            
            button.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)  # Allow width to expand
            button.setIconSize(QtCore.QSize(BW, BH))
            self.toolbar.addWidget(button)  # Add button to the toolbar

        self.addToolBarBreak()
        self.child_toolbar = HoverToolbar("ExptMenus2",self.hideExperimentsSubmenuToolbar)
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.child_toolbar)
        self.child_toolbar.hide()

        self.addToolBarBreak()
        self.coding_toolbar = HoverToolbar("CodingMenu",self.hideExperimentsSubmenuToolbar)
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.coding_toolbar)
        self.coding_toolbar.hide()


        # Create a button to open the IPython console with a Python logo icon
        self.console_button = QtWidgets.QPushButton("Write Code!",self)
        self.console_button.setIcon(QtGui.QIcon(os.path.join("icons","python_logo.png")))  # Set Python logo icon
        self.console_button.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)  # Allow width to expand
        self.console_button.setFixedHeight(H)  # Set fixed height
        self.console_button.setIconSize(QtCore.QSize(BW, BH))
        self.console_button.clicked.connect(self.add_ipython_console)


        # Create a button to open the IPython console with a Python logo icon
        self.sheet_button = QtWidgets.QPushButton("Spreadsheet",self)
        self.sheet_button.setIcon(QtGui.QIcon(os.path.join("icons","spreadsheet.png")))
        self.sheet_button.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)  # Allow width to expand
        self.sheet_button.setFixedHeight(H)  # Set fixed height
        self.sheet_button.setIconSize(QtCore.QSize(BW, BH))
        self.sheet_button.clicked.connect(self.add_spreadsheet)


        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.console_button)
        self.toolbar.addWidget(self.sheet_button)
        self.toolbar.adjustSize()

    def add_spreadsheet(self):
        #Add a plot button on top. when clicked, plot the data in the table
        self.plot_button = QtWidgets.QPushButton("Plot",self)
        self.plot_button.clicked.connect(self.plot_data)
        self.toolbar.addWidget(self.plot_button)    
        #create a right dock and add a table to it. 100 rows, 3 columns
        self.spreadsheet_dock = QtWidgets.QDockWidget("Spreadsheet",self)
        self.spreadsheet_dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.spreadsheet_dock)
        self.spreadsheet_widget = QtWidgets.QTableWidget(self)
        self.spreadsheet_widget.setMinimumWidth(200)
        self.spreadsheet_widget.setRowCount(100)
        self.spreadsheet_widget.setColumnCount(2)
        self.spreadsheet_dock.setWidget(self.spreadsheet_widget)


    def plot_data(self):
        #get the data from the table
        data = self.spreadsheet_widget.toPlainText()
        #Plot with pyqtgraph in a popup window
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.plot(data)
        self.plot_dock = QtWidgets.QDockWidget("Plot",self)
        self.plot_dock.setWidget(self.plot_widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.plot_dock)

    def updateExperimentsSubmenuToolbar(self,items):
        self.child_toolbar.show()
        self.child_toolbar.clear()
        for a in items:
            button = QtWidgets.QPushButton(a['title'],self)
            mod = a['module_name']
            if mod == 'separator':
                self.child_toolbar.addSeparator()
                continue

            if mod.startswith('extra:'): # Device configuration
                opt = mod.split(':')[1]
                if opt == 'simulator':
                    button.clicked.connect(self.launchsimulator)
                elif opt == 'simulator_samples':
                    button.clicked.connect(self.launchsimulatorsamples)
                elif opt == 'ProgrammersManual':
                    button.clicked.connect(self.launchProgrammersManual)
                elif opt == 'device_selector':
                    button.clicked.connect(self.selectDevice)

            else:
                if mod.startswith('scope:'): #OldOscilloscope  
                    mod = 'scope'
                elif mod.startswith('oscilloscope:'): #SimpleOscilloscope
                    mod = 'oscilloscope'

                if 'http' in a['helpname']:
                    helpname = a['helpname']
                else:
                    helpname = a['helpname']+':'+a['title']

                button.clicked.connect(partial(self.load_script,mod,a['title'], helpname))

            if ':' in mod:
                opt = mod.split(':')[1]
            else:
                opt = mod
            iconpath = os.path.join(os.path.dirname('__file__'),"icons",opt+".png")
            if os.path.exists(iconpath):
                button.setIcon(QtGui.QIcon(iconpath))  # Set icon
                button.setIconSize(QtCore.QSize(30, 30))

            button.setFixedHeight(45)  # Set fixed height

            self.child_toolbar.addWidget(button)  # Add button to the toolbar

        self.child_toolbar.adjustSize()

    def createWebserver(self):
        if self.help_server is not None:
            return

        port = 8001
        server_address = ('0.0.0.0', port)
        self.sbar.showMessage('Starting help web server',2000)
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        import threading
        #Start the server

        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory='online', **kwargs)

        # Set up the HTTP server

        httpd = HTTPServer(server_address, Handler)

        # Create a thread to run the server
        self.help_server = threading.Thread(target=httpd.serve_forever)
        self.help_server.daemon = True  # Allows the thread to exit when the main program does
        self.help_server.start()            

    def show_help(self):
        import webbrowser
        if('http' in self.help_file):
            webbrowser.open(self.help_file)
            return
        self.createWebserver()

        if self.help_file is None:
            self.sbar.showMessage('No Help Specified',2000)
        else:
            self.sbar.showMessage('Load Help>>  '+self.help_file,2000)
            url = 'helpFiles/en/'+self.help_file.split(':')[0]+'.html'
            webbrowser.open(f"http://localhost:8001/"+url)  # Adjust the URL as needed

    def launchsimulator(self):
        import webbrowser
        self.createWebserver()
        self.sbar.showMessage('Launching Simulator...',2000)
        webbrowser.open(f"http://localhost:8001/site/circuitjs.html")  # Adjust the URL as needed

    def launchsimulatorsamples(self):
        import webbrowser
        self.createWebserver()
        self.sbar.showMessage('View Simulator samples...',2000)
        webbrowser.open(f"http://localhost:8001/site/circuits.html")  # Adjust the URL as needed

    def launchProgrammersManual(self):
        import webbrowser
        self.createWebserver()
        self.sbar.showMessage('Opening Programmers Manual...',2000)
        webbrowser.open(f"https://eyes17lib.readthedocs.io/en/latest/")  # Adjust the URL as needed

    def hideExperimentsSubmenuToolbar(self):
        self.child_toolbar.clear()
        self.child_toolbar.hide()

    def createFileMenu(self):
        self.file_menu = self.menuBar().addMenu("File")
        self.options_menu = self.menuBar().addMenu("Options")

        # Add actions to the File menu
        self.open_action = QtWidgets.QAction("Open Script", self)
        self.open_action.triggered.connect(self.open_script)
        self.file_menu.addAction(self.open_action)

        self.save_action = QtWidgets.QAction("Save Script", self)
        self.save_action.triggered.connect(self.save_script)
        self.file_menu.addAction(self.save_action)

        # Add a checkbox to the File menu
        # Create an 'Expert' checkbox in the dropdown file menu

        self.edit_code_first = QtWidgets.QAction("Edit Code First", self, checkable=True)
        self.edit_code_first.setChecked(False)  # Set initial state
        self.edit_code_first.triggered.connect(self.enableCodeEditing)  # Connect to a method
        self.options_menu.addAction(self.edit_code_first)

    def createThemeMenu(self):
        self.theme_menu = self.menuBar().addMenu("Theme")
        theme_files = [f for f in os.listdir('themes') if f.endswith('.qss')]
        for theme_file in theme_files:
            theme_action = QtWidgets.QAction(theme_file, self)
            theme_action.triggered.connect(partial(self.setTheme,theme_file[:-4]))
            self.theme_menu.addAction(theme_action)
            print(theme_file[:-4])

    def createPipMenu(self):
        self.pip_menu = self.menuBar().addMenu("Install Packages")
        for a in [("PyQt5 GUI",'pyqt5'),('NumPy','numpy'),('SciPy','scipy'),('pyqtgraph','pyqtgraph'),('pyserial','pyserial'),('matplotlib','matplotlib'),('qtconsole','qtconsole'),('webserver','webserver'),('All of these','numpy scipy pyqtgraph pyqt5 pyserial matplotlib qtconsole webserver')]:
            action = QtWidgets.QAction(a[0], self)
            action.triggered.connect(partial(self.showPipInstaller,a[1] ))
            self.pip_menu.addAction(action)

    def showPipInstaller(self, name):
        from .utilities.pipinstaller import PipInstallDialog
        self.pipdialog = PipInstallDialog(name, self)
        self.pipdialog.show()

    def open_script(self):
        """Open a script file and load its content into the editor."""
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Script File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r',encoding='utf-8') as file:
                self.source_code_edit.setPlainText(file.read())

    def save_script(self):
        """Save the current content of the editor to a script file."""
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Script File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w',encoding='utf-8') as file:
                file.write(self.source_code_edit.toPlainText())

    def enableCodeEditing(self,s):
        pass
        #self.run_code_button.setVisible(s)

    def create_experiments_menu(self):
        """Load Python scripts from the current directory."""
        script_dir = os.path.dirname(__file__)
        scripts = [f[:-3] for f in os.listdir(script_dir) if f.endswith('.py') and f not in ['script_runner.py', 'tmp.py', '__main__.py','__init__.py','utils.py','mycode.py','ipy.py']]

        self.script_menu = self.menuBar().addMenu("Launch Apps")
        for a in scripts:
            action = QtWidgets.QAction(a, self)
            action.triggered.connect(partial(self.load_script,a))
            self.script_menu.addAction(action)



    def load_available_baremetal_scripts(self):
        """Load Python scripts from the current directory."""
        script_dir = os.path.join(os.path.dirname(__file__),'examples')
        scripts = [f[:-3] for f in os.listdir(script_dir) if f.endswith('.py') and f not in ['__init__.py']]
        self.simple_script_selector.addItems(scripts)

    def load_script(self, opt, title=None, helpname=None):
        """Load and display the selected script's source code."""
        self.coding_toolbar.hide()
        self.selected_script = opt
        self.help_file = helpname
        if title is None:
            title = opt
        self.setWindowTitle(f"SEELab3/ExpEYES Sample : {title}")

        if opt == 'scope':
            self.setTheme("style")
        else:
            self.setTheme("default")

        script_path = os.path.join(os.path.dirname(__file__), f"{self.selected_script}.py")
        self.setEditMode()


        with open(script_path, 'r',encoding='utf-8') as file:
            source_code = file.read()

        self.central_widget.setCurrentWidget(self.source_code_edit)  # Show the source code editor

        self.source_code_edit.setPlainText(source_code)
        self.source_code_edit.setReadOnly(False)  # Allow editing
        self.highlight = PythonHighlighter(self.source_code_edit.document())  # Syntax highlighting
        if not self.edit_code_first.isChecked() and self.selected_script != 'tmp':
            self.run_code()

    def load_simple_script(self, opt=None):
        with open(os.path.join( os.path.dirname(__file__), 'examples', opt+'.py'), 'r') as file:
            self.text_editor.setText(file.read())

    def execute_simple_script(self):
        source_code = self.text_editor.toPlainText()
        source_code = '\n'.join([line for line in source_code.split('\n') if 'import eyes17' not in line])
        source_code = '\n'.join([line for line in source_code.split('\n') if 'open()' not in line])

        temp_file_path = os.path.join(os.path.dirname(__file__), 'mycode.py')
        with open(temp_file_path, 'w',encoding='utf-8') as temp_file:
            temp_file.write(source_code)  # Save the edited code

        #self.ipyConsole.execute(source_code)
        self.ipyConsole.execute('%run -i mycode.py')


    def run_code(self):
        """Replace the source code editor with the Expt class of the selected script."""
        if self.editMode:
            if self.selected_script:
                self.editMode = False
                # Save the edited source code to a temporary file
                temp_file_path = os.path.join(os.path.dirname(__file__), 'tmp.py')
                with open(temp_file_path, 'w',encoding='utf-8') as temp_file:
                    temp_file.write(self.source_code_edit.toPlainText())  # Save the edited code
                # Remove tmp* from the __pycache__ directory before import
                pycache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')
                for file in os.listdir(pycache_dir):
                    if file.startswith('tmp'):
                        os.remove(os.path.join(pycache_dir, file))
                importlib.invalidate_caches()
                if self.module:
                    self.module = importlib.reload(self.module)
                if __name__ == '__main__':
                    self.module = importlib.import_module('tmp')  # Import the temporary module with explicit import
                else:
                    self.module = importlib.import_module('.tmp',package='seelab_examples')  

                if self.current_script:
                    try:
                        self.current_script.timer.stop()  # Stop the timer loop of current widget
                    except:
                        pass
                    self.current_script.close()  # Close the current script if it's open
                self.current_script = self.module.Expt(self.device)  # Create an instance of the Expt class
                self.central_widget.addWidget(self.current_script)  # Add the new script's window to the central widget
                self.central_widget.setCurrentWidget(self.current_script)  # Show the new script's window

                # Change button to "Edit Code" with edit icon
                self.run_code_button.setText("Edit Code")
                self.run_code_button.setIcon(QtGui.QIcon(os.path.join("icons","edit_icon.png")))  # Set edit icon

        else:
            self.load_script('tmp')
            self.setEditMode()

    def add_ipython_console(self):
        """Create and add an IPython console widget to the main window."""
        from qtconsole.rich_jupyter_widget import RichJupyterWidget
        from qtconsole.inprocess import QtInProcessKernelManager
        self.setTheme("default")

        class myConsole(RichJupyterWidget):
            def __init__(self,customBanner=None):
                """Start a kernel, connect to it, and create a RichJupyterWidget to use it
                """
                super(myConsole, self).__init__()
                if customBanner is not None:
                    self.banner=customBanner
                self.kernel_manager = QtInProcessKernelManager(kernel_name='python3')

                self.kernel_manager.start_kernel()
                self.kernel = self.kernel_manager.kernel

                self.kernel_manager.kernel.gui = 'qt'
                self.font_size = 8

                self.kernel_client = self.kernel_manager.client()
                self.kernel_client.start_channels()

                def stop():
                    self.kernel_client.stop_channels()
                    self.kernel_manager.shutdown_kernel()
                    #guisupport.get_app_qt().exit()

                self.exit_requested.connect(stop)

            def pushVariables(self,variableDict):
                """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
                self.kernel.shell.push(variableDict)
            def clearTerminal(self):
                """ Clears the terminal """
                self._control.clear()    

            def printText(self,text):
                """ Prints some plain text to the console """
                self._append_plain_text(text)

            def executeCommand(self,command,hidden=False):
                """ Execute a command in the frame of the console widget """
                self._execute(command,hidden)


        if self.current_script:
            try:
                self.current_script.timer.stop()  # Stop the timer loop of current widget
            except:
                pass
            self.current_script.close()  # Close the current script if it's open

        self.coding_toolbar.show()

        try:
            #--------instantiate the iPython class-------
            if self.ipyConsole is None:
                self.ipyConsole = myConsole("################ Interactive Console ###########\nAccess hardware using the Instance 'p'.  e.g.  p.get_voltage('A1')\n\n")
                self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
                self.text_editor = ZoomableTextEdit()
                self.text_editor_highlighter = PythonHighlighter(self.text_editor.document())  # Syntax highlighting

                self.splitter.addWidget(self.ipyConsole)
                self.splitter.addWidget(self.text_editor)
                self.splitter.setSizes([4,2])

                self.central_widget.addWidget(self.splitter)
                cmdDict = {}
                #cmdDict = {"analytics":self.analytics}
                if self.device :
                    cmdDict["p"]=self.device
                    import matplotlib.pyplot as plt
                    cmdDict["plt"]=plt
                cmdDict['me'] = self.ipyConsole
                self.ipyConsole.pushVariables(cmdDict)
                self.console_enabled=True
                self.createPythonCodeOptionsMenu()

                # Create a toolbar for script selection
                #self.toolbar = self.addToolBar("Simple Scripts")
                self.simple_script_selector = QtWidgets.QComboBox(self)

                self.coding_toolbar.addWidget(self.simple_script_selector)
                self.load_available_baremetal_scripts()
                self.simple_script_selector.currentTextChanged.connect(self.load_simple_script)

                self.execute_button = QtWidgets.QPushButton()
                self.execute_button.setIcon(QtGui.QIcon(os.path.join("icons","play_icon.png")))
                self.execute_button.clicked.connect(self.execute_simple_script)
                self.coding_toolbar.addWidget(self.execute_button)

            self.central_widget.setCurrentWidget(self.splitter)  # Show the source code editor

        except Exception as e:
            print ("failed to launch iPython. Is it installed?", e)
            self.close()
            
    def createPythonCodeOptionsMenu(self):
        self.theme_menu = self.menuBar().addMenu("Code Options")
        self.theme_menu.setIcon(QtGui.QIcon(os.path.join("icons","python_logo.png")))  # Set Python logo icon

        action = QtWidgets.QAction("Inline Plots", self)
        action.triggered.connect(partial(self.ipyConsole.execute,'%matplotlib inline' ))
        self.theme_menu.addAction(action)

        action = QtWidgets.QAction("Import Numpy", self)
        action.triggered.connect(partial(self.ipyConsole.execute,'import numpy as np' ))
        self.theme_menu.addAction(action)

    def setEditMode(self):
        self.run_code_button.setText("Run Code")
        self.run_code_button.setIcon(QtGui.QIcon(os.path.join("icons","play_icon.png")))  # Set play icon
        self.editMode = True
        if self.current_script:
            self.current_script.close()  # Close the current script if it's open

    ##############################
    def setTheme(self, theme):
        self.setStyleSheet("")
        self.setStyleSheet(open(os.path.join(os.path.dirname(__file__),'themes', theme + ".qss"), "r").read())

def load_experiments(file_path):
    """Load experiments from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


if __name__ == "__main__":
    import argparse
    import os,sys
    # Add the parent directory to sys.path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    __package__ = 'seelab_examples'


    # Load experiments from experiments.json
    experiments_file = os.path.join(os.path.dirname(__file__), 'experiments.json')
    experiments = load_experiments(experiments_file)

    # Create a list of choices for the argument parser
    choices = []
    for category, items in experiments.items():
        for item in items:
            if item['module_name']:  # Ensure module_name is not empty
                choices.append((item['module_name'], item['title']))


    parser = argparse.ArgumentParser(description='Run a specific script from seelab_examples.')
    script_names = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and f not in ['script_runner.py', 'syntax.py', 'syntax2.py', 'tmp.py', '__main__.py','__init__.py','utils.py']]
    parser.add_argument('script', nargs='?', choices=[name for name, title in choices], help='The name of the script to run')


    # Add a custom help message to show the table of names and titles
    parser.add_argument('--list', action='store_true', help='Show available experiments')

    # Parse the arguments
    args = parser.parse_args()

    if args.list:
        print("Available Experiments:")
        print(f"{'Module Name':<30} {'Title'}")
        print("-" * 50)
        for name, title in choices:
            if title:
                print(f"{name:<30} {title}")
        sys.exit()

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    window = ScriptRunner(args)
    window.show()
    sys.exit(app.exec_())


