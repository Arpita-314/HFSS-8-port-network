# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 18:54:13 2024

@author: go29lap
"""
import ScriptEnv
import math

# Initialize the HFSS environment
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project1")
oDesign = oDesign.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")

# Define parameters
substrate_size = 4  # mm (400 micrometers)
substrate_thickness = 0.05  # mm (50 micrometers, adjust as needed)
microcoil_width = 0.01  # mm (10 micrometers, adjust as needed)
microcoil_thickness = 0.0002  # mm (200 nm)

# Create ground plane
substrate_name = "DiamondSubstrate_1"
oEditor.CreateBox(
        [
                 "NAME:BoxParameters",
                 "XPosition:="      , "-2mm",
                 "YPosition:="      , "-2mm",
                 "ZPosition:="      , "0mm",
                 "XSize:="          , "4mm",
                 "YSize:="          , "4mm",
                 "ZSize:="          , "0.5mm"
         ],
         [
                 "NAME:Attributes",
                 "Name:="                   ,"GndPlane",
                 "Flags:="                  , "",
                 "Color:="                  , "(143 175 143)",
                 "Transparency:="           , 0.8,
                 "PartCoordinateSystem:="   , "Global",
                 "UMDId:="                  , "",
                 "MaterialValue:="          , "diamond",
                 "SolveInside:="            , True
         ])

# Create diamond substrate
substrate_name = "DiamondSubstrate_1"
oEditor.CreateBox(
        [
                 "NAME:BoxParameters",
                 "XPosition:="      , "-2mm",
                 "YPosition:="      , "-2mm",
                 "ZPosition:="      , "0mm",
                 "XSize:="          , "4mm",
                 "YSize:="          , "4mm",
                 "ZSize:="          , "0.5mm"
         ],
         [
                 "NAME:Attributes",
                 "Name:="                   ,"Diamond",
                 "Flags:="                  , "",
                 "Color:="                  , "(143 175 143)",
                 "Transparency:="           , 0.8,
                 "PartCoordinateSystem:="   , "Global",
                 "UMDId:="                  , "",
                 "MaterialValue:="          , "diamond",
                 "SolveInside:="            , True
         ])

# n-port model (magical charm to my simulation stuck for 2 months)
AddNPortData Array("NAME:8 port network",

"ComponentDataType:=", "NportData",

"name:=", <string>, // Name of the item

"filename:=", <string>, // Path to the file to find the data

"numberofports:=", 8,

"filelocation:=", <LocationType>,

"domain:=", <string>, // "time" or "frequency"

"datamode:=", <string> // "EnterData", "Import", or "Link"

"devicename:=", <string>,

"ImpedanceTab:=", True,

"NoiseDataTab:=", False,

"DCBehaviorTab:=", True, #set this to false for AC behaviour

"SolutionName:=", <string>,

"displayformat:=", <DisplayInfo>,

"datatype:=", "SMatrix", "YMatrix", "ZMatrix"

"ShowRefPin:=", <bool>,

"RefNodeCheckbox:=", <bool>, ...

<ProductOptionsInfo>)

# Import the DXF file
oEditor.ImportDXF(
    ["NAME:Selections",
     "FileName:=", "C:/Users/go29lap/code/ansys/microcoils_v3.dxf", #is there a way to define the name of the 3d model here
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

#assign material
oEditor.AssignMaterial(

["NAME:Selections",

"AllowRegionDependentPartSelectionForPMLCreation:=", True,

"AllowRegionSelectionForPMLCreation:=", True,

"Selections:=" , "Box1"

],

["NAME:Attributes",

"MaterialValue:=" , "gold",

"SolveInside:="	, False,

"ShellElement:=" , False,

"ShellElementThickness:=" , "nan",

"IsMaterialEditable:=" , True,

"UseMaterialAppearance:=" , False,

"IsLightweight:=" , False

])

# Thicken the imported sheets
oEditor.ThickenSheet(
     ["NAME:Selections",
      "Selections:=", "0", #selection 0 is the error here - how to solve this error?
      "NewPartsModelFlag:=", "Model"
     ],
     ["NAME:SheetThickenParameters",
      "Thickness:=", "200nm",
      "BothSides:=", False
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

port_centers = []

for i, (x, y) in enumerate(port_positions):
    port_name = "WavePort_{0}".format(i + 1)
    port_centers.append((x, y))
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", "{0}mm".format(x - port_width / 2),
            "YStart:=", "{0}mm".format(y - port_width / 2),
            "ZStart:=", "{0}mm".format(substrate_thickness),
            "Width:=", "{0}mm".format(port_width),
            "Height:=", "{0}mm".format(microcoil_thickness),
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
        ]
    )

# Assign wave ports
oModule = oDesign.GetModule("BoundarySetup")
for i in range(1, 9):  # 8 ports
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
                        "Start:=", ["0mm", "0mm", "0mm"],
                        "End:=", ["0mm", "{0}mm".format(port_height), "0mm"]
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
radiation_boundary_offset = 0.3  # mm (300 micrometers)
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "{0}mm".format(-substrate_size/2 - radiation_boundary_offset),
        "YPosition:=", "{0}mm".format(-substrate_size/2 - radiation_boundary_offset),
        "ZPosition:=", "{0}mm".format(-radiation_boundary_offset),
        "XSize:=", "{0}mm".format(substrate_size + 2*radiation_boundary_offset),
        "YSize:=", "{0}mm".format(substrate_size + 2*radiation_boundary_offset),
        "ZSize:=", "{0}mm".format(substrate_thickness + 2*radiation_boundary_offset)
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
oModule.AssignRadiation(
    [
        "NAME:Rad1",
        "Objects:=", ["RadiationBoundary"],
        "IsFssReference:=", False,
        "IsForPML:=", False
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

# S11-parameters
oModule.CreateReport("S_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["dB(S(1,1))"]
    ], [])

# S21-parameters
oModule.CreateReport("S_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["dB(S(2,1))"]
    ], [])

# Z11-parameters
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

# Z21-parameters
oModule.CreateReport("Z_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
    [
        "Domain:=", "Sweep"
    ], 
    [
        "Freq:=", ["All"]
    ], 
    [
        "X Component:=", "Freq",
        "Y Component:=", ["re(Z(2,1))", "im(Z(2,1))"]
    ], [])

# Save the project
oProject.Save()

# Analyze
oDesign.Analyze("Setup1")
