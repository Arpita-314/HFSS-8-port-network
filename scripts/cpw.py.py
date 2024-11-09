import ScriptEnv
ScriptEnv.Initialize(AnsoftHfss)

# Open HFSS
oDesktop = oDesktop
oProject = oDesktop.NewProject()
oDesign = oProject.InsertDesign(HFSS, CPW_Design, DrivenModal, )

# Define variables (units in mm)
width_signal = 3.0    # Width of signal line
gap = 2.0             # Gap between signal line and ground
height_substrate = 1.0 # Height of the substrate
length = 50.0         # Length of the waveguide

# Create the substrate
oDesign.SetActiveEditor(3D Modeler)
oEditor = oDesign.SetActiveEditor(3D Modeler)
oEditor.CreateBox(
    [
        NAMEBoxParameters,
        XPosition=, -{0}2.format(length),
        YPosition=, -{0}2.format(width_signal + 2gap),
        ZPosition=, 0,
        XSize=, {0}.format(length),
        YSize=, {0}.format(width_signal + 2gap),
        ZSize=, -{0}.format(height_substrate)
    ], 
    [
        NAMEAttributes,
        Name=, Substrate,
        MaterialValue=, FR4_Epoxy,
        Transparency=, 0.7
    ])

# Create the signal line
oEditor.CreateRectangle(
    [
        NAMERectangleParameters,
        IsCovered=, True,
        XStart=, -{0}2.format(length),
        YStart=, -{0}2.format(width_signal),
        ZStart=, 0,
        Width=, {0}.format(length),
        Height=, {0}.format(width_signal),
        WhichAxis=, Z
    ], 
    [
        NAMEAttributes,
        Name=, Signal,
        MaterialValue=, copper,
    ])

# Create the ground planes
for y_offset in [-1, 1]
    oEditor.CreateRectangle(
        [
            NAMERectangleParameters,
            IsCovered=, True,
            XStart=, -{0}2.format(length),
            YStart=, {0}2 + {1}.format(width_signal, y_offsetgap),
            ZStart=, 0,
            Width=, {0}.format(length),
            Height=, {0}2.format(width_signal + 2gap),
            WhichAxis=, Z
        ], 
        [
            NAMEAttributes,
            Name=, Ground_{0}.format(Top if y_offset == 1 else Bottom),
            MaterialValue=, copper,
        ])

# Define excitation ports
oModule = oDesign.GetModule(BoundarySetup)
oModule.AssignWavePort(
    [
        NAMEPort1,
        Objects=, [Signal],
        Faces=, [oEditor.GetFaceIDs([Signal])[0]],
        NumModes=, 1,
        RenormalizeAllTerminals=, True,
        DoDeembed=, False
    ])

# Analysis Setup
oModule = oDesign.GetModule(AnalysisSetup)
oModule.InsertSetup(
    Setup1, 
    [
        NAMESetup1,
        Frequency=, 10GHz,
        MaxDeltaS=, 0.02,
        PortsOnly=, False,
        UseMatrixConv=, False
    ])
oModule.InsertFrequencySweep(
    Setup1, 
    [
        NAMESweep1,
        StartValue=, 1GHz,
        StopValue=, 20GHz,
        Type=, Interpolating,
        SaveFields=, False
    ])

# Solve
oDesign.AnalyzeAll()

# Check the impedance
oModule = oDesign.GetModule(Solutions)
oModule.CreateReport(ImpedancePlot, Modal Solution Data, Rectangular Plot, Setup1  Sweep1, 
    [X Component=, Freq, Y Component=, Zpi(Port1, Port1)])

# Export the results
oModule.ExportToFile(ImpedancePlot, impedance_results.csv)

# Save the project
oProject.SaveAs(CPW_Design.aedt, True)
