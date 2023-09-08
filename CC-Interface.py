#######################################################################################################################
#######################################################################################################################
#Experiment Libraries
#Logic16 Libraries
import sys
import time
import clr

#Adding Logic16 driver to path ensure this is 64bit version and that you have selected allow permissions
sys.path.append('C:\\Users\\lab\\Downloads\\CD V2.35.01\\Applications\\TimeTagExplorer\\Release_2_35_64Bit\\Release')
clr.AddReference('C:\\Users\\lab\\Downloads\\CD V2.35.01\\Applications\\TimeTagExplorer\\Release_2_35_64Bit\\Release\\ttInterface.dll')

#Time Tagging Libraries
from System import Array, Byte, Int64, Int32
from TimeTag import TTInterface, Logic

#Zaber Motion Libraries
import zaber_motion.binary as zmb
import zaber_motion as zm
#######################################################################################################################
#######################################################################################################################
#OptimizationAlgorithm Libraries
from abc import ABC, abstractmethod
#Algorithm Libraries
import random
import math
#######################################################################################################################
#######################################################################################################################
#Database Libraries
#Modelling Libraries 
import matplotlib.pyplot as plt
#######################################################################################################################
#######################################################################################################################

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
        
        self.open_motor_connection()

    def open_motor_connection(self):

        self.devicelist = []

        while (len(self.devicelist) < 4):
            self.connection = zmb.Connection.open_serial_port('COM3')
            self.device_list = self.connection.detect_devices()
            print("\nConnection open\n")
            print("Found {} devices".format(len(self.device_list)))

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
        self.move_to_array(solution)
        # Add your code to evaluate the quality of the alignment, e.g., by measuring the average photon count
        avg_photon_count = self.getAvgPhotonCount(timeInterval, channel)
        return avg_photon_count

# Optimization Algorithm Interface
class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize(self, experiment):
        pass

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, experiment, initial_step_size=200, initial_temperature=1000, cooling_rate=0.95, max_iterations=10000, convergence_threshold=0.001, convergence_lookback=10):
        self.initial_step_size = initial_step_size
        self.step_size = initial_step_size
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.convergence_lookback = convergence_lookback
        self.past_energies = []

    def check_convergence(self):
        if len(self.past_energies) < self.convergence_lookback:
            return False

        recent_energies = self.past_energies[-self.convergence_lookback:]
        min_energy = min(recent_energies)
        max_energy = max(recent_energies)

        return ((max_energy - min_energy)/(max_energy + min_energy)) < self.convergence_threshold
    
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

    def optimize(self, experiment, database):
        current_solution = experiment.get_motor_coordinates()  # Initialize with the current positions of the axes
        current_energy = self.energy(current_solution, experiment)
        
        best_solution = current_solution
        best_energy = current_energy
        
        temperature = self.initial_temperature

        for iteration in range(self.max_iterations):
            neighbor_solution = self.neighbor(current_solution)
            neighbor_energy = self.energy(neighbor_solution, experiment)
            
            #Debugging Code
            print("\n\nIteration num: ", iteration)
            print("Temperature: ", temperature)
            print("Step Size: ", self.step_size)
            print("Current Solution: ", current_solution)
            print("Current Energy: ", current_energy)
            print("Neighbour Solution: ", neighbor_solution)
            print("Neighbour Energy: ", neighbor_energy)

            
            if self.acceptance_probability(current_energy, neighbor_energy, temperature) > random.random():
                current_solution = neighbor_solution
                current_energy = neighbor_energy

                if current_energy > best_energy:
                    best_energy = current_energy
                    best_solution = current_solution

            #Move from 'neighbour' to current solution  
            experiment.move_to_array(current_solution)
            self.past_energies.append(current_energy)
            database.addData(temperature, current_energy, current_solution)
            
            if self.check_convergence():
                print("\nConvergence criteria met. Stopping optimization.")
                break
            # Update step size as a function of the temperature.
            # This line reduces the step size linearly with decreasing temperature.
            self.step_size = self.initial_step_size * (temperature / self.initial_temperature)
            temperature *= self.cooling_rate
        
        print("Optimal solution found with average photon count:", best_energy)
        return best_solution, database

