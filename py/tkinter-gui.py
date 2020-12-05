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
#from PIL import Image, ImageTK
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

empty_matrix = [[0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0]]


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

def create_serial():
  global ser
  ser = serial.Serial()
  # print(ser)

def open_serial(port, baud):
  ser.port = port
  ser.baudrate = baud
  ser.timeout = 3
  ser.open()
  print("Serial is open: {}".format(ser.is_open))
  time.sleep(1.5)

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
  try:
    # Send command to Arduino
    ser.write(b'a')
    incoming_data = ser.readline()[:-2].decode('ascii')
    numbers = find_numbers(incoming_data)
    # If list is empty
    if not numbers:
      print("No data on serial")
      for x in range(48):
        numbers.append(0)
    return numbers
  except:
    print("Error on read_serial()")

def create_init_figure() -> Figure:
  matrix = empty_matrix
  # plot the data
  figure = Figure(figsize=(6, 8))
  ax = figure.subplots()
  sns.heatmap(matrix, square=True, cbar=True, ax=ax)
  return figure

def create_figure() -> Figure:
  try:
    matrix = read_serial()
    matrix = list_to_matrix(matrix)
    print(matrix)
    figure = Figure(figsize=(6, 8))
    ax = figure.subplots()
    sns.heatmap(matrix, square=True, cbar=True, ax=ax)
    return figure
  except:
    ser.close()
    print("Error on create_figure()!")
  
  
def redraw_figure(port, baudrate):
  if not ser.is_open:
    open_serial(port, baudrate)
  try:
    figure = create_figure()
    graph.figure = figure
    graph.draw()
  except:
    print("Error on redraw_figure()!")


def btn_connect_cmd():
  port = select_ports.get()
  baudrate = select_bauds.get()
  print("Selected Port: {}, baudrate: {}".format(port, baudrate))
  redraw_figure(port, baudrate)


# Global variables
avaible_ports = find_ports() # find avaible ports
avaible_baudrates = ['300','1200','2400','4800','9600','19200','38400','57600',
                    '74880','115200','230400','250000','500000','1000000','2000000']
baudrate = avaible_baudrates[4]
#port = '/dev/ttyUSB0'


create_serial() # create now and open later


####################################################
#  set up GUI
####################################################

main_window = tk.Tk()
main_window.title("Tauno Solar Sailer")
main_window.bind('q', 'exit')
main_window.geometry("650x850")

# Style
style = tk.ttk.Style()
#print(style.theme_names())
style.theme_use('clam')

# 1.
menu_frame = Frame(main_window)
menu_frame.pack(side=tk.TOP, fill = tk.X, expand=False)

#1.1
port_frame = Frame(menu_frame)
port_frame.pack(side=tk.LEFT, fill = tk.X, expand=True)
# 1.1.1. Label: Select Port
label_ports = tk.ttk.Label(port_frame, text="Port:")
label_ports.pack(side=tk.LEFT, expand=False)

# 1.1.2. Combobox: Select Port
select_ports = tk.ttk.Combobox(port_frame, textvariable='Ports')
select_ports.insert(0,avaible_ports[0]) # Select first port
select_ports['values'] = avaible_ports
select_ports.pack(side=tk.LEFT, expand=False)

#1.2
baud_frame = Frame(menu_frame)
baud_frame.pack(side=tk.LEFT, fill = tk.X, expand=True)
# 1.2.1. Label: Select Baudrate
label_bauds = tk.ttk.Label(baud_frame, text="Baudrate:")
label_bauds.pack(side=tk.LEFT, expand=False)

# 1.2.2. Combobox: Select Baudrate
select_bauds = tk.ttk.Combobox(baud_frame, textvariable='Baudrates')
select_bauds['values'] = avaible_baudrates
select_bauds.insert(0, baudrate)
select_bauds.pack(side=tk.LEFT, expand=False)

# 1.3. Button
btn_txt = tk.StringVar()
button_connect = tk.ttk.Button(menu_frame, textvariable=btn_txt, command=btn_connect_cmd)
btn_txt.set("Load Data")
button_connect.pack(side=tk.LEFT, expand=True)

# 2.
graph_frame = Frame(main_window)
graph_frame.pack(fill = tk.BOTH, expand=True)

# 2.1. Graph
init_figure = create_init_figure()
graph = FigureCanvasTkAgg(init_figure, master=graph_frame)
graph.draw()
graph.get_tk_widget().pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

main_window.mainloop()