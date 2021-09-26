import serial
import time

class Arduino(object):
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=None)
        self.is_open = self.ser.isOpen()
        if self.is_open:
            print('arduino: %s open' % self.ser.name)
        else:
            print('Failed to open arduino serial port')
    
    def activate_dc(self):
        print("Motor moving forward")
        self.ser.write(b'F')
    
    def stop_dc(self):
        print("Motor stopping")
        self.ser.write(b'Q')