# Example Usage
from Experiment import Experiment
import OptimizationAlgorithm
import Controller
from Database import Database

# # Initialize experiment and algorithm
# experiment = Experiment()
# database = Database()
# iterations = 10
# method = 'Neal-Melder'
# basin_hopping_result = OptimizationAlgorithm.BasinHopping(experiment, database, iterations, method)

# Create controller and run optimization
# try:
#     controller = Controller.Controller(experiment, basin_hopping_result, database)
#     controller.run(experiment)
# finally:
#     controller.model()

def all_methods():
    paired = [7632.0, 14132.0, -5695.0, -6508.0]
    # motors.reset_motor_axis()
    methods = ['Nelder-Mead']
    #some of these need extra
    # methods = ['Powell', 'Nelder-Mead', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 
                #    'COBLYA', 'SLSQP', 'trust-constr', 'dogleg']
    for i in range(len(methods)):    
        # # Initialize experiment and algorithm
        experiment = Experiment()
        #Reset solution to pairing coordinates
        experiment.move_to_array(paired)
        database = Database()
        iterations = 13
        niter_success = 10
        temp = 0.6
        basin_hopping_result = OptimizationAlgorithm.BasinHopping(experiment=experiment, 
                                                                  database=database, 
                                                                  iters=iterations, 
                                                                  method=methods[i], 
                                                                  niter_success=niter_success, 
                                                                  temp=temp)
        database.setMethod(methods[i])
        # Create controller and run optimization
        try:
            controller = Controller.Controller(experiment, basin_hopping_result, database)
            controller.run(experiment)
        finally:
            controller.model()

all_methods()
 


   