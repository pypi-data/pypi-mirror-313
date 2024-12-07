# model_ELISA
Creates a GUI which simulates the mechanisms of a direct Sandwich ELISA

An enzyme-linked immunosorbant assay or ELISA is used to identify and/or quantify proteins. Given its detection abilities, it is highly useful for diagnosing various diseases from immune system disorders to infections. There are multiple different varieties of ELISAs, however one of the most commonly used is the direct sandwich ELISA. In this method the antigen of choice binds to a capture antibody. The capture antibody - antigen complex then binds to another antibody, termed the detection antibody. The detection anitbody is linked to an enzyme. When a substrate is introduced, the enzyme on the detection antibody converts the substrate to a colorimetric product and the amount of signal is used to quantify the amount of antigen in the mixture. 

ELISA development and optimization requires researchers to perform benchtop experiments that are often cumbersome and necessitate many sequential experiments to determine the best concentrations and settings for each species. 

This tool allows the user to mimic the experimental results of a direct sandwich ELISA which can aide when deciding to choose initial species concentration, temperature conditions, and which reaction variables to adjust to obtain an optimal reaction time. 

The user inputs initial concentrations, kinetic constants, and overall reaction time. The output will a plot which shows the concentrations of the species overtime and it also denotes the minimum time to steady state.

## Setup
pip install model_ELISA

## Load GUI

## Choose input parameters or select default parameters

## Run simulation

## Optional: Clear plot and input parameters, enter new parameters and re-run simulation
