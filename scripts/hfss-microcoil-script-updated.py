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

# check with different metals and whether the skin depth for that metal matters or not
oModule.AssignSkinDepthOp

([

"NAME:SkinDepth1", 

"Faces:=", [7], 

"RestrictElem:=", True, 

"NumMaxElem:=", 1000, 

"SkinDepth:=", "1mm", 

"SurfTriMaxLength:=", "1mm", 

"NumLayers:=", 2

])

# Create diamond substrate
substrate_name = "DiamondSubstrate_1"
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-2mm",
        "YPosition:=", "-2mm",
        "ZPosition:=", "0mm",
        "XSize:=", "{0}mm".format(substrate_size),
        "YSize:=", "{0}mm".format(substrate_size),
        "ZSize:=", "{0}mm".format(substrate_thickness)
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

# Import the DXF file
oEditor.ImportDXF(
    ["NAME:options",
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

# Thicken the imported sheets
oEditor.ThickenSheet(
    ["NAME:Selections",
     "Selections:=", "0",
     "NewPartsModelFlag:=", "Model"
    ],
    ["NAME:SheetThickenParameters",
     "Thickness:=", "200nm",
     "BothSides:=", False
    ])

#add material dielectric loss of Au
oDefinitionManager.AddMaterial(

["permittivity:=", "2.2", "0.002"])
#should i put the code for the skin depth
#material 2 layer Au and Ti
#consider the dielectric loss
#figure out the crosstalk

#dieelectric loss
oDefinitionManager.AddMaterial(
    ["NAME:Material2",_
    
    "dielectric_loss_tangent:=", 44,
    
    Array("NAME:saturation_mag",_ D
    
    "property_type:=", "AnisoProperty",_
    
    "unit:=", "Gauss",_
    
    "component1:=", "11", _
    
    "component2:=", "22", _ 
    
    "component3:=", "33"), _
    
    "delta_H:=", "44Oe"])

#add material dieelectric loss of Ti

#=======================================================
#here you need to create equation based curve 
oEditor.CreateEquationCurve(

    ["NAME:EquationBasedCurveParameters",
    
    "XtFunction:="		, "1",
    
    "YtFunction:="		, "3",
    
    "ZtFunction:="		, "32",
    
    "tStart:="		, "1",
    
    "tEnd:="		, "3",
    
    "NumOfPointsOnCurve:="	, "0",
    
    "Version:="		, 1,
    ]
    
    ["NAME:PolylineXSection",
    
    "XSectionType:="	, "None",
    
    "XSectionOrient:="	, "Auto",
    
    "XSectionWidth:="	, "0",
    
    "XSectionTopWidth:="	, "0",
    
    "XSectionHeight:="	, "0",
    
    "XSectionNumSegments:="	, "0",
    
    "XSectionBendType:="	, "Corner"
    
    ]

),

    ["NAME:Attributes",
    
    "Name:="		, "EquationCurve1",
    
    "Flags:="		, "",
    
    "Color:="		, "(143 175 143)",
    
    "Transparency:="	, 0,
    
    "PartCoordinateSystem:=", "Global",
    
    "UDMId:="		, "",
    
    "MaterialValue:="	, "\"copper\"",
    
    "SurfaceMaterialValue:=", "\"\"",
    
    "SolveInside:="		, False,
    
    "ShellElement:="	, False,
    
    "ShellElementThickness:=", "0mm",
    
    "IsMaterialEditable:="	, True,
    
    "UseMaterialAppearance:=", False,
    
    "IsLightweight:="	, False
    
    ])
#================================================================

#UDM might be worth a try but python scripting is way better
oEditor.CreateUserDefinedModel(

["NAME:UserDefinedModelParameters",

["NAME:Definition"],

["NAME:Options"],

["NAME:GeometryParams",

["NAME:UDMParam",

"Name:="		, "WaveguideRadius",

"Value:="		, "5mm",

"PropType2:="		, 3,

"PropFlag2:="		, 4

],

["NAME:UDMParam",

"Name:="		, "WaveguideLength",

"Value:="		, "10mm",

"PropType2:="		, 3,

"PropFlag2:="		, 4

],

["NAME:UDMParam",

"Name:="		, "FlareAngle",

"Value:="		, "32deg",

"PropType2:="		, 3,

"PropFlag2:="		, 4

],

["NAME:UDMParam",

"Name:="		, "NumberOfNotches",

"Value:="		, "12",

"PropType2:="		, 3,

"PropFlag2:="		, 2

],

["NAME:UDMParam",

"Name:="		, "WidthOfNotch",

"Value:="		, "1mm",

"PropType2:="		, 3,

"PropFlag2:="		, 4

],

["NAME:UDMParam",

"Name:="		, "DepthOfNotch",

"Value:="		, "2mm",

"PropType2:="		, 3,

"PropFlag2:="		, 4

],

["NAME:UDMParam",

"Name:="		, "WidthOfTooth",

"Value:="		, "2mm",

"PropType2:="		, 3,

"PropFlag2:="		, 4

],

["NAME:UDMParam",

"Name:="		, "WallThickness",

"Value:="		, "2.5mm",

"PropType2:="		, 3,

"PropFlag2:="		, 4

]

],

"DllName:="		, "HFSS/Antenna Toolkit/Horn/Corrugated.py",

"Library:="		, "syslib",

"Version:="		, "1.1",

"ConnectionID:="	, ""

])
#==========================================================

# Create wave ports
port_width = microcoil_width
port_positions = [
    (2, -1.170478567), (1.201158763, 2), (0, 2), 
    (-1.019214464, 2), (-2, 1.201158763),
    (-2, -1.019214464), (-1.201158763, -2),
    (1.050351405, -2)
]

for i, (x, y) in enumerate(port_positions):
    port_name = "WavePort_{0}".format(i+1)
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:=", True,
            "XStart:=", "{0}mm".format(x - port_width/2),
            "YStart:=", "{0}mm".format(y - port_width/2),
            "ZStart:=", "{0}mm".format(substrate_thickness),
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

# Project sheet to connect the waveports with the wires
oEditor.ProjectSheet(
    ['NAME:Selections',
     'Selections:=','hWavePort_1, WavePort_2,WavePort_3,WavePort_4,WavePort_5,WavePort_6,WavePort_7,WavePort_8'],
    ['NAME:ProjectSheetParameters',
     'Thickness:=', '0mm']
)

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
oModule = oDesign.GetModule("BoundarySetup") #looks like an extra step
oModule.AssignRadiation(
    [
        "NAME:Rad1",
        "Objects:=", ["RadiationBoundary"],
        "IsFssReference:=", False,
        "IsForPML:=", False
    ])

# Assign wave ports (sizing of the waveports matter)
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
                    "UseIntLine:=", True
                ]
            ],
            "ShowReporterFilter:=", False,
            "ReporterFilter:=", [True],
            "UseAnalyticAlignment:=", False
        ])

