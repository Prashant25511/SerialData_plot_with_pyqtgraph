from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
import csv


global data_display
# 
app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()

raw=serial.Serial("com3",baudrate=115200,bytesize=8,stopbits=1,timeout=1)
raw.flushInput()
data_display = []

chunk_size=1# smaller chunk size = slower data
def update():
	
	global  data_display
	
	current_data = np.zeros(chunk_size,dtype=int)
	tic = time.perf_counter()
	for i in range(chunk_size):
		
		current_data[i]=raw.readline()
		
	# mean_data = np.mean(current_data)
	# current_data=int(raw.readline()) # this makes it sloww
	# toc = time.perf_counter()
	#print(current_data)


	# print(f"For loop completed in {toc - tic:0.4f} seconds")
	data_display = np.append(data_display, (current_data))

	curve.setData(data_display)
	app.processEvents()
	




timer = QtCore.QTimer()
timer.start() 
timer.timeout.connect(update)



if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()