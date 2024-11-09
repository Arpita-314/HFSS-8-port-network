# Import the necessary HFSS modules
import ScriptEnv
ScriptEnv.Initialize("Ansoft.HFSS")

oDesktop = oDesktop
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "MicrostripDesign", "DrivenModal", "")

oDesign = oProject.SetActiveDesign("MicrostripDesign")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oModule = oDesign.GetModule("BoundarySetup")

# Define parameters
freq = "10GHz"
substrate_height = "0.5mm"
trace_width = "1mm"
trace_length = "10mm"
substrate_permittivity = "5.7"
conductor_thickness = "0.035mm"
substrate_size = "20mm"  # Dimensions of the substrate

# Create the substrate (diamond)
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "-substrate_size/2",
        "YPosition:=", "-substrate_size/2",
        "ZPosition:=", "0mm",
        "XSize:=", "substrate_size",
        "YSize:=", "substrate_size",
        "ZSize:=", substrate_height
    ],
    [
        "NAME:Attributes",
        "Name:=", "Substrate",
        "MaterialValue:=", "\"diamond\"",
        "SolveInside:=", True
    ]
)

# Create the microstrip line (gold trace)
oEditor.CreateRectangle(
    [
        "NAME:RectangleParameters",
        "IsCovered:=", True,
        "XStart:=", "-trace_length/2",
        "YStart:=", "0mm",
        "ZStart:=", substrate_height,
        "Width:=", "trace_length",
        "Height:=", trace_width,
        "WhichAxis:=", "X"
    ],
    [
        "NAME:Attributes",
        "Name:=", "MicrostripLine",
        "MaterialValue:=", "\"gold\"",
        "SolveInside:=", False
    ]
)

# Assign Perfect E boundary to the microstrip line
oModule.AssignPerfectE(
    [
        "NAME:PerfE1",
        "Objects:=", ["MicrostripLine"]
    ]
)

# Create ground plane at the bottom of the substrate
oEditor.CreateRectangle(
    [
        "NAME:RectangleParameters",
        "IsCovered:=", True,
        "XStart:=", "-substrate_size/2",
        "YStart:=", "-substrate_size/2",
        "ZStart:=", "0mm",
        "Width:=", "substrate_size",
        "Height:=", "substrate_size",
        "WhichAxis:=", "Z"
    ],
    [
        "NAME:Attributes",
        "Name:=", "GroundPlane",
        "MaterialValue:=", "\"gold\"",
        "SolveInside:=", False
    ]
)

# Assign Perfect E boundary to the ground plane
oModule.AssignPerfectE(
    [
        "NAME:PerfE2",
        "Objects:=", ["GroundPlane"]
    ]
)

# Create a wave port for the input signal
oEditor.CreateRectangle(
    [
        "NAME:RectangleParameters",
        "IsCovered:=", True,
        "XStart:=", "-trace_width/2",
        "YStart:=", "-substrate_size/2",
        "ZStart:=", substrate_height,
        "Width:=", "trace_width",
        "Height:=", substrate_height,
        "WhichAxis:=", "Y"
    ],
    [
        "NAME:Attributes",
        "Name:=", "WavePort",
        "MaterialValue:=", "\"gold\"",
        "SolveInside:=", False
    ]
)

# Assign wave port excitation
oModule.AssignWavePort(
    [
        "NAME:WavePort1",
        "Objects:=", ["WavePort"],
        "NumModes:=", 1,
        "RenormalizeAllTerminals:=", True,
        "DoDeembed:=", False
    ],
    [
        "NAME:Modes",
        [
            "NAME:Mode1",
            "ModeNum:=", 1,
            "UseIntLine:=", False,
            "CharImp:=", "Zpi",
            "AlignmentGroup:=", 0,
            "RenormImp:=", 50
        ]
    ]
)

# Set up analysis
oDesign.SetSolutionType("DrivenModal")
oDesign.CreateSetup(
    [
        "NAME:Setup1",
        "Frequency:=", freq,
        "PortsOnly:=", False,
        "MaxDeltaS:=", 0.02,
        "UseMatrixConv:=", False,
        "MaximumPasses:=", 20,
        "MinimumPasses:=", 2,
        "MinimumConvergedPasses:=", 2,
        "PercentRefinement:=", 30,
        "IsEnabled:=", True
    ]
)

# Define the frequency sweep
oDesign.CreateFrequencySweep(
    [
        "NAME:Sweep1",
        "StartValue:=", "8GHz",
        "StopValue:=", "12GHz",
        "Type:=", "LinearStep",
        "Increment:=", "0.05GHz",
        "IsEnabled:=", True
    ]
)

# Analyze the setup
oDesign.Analyze("Setup1")

# Export S11 parameter results
oModule.ExportToFile("Setup1:Sweep1", "S11_Parameters.csv")
print("S11 parameters exported successfully to S11_Parameters.csv")

# Plot the Smith chart
oModule.CreateReport(
    "S11_SmithChart", "Smith Chart", "Rectangular Plot", "Setup1:Sweep1",
    [
        "NAME:Context",
        "Domain:=", "Frequency"
    ],
    [
        "NAME:Trace",
        "X Component:=", "re(S(1,1))",
        "Y Component:=", "im(S(1,1))"
    ]
)
