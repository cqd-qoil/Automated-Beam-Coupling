# Example Usage
import Experiment
import OptimizationAlgorithm
import Controller

# # Initialize experiment and algorithm
experiment = Experiment.Experiment()
simulated_annealing_algorithm = OptimizationAlgorithm.SciPiSimAnneal(experiment)

# Create controller and run optimization
controller = Controller.Controller(experiment, simulated_annealing_algorithm)
controller.run(experiment)
controller.model()
