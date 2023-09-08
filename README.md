## README file for Counting-Card-Interface

Optimisation software for Quantum Optics Lab. Software architecture consists of Experiment which initialises and interfaces with hardware, an abstract class OptimizationAlgorithm, as well as a child implementation SimulatedAnnealing. Controller and DataBase classes have also been implemented for running the experiment and tracking/modeling information accordingly. 


## Project Overview
This software is used for the optimisation of beam coupling or using Zaber TMM-2 motor mounted mirrors. The software uses an abstact OptimizationAlgorithm class to allow for Simmulated Annealing, Gaussian Estimation, SVR amongst other methods to predict the optimal alignment parameters for the mirrors based off semi-frequent data sampling. Initially the script was written to optimise power coupling but has now been migrated to maximuse photon count with a Logic16 Counting Card. Future work for the project will be to alter the software for optimization of coincidence detections. 

## Prerequisites
### Software Requiremements
Ensure you have python installed. Other than that all libraries used are available for download with the `requirements.txt` file.

### Hardware Requirements
The experimental set up for the mirrors requires optionally 1 - 2 Zaber T-MM2 Motor Mounted Mirrors as well as a UQDevices Logic16 CC.

 A 69mA 750nm laser was used for development of the project, though this will only be relavant to your optics and the algorithm should work the same regardless. The laser was emmited from a single mode fibre held in place and collimated with a stage. Two ThorLabs BB1-E03 Mirrors were mounted in the Zaber T-MM2 motors and mirror brackets and focused into another stage with attached SMF which fed into an APD. The APD is linked into the second channel of the Logic16 which then connects to the conputer along with the Zaber Motors.

## Installation
If python is installed and up to date with pip, use 
```
pip install requirements.txt
```
to install all required libraries. 

## Usage
The `Beam-Coupling-Optimisation.ipynb` file has been included as an example demonstation for the optimisation. Steps in the notebook are annotated with explanations and are ready to go provided the user has 2 mirrors and is working with a 780nm laser. Some modelling is provided at the end of this notebook for visualisation of the coupling proccess.

* The use of the software requires importing the library 
```
import AutoAlignLib as alb
```
* Open the connection with T-MM2 devices and initialise power meter. 
* Optionally, you can enter a wavelength in `powerMeterInit()` otherwise it will default to 780nm.
```
alb.powerMeterInit()
alb.openConnection()
```
* Manually achieve some coupling into your SMF then use the following to set the starting coordinate
```
x0 = alb.getCurrentCoordinates()
```
* Now, run the optimisation loop 
```
results = alb.optimise(numPoints, x0, Boundary, saveData, convergenceInt, dimensions)
```
The output of the optimise function will be a dictionary containing `x0`: the coordinates of best coupling, `p0`: the best coupling power, `data`: a dataframe with all coordinates visited and power measured there (with std of power) and `numRuns`: the total mnumber of algorithm iterations taken.

## Experimental Results 
Experimental data model examples with 'Database.py' class:


## Contact Information
If you have any questions or comments about the software, I can be contacted either via email <brendanwallis01@gmail.com>, mobile 0421883516, or <a href="https://www.linkedin.com/in/brendan-wallis-5bb214192/" target="_blank">LinkedIn</a>.


