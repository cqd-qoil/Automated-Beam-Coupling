from abc import ABC, abstractmethod

#Logic16 Libraries
import sys
import time
import clr
from System import Array, Byte, Int64, Int32
from TimeTag import TTInterface, Logic

#Zaber Motion Libraries
import zaber_motion.binary as zmb
import zaber_motion as zm

# Experiment Interface
class Experiment:
    def __init__(self):

        # Initialization code, including opening the tagger
        self.MyTagger = TTInterface()
        self.MyTagger.Open()

        # Configure the channel for measurement
        self.test_channel = 2
        self.MyTagger.SetInputThreshold(self.test_channel, 0.5)

        # Activate the Logic Mode
        self.MyLogic = Logic(self.MyTagger)
        self.MyLogic.SwitchLogicMode()
        self.TimerCounter1 = Int32
        self.MyLogic.ReadLogic()

        self.open_motor_connection()

    def open_motor_connection(self):
        global connection
        global device_list
        self.connection = zmb.Connection.open_serial_port('COM3')
        self.device_list = self.connection.detect_devices()
        print("Connection open")
        print("Found {} devices".format(len(device_list)))

    def close_motor_connection(self):
        self.connection.close()
        print("Connection closed")

    def get_motor_coordinates(self):
        current_coords = []
        for device in range(0, 4):
            device = self.device_list[device]
            current_coords.extend([device.get_position()]) 
        return current_coords

    def move_to_array(self, array):
        for i in range(len(device_list)):
            device = device_list[i]
            device.move_absolute(array[i], zm.Units.NATIVE)
            device.wait_until_idle()

    def clearBuffer(self):
        self.MyLogic.ReadLogic()
        TimeCounter1 = self.MyLogic.GetTimeCounter()

    def readCounts(self, timeInterval, channel):
        time.sleep(timeInterval)
        self.MyLogic.ReadLogic()
        TimeCounter1 = self.MyLogic.GetTimeCounter()
        counts=self.MyLogic.CalcCountPos(2**(channel-1))
        delta_t=(TimeCounter1)*5e-9
        return counts, delta_t

    def printData(self, counts, delta_t, k):
        delta_t_text = "Delta-T [s] = %.4f, " %(delta_t)
        counter_text = " Ch%d Events = %d," %(k,counts)
        freq_text = " Freq [Hz] = %.2f, " %(counts/delta_t)
        print(delta_t_text +counter_text + freq_text)

    def getAvgPhotonCount(self, timeInterval, channel):
        counts_list = []
        for i in range(1, 20):
            self.clearBuffer()
            counts, delta_t = self.readCounts(timeInterval, channel)
            counts_list.append(counts / delta_t)
        counts_avg = sum(counts_list) / len(counts_list)
        return counts_avg
    
    def run_logic_reading(self, timeInterval, channel):
        self.clearBuffer()
        counts, delta_t = self.readCounts(timeInterval, channel)
        self.printData(counts, delta_t, channel)

    def evaluate_solution(self, solution):
        timeInterval = 0.5
        channel = self.test_channel
        # Move to the solution's coordinates
        self.move_to_array(solution)
        # Add your code to evaluate the quality of the alignment, e.g., by measuring the average photon count
        avg_photon_count = self.getAvgPhotonCount(timeInterval, channel)
        return avg_photon_count

# Optimization Algorithm Interface
class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize(self, experiment):
        pass

# Genetic Algorithm Implementation
class GeneticAlgorithm(OptimizationAlgorithm):
    def optimize(self, experiment):
        # Implement GA here
        pass

# Simulated Annealing Implementation
class SimulatedAnnealing(OptimizationAlgorithm):
    def optimize(self, experiment):
        # Implement SA here
        pass

# Main Controller
class Controller:
    def __init__(self, experiment, algorithm):
        self.experiment = experiment
        self.algorithm = algorithm
    
    def run(self):
        optimal_solution = self.algorithm.optimize(self.experiment)
        # Use the optimal solution, e.g., align mirrors accordingly
        print("Optimal solution found:", optimal_solution)

# Example Usage
experiment = Experiment()
timeInterval = 0.5
channel = 2
experiment.run_logic_reading(timeInterval, channel)
