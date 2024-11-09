# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 20:51:13 2024

@author: Stierlab
"""

from pyaedt import Hfss

# Launch HFSS and create a new project
hfss = Hfss()

# Load an existing project
project_path = r"C:\path_to_your_project\your_project.aedt"  # Replace with your project path
hfss.load_project(project_path)

# Set the active design
hfss.set_active_design("Your_Design_Name")  # Replace with your design name

# Define or modify parameters
hfss["Wire_Diameter"] = "20um"
hfss["Coil_Pad_Size"] = "500um"
hfss["Enclosed_Area"] = "100um"

# Modify the width of all polylines to 20 um
for obj in hfss.modeler.objects:
    if hfss.modeler.objects[obj].object_type == "Polyline":
        hfss.modeler.change_property(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers", obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Width",
                            "Value:=", "20um"
                        ]
                    ]
                ]
            ]
        )

# Set up a simulation
setup = hfss.create_setup(setupname="Setup1")
setup.props["Frequency"] = "1GHz"
setup.props["MaximumPasses"] = 10
setup.props["MinimumPasses"] = 2
setup.props["MaxDeltaS"] = 0.02
setup.update()

# Run the simulation
hfss.analyze_setup("Setup1")

# Export results
report = hfss.post.create_report("Inductance", "Setup1", "Rectangular Plot")
report.export_to_file("inductance.csv")

# Save the project
hfss.save_project()

# Release the HFSS instance
hfss.release_desktop()

