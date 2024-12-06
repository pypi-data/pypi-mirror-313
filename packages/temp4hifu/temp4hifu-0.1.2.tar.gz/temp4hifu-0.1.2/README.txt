# TEMP4HIFU

Author: Gerald Lee

Last Updated: 12/03/2024

*Final Project, BIOEN 537: Computational System Biology. University of Washington, Seattle*

A Python package designed to estimate the temperature increase due to high intensity focused ultrasound (HIFU) excitation. 


## BACKGROUND
High Intensity Focused Ultrasound (HIFU) and Focused Ultrasound (FUS) are used for thermal treatment of cells such as for cancer treatment. The generated increase of temperature during HIFU thermal treatment must be within safety guidelines for human use (44 degrees Celsius), which is essential for FDA approval and compliance. Accurate predictions of temperature bioeffects must be demonstrated through computational simulations before applications ex vivo and in vivo. Computational simulations requires modeling for both HIFU/FUS pressure fields and then the Bioheat equation; not complicated individually, but when combined can be tricky to navigate based on initial conditions.

Provided here is a tool to estimate bioheat from HIFU, usable as a GUI or importable as functions for integration with other code. The GUI provides an entry-friendly visualization of all aspects of bioheat due to HIFU. 


## INSTALLATION AND USE
This package is designed to be used within a provided GUI or as independent functions. Inputs 

### SETUP
pip install temp4hifu

### PRE-REQUISITES
Ensure you have the following additional Python packages:
    1. numpy
    2. pandas
    3. dash
If not, please pip install these packages as well. 

### GUI
import temp4hifu.startApp
temp4hifu.startApp

### INDIVIDUAL FUNCTIONS
from temp4hifu import setParam, calculateBioheat, calculateRayleighIntegral
setParam.setMedium(INPUT_ARG)
calculateBioheat.generateVec(INPUT_ARG)
calculateRayleighIntegral.generateField(INPUT_ARG)

## GUI COMPONENTS AND FUNCTION NOTES
The GUI is able to perform and sustain the following actions:
1) 




The function calculateRayleighIntegral.py allows the calculation of a pressure field in cylindrical coordinate space 
