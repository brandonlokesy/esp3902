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

if __name__ == '__main__':
    port = 'COM5'
    arduino = Arduino(port)
    time.sleep(1)
    # arduino.start()
    while True:
        # arduino.activate_dc()
        # arduino.activate_vibration()
        arduino.start()
        time.sleep(1)
        # arduino.stop_dc()
        # arduino.deactivate_vibration()
        arduino.stop()
        time.sleep(1)