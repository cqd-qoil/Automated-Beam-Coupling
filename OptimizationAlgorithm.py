#######################################################################################################################
#######################################################################################################################
#OptimizationAlgorithm Libraries
from abc import ABC, abstractmethod
#Algorithm Libraries
import random
import math
#######################################################################################################################
#######################################################################################################################

# Optimization Algorithm Interface
class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize(self, experiment):
        pass

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, experiment, initial_step_size=200, initial_temperature=1000, cooling_rate=0.95, max_iterations=10000, convergence_threshold=0.001, convergence_lookback=25):
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
            self.step_size = self.initial_step_size * ((2 * temperature) / self.initial_temperature)
            temperature *= self.cooling_rate
        
        print("Optimal solution found with average photon count:", best_energy)
        return best_solution, database
