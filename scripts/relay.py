#!/usr/bin/python

import serial
import sys
import struct

class Monitor:
    def __init__(self):
        self.serialPort = None

    def open(self,portName,baud=9600):
        self.serialPort = serial.Serial(portName, baud, timeout=0.5)
        try:
            self.serialPort.open()
        except serial.SerialException, e:
            sys.stderr.write("Could not open serial port %s: %s\n" % (self.serialPort.portstr, e))
    def close(self):
        self.serialPort.close()

mon = Monitor()
mon.open("/dev/ttyACM0")

if len(sys.argv) > 1:
    if sys.argv[1] == 'on':
        state = 1
    elif sys.argv[1] == 'off':
        state = 0
    else:
        print("bad state, exiting")
        sys.exit(1)
    mon.serialPort.write(struct.pack("BBB",0xA6,1,state))
    rsp = mon.serialPort.read(2)
    ok = len(rsp) == 2 and rsp[0] == '\x00' and rsp[1] == '\x00'
    if not ok:
        print("Did not receive correct response!")
        print("Response: "+",".join(map(lambda x:hex(ord(x)),rsp)))

mon.close()




