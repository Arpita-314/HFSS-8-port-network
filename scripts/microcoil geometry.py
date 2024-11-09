# -*- coding: utf-8 -*-

import ScriptEnv
import math

# Initialize the HFSS environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

# Check if there's an active project, if not, create a new one
oProject = oDesktop.GetActiveProject()
if oProject is None:
    oProject = oDesktop.NewProject()

# Check if there's an active design, if not, create a new one
oDesign = oProject.GetActiveDesign()
if oDesign is None:
    oDesign = oProject.InsertDesign("HFSS", "HFSSDesign1", "DrivenModal", "")

# Set the active editor to 3D Modeler
oEditor = oDesign.SetActiveEditor("3D Modeler")

# Parameters for the microstrip geometry
width = 110e-3  # Width of the microstrip line (110 µm converted to mm)
radius = 2.88  # Radius for the curved sections (from center to end, 2.88 mm)
length = 4.0  # Length of the straight sections (total span, 4 mm)
thickness = 0.035  # Thickness of the microstrip line (adjust as needed)

# Create equation-based curve for one arm
def create_microstrip_arm(angle):
    # Parametric equation for a U-shaped arm without using if statements
    # Let's use a smooth function that covers the curve and the straight section
    eq_x = "{0}*cos(pi*t) + ({1}-{0})*t".format(radius, length)
    eq_y = "{0}*sin(pi*t)".format(radius)
    
    arm_name = "MicrostripArm_{0}".format(int(angle * 180 / math.pi))
    
    oEditor.CreateEquationCurve(
        [
            "NAME:EquationBasedCurveParameters",
            "XtFunction:=", eq_x,
            "YtFunction:=", eq_y,
            "ZtFunction:=", "0mm",
            "tStart:=", "0",
            "tEnd:=", "1",
            "NumOfPoints:=", "1001"
        ],
        [
            "NAME:Attributes",
            "Name:=", arm_name,
            "Flags:=", "",
            "Color:=", "(255 215 0)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "copper",
            "SolveInside:=", True
        ])
    
    # Rotate the arm to the correct orientation
    oEditor.Rotate(
        [
            "NAME:Selections",
            "Selections:=", arm_name
        ],
        [
            "NAME:RotateParameters",
            "RotateAxis:=", "Z",
            "RotateAngle:=", "{0}deg".format(angle)
        ])
    
    return arm_name

# Create all 8 arms of the microstrip geometry
angles = [0, 45, 90, 135, 180, 225, 270, 315]
arm_names = []

for angle in angles:
    arm_names.append(create_microstrip_arm(angle))

# Unite all arms into a single structure
oEditor.Unite(
    [
        "NAME:Selections",
        "Selections:=", ",".join(arm_names)
    ],
    [
        "NAME:UniteParameters",
        "KeepOriginals:=", False
    ])

# Rename the united structure
oEditor.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:Geometry3DAttributeTab",
            ["NAME:PropServers", arm_names[0]],
            ["NAME:ChangedProps", ["NAME:Name", "Value:=", "MicrostripStructure"]]
        ]
    ])
