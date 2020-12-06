#!/usr/bin/env python3
'''
https://stackoverflow.com/questions/55680827/how-can-i-integrate-seaborn-plot-into-tkinter-gui
https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
https://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python

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


class SolarSerial():
  def __init__(self):
    print("init")
    self.avaible_ports = ['']
    self.avaible_baudrates = ['300','1200','2400','4800','9600','19200','38400','57600',
                    '74880','115200','230400','250000','500000','1000000','2000000']
    self.baudrate = self.avaible_baudrates[4]
    self.ser = serial.Serial()
    self.find_ports()
    self.port = self.avaible_ports[0]

  def get_port(self):
    return self.port
  
  def get_avaible_ports(self):
    return self.avaible_ports

  def get_baudrate(self):
    return self.baudrate

  def get_avaible_baudrates(self):
    return self.avaible_baudrates

  def find_ports(self):
    self.avaible_ports.clear()
    found_ports = list(serial.tools.list_ports.comports())
    for port in found_ports:
      self.avaible_ports.append(port[0]) # /dev/ttyACM0
    print(self.avaible_ports)

  def find_numbers(self, str):
    """
    Extract all the numbers from the given string.
    Return list.
    """
    numbers = re.findall(r'[-+]?[0-9]*\.?[0-9]+', str) 
    # using map() to 
    # convert str to int
    numbers = list(map(int, numbers)) 
    return numbers

  def open_serial(self, port, baud):
    self.ser.port = port
    self.ser.baudrate = baud
    self.ser.timeout = 3
    self.ser.open()
    print("Open serial: {} {}".format(self.ser.name, self.ser.baudrate))
    print("Serial is open: {}".format(self.ser.is_open))
    time.sleep(1.5)

  def list_to_matrix(self, list):
    matrix = np.array(list)
    new_matrix = np.reshape(matrix, (6, 8))
    new_matrix = np.rot90(new_matrix, 3)
    return new_matrix

  def read_serial(self):
    try:
      self.ser.write(b'a')
      print(self.ser) 
      incoming_data = self.ser.readline()[:-2].decode('ascii')
      numbers = self.find_numbers(incoming_data)
      # If list is empty
      if not numbers:
        print("No data on serial")
        for x in range(48):
          numbers.append(0)
      return numbers
    except:
      print("Error on read_serial()")
'''
class SolarGui(tk.TK):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    tk.Tk.wm_title(self, "Tauno Solar Sailer")
'''

empty_matrix = [[0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0]]

def create_init_figure() -> Figure:
  matrix = empty_matrix
  # plot the data
  figure = Figure(figsize=(6, 8))
  ax = figure.subplots()
  sns.heatmap(matrix, square=True, cbar=True, ax=ax)
  return figure

def create_figure() -> Figure:
  try:
    matrix = app.read_serial()
    matrix = app.list_to_matrix(matrix)
    print(matrix)
    figure = Figure(figsize=(6, 8))
    ax = figure.subplots()
    sns.heatmap(matrix, square=True, cbar=True, ax=ax)
    return figure
  except:
    app.ser.close()
    print("Error on create_figure()!")
  
def redraw_figure(port, baudrate):
  if not app.ser.is_open:
    app.open_serial(port, baudrate)
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




####################################################
#  set up GUI
####################################################
main_window = tk.Tk()
app = SolarSerial()
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
select_ports['values'] = app.get_avaible_ports()
select_ports.insert(0,app.get_port()) # Select first port
select_ports.pack(side=tk.LEFT, expand=False)

#1.2
baud_frame = Frame(menu_frame)
baud_frame.pack(side=tk.LEFT, fill = tk.X, expand=True)
# 1.2.1. Label: Select Baudrate
label_bauds = tk.ttk.Label(baud_frame, text="Baudrate:")
label_bauds.pack(side=tk.LEFT, expand=False)

# 1.2.2. Combobox: Select Baudrate
select_bauds = tk.ttk.Combobox(baud_frame, textvariable='Baudrates')
select_bauds['values'] = app.get_avaible_baudrates()
select_bauds.insert(0, app.get_baudrate())
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