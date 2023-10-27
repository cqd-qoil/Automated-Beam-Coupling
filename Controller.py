import Database

# Main Controller
class Controller:
    def __init__(self, experiment, algorithm):
        self.experiment = experiment
        self.algorithm = algorithm
    
    def run(self, experiment):
        optimal_solution = self.algorithm.optimize()
        # Use the optimal solution, e.g., align mirrors accordingly
        print("Optimal solution found at:", optimal_solution)
        experiment.close_motor_connection()
        print("Optimal solution should be: ", self.experiment.benchmark())

    def model(self):
        self.database.print()
        self.database.modelCountVsTime()
        self.database.modelCountVsAxis()
        #self.database.modelTimeVsAxis()
        

