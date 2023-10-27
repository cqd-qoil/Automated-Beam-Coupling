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
import numpy as np


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
        self.count = self.experiment.evaluate_solution(self.solution)
        self.step_size = 50

    # def update(self):
    #     self.solution = 
    #     self.x0 = 
    # def objective(self):
    #     #Objective Function for Optimization
    #     self.count = self.experiment.evaluate_solution(self.solution)
    #     return -1*self.count
    def objective(self,coords):
    #Objective Function for Optimization
        # self.update()
        return -1*self.experiment.evaluate_solution(coords) 
    
    def x0(self):
        return self.experiment.get_motor_coordinates()

    def callback(self, x, f, accept):
        #Append List here
        self.database.addData(self.count, self.solution)

    def optimize(self):
        x0 = self.experiment.get_motor_coordinates()
        func = self.objective
        take_step = MyTakeStep(self.experiment)
        callback = self.callback
        return basinhopping(func=func, x0=x0, niter=1000, T=1,
                            minimizer_kwargs=None, take_step=take_step, callback=callback, interval=10, disp=True, niter_success=20, seed=None,
                            target_accept_rate=0.25, stepwise_factor=0.9)
        
class MyTakeStep:
    def __init__(self, experiment, stepsize=20):
        self.stepsize = stepsize
        self.rng = np.random.default_rng()
        self.experiment = experiment
    def __call__(self, x):
        s = self.stepsize
        for i in range(len(x)): 
            x[i] += self.rng.uniform(-s, s)
        print("new coords: ", x)
        self.experiment.move_to_array(x)
        return x
