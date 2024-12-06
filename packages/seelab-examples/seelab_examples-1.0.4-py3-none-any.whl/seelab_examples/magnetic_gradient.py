import os
import socket
import sys
import time
import webbrowser
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QPixmap, QTransform
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import serial


from .layouts import ui_mag_gradient

class KalmanFilter:
    def __init__(self):
        # Initialize state (position and velocity)
        self.x = np.zeros((2, 1))  # State vector [position, velocity]
        self.P = np.eye(2)          # State covariance matrix
        self.F = np.array([[1, 1],  # State transition matrix
                           [0, 1]])
        self.H = np.array([[1, 0]]) # Measurement matrix
        self.R = np.array([[0.5]])     # Measurement noise covariance
        self.Q = np.eye(2) * 0.5     # Process noise covariance

    def predict(self):
        # Predict the next state
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z):
        # Update the state with the measurement
        y = z - (self.H @ self.x)  # Measurement residual
        S = self.H @ self.P @ self.H.T + self.R  # Residual covariance
        K = self.P @ self.H.T @ np.linalg.inv(S)  # Kalman gain

        # Update state and covariance
        self.x += K @ y
        self.P = (np.eye(2) - K @ self.H) @ self.P

        return self.x[0, 0]  # Return the stabilized position

class Expt(QtWidgets.QWidget, ui_mag_gradient.Ui_Form):
    cameraReadySignal = QtCore.pyqtSignal()
    logThis = QtCore.pyqtSignal(str)
    showStatusSignal = QtCore.pyqtSignal(str, bool)
    serverSignal = QtCore.pyqtSignal(str)

    def __init__(self, device):
        super(Expt, self).__init__()
        self.setupUi(self)
        self.device = device  # Device handler passed to the Expt class.
        self.serverActive = False
        self.external = None
        self.sensormesh = None

        self.dir = 1
        self.ydir = 1
        self.offset=0
        self.looping = True

        self.laser = None
        self.p = None
        self.mag = None
        self.basemag = [0,0,0]
        self.zoomLevel = 1.

        self.mag = None


        # Create the 3D vector field using GLViewWidget
        self.view = gl.GLViewWidget()
        axisitem = gl.GLAxisItem()
        self.view.addItem(axisitem)
        self.viewLayout.addWidget(self.view)


        self.mpLabel.setMinimumHeight(300)
        self.mp_thread = None
        #self.addMP()


        # Display the 3D vector field
        self.pts = 30
        self.scale = 150./self.pts #mm per point.
        self.magscale = 5. # 8mg range should become 1 unit.

        self.baseColor = [0,0,1.,1.]
        self.baseColorButton.setColor([0,0,255], False)

        self.tipColor = [1.,0.2,0.2,1.]
        self.tipColorButton.setColor([255,0,0], False)

        self.create_vector_field()

        self.sensorText = gl.GLTextItem()
        self.sensorText.setData(pos=(-self.pts/2, -self.pts/2, 1), color=(127, 255, 127, 255), text='SENSOR')
        self.view.addItem(self.sensorText)

        self.view.setBackgroundColor(pg.mkColor('#223'))
        self.bgColor = [0.2,0.2,0.2]
        self.bgColorButton.setColor([30,30,30], False)

        self.view.setCameraPosition(distance=self.pts*1.5)
        self.grid = gl.GLGridItem()
        self.grid.scale(2, 2, 1)
        self.view.addItem(self.grid)

        ## Add a cartoon character model to the view
        # Load the 3D model
        # self.addShark()
        self.addSensor()



        self.xpos=0
        self.ypos=0
        self.timer = QTimer()

        self.kf_x = KalmanFilter()  # Kalman filter for xc
        self.kf_y = KalmanFilter()  # Kalman filter for yc
        self.kf_distance = KalmanFilter()  # Kalman filter for distance     
        self.previous_vector_x = 0
        self.previous_vector_y = 0


        self.magtimer = QTimer()
        self.magtimer.timeout.connect(self.updateMag)
        self.magtimer.start(10)
        self.magvec = [0,0,0]


    def addSensor(self):
        ## Array of vertex positions, three per face
        verts = np.empty((36, 3, 3), dtype=np.float32)
        theta = np.linspace(0, 2*np.pi, 37)[:-1]
        verts[:,0] = np.vstack([np.cos(theta), np.sin(theta), [0]*36]).T
        verts[:,1] = np.vstack([2*np.cos(theta+0.2), 2*np.sin(theta+0.2), [-0.5]*36]).T
        verts[:,2] = np.vstack([2*np.cos(theta-0.2), 2*np.sin(theta-0.2), [0.5]*36]).T
            
        ## Colors are specified per-vertex
        colors = np.random.random(size=(verts.shape[0], 3, 4))
        self.sensormesh = gl.GLMeshItem(vertexes=verts, vertexColors=colors, smooth=False, shader='balloon', 
                        drawEdges=True, edgeColor=(1, 1, 0, 1))
        self.sensormesh.translate(-1.2*self.pts/2, -1.2*self.pts/2, 0.3)
        self.view.addItem(self.sensormesh)



    def addShark(self):
        import pywavefront
        shark = scene = pywavefront.Wavefront(os.path.join(os.path.dirname(__file__), 'online/shark.obj'), strict=False, create_materials=True, collect_faces=True)#, cache=True) # Cache is currently not working?!

        # Conversion - Pywavefront to PyQtGraph GLMeshItem
        vertices_array = np.asarray(shark.vertices)
        faces_array = []
        for mesh_lists in shark.mesh_list:
            for faces in mesh_lists.faces:
                faces_array.append(np.array([faces[0],faces[1],faces[2]]))
        faces_array = np.asarray(faces_array)

        # Plotting the data in PyQtGraph
        vehicleMesh = gl.MeshData(vertexes=vertices_array, faces=faces_array)
        self.shark = gl.GLMeshItem(meshdata=vehicleMesh, drawEdges=True, edgeColor=(0,0.2,0,0.8), smooth=True)
        self.shark.scale(0.02,0.02,0.02)
        self.view.addItem(self.shark)

    def start_recording(self):
        self.xpos=0
        self.ypos=0
        self.dir=1
        self.timer.timeout.connect(self.updateEverything)
        self.timer.start(130)
        if self.looping:
            #self.controlsFrame.setEnabled(False)
            self.viewFrame.showFullScreen()

    def stopRecording(self):
        self.timer.disconnect()
        np.save('binarydata.npy', self.vectors)

        hdr = f"Distance Scale:{self.scale}\n"
        hdr += f"Points:{self.pts}\n"

        np.savetxt('txtdata.txt', self.vectormags, fmt='%1.2f', header=hdr)
        self.statusbar.showMessage('Finished', 2000)

    def goHome(self):
        print('homing...')
        self.sensorText.setData(pos=(- self.pts / 2,- self.pts / 2,1))
        self.laser.write(f'G1 X{0} Y{0}\n'.encode('utf-8'))
        self.statusbar.showMessage('homing...',2000)

    def goCenter(self):
        self.laser.write(f'G1 X{self.pts*self.scale/2} Y{self.pts*self.scale/2}\n'.encode('utf-8'))
        self.sensorText.setData(pos=(0,0,1))
        self.statusbar.showMessage('centering...',2000)

    def removeBG(self):
        sum = np.zeros(3)
        avg = 5
        for a in range(avg):
            sum = sum + np.array(self.mag.getRaw())
        self.basemag = sum / avg
        print (self.basemag)

    def setZoom(self,z):
        z /= 20.
        self.zoomLevel = z
        for x in range(self.pts):
            for y in range(self.pts):
                orig = np.array([x - self.pts / 2, y - self.pts / 2, 0])
                vec = self.vectors[x][y]
                start = orig - [vec[0]*z,vec[1]*z,vec[2]*z]
                end = orig + [vec[0]*z,vec[1]*z,vec[2]*z]
                color = np.array([self.baseColor, self.tipColor])

                self.arrows[x][y].setData(pos = [start, end], color = color)



    def clearVectors(self):
        for x in range(self.pts):
            for y in range(self.pts):
                orig = np.array([x - self.pts / 2, y - self.pts / 2, 0])
                color = np.array([self.baseColor, self.tipColor])

                self.arrows[x][y].setData(pos=[orig, orig], color=color)

    def setArrowColor(self,btn):
        self.tipColor = btn.color().getRgbF()
        self.setZoom(self.zoomLevel*20.)

    def setArrowStartColor(self,btn):
        self.baseColor = btn.color().getRgbF()
        self.setZoom(self.zoomLevel*20.)

    def setBGColor(self,btn):
        self.bgColor = btn.color().getRgb()
        self.view.setBackgroundColor(self.bgColor)

    def updateEverything(self):
        m = None
        pos = np.array([self.xpos - self.pts / 2, self.ypos - self.pts / 2, 0])
        #pos = self.arrows[self.xpos][self.ypos].pos
        if self.p is not None:
            sum = np.zeros(3)
            avg = 5
            for a in range(avg):
                sum = sum+ np.array(self.mag.getRaw())
            m = sum/avg
            # interchange x, y. y is ok.
            m = m - np.array(self.basemag) #baseline subtraction. with magnet removed.
            x = m[2]
            y = m[1]  #sensor is mounted incorrectly.
            z = -1*m[0]

            magnitude = np.sqrt(m[0]**2+m[1]**2+m[2]**2)
            start = pos-[x*self.magscale*self.zoomLevel,y*self.magscale*self.zoomLevel,z*self.magscale*self.zoomLevel]
            end = pos+[x*self.magscale*self.zoomLevel,y*self.magscale*self.zoomLevel,z*self.magscale*self.zoomLevel]
        else:  # Dummy
            start = pos
            end = pos+[0,0,self.xpos/5]

        self.arrows[self.xpos][self.pts - self.ypos -1 ].setData(pos = [start,end], color=np.array([self.baseColor, self.tipColor]),width=3)
        self.vectors[self.xpos][self.pts - self.ypos -1 ] = np.array([x*self.magscale, y*self.magscale, z*self.magscale])
        self.vectormags[self.xpos][self.pts - self.ypos -1] = self.xpos/5
        self.xpos+=self.dir
        if self.xpos==self.pts: #Reached one end. reverse
            self.xpos=self.pts-1
            self.dir=-1
            self.incrementY()
        elif self.xpos==-1:
            self.xpos=0
            self.dir=1
            self.incrementY()

        if self.laser is not None: #Go to new position
            cmd = f'G1 X{self.xpos * self.scale} Y{self.ypos * self.scale}\n'.encode('utf-8')
            self.laser.write(cmd)
            self.sensorText.setData(pos=(self.xpos - self.pts / 2, self.ypos - self.pts / 2, 1))
            self.statusbar.showMessage(f"{cmd}, {self.xpos}, {self.ypos}, {m}, {magnitude}",500)
            #print(cmd, self.xpos, self.ypos, m, magnitude)

    def incrementY(self):
        self.ypos += self.ydir
        if self.ypos == -1:# was in reverse
            self.ypos = 0
            self.ydir *= -1
            self.clearVectors()
            return

        elif self.ypos == self.pts:
            if self.looping:
                self.ydir *= -1
                self.ypos = self.pts - 1
                self.clearVectors()
                return

            self.ypos = 0
            self.timer.disconnect()
            np.save('binarydata.npy', self.vectors)

            hdr = f"Distance Scale:{self.scale}\n"
            hdr += f"Points:{self.pts}\n"

            np.savetxt('txtdata.txt', self.vectormags, fmt='%1.2f', header=hdr)
            self.statusbar.showMessage('Finished',2000)
            print('finished')


    def create_vector_field(self):
        # Create a grid of points in 3D space for the vector field
        self.arrows = [[0 for k in range(self.pts)] for j in range(self.pts)] # 2D plane
        self.vectors = np.zeros([self.pts, self.pts, 3])
        self.vectormags = np.zeros([self.pts, self.pts])

        # Create arrows at each grid point
        for i in range(self.pts):
            for j in range(self.pts):
                #pos = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])  # Convert to NumPy array
                pos = np.array([i - self.pts/2, j- self.pts/2, 0])

                # Create a line for the vector (an arrow can be added if needed)
                arrow = gl.GLLinePlotItem(pos=np.array([pos, pos + [0,0,0.1]]), color=np.array([[1, 1, 1, 1],[.5 , 1., 0.2, 1]]), width=2)
                arrow.setGLOptions('translucent')

                self.arrows[i][j] = arrow
                self.view.addItem(arrow)



    def addMP(self):
        try:
            from .online.mp import HandLandmarkThread
        except:
            self.enableMPButton.setVisible(True)
            reply = QtWidgets.QMessageBox.question(self, 'Missing Packages', 'Download additional packages? install mediapipe, python-opencv, and download the hands model.', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.launchPipInstaller()
            return

        self.enableMPButton.setVisible(False)
        self.last_query_time = time.time()
        if self.mp_thread is not None and self.mp_thread.isRunning():  #Available. ignore.
            self.mp_thread.ping()  # nudge
            pass
        else:
            self.mp_thread = HandLandmarkThread()
        self.mp_thread.setPriority(QThread.HighestPriority)
        self.mp_thread.change_pixmap_signal.connect(self.update_image)
        self.mp_thread.coordinates_signal.connect(self.updateCoords)
        self.mp_thread.dead_signal.connect(self.delMP)
        self.cameraReadySignal.connect(self.camReady)
        self.mp_thread.setCameraReadySignal(self.cameraReadySignal)
        self.mp_thread.start()

    def camReady(self):
        print('cam ready')

    def updateMag(self):
        if self.mag is None:
            sensors = self.device.guess_sensor()
            if len(sensors)>0:
                self.mag = sensors[0]
                time.sleep(0.5)
                for a in range(10):
                    self.mag.getRaw()
            else:
                return
            #self.basemag = np.array([-0.37304348,  0.09217391, -0.83391304]) #[-0.42521739  0.26608696 -0.80869565]


        sum = np.zeros(3)
        avg = 5
        for a in range(avg):
            sum = sum+ np.array(self.mag.getRaw())
        self.magvec = sum/avg
        m = self.magvec

        # interchange x, y. y is ok.
        m = m - np.array(self.basemag) #baseline subtraction. with magnet removed.
        x = m[2]
        y = m[1]  #sensor is mounted incorrectly.
        z = -1*m[0]
        magnitude = np.sqrt(m[0]**2+m[1]**2+m[2]**2)


        if magnitude > 0:
            x /= magnitude
            y /= magnitude
            z /= magnitude
            self.sensormesh.resetTransform()

            # Calculate rotation angle (in radians) and axis
            angle = np.arccos(z)  # Angle from the Z-axis
            axis = np.array([-y, x, 0])  # Rotation axis (orthogonal to the vector)

            # Apply rotation to the sensor mesh
            self.sensormesh.resetTransform()
            self.sensormesh.rotate(np.degrees(angle), axis[0], axis[1], axis[2])  # Rotate around the calculated axis

            self.sensormesh.translate(1.05*self.pts/2, 1.05*self.pts/2, 0.3)


    def updateCoords(self, c):
        self.coords = c
        d = self.get_distance(c[4], c[8])
        xc = (c[4][0])
        yc = (c[4][1] - 200)

        # Add kalman filter
        self.kf_x.predict()
        self.kf_y.predict()
        self.kf_distance.predict()
        xc = self.kf_x.update(xc)
        yc = self.kf_y.update(yc)
        d = self.kf_distance.update(d)

        self.coordinateLabel.setText(f'Distance: {d:.2f}, X: {xc:.2f}, Y: {yc:.2f}')
        # Normalize to 0 to self.pts
        xc = int(self.pts * (xc - 200) / 200)
        yc = int(self.pts * yc / 200)

        col = pg.mkColor(50, 255, 50)
        if d < 70:
            col = pg.mkColor(255, 50, 50)

        self.sensorText.setData(pos=( xc - self.pts/2, yc - self.pts/2, 1), text=f'X: {xc:.2f}, Y: {yc:.2f}', color=col)

        ## reset previous arrow
        if self.previous_vector_x>=0 and self.previous_vector_x < self.pts and self.previous_vector_y>=0 and self.previous_vector_y < self.pts:
            pos = np.array([self.previous_vector_x - self.pts/2, self.previous_vector_y- self.pts/2, 0])
            self.arrows[self.previous_vector_x][self.previous_vector_y].setData(pos=np.array([pos, pos + [0,0,0.1]]), color=np.array([[1, 1, 1, 1],[.5 , 1., 0.2, 1]]), width = 2)

        ## Show long arrow at position
        if xc>=0 and xc < self.pts and yc>=0 and yc < self.pts:
            pos = np.array([xc - self.pts/2, yc- self.pts/2, 0])


            m = self.magvec
            # interchange x, y. y is ok.
            m = m - np.array(self.basemag) #baseline subtraction. with magnet removed.
            x = m[2]
            y = m[1]  #sensor is mounted incorrectly.
            z = -1*m[0]
            magnitude = np.sqrt(m[0]**2+m[1]**2+m[2]**2)
            start = pos-[x*self.magscale*self.zoomLevel,y*self.magscale*self.zoomLevel,z*self.magscale*self.zoomLevel]
            end = pos+[x*self.magscale*self.zoomLevel,y*self.magscale*self.zoomLevel,z*self.magscale*self.zoomLevel]


            self.arrows[xc][yc].setData(pos=np.array([start, end]), color=np.array([[1, 0, 1, 1],[.5 , 1., 1, 1]]),width=3)


            self.previous_vector_x = xc
            self.previous_vector_y = yc


    def get_distance(self, c1, c2):
        return np.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

    def update_image(self, qt_image):
        """Update the QLabel with the new frame."""
        pixmap = QPixmap.fromImage(qt_image)
        #mirror the image
        pixmap = pixmap.transformed(QTransform().scale(-1, 1))
        self.mpLabel.setPixmap(pixmap)

    def closeEvent(self, event):
        """Ensure the thread is stopped when the dialog is closed."""
        event.ignore()
        print('closing...')

        if self.mp_thread is not None and self.mp_thread.isRunning:
            print('terminating camera...')
            self.mp_thread.terminate()
            self.mp_thread.wait()
            print('terminated.')
        event.accept()


    def delMP(self):
        print('closing MP window')
        if self.mp_thread is not None:
            self.mp_thread.running = False
        self.mpLabel.setVisible(False)

    def queryMP(self):
        if self.mp_thread is not None:
            self.mp_thread.ping()


    def showStatus(self, msg, error=None):
        self.debug_text_browser.append(f"{msg} {'(Error)' if error else ''}")

    def showPipInstaller(self, name):
        from .utilities.pipinstallerMP import PipInstallDialog
        self.pipdialog = PipInstallDialog(name, self)
        self.pipdialog.show()
        self.pipdialog.closeEvent

    def launchPipInstaller(self):
        self.showPipInstaller("mediapipe opencv-python")  # Replace "Package Name" with actual package name or logic to determine missing packages

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 