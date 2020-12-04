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
  # Send command to Arduino
  ser.write(b'a')
  incoming_data = ser.readline()[:-2].decode('ascii')
  
  if type(incoming_data) == str:
    numbers = find_numbers(incoming_data)
    return numbers
  return 0

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
  matrix = read_serial()
  if type(matrix) != list:
    print("Bad data")
  matrix = list_to_matrix(matrix)
  # print(matrix)
  figure = Figure(figsize=(6, 8))
  ax = figure.subplots()
  sns.heatmap(matrix, square=True, cbar=True, ax=ax)
  return figure
  
def redraw_figure(port, baudrate):
  # if live mode
  if check_live.instate(['disabled','selected']):
    if not ser.is_open:
      open_serial(port, baudrate)
    figure = create_figure()
    canvas.figure = figure
    canvas.draw()
    #main_window.after(200,redraw_figure(port, baudrate))
  
  #main_window.after(100, redraw_figure(port, baudrate))

def btn_connect_cmd():
  port = select_ports.get()
  print(port)
  baudrate = select_bauds.get()
  print(baudrate)
  live = check_live.state()
  check_live.state(['disabled'])
  #check_live.instate(['selected'])  # returns True if the box is checked
  print(live)

  redraw_figure(port, baudrate)

def idle(parent,canvas):
  print("idle")
  if check_live.instate(['disabled','selected']):
    redraw_figure(port, baudrate)
    canvas.update()
    parent.after_idle(idle,parent,canvas)

# Global variables

avaible_ports = find_ports() # find avaible ports
avaible_baudrates = ['300','1200','2400','4800','9600','19200','38400','57600',
                    '74880','115200','230400','250000','500000','1000000','2000000']
baudrate = avaible_baudrates[4]
port = '/dev/ttyUSB0'

create_serial()


####################################################
#  set up GUI
####################################################

main_window = tk.Tk()
main_window.title("Tauno Solar Sailer")
main_window.bind('q', 'exit')

style = tk.ttk.Style()
#print(style.theme_names())
style.theme_use('clam')


#style.configure("TButton", padding=6, relief="flat", background="#ccc")
#style.configure("TLabel", padding=6, foreground="black", background="white")

# Select Port
label_ports = tk.ttk.Label(main_window, text="Port:", width=10)
label_ports.grid(row=0, column=0)

select_ports = tk.ttk.Combobox(textvariable='Ports', width=15)
select_ports.insert(0,avaible_ports[0]) # Select first port
select_ports['values'] = avaible_ports
select_ports.grid(row=0, column=1)

# Select Badrate
label_bauds = tk.ttk.Label(main_window, text="Baudrate:", width=15)
label_bauds.grid(row=0, column=2)
select_bauds = tk.ttk.Combobox(textvariable='Baudrates', width=15)
select_bauds['values'] = avaible_baudrates
select_bauds.insert(0, baudrate)
select_bauds.grid(row=0, column=3)

# Live Checkbutton
check_live = tk.ttk.Checkbutton(main_window, text="Stay live", width=15)
check_live.state(['!selected'])
check_live.grid(row=0, column=4)

# Button
button_connect = tk.ttk.Button(text="Load Data", command=btn_connect_cmd, width=15)
button_connect.grid(row=0, column=5)

# create empty figure and draw
init_figure = create_init_figure()
canvas = FigureCanvasTkAgg(init_figure, master=main_window)

canvas.draw()
#canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=6)

# Loop
#main_window.after(0,redraw_figure(port, baudrate))
main_window.mainloop()