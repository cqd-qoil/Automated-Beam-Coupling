import Database
import time

# Main Controller
class Controller:
    def __init__(self, experiment, algorithm, database):
        self.experiment = experiment
        self.algorithm = algorithm
        self.database = database
    
    def run(self, experiment):
        try:
            solution = self.algorithm.optimize()
            experiment.move_to_array(solution.x)
        finally:
            experiment.close_motor_connection()
        # Use the optimal solution, e.g., align mirrors accordingly
        print("Solution found at:", -1 * solution.fun, " [W]. Optimal solution should be: ", self.experiment.benchmark(), "[W]")
 
    def reset_pairing(self):
        paired = [7632.0, 14132.0, -5695.0, -6508.0]
        # motors.reset_motor_axis()
        self.experiment.move_to_array(paired)
        time.sleep(2)

    def model(self):
        # self.database.print()
        bench = self.experiment.benchmark()
        self.database.modelCountVsTime(bench)
        self.database.modelCountVsAxis(bench)
        

