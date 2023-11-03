# Example Usage
from Experiment import Experiment
import OptimizationAlgorithm
import Controller
from Database import Database

# # Initialize experiment and algorithm
experiment = Experiment()
database = Database()
basin_hopping_result = OptimizationAlgorithm.BasinHopping(experiment, database)

# Create controller and run optimization
try:
    controller = Controller.Controller(experiment, basin_hopping_result)
    controller.run(experiment)
finally:
    controller.model()