# autocreate PECCapfor WavePort
AutoCreatePECCapForWavePort(

[

"NAME:AutoCreatePECCapForWavePort",

"Wave Port Name:="	, "2",

"Face ID:="		, 280,

"Flip Side:="		, False,

"Thickness:="		, "0.18mm"

])

#initiation of port impedances
oNDE = oDesktop.GetTool("ndExplorer")

oPostProc.SetAllPortImpedances([23, "2+3i", 50]) -or- oData.SetAllPortImpedances(50) 	

#edit impedance

oModule.AssignImpedance("Imped1"

["NAME:Imped1After",

"Resistance:=", "50",

"Reactance:=", "50",

"InfGroundPlane:=", False]

)
#to assign different material for different metals
#assign material
oEditor.AssignMaterial(

["NAME:Selections",

"AllowRegionDependentPartSelectionForPMLCreation:=", True,

"AllowRegionSelectionForPMLCreation:=", True,

"Selections:=" , "Box1"

],

["NAME:Attributes",

"MaterialValue:=" , "diamond",

"SolveInside:="	, False,

"ShellElement:=" , False,

"ShellElementThickness:=" , "nan",

"IsMaterialEditable:=" , True,

"UseMaterialAppearance:=" , False,

"IsLightweight:=" , False

])
#assign bondwire
oEditor.CreateBondwire(

["NAME:BondwireParameters",

"WireType:="		, "JEDEC_4Points",

"WireDiameter:="	, "0.025mm",

"NumSides:="		, "6",

"XPadPos:="		, "1.6mm",

"YPadPos:="		, "-0.2mm",

"ZPadPos:="		, "0mm",

"XDir:="		, "-2.2mm",

"YDir:="		, "-1.4mm",

"ZDir:="		, "0mm",

"Distance:="		, "2.60768096208106mm",

"h1:="			, "0.2mm",

"h2:="			, "0mm",

"alpha:="		, "80deg",

"beta:="		, "0",

"WhichAxis:="		, "Z",

"ReverseDirection:="	, True

],

["NAME:Attributes",

"Name:="		, "Bondwire1",

"Flags:="		, "",

"Color:="		, "(143 175 143)",

"Transparency:="	, 0,

"PartCoordinateSystem:=", "Global",

"UDMId:="		, "",

"MaterialValue:="	, "\"vacuum\"",

"SurfaceMaterialValue:=", "\"\"",

"SolveInside:="		, True,

"ShellElement:="	, False,

"ShellElementThickness:=", "0mm",

"IsMaterialEditable:="	, True,

"UseMaterialAppearance:=", False,

"IsLightweight:="	, False

])

