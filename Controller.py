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
        print("Solution found at:", solution.fun * -1000, "Optimal solution should be: ", self.experiment.benchmark())
 
    def reset_pairing(self, experiment):
        paired = [7632.0, 14132.0, -5695.0, -6508.0]
        # motors.reset_motor_axis()
        experiment.move_to_array(paired)
        time.sleep(2)

    def model(self):
        # self.database.print()
        self.database.modelCountVsTime()
        self.database.modelCountVsAxis()
        

