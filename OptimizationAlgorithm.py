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
from functools import partial

##CREATE OPT GRAPH WITH EACH OPT METHOD


# Optimization Algorithm Interface
class OptimizationAlgorithm(ABC):
    @abstractmethod
    def optimize(self, experiment):
        pass

class opt():
    def __init__(self, experiment):
        # Output Detector
        self.detector1 = experiment.detector1
        # Motor initialization
        self.motors = experiment.motors

    def objective(self, x):
        # motors.move_to_array will return 1 when motors finished moving
        while not self.motors.move_to_array(x):
            pass
        count = self.detector1.read()
        if count < 0:
            count = 0
        # print("count: ", count)
        return -1*count

class BasinHopping(OptimizationAlgorithm):
    def __init__(self, experiment, database):
        self.experiment = experiment
        self.stepsize = 100
        self.niters = 4
        self.database = database

    def objective(self, x):
        # motors.move_to_array will return 1 when motors finished moving
        while not self.motors.move_to_array(x):
            pass
        count = self.detector1.read()
        if count < 0:
            count = 0
        # print("count: ", count)
        return -1*count 
    def callback(self, x, f, accept):
        print("x ", x)
        print("f ", f)
        #ADD TO DATABASE when we know what x and f are 
        self.database.addData(x, f)
    def optimize(self, method):
        #Objective partial func to include self
        opt_instance = opt(self.experiment)
        objective_with_self = partial(opt_instance.objective)

        #callback partial func to include self 
        callback_with_self = partial(self.callback)

        #get x0 starting position
        x0 = self.experiment.get_motor_coordinates()
        minimizer_kwargs = {"method" : method}

        result = basinhopping(
            func=objective_with_self,
            x0=x0,
            minimizer_kwargs= minimizer_kwargs,
            callback=callback_with_self,
            niter=self.niters,
            stepsize=self.stepsize,
            T = 0.05,
            disp=True,
            niter_success=20,
            seed=None
        )
        return result
        



