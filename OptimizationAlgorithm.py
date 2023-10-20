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
    def __init__(self, experiment, database):
        self.experiment = experiment
        self.solution = self.x0()
        self.database = database
        self.count = self.objective()

    def objective(self):
        #Objective Function for Optimization
        self.count, _ = self.experiment.evaluate_solution(self.solution)
        return -1 * self.count
    
    def x0(self):
        return self.experiment.get_motor_coordinates()
    
    def take_step(self):
        new_solution = [axis + random.uniform(-self.initial_step_size, self.initial_step_size) for axis in self.solution]
        self.experiment.move_to_array(new_solution)
        self.solution = new_solution
        return new_solution

    def callback(self):
        #Append List here
        self.database.addData(self.count, self.solution)
        pass

    def optimize(self):
        return basinhopping(func=lambda: self.objective(), x0=lambda: self.x0(), niter=1000, T=1, stepsize=20,
                            minimizer_kwargs=None, interval=50, disp=True, niter_success=20, seed=None,
                            target_accept_rate=0.5, stepwise_factor=0.9)
        
