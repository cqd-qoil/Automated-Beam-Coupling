## README file for Counting-Card-Interface

Optimisation software for Quantum Optics Lab. Software architecture consists of Experiment which initialises and interfaces with hardware, an abstract class OptimizationAlgorithm, as well as a child implementation SimulatedAnnealing. Controller and DataBase classes have also been implemented for running the experiment and tracking/modeling information accordingly. 


## Project Overview
This software is used for the optimisation of beam coupling using two Zaber TMM-2 motor mounted mirrors. The software uses a gaussian estimation method to predict the optimal alignment of the 4 axial parameters based off some sampled data and iteratively determines the most optimal alignment for a laser beam based off the power coupling output. 

A second optimisation algorithm was incorporated into the software using SVR supported vector regression which provided faster and more efficient coupling.

## Prerequisites
### Software Requiremements
Ensure you have python installed. You also may need to download National Instruments VISA drivers. Other than that all libraries used are available for download with the `requirements.txt` file.

### Hardware Requirements
The experimental set up for the mirrors requires optionally 1 - 2 Zaber T-MM2 Motor Mounted Mirrors as well as a ThorLabs PM powermeter. The software should be able to autodetect any kind of powermeter so long as it is a PM100 type though it was written using a PM100D. The software also configures the powermeter to for laser wavelengths on 780nm and uses the auto-ranging feature. This value can be changed in the `powerMeterInit()` function of `AutoAlignLib`.

 A 69mA 750nm laser was used for development of the project. The laser was emmited from a single mode fibre held in place and collimated with a stage. Two ThorLabs BB1-E03 Mirrors were mounted in the Zaber T-MM2 motors and mirror brackets and focused into another stage with attached SMF which fed into the PM100D.

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
If you have any questions or comments about the software, i can be contacted either via email <brendanwallis01@gmail.com>, mobile 0421883516 or [<linkedIn>](<https://www.linkedin.com/in/brendan-wallis-5bb214192/>) 


