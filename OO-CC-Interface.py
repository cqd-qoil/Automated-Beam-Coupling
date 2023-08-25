from abc import ABC, abstractmethod

#Logic16 Libraries
import sys
import time
import clr

# Simulated Annealing Implementation
import random
import math

sys.path.append('C:\\Users\\lab\\Downloads\\CD V2.35.01\\Applications\\TimeTagExplorer\\Release_2_35_64Bit\\Release')
clr.AddReference('C:\\Users\\lab\\Downloads\\CD V2.35.01\\Applications\\TimeTagExplorer\\Release_2_35_64Bit\\Release\\ttInterface.dll')

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
        self.clearBuffer()
        
        #self.open_motor_connection()

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
        delta_t_text = "\n Delta-T [s] = %.4f, " %(delta_t)
        counter_text = "\n Ch%d Counts per %.2f [S] Interval = %d," %(k,timeInterval,counts)
        freq_text = "\n Normalised Counts per S = %.2f, " %(counts/delta_t)
        print(delta_t_text +counter_text + freq_text)

    def getAvgPhotonCount(self, timeInterval, channel):
        counts_list = []
        num_counts = 10
        for i in range(1, num_counts):
            self.clearBuffer()
            counts, delta_t = self.readCounts(timeInterval, channel)
            counts_list.append(counts / delta_t)
        counts_avg = sum(counts_list) / len(counts_list)
        return counts_avg, delta_t
    
    def run_logic_reading(self, timeInterval):
        self.clearBuffer()
        counts, delta_t = self.getAvgPhotonCount(timeInterval, self.test_channel)
        self.printData(counts, delta_t, self.test_channel)

    def evaluate_solution(self, solution):
        timeInterval = 0.5
        channel = self.test_channel
        # Move to the solution's coordinates
        #self.move_to_array(solution)
        # Add your code to evaluate the quality of the alignment, e.g., by measuring the average photon count
        avg_photon_count = self.getAvgPhotonCount(timeInterval, channel)
        return avg_photon_count

# Optimization Algorithm Interface
class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize(self, experiment):
        pass

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, step_size=1, initial_temperature=1000, cooling_rate=0.95, max_iterations=10000):
        self.step_size = step_size
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations

    def energy(self, solution, experiment):
        avg_photon_count, _ = experiment.evaluate_solution(solution)
        return avg_photon_count

    def neighbor(self, solution):
        # Generate a neighboring solution by adjusting each axis by a small random step
        new_solution = [axis + random.uniform(-self.step_size, self.step_size) for axis in solution]
        return new_solution

    def acceptance_probability(self, energy_old, energy_new, temperature):
        if energy_new > energy_old:
            return 1.0
        return math.exp((energy_new - energy_old) / temperature)

    def optimize(self, experiment):
        current_solution = experiment.get_motor_coordinates()  # Initialize with the current positions of the axes
        current_energy = self.energy(current_solution, experiment)
        
        best_solution = current_solution
        best_energy = current_energy
        
        temperature = self.initial_temperature

        for iteration in range(self.max_iterations):
            neighbor_solution = self.neighbor(current_solution)
            neighbor_energy = self.energy(neighbor_solution, experiment)

            if self.acceptance_probability(current_energy, neighbor_energy, temperature) > random.random():
                current_solution = neighbor_solution
                current_energy = neighbor_energy

                if current_energy > best_energy:
                    best_energy = current_energy
                    best_solution = current_solution

            temperature *= self.cooling_rate
        
        print("Optimal solution found with average photon count:", best_energy)
        return best_solution

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
for i in range(4):
    experiment.run_logic_reading(timeInterval)
