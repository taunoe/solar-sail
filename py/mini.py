#!/usr/bin/env python3

"""
  Tauno Erik
  17.10.2020
  Read and log data to csv file

  Usage: python3 ./read.py /dev/ttyACM0 9600
  baudrates = ['300','1200','2400','4800','9600','19200','38400','57600',
                        '74880','115200','230400','250000','500000','1000000','2000000']

  Links:
  https://docs.python.org/3.9/library/argparse.html#module-argparse
  https://docs.python.org/3.7/howto/argparse.html#id1
  https://www.devdungeon.com/content/python-catch-sigint-ctrl-c
  https://pythonhosted.org/pyserial/shortintro.html
"""

import serial # pip3 install pyserial
import time

# Open serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
time.sleep(1.5) # On vajalik esimesel korral!

ser.write(b'a')
incoming_data = ser.readline()[:-2].decode('ascii') # [:-2] gets rid of the new-line chars
print("{}".format(incoming_data))

time.sleep(0.1)
ser.write(b'a')
incoming_data = ser.readline()[:-2].decode('ascii') # [:-2] gets rid of the new-line chars
print("{}".format(incoming_data))

time.sleep(0.1)
ser.write(b'a')
incoming_data = ser.readline()[:-2].decode('ascii') # [:-2] gets rid of the new-line chars
print("{}".format(incoming_data))
  
ser.close()