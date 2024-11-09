import ScriptEnv
import math

def initialize_hfss():
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    oDesktop = ScriptEnv.GetAppDesktop()
    oDesktop.RestoreWindow()
    return oDesktop

def get_or_create_project(oDesktop):
    oProject = oDesktop.GetActiveProject()
    if oProject is None:
        oProject = oDesktop.NewProject()
    return oProject

def get_or_create_design(oProject):
    oDesign = oProject.GetActiveDesign()
    if oDesign is None:
        oDesign = oProject.InsertDesign("HFSS", "HFSSDesign1", "DrivenModal", "")
    return oDesign

try:
    # Initialize HFSS environment
    oDesktop = initialize_hfss()
    oProject = get_or_create_project(oDesktop)
    oDesign = get_or_create_design(oProject)
    oEditor = oDesign.SetActiveEditor("3D Modeler")

    # Define parameters
    substrate_size = 4  # mm
    substrate_thickness = 0.05  # mm
    microcoil_width = 0.01  # mm
    microcoil_thickness = 0.0002  # mm

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

    # Thicken the imported sheets and assign material
    oEditor.ThickenSheet(
        ["NAME:Selections",
         "Selections:=", "0",
         "NewPartsModelFlag:=", "Model"
        ],
        ["NAME:SheetThickenParameters",
         "Thickness:=", f"{microcoil_thickness}mm",
         "BothSides:=", False
        ])
    
    oEditor.ChangeProperty(
        ["NAME:AllTabs",
         ["NAME:Geometry3DAttributeTab",
          ["NAME:PropServers", "0"],
          ["NAME:ChangedProps",
           ["NAME:Material", "Value:=", "copper"]
          ]
         ]
        ])

    # Create and assign wave ports
    port_positions = [
        (2, -1.170478567), (1.201158763, 2), (0, 2), 
        (-1.019214464, 2), (-2, 1.201158763),
        (-2, -1.019214464), (-1.201158763, -2),
        (1.050351405, -2)
    ]

    oBoundarySetup = oDesign.GetModule("BoundarySetup")
    for i, (x, y) in enumerate(port_positions):
        port_name = f"WavePort_{i+1}"
        oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:=", True,
                "XStart:=", f"{x - microcoil_width/2}mm",
                "YStart:=", f"{y - microcoil_width/2}mm",
                "ZStart:=", f"{substrate_thickness}mm",
                "Width:=", f"{microcoil_width}mm",
                "Height:=", f"{microcoil_thickness}mm",
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

        oBoundarySetup.AssignWavePort(
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
                            "Start:=", ["0mm", "0mm", f"{substrate_thickness}mm"],
                            "End:=", ["0mm", "0mm", f"{substrate_thickness + microcoil_thickness}mm"]
                        ],
                        "AlignmentGroup:=", 0,
                        "CharImp:=", "Zpi"
                    ]
                ],
                "ShowReporterFilter:=", False,
                "ReporterFilter:=", [True],
                "UseAnalyticAlignment:=", False
            ])

    # Create and assign radiation boundary
    radiation_boundary_offset = 0.3  # mm
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

    oBoundarySetup.AssignRadiation(
        [
            "NAME:Rad1",
            "Objects:=", ["RadiationBoundary"],
            "IsFssReference:=", False,
            "IsForPML:=", False
        ])

    # Mesh operations
    oMeshSetup = oDesign.GetModule("MeshSetup")

    # 1. Surface approximation for the microcoils
    oMeshSetup.AssignLengthOp(
        [
            "NAME:Length_Microcoils",
            "RefineInside:=", True,
            "Enabled:=", True,
            "Objects:=", ["0"],  # Assuming "0" is the name of the imported microcoil object
            "RestrictElem:=", False,
            "NumMaxElem:=", "1000",
            "RestrictLength:=", True,
            "MaxLength:=", f"{microcoil_width/5}mm"
        ])

    # 2. Surface approximation for the wave ports
    for i in range(1, 9):  # 8 ports
        port_name = f"WavePort_{i}"
        oMeshSetup.AssignLengthOp(
            [
                f"NAME:Length_{port_name}",
                "RefineInside:=", True,
                "Enabled:=", True,
                "Objects:=", [port_name],
                "RestrictElem:=", False,
                "NumMaxElem:=", "1000",
                "RestrictLength:=", True,
                "MaxLength:=", f"{microcoil_width/5}mm"
            ])

    # 3. Volume refinement around the microcoils
    oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:=", "-2.1mm",
            "YPosition:=", "-2.1mm",
            "ZPosition:=", f"{substrate_thickness - 0.01}mm",
            "XSize:=", "4.2mm",
            "YSize:=", "4.2mm",
            "ZSize:=", f"{microcoil_thickness + 0.02}mm"
        ],
        [
            "NAME:Attributes",
            "Name:=", "RefinementRegion",
            "Flags:=", "",
            "Color:=", "(143 175 143)",
            "Transparency:=", 0.8,
            "PartCoordinateSystem:=", "Global",
            "MaterialName:=", "vacuum",
            "SolveInside:=", True
        ])

    oMeshSetup.AssignTrueSurfOp(
        [
            "NAME:SurfApprox_Refinement",
            "Objects:=", ["RefinementRegion"],
            "CurveApproxType:=", "ArcLength",
            "MaxArcPointDev:=", "0.001mm",
            "MaxSag:=", "0.001mm",
            "NormalRes:=", "30deg",
            "AspectRatioControl:=", "4"
        ])

    # 4. Mesh operation for the substrate
    oMeshSetup.AssignLengthOp(
        [
            "NAME:Length_Substrate",
            "RefineInside:=", True,
            "Enabled:=", True,
            "Objects:=", ["DiamondSubstrate_1"],
            "RestrictElem:=", False,
            "NumMaxElem:=", "1000000",
            "RestrictLength:=", True,
            "MaxLength:=", f"{substrate_size/20}mm"
        ])

    # 5. Skin depth refinement for the microcoils
    oMeshSetup.AssignSkinDepthOp(
        [
            "NAME:SkinDepth_Microcoils",
            "Objects:=", ["0"],  # Assuming "0" is the name of the imported microcoil object
            "Enabled:=", True,
            "UseAutomaticProfile:=", True,
            "UserSpecifiedMaxLength:=", False,
            "MaxLength:=", "0mm",
            "UserSpecifiedNumLayers:=", True,
            "NumLayers:=", "2",
            "SkinDepth:=", "0.0001mm",
            "FreqForSkinDepthCalc:=", "50MHz"
        ])

    # Set up analysis
    oAnalysisSetup = oDesign.GetModule("AnalysisSetup")
    oAnalysisSetup.InsertSetup("HfssDriven", 
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

    oAnalysisSetup.InsertFrequencySweep("Setup1", 
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

    # Create reports
    oReportSetup = oDesign.GetModule("ReportSetup")
    oReportSetup.CreateReport("S_Parameters", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
        [
            "Domain:=", "Sweep"
        ],