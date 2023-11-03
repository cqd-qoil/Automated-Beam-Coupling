import Database
import time

# Main Controller
class Controller:
    def __init__(self, experiment, algorithm):
        self.experiment = experiment
        self.algorithm = algorithm
        self.database = Database.Database()
    
    def run(self, experiment):
        self.method_loop(experiment)
        # try:
        #     solution = self.algorithm.optimize(method)
        #     experiment.move_to_array(solution.x)
        # finally:
        #     experiment.close_motor_connection()
        # # Use the optimal solution, e.g., align mirrors accordingly
        # print("Solution found at:", solution.fun * -1000, "Optimal solution should be: ", self.experiment.benchmark())

    def method_loop(self, experiment):
        methods_full = ['Powell', 'Nelder-Mead', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 
                   'COBLYA', 'SLSQP', 'trust-constr', 'dogleg']
        
        methods = ['Powell', 'Nelder-Mead']

        final_couplings = []
        """
        Need to add different database for every method to get seperate graphs
        OR 
        model inside for loop
        """
        try:
            for i in range(len(methods)): 
                self.reset_pairing
                method = methods[i]
                solution = self.algorithm.optimize(method)
                experiment.move_to_array(solution.x)
                # Use the optimal solution, e.g., align mirrors accordingly
                print(methods[i], " solution found at:", solution.fun * -1000, "Optimal solution should be: ", self.experiment.benchmark())
                final_couplings.append(solution.fun)
        finally:
            print("Experiment Concluding...")
            print(methods)
            print(final_couplings)
            experiment.close_motor_connection()
    
    def reset_pairing(self, experiment):
        paired = [7632.0, 14132.0, -5695.0, -6508.0]
        # motors.reset_motor_axis()
        experiment.move_to_array(paired)
        time.sleep(2)

    def model(self):
        self.database.print()
        self.database.modelCountVsTime()
        self.database.modelCountVsAxis()
        

