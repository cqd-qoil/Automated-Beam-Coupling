#Zaber Motion Libraries
import zaber_motion.binary as zmb
import zaber_motion as zm
import time
class ZaberMotor:
    def __init__(self):
        self.device_list = []
        self.open_motor_connection()
        # self.reset_motor_axis(324)

    def open_motor_connection(self):
        # while (len(self.device_list) < 4):
        try:
            self.connection = zmb.Connection.open_serial_port('COM3')
            self.device_list = self.connection.detect_devices()
            if len(self.device_list) < 3:
                time.sleep(1)
                print("Did not find 4 motors. Trying again...")
        except:
            print("Failed motor connection, trying again...")
        finally:
            print("\nConnection open")
            print("Found {} devices\n".format(len(self.device_list)))

    def close_motor_connection(self):
        self.connection.close()
        print("Connection closed")

    def reset_motor_axis(self):
        """
        Notes current coordinates, homes all axis then returns to starting
        Sometimes axis get blocked at half way this resets them
        """
        for i in range(len(self.device_list)):
            device = self.device_list[i]
            device.home()
            device.wait_until_idle()

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
        #return 1 when completed
        return 1