#initiation of mesh
oModule.InitialMeshSettings

([

"NAME:MeshSettings",

[

"NAME:GlobalSurfApproximation",

"CurvedSurfaceApproxChoice:=", "UseSlider",

"SliderMeshSettings:="	, 7

],

[

"NAME:GlobalCurvilinear",

"Apply:="		, False

],

[

"NAME:GlobalModelRes",

"UseAutoLength:="	, True

],

"MeshMethod:="		, "Auto",

"UseLegacyFaceterForTAUVolumeMesh:=", False,

"DynamicSurfaceResolution:=", False,

"UseFlexMeshingForTAUvolumeMesh:=", False,

"UseAlternativeMeshMethodsAsFallBack:=", False,

"AllowPhiForLayeredGeometry:=", True


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
        "RangeType:=", "LinearStep", #intepolating an fast step is more better
        "RangeStart:=", "1MHz",
        "RangeEnd:=", "50MHz",
        "RangeStep:=", "1MHz",
        "Type:=", "Discrete",
        "SaveFields:=", False,
        "SaveRadFields:=", False,
        "ExtrapToDC:=", False #don't understand this part of the code
    ])

#questions which I don't know the answers to?
# s11 and s21 and z11 and z21 parameters are important and gamma parameters
# add diamond antennae since the impedance of diamond antennae is going to affect the impedance of the microcoils

# figure out the crosstalk between diamond antennae and microcoils
# which part of the code should I put the near and far field region?
# microcoils is multifrequency while diamond is single frequency. how does this effect theimpedance matching?

# does doping of nvs affects the impedance? should since the orientation of NVs affect the gradient magnetic field hence it should affect the impedance? how to incorporate this feature into the simulations?

# include near field and far field setup
oModule.InsertNearFieldLineSetup(

[

"NAME:Line1",

"UseCustomRadiationSurface:=", False,

"Line:="		, "Polyline1",

"NumPts:="		, "1000"

])

# include far field setup
oModule.InsertFarFieldSphereSetup(

[

"NAME:Infinite Sphere1",

"UseCustomRadiationSurface:=", False,

"CSDefinition:="	, "Theta-Phi",

"Polarization:="	, "Linear",

"ThetaStart:="		, "0deg",

"ThetaStop:="		, "180deg",

"ThetaStep:="		, "2deg",

"PhiStart:="		, "-180deg",

"PhiStop:="		, "180deg",

"PhiStep:="		, "2deg",

"UseLocalCS:="		, False

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
oModule.CreateReport("Z_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
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


# Function to generate list of frequencies from 1 MHz to 50 MHz
def generate_frequencies(start_freq, end_freq, step):
    return [f"{freq}MHz" for freq in range(start_freq, end_freq + 1, step)]

#what the hell is this phase about? read up more
# Get user-defined phases
user_phases = input("Enter the phases separated by commas (e.g., 0deg,90deg,180deg): ").split(",")

# Generate frequency list from 1 MHz to 50 MHz
frequencies = generate_frequencies(1, 50, 1)  # Step size is 1 MHz

# Loop over each frequency and phase combination
for freq in frequencies:
    for phase in user_phases:
        oModule.CreateFieldPlot(
            Array("NAME:Mag_E1", 
                  "SolutionName:=", "Setup1 : LastAdaptive", 
                  "QuantityName:=", "Mag_E", 
                  "PlotFolder:=", "E Field1", 
                  "UserSpecifyName:=", 0, 
                  "UserSpecifyFolder:=", 0, 
                  "IntrinsicVar:=", f"Freq='{freq}' Phase='{phase.strip()}'",  # Use user-defined phase
                  "PlotGeomInfo:=", Array(1, "Surface", "FacesList", 1, "7"),  # Adjust face ID as needed
                  "FilterBoxes:=", Array(0),
                  Array("NAME:PlotOnSurfaceSettings", 
                        "Filled:=", False, 
                        "IsoValType:=", "Fringe", 
                        "SmoothShade:=", True, 
                        "AddGrid:=", False, 
                        "MapTransparency:=", True, 
                        "Transparency:=", 0, 
                        "ArrowUniform:=", True, 
                        "ArrowSpacing:=", 0.100000001490116, 
                        "GridColor:=", Array(255, 255, 255))
            )
        )


# Export Z11 parameter dataset
oProject.ExportDataset('e:/tmp/dsdata.txt')

oDesign.ExportDataset('e:/tmp/dsdata.txt')


# Save the project
oProject.Save()

# Analyze
oDesign.Analyze("Setup1")

# Delete
oDesign.Delete("Setup1") 