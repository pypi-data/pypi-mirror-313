# model_ELISA
Creates a GUI which simulates the mechanisms of a direct Sandwich ELISA

An enzyme-linked immunosorbant assay or ELISA is used to identify and/or quantify proteins. Given its detection abilities, it is highly useful for diagnosing various diseases from immune system disorders to infections. There are multiple different varieties of ELISAs, however one of the most commonly used is the direct sandwich ELISA. In this method the antigen of choice binds to a capture antibody. The capture antibody - antigen complex then binds to another antibody, termed the detection antibody. The detection anitbody is linked to an enzyme. When a substrate is introduced, the enzyme on the detection antibody converts the substrate to a colorimetric product and the amount of signal is used to quantify the amount of antigen in the mixture. 

ELISA development and optimization requires researchers to perform benchtop experiments that are often cumbersome and necessitate many sequential experiments to determine the best concentrations and settings for each species. 

This tool allows the user to mimic the experimental results of a direct sandwich ELISA which can aide when deciding to choose initial species concentration, temperature conditions, and which reaction variables to adjust to obtain an optimal reaction time. 

The user inputs initial concentrations, kinetic constants, and overall reaction time. The output will a plot which shows the concentrations of the species overtime and it also denotes the minimum time to steady state.

## Setup
pip install model_ELISA

## Load GUI
<img width="454" alt="Screenshot 2024-12-05 at 7 59 24 PM" src="https://github.com/user-attachments/assets/41a1cc17-b765-42be-8898-76ed753cea18">

## Choose input parameters or select default parameters
<img width="455" alt="Screenshot 2024-12-05 at 7 59 52 PM" src="https://github.com/user-attachments/assets/b30bfb84-042c-4abf-b591-18429f263178">

## Run simulation
<img width="1100" alt="Screenshot 2024-12-05 at 8 00 29 PM" src="https://github.com/user-attachments/assets/07fe5d32-7e21-4094-90d5-efbe52d03ee1">

## Optional: Clear plot and input parameters, enter new parameters and re-run simulation
<img width="1097" alt="Screenshot 2024-12-05 at 8 00 50 PM" src="https://github.com/user-attachments/assets/b076f628-17d8-43a9-b70b-508835b2b9fd">
