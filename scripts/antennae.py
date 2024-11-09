# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 20:38:50 2024

@author: go29lap
"""

import matplotlib.pyplot as plt
from pyaedt import Hfss
import numpy as np

# Launch HFSS in non-graphical mode
hfss = Hfss(specified_version="2024.1", non_graphical=True, new_desktop_session=True)

# Create a new project and design
hfss.save_project(r"C:\path_to_your_project\my_hfss_project.aedt")
hfss.insert_design("S-Parameters_Design")

# Set the frequency for the analysis (in GHz)
setup = hfss.create_setup("MySetup")
setup.props["Frequency"] = "10GHz"  # Example: 10 GHz
setup.update()

# Create geometry (example: box as a simple placeholder structure)
hfss.modeler.create_box([0, 0, 0], [10, 5, 1], name="MyBox", material="copper")

# Assign boundaries and excitations (wave ports)
hfss.solution_type = "DrivenModal"

# Create two wave ports (Port 1 and Port 2)
port1 = hfss.create_wave_port(
    hfss.faces[0], 
    num_modes=1, 
    name="Port1", 
    renormalize=True, 
    port_impedance=50
)
port2 = hfss.create_wave_port(
    hfss.faces[1], 
    num_modes=1, 
    name="Port2", 
    renormalize=True, 
    port_impedance=50
)

# Run the setup
hfss.analyze_setup("MySetup")

# Extract the S-parameters results
s_params_data = hfss.get_sparameters_data(setup_name="MySetup", output_type="Magnitude")

# Convert the S-parameters data into a numpy array for easy plotting
frequencies = np.array(s_params_data["Freq (GHz)"])
s11 = np.array(s_params_data["S11"])  # S11 reflection coefficient
s21 = np.array(s_params_data["S21"])  # S21 transmission coefficient

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(frequencies, 20 * np.log10(abs(s11)), label='S11 (Reflection)', marker='o')
plt.plot(frequencies, 20 * np.log10(abs(s21)), label='S21 (Transmission)', marker='x')

plt.title('S-Parameters Plot')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()
plt.show()

# Save project after running the simulation
hfss.save_project()

# Close HFSS when done
hfss.close_project()
hfss.release_desktop()

