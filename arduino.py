import serial
import time

class Arduino(object):
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=None)
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
    
    def feed_bricks(self):
        self.ser.write(b'G')
    
    def stop_feed(self):
        self.ser.write(b'T')

    def on(self):
        while True:
            self.activate_dc()
            time.sleep(0.5)
            self.stop_dc()
            time.sleep(1.5)

    def activate_vibration(self):
        print("Vibration motors activating")
        self.ser.write(b'V')
    
    def deactivate_vibration(self):
        print("Vibration motors deactivaitng")
        self.ser.write(b'S')

    def start(self):
        self.activate_dc()
        self.activate_vibration()
    
    def stop(self):
        self.stop_dc()
        self.deactivate_vibration()

    def operate(self):
        self.ser.write(b'W')
        print('dc running')

if __name__ == '__main__':
    port = 'COM7'
    arduino = Arduino(port)
    time.sleep(3)
    # while True:
    while True:
        arduino.operate()
        # arduino.activate_vibration()
    # time.sleep(10)
    # arduino.deactivate_vibration()
    # time.sleep(1)