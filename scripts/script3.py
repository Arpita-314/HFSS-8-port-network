# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Student Version 2023.2.0
# 15:17:42  Jul 03, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project7")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.CreateCutplane(
	[
		"NAME:PlaneParameters",
		"PlaneBaseX:="		, "1.002um",
		"PlaneBaseY:="		, "-3.852um",
		"PlaneBaseZ:="		, "0um",
		"PlaneNormalX:="	, "0um",
		"PlaneNormalY:="	, "0.00200000000000022um",
		"PlaneNormalZ:="	, "0um"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Plane1",
		"Color:="		, "(143 175 143)"
	])
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignImpedance(
	[
		"NAME:Imped3",
		"Objects:="		, ["Polyline6"],
		"Resistance:="		, "50",
		"Reactance:="		, "50",
		"InfGroundPlane:="	, False
	])
oProject.Save()
oModule.AssignImpedance(
	[
		"NAME:Imped4",
		"Objects:="		, ["Polyline6"],
		"Resistance:="		, "50",
		"Reactance:="		, "50",
		"InfGroundPlane:="	, False
	])
oModule.AssignImpedance(
	[
		"NAME:Imped5",
		"Objects:="		, ["Polyline4"],
		"Resistance:="		, "50",
		"Reactance:="		, "50",
		"InfGroundPlane:="	, False
	])
oModule.AssignImpedance(
	[
		"NAME:Imped6",
		"Objects:="		, ["Polyline5"],
		"Resistance:="		, "50",
		"Reactance:="		, "50",
		"InfGroundPlane:="	, False
	])
oModule.AssignImpedance(
	[
		"NAME:Imped7",
		"Objects:="		, ["Polyline4"],
		"Resistance:="		, "50",
		"Reactance:="		, "50",
		"InfGroundPlane:="	, False
	])
oModule.AssignImpedance(
	[
		"NAME:Imped8",
		"Objects:="		, ["Polyline3"],
		"Resistance:="		, "50",
		"Reactance:="		, "50",
		"InfGroundPlane:="	, False
	])
oProject.RunToolkit("SysLib", "[Beta] Install PyAEDT", [])
