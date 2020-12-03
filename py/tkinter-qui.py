#!/usr/bin/env python3
'''
https://stackoverflow.com/questions/55680827/how-can-i-integrate-seaborn-plot-into-tkinter-gui
'''

import argparse
import os
from os import path
import re
import serial # pip3 install pyserial
import serial.tools.list_ports
import sys
import tkinter as tk
from tkinter.ttk import *
import numpy as np
import seaborn as sns
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def find_numbers(str):
  """
    Extract all the numbers from the given string.
    Return list.
  """
  numbers = re.findall(r'[-+]?[0-9]*\.?[0-9]+', str)
  # https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
  # using map() to 
  # convert str to int
  numbers = list(map(int, numbers)) 
  return numbers


def find_ports():
  """
    Return list a avaible ports.
  """
  avaible_ports = []
  ports = list(serial.tools.list_ports.comports())
  for port in ports:
    avaible_ports.append(port[0]) # /dev/ttyACM0
  return avaible_ports


def open_serial(port, baud):
  global ser
  ser = serial.Serial(port, baud, timeout=3)
  #print("Serial is open: {}".format(ser.isOpen()))

def list_to_matrix(list):
  # https://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python
  matrix = np.array(list)
  new_matrix = np.reshape(matrix, (6, 8))
  new_matrix = np.rot90(new_matrix, 3)
  return new_matrix

def read_serial():
  """
    Read Serial port.
    Return matrix
  """
  # Send command to Arduino
  ser.write(b'a')
  incoming_data = ser.readline()[:-2].decode('ascii')
  numbers = find_numbers(incoming_data)
  return numbers

def create_init_figure() -> Figure:
  matrix = [[0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0]]

  # plot the data
  figure = Figure(figsize=(6, 8))
  ax = figure.subplots()
  sns.heatmap(matrix, square=True, cbar=True, ax=ax)
  return figure

def create_figure() -> Figure:
  # generate some data
  matrix = read_serial()
  matrix = list_to_matrix(matrix)
  print(matrix)
  # plot the data
  figure = Figure(figsize=(6, 8))
  ax = figure.subplots()
  sns.heatmap(matrix, square=True, cbar=True, ax=ax)
  return figure
  
def redraw_figure():
    figure = create_figure()
    canvas.figure = figure
    canvas.draw()

def idle(parent,canvas):
  """
  Update canvas.
  """
  data = str(read_serial())
  canvas.itemconfigure("text",text="+"+data+"°C")

  canvas.update()
  parent.after_idle(idle,parent,canvas)

'''
# Check command line arguments
if (len(sys.argv) != 3):
   print("command line: gui.py port baudrate") #/dev/ttyUSB0 4800
   sys.exit()
port = sys.argv[1]
baudrate = int(sys.argv[2])

# kas port on olemas????
if not path.exists(port):
  print("{} not avaible. Try the ones below:". format(port))
  print(find_ports())
  exit(0)

print("Port: {}".format(port))
print("Baudrate: {}".format(baudrate))
'''
# Open serial port
port = '/dev/ttyUSB0'
baudrate = 9600
open_serial(port, baudrate)
avaible_ports = find_ports() # find avaible ports
avaible_baudrates = ['300','1200','2400','4800','9600','19200','38400','57600',
                    '74880','115200','230400','250000','500000','1000000','2000000']
default_baudrate = avaible_baudrates[4]

####################################################
#  set up GUI
#################################################### 
#WINDOW = 200 # window size
main_window = tk.Tk()
main_window.title("Tauno Solar Sailer")
main_window.bind('q', 'exit')

#time.sleep(1.5) # On vajalik esimesel korral!

# Select Port
label_ports = tk.Label(main_window, text="Port:", width=10, padx=5, pady=5)
#label_ports.pack()
label_ports.grid(row=0, column=0)

select_ports = tk.ttk.Combobox(textvariable='Ports', width=15)
select_ports.insert(0,avaible_ports[0]) # Select first port
select_ports['values'] = avaible_ports
#select_ports.pack()
select_ports.grid(row=0, column=1)

# Select Badrate
label_bauds = tk.Label(main_window, text="Baudrate:", width=15, padx=5, pady=5)
label_bauds.grid(row=0, column=2)
select_bauds = tk.ttk.Combobox(textvariable='Baudrates', width=15)
select_bauds['values'] = avaible_baudrates
select_bauds.insert(0, default_baudrate)
select_bauds.grid(row=0, column=3)

# Live Checkbutton
check_live = tk.Checkbutton(main_window, text="Stay live",  onvalue="Live", offvalue="Offline", width=15)
check_live.grid(row=0, column=4) # command=pass,

# Button
button_connect = tk.Button(text="Load Data", command=redraw_figure, width=15, padx=5, pady=5)
#button_connect.pack()
button_connect.grid(row=0, column=5)

# create empty figure and draw
init_figure = create_init_figure()

canvas = FigureCanvasTkAgg(init_figure, master=main_window)
canvas.draw()
#canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=6)

#canvas = tk.Canvas(window, width=2*WINDOW, height=WINDOW, background='white')
#canvas.create_text(WINDOW,.5*WINDOW,text="0°C",font=("Ubuntu", 36),tags="text",fill="#525252")
#canvas.pack()

# Loop
#main_window.after(100,idle,main_window,canvas)
main_window.mainloop()