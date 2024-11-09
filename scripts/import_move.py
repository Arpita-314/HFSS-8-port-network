# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2024.2.0
# 11:26:11  Sep 26, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project18")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.Unite(
	[
		"NAME:Selections",
		"Selections:="		, "0_4,0_3,0_2,0_1"
	], 
	[
		"NAME:UniteParameters",
		"KeepOriginals:="	, False,
		"TurnOnNBodyBoolean:="	, True
	])
oEditor.Move(
	[
		"NAME:Selections",
		"Selections:="		, "0_4",
		"NewPartsModelFlag:="	, "Model"
	], 
	[
		"NAME:TranslateParameters",
		"TranslateVectorX:="	, "-0.586960479580852mm",
		"TranslateVectorY:="	, "0.392327744862925mm",
		"TranslateVectorZ:="	, "0mm"
	])
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DCmdTab",
			[
				"NAME:PropServers", 
				"0_4:Move:1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Move Vector",
					"X:="			, "0mm",
					"Y:="			, "0mm",
					"Z:="			, "0.5mm"
				]
			]
		]
	])
