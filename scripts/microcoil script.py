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

# Define parameters
substrate_size = 4  # mm (400 micrometers)
substrate_thickness = 0.05  # mm (50 micrometers, adjust as needed)
microcoil_width = 0.01  # mm (10 micrometers, adjust as needed)
microcoil_thickness = 0.0002  # mm (200 nm)
center_gap_radius = 0.02  # mm (20 micrometers, adjust as needed)

# Create diamond substrate
substrate_name = "DiamondSubstrate_1"
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-2mm",
        "YPosition:=", "-2mm",
        "ZPosition:=", "0mm",
        "XSize:=", f"{substrate_size}mm",
        "YSize:=", f"{substrate_size}mm",
        "ZSize:=", f"{substrate_thickness}mm"
    ],
    [
        "NAME:Attributes",
        "Name:=", substrate_name,
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0.1,
        "PartCoordinateSystem:=", "Global",
        "MaterialName:=", "diamond",
        "SolveInside:=", True
    ])

# Define the specific end coordinates for each microcoil arm
arm_end_positions = [
    (2, -1.170478567),
    (-2, -1.019214464),
    (1.201158763, 2),
    (-1.019214464, 2),
    (-2, 1.201158763),
    (-2, -1.019214464),
    (-1.201158763, -2),
    (1.050351405, -2)
]

# Function to create a single microcoil arm
def create_microcoil_arm(index, end_x, end_y):
    start_x, start_y = 0, 0  # Assuming all arms start from the center
    
    arm_name = f"MicrocoilArm_{index}"
    
    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:=", True,
            "IsPolylineClosed:=", False,
            ["NAME:PolylinePoints",
             ["NAME:PLPoint", "X:=", f"{start_x}mm", "Y:=", f"{start_y}mm", "Z:=", f"{substrate_thickness}mm"],
             ["NAME:PLPoint", "X:=", f"{end_x}mm", "Y:=", f"{end_y}mm", "Z:=", f"{substrate_thickness}mm"]],
            ["NAME:PolylineSegments", ["NAME:PLSegment", "SegmentType:=", "Line", "StartIndex:=", 0, "NoOfPoints:=", 2]],
        ],
        [
            "NAME:Attributes",
            "Name:=", arm_name,
            "Flags:=", "",
            "Color:=", "(255 215 0)",
            "Transparency:=", 0,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "gold",
            "SolveInside:=", True
        ])

    # Thicken the arm
    oEditor.SweepAlongVector(
        [
            "NAME:Selections",
            "Selections:=", arm_name,
            "NewPartsModelFlag:=", "Model"
        ],
        [
            "NAME:VectorSweepParameters",
            "DraftAngle:=", "0deg",
            "DraftType:=", "Round",
            "CheckFaceFaceIntersection:=", False,
            "SweepVectorX:=", "0mm",
            "SweepVectorY:=", "0mm",
            "SweepVectorZ:=", f"{microcoil_thickness}mm"
        ])

    return arm_name

# Create 8 microcoil arms
arm_names = []
for i, (end_x, end_y) in enumerate(arm_end_positions):
    arm_names.append(create_microcoil_arm(i, end_x, end_y))

# Unite all microcoil arms
oEditor.Unite(
    [
        "NAME:Selections",
        "Selections:=", ",".join(arm_names)
    ],
    [
        "NAME:UniteParameters",
        "KeepOriginals:=", False
    ])

# Rename the united object
oEditor.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:Geometry3DAttributeTab",
            ["NAME:PropServers", arm_names[0]],
            ["NAME:ChangedProps", ["NAME:Name", "Value:=", "Microcoil"]]
        ]
    ])

# Import the DXF file
oEditor.ImportDXF(
    [
        "NAME:options",
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

# Create wave ports
port_width = microcoil_width
port_positions = arm_end_positions

for i, (x, y) in enumerate(port_positions):
    port_name = f"WavePort_{i+1}"
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", f"{x - port_width/2}mm",
            "YStart:=", f"{y - port_width/2}mm",
            "ZStart:=", f"{substrate_thickness}mm",
            "Width:=", f"{port_width}mm",
            "Height:=", f"{port_width}mm",
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

# Create radiation boundary
radiation_boundary_offset = 0.3  # mm (300 micrometers)
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", f"{-substrate_size/2 - radiation_boundary_offset}mm",
        "YPosition:=", f"{-substrate_size/2 - radiation_boundary_offset}mm",
        "ZPosition:=", f"{-radiation_boundary_offset}mm",
        "XSize:=", f"{substrate_size + 2*radiation_boundary_offset}mm",
        "YSize:=", f"{substrate_size + 2*radiation_boundary_offset}mm",
        "ZSize:=", f"{substrate_thickness + 2*radiation_boundary_offset}mm"
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

# Assign wave ports
for i in range(1, 9):  # 8 ports
    port_name = f"WavePort_{i}"
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
                    "UseIntLine:=", True
                ]
            ],
            "ShowReporterFilter:=", False,
            "ReporterFilter:=", [True],
            "UseAnalyticAlignment:=", False
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
        "Type:=", "Discrete",
        "SaveFields:=", False,
        "SaveRadFields:=", False,
        "ExtrapToDC:=", False
    ])

# Create reports (S-parameters and Z-parameters)
oModule = oDesign.GetModule("ReportSetup")
oModule.CreateReport("S_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["dB(S(1,1))", "dB(S(2,1))"]
    ], [])

# Z-parameters
oModule.CreateReport("Z_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["re(Z(1,1))", "im(Z(1,1))"]
    ], [])

# Save the project
oProject.Save()

# Analyze
oDesign.Analyze("Setup1")
