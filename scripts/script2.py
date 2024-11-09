# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Student Version 2023.2.0
# 11:57:34  Jul 03, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project7")
oProject.InsertDesign("HFSS", "HFSSDesign3", "HFSS Terminal Network", "")
oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", "HFSSDesign1", "HFSS Terminal Network", "")
oDesktop.OpenProject("C:/Users/Stierlab/Desktop/Arpita/ansys/script/Project7.aedt")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "-0.4mm",
		"YStart:="		, "-0.4mm",
		"ZStart:="		, "0mm",
		"Width:="		, "0.8mm",
		"Height:="		, "0.8mm",
		"WhichAxis:="		, "Z"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Rectangle1",
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
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])
oDesktop.OpenProject("C:/Users/Stierlab/Desktop/Arpita/ansys/script/Project7.aedt")
