from math import pi, sin, cos

 

oProject = oDesktop.GetActiveProject()

oDesign = oProject.GetActiveDesign()

oEditor = oDesign.SetActiveEditor("3D Modeler")

 

Start_t = 0

End_t = pi*2

 

Npoint = 128

Nsection = Npoint-1

 

d_t = (End_t-Start_t)/Nsection

 

for n in range(1,Nsection):

 

P1 = Start_t+d_t*(n-1)

P2 = P1+d_t

X_t1 = cos(P1*6)

Y_t1 = sin(P1*6)

Z_t1 = P1

X_t2 = cos(P2*6)

Y_t2 = sin(P2*6)

Z_t2 = P2

 

 

oEditor.CreatePolyline(

[

"NAME:PolylineParameters",

"IsPolylineCovered:=" , True,

"IsPolylineClosed:=" , False,

[

"NAME:PolylinePoints",

[

"NAME:PLPoint",

"X:=" , '1mm*' + str(X_t1),

"Y:=" , '1mm*' + str(Y_t1),

"Z:=" , '1mm*' + str(Z_t1)

],

[

"NAME:PLPoint",

"X:=" , '1mm*' + str(X_t2),

"Y:=" , '1mm*' + str(Y_t2),

"Z:=" , '1mm*' + str(Z_t2)

]

],

[

"NAME:PolylineSegments",

[

"NAME:PLSegment",

"SegmentType:=" , "Line",

"StartIndex:=" , 0,

"NoOfPoints:=" , 2

]

],

[

"NAME:PolylineXSection",

"XSectionType:=" , "None",

"XSectionOrient:=" , "Auto",

"XSectionWidth:=" , "0mm",

"XSectionTopWidth:=" , "0mm",

"XSectionHeight:=" , "0mm",

"XSectionNumSegments:=" , "0",

"XSectionBendType:=" , "Corner"

]

],

[

"NAME:Attributes",

"Name:=" , "Polyline"+str(n),

"Flags:=" , "",

"Color:=" , "(132 132 193)",

"Transparency:=" , 0,

"PartCoordinateSystem:=", "Global",

"UDMId:=" , "",

"MaterialValue:=" , "\"vacuum\"",

"SurfaceMaterialValue:=", "\"\"",

"SolveInside:=" , True,

"IsMaterialEditable:=" , True,

"UseMaterialAppearance:=", False,

"IsLightweight:=" , False

])