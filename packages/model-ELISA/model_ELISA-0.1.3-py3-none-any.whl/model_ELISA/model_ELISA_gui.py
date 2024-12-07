import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tellurium as te

'''This program simulates the direct ELISA model via GUI with input parameters

    # General concentration input format
    capture =  Initial capture antibody concentration (M)
    antigen =  Initial antigen concentration (M)
    capture_antigen =  Capture antibody-antigen complex (M)
    detection = Initial detection antibody concentration (M)
    capture_antigen_detection = Capture antibody-antigen-detection antibody complex (M)
    substrate = Substrate concentration (M)
    product =  Product concentration (M)

    # General kinetic constant input format
    k_on1 =  Forward rate constant for capture antibody and antigen (s^-1)
    k_off1 = Reverse rate constant for capture antibody and antigen (s^-1)
    k_on2 = Forward rate constant for detection antibody and antigen (s^-1)
    k_off2 = Reverse rate constant for detection antibody and antigen (s^-1)
    k_cat1 = Catalytic rate constant for substrate conversion (s^-1)
    k_cat2 = Rate constant for substrate conversion (s^-1)

    If there is an enry after the variable name it refers to the GUI grabbing the 
    value from the user inputs. Default values are specified below if the user
    chooses to use them, however the input field are left blank at the beginning
    to allow the user to input their own values.'''    

