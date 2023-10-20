#Zaber Motion Libraries
import zaber_motion.binary as zmb
import zaber_motion as zm

class ZaberMotor:
    def __init__(self):
        self.open_motor_connection()
        
    def open_motor_connection(self):
        self.device_list = []

        while (len(self.device_list) < 4):
            self.connection = zmb.Connection.open_serial_port('COM3')
            self.device_list = self.connection.detect_devices()
            print("\nConnection open")
            print("Found {} devices\n".format(len(self.device_list)))

    def close_motor_connection(self):
        self.connection.close()
        print("Connection closed")

    def get_motor_coordinates(self):
        current_coords = []
        for device in range(len(self.device_list)):
            device = self.device_list[device]
            current_coords.extend([device.get_position()]) 
        return current_coords

    def move_to_array(self, array):
        for i in range(len(self.device_list)):
            device = self.device_list[i]
            device.move_absolute(array[i], zm.Units.NATIVE)
            device.wait_until_idle()