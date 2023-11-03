import Detector
import ZaberMotor
from Database import Database 
from scipy.optimize import basinhopping
import random
import math
import time
import numpy as np
from scipy.optimize import minimize
from functools import partial

class opt:
    def __init__(self):
        # Output Detector
        self.detector1 = Detector.PowerMeter('PM100D')
        # Motor initialization
        self.motors = ZaberMotor.ZaberMotor()
        self.motors.open_motor_connection()

    def objective(self, x):
        # motors.move_to_array will return 1 when motors finished moving
        while not self.motors.move_to_array(x):
            pass
        count = self.detector1.read()
        if count < 0:
            count = 0
        # print("count: ", count)
        return -1*count
    
    def getMotors(self):
        return self.motors.get_motor_coordinates()
    
    def move_to_array(self, x):
        self.motors.move_to_array(x)
    
    def closeMotors(self):
        self.motors.close_motor_connection()

def optimize(opt_instance, ):
    objective_with_self = partial(opt_instance.objective)
    x0 = opt_instance.getMotors()

    result = basinhopping(
        func=objective_with_self,
        x0=x0,
        minimizer_kwargs={"method" : "Nelder-Mead"},
        niter=30,
        stepsize=20,
        T = 0.05,
        disp=True,
        niter_success=20,
        seed=None
    )
    return result

trial = opt()

try:
    result = optimize(trial)
    trial.move_to_array(result.x)
finally:
    trial.closeMotors()
    print("Closed port")

print("++++++++++++++++++  Optimization Complete, printing results...  +++++++++++++++++++++++")
print(result.x)
print(result.fun)
print(result.message)

# def local_optimization_test(objective, starting_points):
#     for x0 in starting_points:
#         res = minimize(objective, x0, method='Nelder-Mead')  # Use the same method as in basinhopping
#         if not res.success:
#             print(f"Local optimization failed for starting point {x0}")
#             print(f"Message: {res.message}")
#         else:
#             print(f"Local optimization succeeded for starting point {x0}")
#             print(f"Result: {res.x}")

# starting_points = [np.random.rand(4) for _ in range(10)]
# local_optimization_test(trial.objective, starting_points)

