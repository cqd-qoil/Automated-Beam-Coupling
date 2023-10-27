import Detector
from ZaberMotor import ZaberMotor
from Database import Database
#Output Detector
detector1 = Detector.PowerMeter('PM100D')

#Motor initialisation
motors = ZaberMotor()
motors.open_motor_connection()
database = Database()

def objective():
    #Objective Function for Optimization
    count = detector1.read()
    return -1*count

def x0():
    return motors.get_motor_coordinates()

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
    