def run_simulation(capture_entry:float, antigen_entry:float, detection_entry:float, substrate_entry:float,
    k_on1_entry:float, k_off1_entry:float, k_on2_entry:float, k_off2_entry:float,
    k_cat1_entry:float, k_cat2_entry:float, overall_time_entry:float, plot_frame:float
) -> plt:

    '''
    Run the simulation and plot the results.
    
    This function reads the input values from the GUI, simulates the direct ELISA model,
    and plots the results. The steady state is determined by comparing the change in
    concentration between time points. The steady state time is marked on the plot.

    Parameters:
    capture_entry: Entry widget for the capture antibody concentration
    antigen_entry: Entry widget for the antigen concentration
    detection_entry: Entry widget for the detection antibody concentration
    substrate_entry: Entry widget for the substrate concentration
    k_on1_entry: Entry widget for the forward rate constant for capture antibody and antigen
    k_off1_entry: Entry widget for the reverse rate constant for capture antibody and antigen
    k_on2_entry: Entry widget for the forward rate constant for detection antibody and antigen
    k_off2_entry: Entry widget for the reverse rate constant for detection antibody and antigen
    k_cat1_entry: Entry widget for the catalytic rate constant for substrate conversion
    k_cat2_entry: Entry widget for the rate constant for substrate conversion
    overall_time_entry: Entry widget for the overall reaction time
    plot_frame: Frame to display the plot
    
    '''

    global canvas  # Declare canvas as global to access it in the clear_button command

    # Get input values
    capture = float(capture_entry.get())
    antigen = float(antigen_entry.get())
    detection = float(detection_entry.get())
    substrate = float(substrate_entry.get())
    k_on1 = float(k_on1_entry.get())
    k_off1 = float(k_off1_entry.get())
    k_on2 = float(k_on2_entry.get())
    k_off2 = float(k_off2_entry.get())
    k_cat1 = float(k_cat1_entry.get())
    k_cat2 = float(k_cat2_entry.get())
    overall_time = float(overall_time_entry.get())

    # Antimony model
    '''Create the direct ELISA model in antimony with input parameters'''

    model = f"""
    # Species
    capture = {capture};  # Initial capture antibody concentration (M)
    antigen = {antigen};  # Initial antigen concentration (M)
    capture_antigen = 0;    # Capture antibody-antigen complex (M)
    detection = {detection};  # Initial detection antibody concentration (M)
    capture_antigen_detection = 0;   # Capture antibody-antigen-detection antibody complex (M)
    substrate = {substrate};  # Substrate concentration (M)
    product = 0;     # Product concentration (M)

    # Parameters
    k_on1 = {k_on1};   # Forward rate constant for capture antibody and antigen (s^-1)
    k_off1 = {k_off1}; # Reverse rate constant for capture antibody and antigen (s^-1)
    k_on2 = {k_on2};   # Forward rate constant for detection antibody and antigen (s^-1)
    k_off2 = {k_off2}; # Reverse rate constant for detection antibody and antigen (s^-1)
    k_cat1 = {k_cat1};  # Catalytic rate constant for substrate conversion (s^-1)
    k_cat2 = {k_cat2};  # Rate constant for substrate conversion (s^-1)

    # Reactions
    R1: capture + antigen -> capture_antigen; k_on1 * capture * antigen;
    R2: capture_antigen -> capture + antigen; k_off1 * capture_antigen;
    R3: capture_antigen + detection -> capture_antigen_detection; k_on2 * capture_antigen * detection;
    R4: capture_antigen_detection -> capture_antigen + detection; k_off2 * capture_antigen_detection;
    R5: capture_antigen_detection + substrate -> capture_antigen_detection_substrate; k_cat1 * capture_antigen_detection * substrate;
    R6: capture_antigen_detection_substrate -> capture_antigen_detection + product; k_cat2 * capture_antigen_detection_substrate;
    """

    # Load and simulate the model
    r = te.loada(model)
    results = r.simulate(0, overall_time, 1000)
    time = results[:, 0]
    concentrations = results[:, 1:]

    # Find steady state
    steady_state_time = None
    THRESHOLD = 1e-6
    for i in range(1, len(time)):
        deltas = np.abs(concentrations[i] - concentrations[i - 1])
        if np.all(deltas < THRESHOLD):
            steady_state_time = time[i]
            break

    # Plot the results
    fig, ax = plt.subplots(figsize=(10, 6))
    for idx, species in enumerate(r.getFloatingSpeciesIds()):
        ax.plot(time, results[:, idx + 1], label=species)

    # Mark the steady-state time
    if steady_state_time is not None:
        ax.axvline(x=steady_state_time, color='red', linestyle='--')
        ax.text(
            steady_state_time, 
            max(np.max(results[:, 1:], axis=0)) * 0.9,  # Position the text near the top of the plot
            f'Steady State\n{steady_state_time:.2f} s', 
            color='red', 
            ha='left',
            va='center',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

    # Add labels and legend
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Concentration (M)')
    ax.set_title('Direct ELISA Simulation')
    ax.legend()

    # Clear the previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    # Display the plot in the GUI
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def insert_default_parameters(entries:dict) -> None:
    '''
    This function inserts default parameters into the input fields
    if the user does not know which values to start with. values are:
    for all the entry fields denoted in the antimony model above.

    Parameters:
    entries: Dictionary of entry widgets

    '''
    default_values = {
        "capture_entry": 10,
        "antigen_entry": 1,
        "detection_entry": 10,
        "substrate_entry": 100,
        "k_on1_entry": 1e1,
        "k_off1_entry": 1e-2,
        "k_on2_entry": 1e1,
        "k_off2_entry": 1e-2,
        "k_cat1_entry": 1e1,
        "k_cat2_entry": 1e1,
        "overall_time_entry": 200
    }
    for key, value in default_values.items():
        entry = entries[key]
        entry.delete(0, tk.END)
        entry.insert(0, value)

def clear_plot_and_inputs(entries:dict, plot_frame:float) -> None:
    """
    This function clears the plot and input fields if the user 
    wants to start over and tests new values.

    Parameters:
    entries: Dictionary of entry widgets
    plot_frame: Frame to display the plot
    """
    for widget in plot_frame.winfo_children():
        widget.destroy()
    for entry in entries.values():
        entry.delete(0, tk.END)

#Creating the GUI

# Create the main window
window = tk.Tk()
window.title("Direct ELISA Simulation")

# Set a specific theme
style = ttk.Style()
style.theme_use('clam')  # You can try 'clam', 'alt', 'default', 'classic'

# Create a main frame to hold inputs and plots
main_frame = ttk.Frame(window, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

#Create input frame
input_frame = ttk.Frame(main_frame, padding="10")
input_frame.pack(side=tk.LEFT, fill=tk.BOTH)

# Create input fields
fields = [
    ("Capture (M)", "capture_entry"),
    ("Antigen (M)", "antigen_entry"),
    ("Detection (M)", "detection_entry"),
    ("Substrate (M)", "substrate_entry"),
    ("Forward rate constant step 1 (s^-1)", "k_on1_entry"),
    ("Reverse rate constant step 1 (s^-1)", "k_off1_entry"),
    ("Forward rate constant step 2 (s^-1)", "k_on2_entry"),
    ("Reverse rate constant step 2 (s^-1)", "k_off2_entry"),
    ("Catalysis constant 1 (s^-1)", "k_cat1_entry"),
    ("Catalysis constant 2 (s^-1)", "k_cat2_entry"),
    ("Overall reaction time (s)", "overall_time_entry")
]

entries = {}    # Dictionary to store entry widgets
for label_text, var_name in fields:
    frame = ttk.Frame(input_frame, padding="3 3 12 12")
    frame.pack(side=tk.TOP, fill=tk.X)
    label = ttk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT)
    entry = ttk.Entry(frame)
    entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    entries[var_name] = entry

# Add a button to insert default parameters
default_button = ttk.Button(input_frame, text="Insert Default Parameters", command=lambda: insert_default_parameters(entries))
default_button.pack(side=tk.TOP, pady=10)

# Add a button to run the simulation
run_button = ttk.Button(input_frame, text="Run Simulation", command=lambda: run_simulation(
    entries["capture_entry"], entries["antigen_entry"], entries["detection_entry"],
    entries["substrate_entry"], entries["k_on1_entry"], entries["k_off1_entry"],
    entries["k_on2_entry"], entries["k_off2_entry"], entries["k_cat1_entry"],
    entries["k_cat2_entry"], entries["overall_time_entry"], plot_frame
))
run_button.pack(side=tk.TOP, pady=10)

#Add a button which clears the plot and the input fields
clear_button = ttk.Button(input_frame, text="Clear", command=lambda: clear_plot_and_inputs(entries, plot_frame))
clear_button.pack(side=tk.TOP, pady=10)

# Create a frame for the plot
plot_frame = ttk.Frame(main_frame, padding="10")
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Start the GUI event loop
window.mainloop()