import Detector
import ZaberMotor

# Experiment Interface
class Experiment:
    def __init__(self):
        #Detector Initialisation
        # self.detector = Detector.Logic16
        #Output Detector
        self.detector1 = Detector.PowerMeter('PM100D')
        #Split Beam Detector
        self.detector2 = Detector.PowerMeter('PM16')

        #Motor initialisation
        self.motors = ZaberMotor.ZaberMotor()
        self.motors.open_motor_connection()

        #Variable Initialisation
        self.filtering_coefficient = 76e-6

        # print("Starting Motor Coordinates: ", self.motors.get_motor_coordinates)

    def move_to_array(self, solution):
        self.motors.move_to_array(solution)
        
    def get_motor_coordinates(self):
        return self.motors.get_motor_coordinates()

    def evaluate_solution(self, solution):
        return self.detector1.read()
    
    def benchmark(self):
        #Theoretical maximum pairing based off heralded detector split ration + filtering aspect
        p_opt = (1.185/4.640) * self.detector2.read() #* self.filtering_coefficient
        return self.detector1.read()/p_opt

    def close_motor_connection(self):
        self.motors.close_motor_connection()