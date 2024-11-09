# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 22:48:30 2024

@author: go29lap
"""

import pyaedt

# Launch AEDT and HFSS (desktop graphical mode or non-graphical mode can be specified)
hfss = pyaedt.Hfss(projectname="Microcoil_Network", designname="8_Port_Microcoil_Design", solution_type="DrivenTerminal")

# Set the frequency sweep range
start_freq = "1MHz"
stop_freq = "50MHz"

# Create the diamond substrate
substrate_thickness = 0.5  # Thickness of the substrate in mm
substrate_length = 10  # Length/Width of the substrate in mm
diamond_material = "Diamond"

hfss.modeler.create_box([0, 0, 0], [substrate_length, substrate_length, substrate_thickness], name="Diamond_Substrate", matname=diamond_material)

# Create microcoils made of gold (approximating radial layout)
num_ports = 8
coil_radius = 2  # mm
coil_thickness = 0.1  # mm (gold wire thickness)
coil_height = 0.1  # mm (height of the coil)
coil_material = "Gold"
center_point = [substrate_length / 2, substrate_length / 2, substrate_thickness]  # Center of the substrate

# Create each microcoil (positioned radially)
for i in range(num_ports):
    angle = (360 / num_ports) * i  # Calculate angle for each coil
    # Create start and end points for each radial coil
    x_start = center_point[0]
    y_start = center_point[1]
    
    x_end = center_point[0] + coil_radius * pyaedt.modeler.geometry_operations.cos(angle)
    y_end = center_point[1] + coil_radius * pyaedt.modeler.geometry_operations.sin(angle)
    
    hfss.modeler.create_cylinder(cs_axis="Z", position=[x_start, y_start, substrate_thickness], radius=coil_thickness, height=coil_height, name=f"Coil_{i+1}", matname=coil_material)

    # Add excitation ports to the ends of the coils
    hfss.create_lumped_port(f"Port_{i+1}", [x_end, y_end, substrate_thickness], [x_end, y_end, substrate_thickness + coil_height])

# Setup the analysis
hfss.insert_setup("Setup1")
hfss.setup_options["Frequency"] = "10MHz"  # Nominal setup frequency
hfss.insert_frequency_sweep("Setup1", start_freq, stop_freq, count=1000)

# Run the simulation
hfss.analyze_setup("Setup1")

# Save project
hfss.save_project()

# Plot S-Parameters (S11, S21, etc.) on a Smith chart
hfss.post.create_report(
    expressions="S11",
    primary_sweep_variable="Freq",
    output_type="Smith Chart",
    report_category="S Parameters"
)

# Export the S-parameters
s_params_file = r"C:\path_to_export\SParameters.s2p"
hfss.export_touchstone("Setup1", s_params_file)

# Close AEDT (comment out if you want to keep AEDT running)
hfss.release_desktop()

