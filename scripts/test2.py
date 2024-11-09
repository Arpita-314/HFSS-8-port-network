# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 00:12:04 2024

@author: Arpita Paul
"""

import pyaedt

# Initialize HFSS
hfss = pyaedt.Hfss(
    specified_version="2023.1",
    non_graphical=False,
    new_desktop_session=True,
    projectname="Project_name",
    designname="Design_name"
)

# Function to create a trapezoid
def create_trapezoid(center, width_top, width_bottom, height, thickness, name):
    half_width_top = width_top / 2
    half_width_bottom = width_bottom / 2
    half_height = height / 2
    vertices = [
        [center[0] - half_width_bottom, center[1] - half_height, center[2]],  # Bottom left
        [center[0] + half_width_bottom, center[1] - half_height, center[2]],  # Bottom right
        [center[0] + half_width_top, center[1] + half_height, center[2]],     # Top right
        [center[0] - half_width_top, center[1] + half_height, center[2]]      # Top left
    ]
    trapezoid = hfss.modeler.create_polyline(
        position_list=vertices,
        closed=True,
        name=name,
        matname="copper"
    )
    hfss.modeler.thicken_sheet(trapezoid, thickness=thickness)
    return trapezoid

# Create the four trapezoids
center_positions = [
    [-5, -5, 0],
    [5, -5, 0],
    [5, 5, 0],
    [-5, 5, 0]
]
width_top = 6
width_bottom = 12
height = 10
thickness = 1

for i, center in enumerate(center_positions):
    create_trapezoid(center, width_top, width_bottom, height, thickness, f"Trapezoid{i+1}")

# Create an open region
hfss.create_open_region(Frequency="1GHz")

# Assign a radiation boundary
hfss.assign_radiation_boundary_to_objects("Trapezoid1")

# Save and close the project
hfss.save_project()
hfss.close_desktop()