class Database:
    """
    Class for tracking data through experiment and modelling when completed
    """
    def __init__(self):
        self.templist = []
        self.energylist = []
        self.solutions = []

    def addData(self, temp, energy, solution):
        self.addtemp(temp)
        self.addenergy(energy)
        self.addsolution(solution)

    def addtemp(self, temp):
        self.templist.append(temp)
    def addenergy(self, energy):
        self.energylist.append(energy)
    def addsolution(self, solution):
        self.solutions.append(solution)

    def modelCountVsAxis(self):
        """
        Models Photon count vs Solution steps 

        Takes no inputs
        """

        #get each axis steps list 
        x1_steps = []
        y1_steps = []
        x2_steps = []
        y2_steps = []

        for i in self.solutions:
            # extract data from solutions list
            x1_steps.append(self.solutions[i][0])
            y1_steps.append(self.solutions[i][1])
            x2_steps.append(self.solutions[i][2])
            y2_steps.append(self.solutions[i][3])


        # create subplots
        fig, axs = plt.subplots(2, 2)

        # scatter plot x0 against p0
        axs[0, 0].scatter(x1_steps, self.energylist, color='black')
        axs[0, 0].set_title('x1 vs p0')

        # scatter plot x0 against p1
        axs[0, 1].scatter(y1_steps, self.energylist, color='black')
        axs[0, 1].set_title('y1 vs p0')

        # scatter plot x1 against p0
        axs[1, 0].scatter(x2_steps, self.energylist, color='black')
        axs[1, 0].set_title('x2 vs p0')

        # scatter plot x1 against p1
        axs[1, 1].scatter(y2_steps, self.energylist, color='black')
        axs[1, 1].set_title('y1 vs p0')

        # adjust spacing between subplots
        plt.subplots_adjust(wspace=0.3, hspace=0.5)

        # add caption to the figure
        fig.text(0.5, 0.01, 'Subplots representing each axis coordinate vs Normalised Photon Counts (#).', ha='center')

        # display the plot
        plt.show()
    
    def modelCountVsTime(self):      
        """
        Models Photon count achieved vs iteration 

        Takes no inputs
        """       
        #Plot for energy (coupling) vs solution coordinates
        fig, ax = plt.subplots()
        time = range(len(self.energylist))
        ax.plot(self.energylist, time, color='black')

        best_coupling = self.energylist.max()  # Corrected line
        best_coupling_str = str(round(best_coupling, 4))

        ax.set_title('Coupling achieved using optimization algorithm vs Solution Coordinates (steps)')
        ax.set_xlabel('Time [Iteration #]')
        ax.set_ylabel('Normalised Photon Counts [#]')
        caption = '\n\n\n\nConvergence is achieved at a coupling of ' + best_coupling_str + ' counts.'
        ax.text(0.5, -0.1, caption, ha='center', va='center', transform=ax.transAxes)

        # Show the plot
        plt.show()

# Main Controller
class Controller:
    def __init__(self, experiment, algorithm):
        self.experiment = experiment
        self.algorithm = algorithm
        self.database = Database()
    
    def run(self, experiment):
        optimal_solution = self.algorithm.optimize(self.experiment, self.database)
        # Use the optimal solution, e.g., align mirrors accordingly
        print("Optimal solution found:", optimal_solution)
        experiment.close_motor_connection()

    def model(self):
        self.database.modelCountVsTime()
        self.database.modelCountVsAxis()


# Example Usage
# experiment = Experiment()
# timeInterval = 0.5
# print("Energy: ", experiment.run_logic_reading(timeInterval))
# print("Solution: ",experiment.get_motor_coordinates())


# # Initialize experiment and algorithm
experiment = Experiment()
simulated_annealing_algorithm = SimulatedAnnealing(experiment)

# Create controller and run optimization
controller = Controller(experiment, simulated_annealing_algorithm)
controller.run(experiment)
controller.model()
