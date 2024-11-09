# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 12:22:28 2024

@author: go29lap
"""

# -- coding: utf-8 --

import ScriptEnv
import math

# Initialize the HFSS environment
ScriptEnv.Initialize('Ansoft.ElectronicsDesktop')
oDesktop = ScriptEnv.GetDesktop()
oDesktop.RestoreWindow()

# Check if there's an active project, if not, create a new one
try:
    oProject = oDesktop.GetActiveProject()
except:
    oProject = oDesktop.NewProject()

# Check if there's an active design, if not, create a new one
try:
    oDesign = oProject.GetActiveDesign()
except:
    oDesign = oProject.InsertDesign('HFSS', 'HFSSDesign1', 'DrivenModal', '')

# Set the active editor to 3D Modeler
oEditor = oDesign.SetActiveEditor('3D Modeler')
print(oEditor)

# Define parameters
substrate_size = 4  # mm
substrate_thickness = 0.5  # mm
microcoil_width = 0.01  # mm
microcoil_thickness = 0.0002  # mm

# Create ground plane
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-2mm",
        "YPosition:=", "-2mm",
        "ZPosition:=", "0mm",
        "XSize:=", "4mm",
        "YSize:=", "4mm",
        "ZSize:=", "0.001mm"
    ],
    [
        "NAME:Attributes",
        "Name:=", "GndPlane",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0.8,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "copper",
        "SolveInside:=", False
    ])

# Create diamond substrate
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-2mm",
        "YPosition:=", "-2mm",
        "ZPosition:=", "0mm",
        "XSize:=", "4mm",
        "YSize:=", "4mm",
        "ZSize:=", "0.5mm"
    ],
    [
        "NAME:Attributes",
        "Name:=", "Diamond",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0.8,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "diamond",
        "SolveInside:=", True
    ])

# Import the DXF file
oEditor.ImportDXF(
    ["NAME:Microcoils",
     "FileName:=", "C:/Users/go29lap/code/ansys/microcoils_v3.dxf",
     "Scale:=", 0.001,
     "AutoDetectClosed:=", True,
     "SelfStitch:=", True,
     "DefeatureGeometry:=", False,
     "DefeatureDistance:=", 0,
     "RoundCoordinates:=", False,
     "RoundNumDigits:=", 4,
     "WritePolyWithWidthAsFilledPoly:=", False,
     "ImportMethod:=", 1,
     "2DSheetBodies:=", True,
     ["NAME:LayerInfo",
      ["NAME:0",
       "source:=", "0",
       "display_source:=", "0",
       "import:=", True,
       "dest:=", "0",
       "dest_selected:=", False,
       "layer_type:=", "signal"
       ],
      ["NAME:LAYER_1",
       "source:=", "LAYER_1",
       "display_source:=", "LAYER_1",
       "import:=", False,
       "dest:=", "LAYER_1",
       "dest_selected:=", False,
       "layer_type:=", "signal"
       ],
      ["NAME:LAYER_2",
       "source:=", "LAYER_2",
       "display_source:=", "LAYER_2",
       "import:=", False,
       "dest:=", "LAYER_2",
       "dest_selected:=", False,
       "layer_type:=", "signal"
       ]
      ]
     ])

# Get all imported sheet objects
all_objects = oEditor.GetObjectsInGroup("Sheets")

# Define the height increase
height_increase = "0.5mm"

# Move each imported object upward
for obj in all_objects:
    if obj.startswith("0"):
        oEditor.Move(
            [
                "NAME:Selections",
                "Selections:=", obj,
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:TranslateParameters",
                "TranslateVectorX:=", "0mm",
                "TranslateVectorY:=", "0mm",
                "TranslateVectorZ:=", height_increase
            ])

# Unite the imported sheets
sheet_objects = [obj for obj in all_objects if obj.startswith("0")]
if len(sheet_objects) > 1:
    oEditor.Unite(
        [
            "NAME:Selections",
            "Selections:=", ",".join(sheet_objects)
        ],
        [
            "NAME:UniteParameters",
            "KeepOriginals:=", False
        ])

# Create wave ports
port_width = microcoil_width
port_height = microcoil_thickness
port_positions = [
    (2, -1.170478567), (1.201158763, 2), (0, 2),
    (-1.019214464, 2), (-2, 1.201158763),
    (-2, -1.019214464), (-1.201158763, -2),
    (1.050351405, -2)
]

for i, (x, y) in enumerate(port_positions):
    port_name = "WavePort_{0}".format(i + 1)
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", "{0}mm".format(x - port_width / 2),
            "YStart:=", "{0}mm".format(y - port_width / 2),
            "ZStart:=", height_increase,
            "Width:=", "{0}mm".format(port_width),
            "Height:=", "{0}mm".format(port_width),
            "WhichAxis:=", "Z"
        ],
        [
            "NAME:Attributes",
            "Name:=", port_name,
            "Flags:=", "",
            "Color:=", "(0 0 255)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "vacuum",
            "SolveInside:=", True
        ])

# Assign wave ports
oModule = oDesign.GetModule("BoundarySetup")
for i in range(1, 9):
    port_name = "WavePort_{0}".format(i)
    oModule.AssignWavePort(
        [
            "NAME:" + port_name,
            "Objects:=", [port_name],
            "NumModes:=", 1,
            "RenormalizeAllTerminals:=", True,
            "UseLineModeAlignment:=", False,
            "DoDeembed:=", False,
            [
                "NAME:Modes",
                [
                    "NAME:Mode1",
                    "ModeNum:=", 1,
                    "UseIntLine:=", True,
                    [
                        "NAME:IntLine",
                        "Start:=", ["{0}mm".format(port_positions[i - 1][0]), "{0}mm".format(port_positions[i - 1][1]), height_increase],
                        "End:=", ["{0}mm".format(port_positions[i - 1][0]), "{0}mm".format(port_positions[i - 1][1] + port_width), height_increase]
                    ],
                    "AlignmentGroup:=", 0,
                    "CharImp:=", "Zpi"
                ]
            ],
            "ShowReporterFilter:=", False,
            "ReporterFilter:=", [True],
            "UseAnalyticAlignment:=", False
        ])

# Create radiation boundary
radiation_boundary_offset = 0.3  # mm
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "{0}mm".format(-substrate_size / 2 - radiation_boundary_offset),
        "YPosition:=", "{0}mm".format(-substrate_size / 2 - radiation_boundary_offset),
        "ZPosition:=", "0mm",
        "XSize:=", "{0}mm".format(substrate_size + 2 * radiation_boundary_offset),
        "YSize:=", "{0}mm".format(substrate_size + 2 * radiation_boundary_offset),
        "ZSize:=", "{0}mm".format(substrate_thickness + 2 * float(height_increase.strip('mm')) + 2 * radiation_boundary_offset),
    ],
    [
        "NAME:Attributes",
        "Name:=", "RadiationBoundary",
        "Flags:=", "",
        "Color:=", "(0 0 255)",
        "Transparency:=", 0.8,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "vacuum",
        "SolveInside:=", False
    ])

# Assign radiation boundary condition
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignRadiation(
    [
        "NAME:Rad1",
        "Objects:=", ["RadiationBoundary"],
        "IsFssReference:=", False,
        "IsForPML:=", False
    ])

# Mesh operations
oMeshSetup = oDesign.GetModule("MeshSetup")

# Surface approximation for the microcoils
oMeshSetup.AssignLengthOp(
    [
        "NAME:Length_Microcoils",
        "RefineInside:=", True,
        "Enabled:=", True,
        "Objects:=", ["0"],
        "RestrictElem:=", False,
        "NumMaxElem:=", "1000",
        "RestrictLength:=", True,
        "MaxLength:=", "{0}mm".format(microcoil_width),
    ])

# Surface approximation for the wave ports
for i in range(1, 9):
    port_name = "WavePort_{}".format(i)
    oMeshSetup.AssignLengthOp(
        [
            "NAME:Length_{}".format(port_name),
            "RefineInside:=", True,
            "Enabled:=", True,
            "Objects:=", [port_name],
            "RestrictElem:=", False,
            "NumMaxElem:=", "1000",
            "RestrictLength:=", True,
            "MaxLength:=", "{0}mm".format(microcoil_width / 5)
        ])

# Set up analysis
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup("HfssDriven",
                    [
                        "NAME:Setup1",
                        "AdaptMultipleFreqs:=", True,
                        "Frequency:=", "25MHz",
                        "MaxDeltaS:=", 0.02,
                        "PortsOnly:=", False,
                        "UseMatrixConv:=", False,
                        "MaximumPasses:=", 6,
                        "MinimumPasses:=", 1,
                        "MinimumConvergedPasses:=", 1,
                        "PercentRefinement:=", 30,
                        "IsEnabled:=", True,
                        "BasisOrder:=", 1,
                        "DoLambdaRefine:=", True,
                        "DoMaterialLambda:=", True,
                        "SetLambdaTarget:=", False,
                        "Target:=", 0.3333,
                        "UseMaxTetIncrease:=", False,
                        "PortAccuracy:=", 2,
                        "UseABCOnPort:=", False,
                        "SetPortMinMaxTri:=", False,
                        "UseDomains:=", False,
                        "UseIterativeSolver:=", False,
                        "SaveRadFieldsOnly:=", False,
                        "SaveAnyFields:=", True,
                        "IESolverType:=", "Auto",
                        "LambdaTargetForIESolver:=", 0.15,
                        "UseDefaultLambdaTgtForIESolver:=", True
                    ])

# Set up frequency sweep
oModule.InsertFrequencySweep("Setup1",
                             [
                                 "NAME:Sweep",
                                 "IsEnabled:=", True,
                                 "RangeType:=", "LinearStep",
                                 "RangeStart:=", "1MHz",
                                 "RangeEnd:=", "50MHz",
                                 "RangeStep:=", "1MHz",
                                 "Type:=", "Interpolating",
                                 "SaveFields:=", False,
                                 "SaveRadFields:=", False,
                                 "ExtrapToDC:=", False
                             ])

# Create reports (S-parameters and Z-parameters)
oModule = oDesign.GetModule("ReportSetup")

# S-parameters
for param in ["dB(S(1,1))", "dB(S(2,1))", "dB(S(2,2))"]:
    oModule.CreateReport("S_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep",
                         [
                             "Domain:=", "Sweep"
                         ],
                         [
                             "Freq:=", ["All"]
                         ],
                         [
                             "X Component:=", "Freq",
                             "Y Component:=", [param]
                         ], [])

# Z-parameters
for param in [["re(Z(1,1))", "im(Z(1,1))"], ["re(Z(2,1))", "im(Z(2,1))"]]:
    oModule.CreateReport("Z_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep",
                         [
                             "Domain:=", "Sweep"
                         ],
                         [
                             "Freq:=", ["All"]
                         ],
                         [
                             "X Component:=", "Freq",
                             "Y Component:=", param
                         ], [])

# Save the project
oProject.Save()

# Analyze
oDesign.Analyze("Setup1")
