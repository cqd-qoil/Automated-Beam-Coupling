#######################################################################################################################
#######################################################################################################################
#OptimizationAlgorithm Libraries
from abc import ABC, abstractmethod
#Algorithm Libraries
import random
import math
#######################################################################################################################
#######################################################################################################################
from scipy.optimize import basinhopping
import random
import math


# Optimization Algorithm Interface
class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize(self, experiment):
        pass

class BasinHopping(OptimizationAlgorithm):
    def __init__(self, experiment):
        self.experiment = experiment
        self.solution = self.x0()

    def objective(self):
        #Objective Function for Optimization
        avg_photon_count, _ = self.experiment.evaluate_solution(self.solution)
        return -1 * avg_photon_count
    
    def x0(self):
        return self.experiment.get_motor_coordinates()
    
    def take_step(self):
        new_solution = [axis + random.uniform(-self.initial_step_size, self.initial_step_size) for axis in self.solution]
        self.experiment.move_to_array(new_solution)
        self.solution = new_solution
        return new_solution

    def callback(self):
        #Append List here
        pass

    def optimize(self):
        return basinhopping(func=lambda: self.objective(), x0=lambda: self.x0(), niter=1000, T=1, stepsize=20,
                            minimizer_kwargs=None, interval=50, disp=True, niter_success=20, seed=None,
                            target_accept_rate=0.5, stepwise_factor=0.9)
        

class SciPySimAnneal(OptimizationAlgorithm):
    def __init__(self, initial_step_size=150, max_iterations=10000, initial_temperature=1000, convergence_threshold=0.001, convergence_lookback=25):
        self.initial_step_size = initial_step_size
        self.max_iterations = max_iterations
        self.initial_temperature = initial_temperature
        self.convergence_threshold = convergence_threshold
        self.convergence_lookback = convergence_lookback
        self.past_energies = []

    def check_convergence(self):
        if len(self.past_energies) < self.convergence_lookback:
            return False

        recent_energies = self.past_energies[-self.convergence_lookback:]
        min_energy = min(recent_energies)
        max_energy = max(recent_energies)

        return ((max_energy - min_energy) / (max_energy + min_energy)) < self.convergence_threshold

    def energy(self, solution, experiment):
        experiment.move_to_array(solution)  # Move the motors to the new solution coordinates
        avg_photon_count, _ = experiment.evaluate_solution(solution)
        return avg_photon_count

    def take_step(self, solution):
        new_solution = [axis + random.uniform(-self.initial_step_size, self.initial_step_size) for axis in solution]
        return new_solution

    def optimize(self, experiment, database):
        initial_solution = experiment.get_motor_coordinates()

        def callback(x, f, accept):
            self.past_energies.append(f)
            database.addData(self.initial_temperature, f, x)
            experiment.move_to_array(x)

            if self.check_convergence():
                print("Convergence criteria met. Stopping optimization.")
                raise Exception("Convergence reached")

        minimizer_kwargs = {"args": (experiment,)}
        try:
            ret = basinhopping(self.energy, initial_solution, minimizer_kwargs=minimizer_kwargs, take_step=self.take_step, niter=self.max_iterations, T=self.initial_temperature, callback=callback)
        except Exception as e:
            if str(e) == "Convergence reached":
                print("Optimization stopped due to convergence.")
        
        best_solution = ret.x if 'ret' in locals() else initial_solution
        best_energy = ret.fun if 'ret' in locals() else self.energy(initial_solution, experiment)

        print("Optimal solution found with average photon count:", best_energy)
        return best_solution, database

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, experiment, initial_step_size=150, initial_temperature=1000, cooling_rate=0.98, max_iterations=10000, convergence_threshold=0.001, convergence_lookback=25):
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
        print("Recent Energies: ")
        enumerate(recent_energies)
        min_energy = min(recent_energies)
        max_energy = max(recent_energies)

        return ((max_energy - min_energy)/(max_energy + min_energy)) < self.convergence_threshold
    
    def energy(self, solution, experiment):
        avg_photon_count, _ = experiment.evaluate_solution(solution)
        return avg_photon_count

    def neighbor(self, solution):
        new_solution = [axis + random.uniform(-self.step_size, self.step_size) for axis in solution]
        return new_solution

    def acceptance_probability(self, energy_old, energy_new, temperature):
        if energy_new > energy_old:
            return 1.0
        prob = math.exp((energy_old - energy_new) / 100 * temperature)
        print("\n\nAcceptance Probability: ", prob)
        return prob

    def optimize(self, experiment, database):
        current_solution = experiment.get_motor_coordinates()  # Initialize with the current positions of the axes
        current_energy = self.energy(current_solution, experiment)
        print("Starting energy at: ", current_energy)
        
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
                print("Accepted")
                current_solution = neighbor_solution
                current_energy = neighbor_energy
            else:
                print("Not accepted")

                if current_energy > best_energy:
                    best_energy = current_energy
                    best_solution = current_solution

            #Move from 'neighbour' to current solution  
            experiment.move_to_array(current_solution)

            #Add stats to database
            self.past_energies.append(current_energy)
            database.addData(temperature, current_energy, current_solution)
            
            if self.check_convergence():
                print("\nConvergence criteria met. Stopping optimization.")
                break
            # Update step size as a function of the temperature?
            # This line reduces the step size linearly with decreasing temperature.
            self.step_size = self.initial_step_size * (temperature / (2*self.initial_temperature))
            temperature *= self.cooling_rate
        
        print("\n\nOptimal solution found with average photon count:", best_energy)
        return best_solution, database
