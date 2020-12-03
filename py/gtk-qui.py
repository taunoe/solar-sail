#!/usr/bin/env python3

# sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
# sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 
# pip3 install pycairo
# pip3 install PyGObject

# https://stackoverflow.com/questions/31162398/create-a-radio-action-in-a-gtk-popovermenu
# https://stackoverflow.com/questions/31012645/properly-structure-and-highlight-a-gtkpopovermenu-using-pygobject

# Load Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import re
import serial # pip3 install pyserial
import serial.tools.list_ports
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



class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Lämmämõõdusk")
        self.set_default_size(600, 400)
        self.set_position(Gtk.WindowPosition.CENTER)

        # HeaderBar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Lämmämõõdusk"
        self.set_titlebar(hb)

        # Menu icon on HeaderBar
        button_settings = Gtk.MenuButton()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_settings.add(image)
        hb.pack_end(button_settings)

        # Button on window center
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked) # signal clicked calls Method
        self.add(self.button)

        # Open serial port
        port = '/dev/ttyUSB0'
        baudrate = 9600
        open_serial(port, baudrate)
        time.sleep(1.5)

        # create empty figure and draw
        init_figure = create_figure()

    # Method
    def on_button_clicked(self, widget):
        print("Hello World")

if __name__ == "__main__":
    window = MyWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()