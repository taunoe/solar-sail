#!/usr/bin/env python3
"""
Copyright 2020 Tauno Erik
"""
import argparse
import serial # pip3 install pyserial
import sys
import time
from pynput.keyboard import Listener, Key

def open_serial(port, baud):
  global ser
  ser = serial.Serial(port, baud, timeout=3)
  #print("Serial is open: {}".format(ser.isOpen()))

def read_serial():
  # Send command to Arduino
  ser.write(b'a')
  incoming_data = ser.readline()[:-2].decode('ascii') # [:-2] gets rid of the new-line chars
  print("{}".format(incoming_data))

def on_press(key):
  if key == Key.space:
    read_serial()
    
def main(argv):
  # commandline argument parser
  parser = argparse.ArgumentParser()

  # Required arguments
  parser.add_argument("port", help="Serial port to open.")  
  parser.add_argument("baudrate", type=int, help="Baudrate speed.")

  # Optional arguments
  parser.add_argument("-l","--log", help="Log data to file", action="store_true")

  args = parser.parse_args()

  print("Open Port: {}, Baudrate: {}".format(args.port, args.baudrate))
  print("Press [space] to read data. And CTRL+c to close program.")

  open_serial(args.port, args.baudrate)



if __name__ == '__main__':
  try:
    main(sys.argv)
    with Listener(on_press=on_press) as listener:  # Setup the listener
      listener.join()  # Join the thread to the main thread
  except KeyboardInterrupt:
    # Exit when CTRL-C pressed
    print(' Goodbye!')
    ser.close()
    exit(0)