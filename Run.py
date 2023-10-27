# Example Usage
from Experiment import Experiment
import OptimizationAlgorithm
import Controller

# # Initialize experiment and algorithm
experiment = Experiment()
basin_hopping_result = OptimizationAlgorithm.BasinHopping(experiment, )

# Create controller and run optimization
controller = Controller.Controller(experiment, basin_hopping_result)
controller.run(experiment)
controller.model()
