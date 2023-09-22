import Database

# Main Controller
class Controller:
    def __init__(self, experiment, algorithm):
        self.experiment = experiment
        self.algorithm = algorithm
        self.database = Database.Database()
    
    def run(self, experiment):
        optimal_solution = self.algorithm.optimize(self.experiment, self.database)
        # Use the optimal solution, e.g., align mirrors accordingly
        print("Optimal solution found at:", optimal_solution)
        experiment.close_motor_connection()

    def model(self):
        self.database.print()
        self.database.modelCountVsTime()
        self.database.modelCountVsAxis()
        self.database.modelTimeVsAxis()
        

