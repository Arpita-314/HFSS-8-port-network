# Perform required imports.

import os
from ansys.aedt.core import Hfss, downloads

##########################################################
# Set AEDT version
# ~~~~~~~~~~~~~~~~
# Set AEDT version.

aedt_version = "2024.2"

###############################################################################
# Set non-graphical mode
# ~~~~~~~~~~~~~~~~~~~~~~
# Set non-graphical mode. 
# You can set ``non_graphical`` either to ``True`` or ``False``.

non_graphical = False

# Set model units to mm
hfss.modeler.model_units = 'mm'

# Define parameters
substrate_size = 4.0  # mm
substrate_thickness = 0.05  # mm (50 micrometers)
microcoil_width = 0.01  # mm (10 micrometers)
microcoil_thickness = 0.02  # mm (20 micrometers)

# Create the diamond substrate
substrate_name = "DiamondSubstrate_1"
hfss.modeler.create_box(
    position=[-substrate_size / 2, -substrate_size / 2, 0],
    dimensions_list=[substrate_size, substrate_size, substrate_thickness],
    name=substrate_name,
    matname="diamond"
)

# Import the DXF file
dxf_file_path = "C:/Users/go29lap/code/ansys/microcoils_v3.dxf"
hfss.modeler.import_dxf(dxf_file_path, scale_factor=0.001)

# Retrieve imported sheets
imported_sheets = [obj for obj in hfss.modeler.sheets]

# Thicken the imported sheets
for sheet in imported_sheets:
    hfss.modeler.thicken_sheet(sheet.name, microcoil_thickness, both_sides=False)

# Get the list of new solids (microcoils)
all_solids = [obj for obj in hfss.modeler.solids]
known_solids = [substrate_name, "RadiationBoundary"]
microcoil_solids = [obj for obj in all_solids if obj.name not in known_solids]

# Assign material to microcoils
for coil in microcoil_solids:
    coil.material_name = "copper"

# Create wave ports
port_width = microcoil_width
port_positions = [
    (2, -1.170478567), (1.201158763, 2), (0, 2),
    (-1.019214464, 2), (-2, 1.201158763),
    (-2, -1.019214464), (-1.201158763, -2),
    (1.050351405, -2)
]

port_names = []
port_centers = []

for i, (x, y) in enumerate(port_positions):
    port_name = "WavePort_{0}".format(i + 1)
    port_names.append(port_name)
    port_centers.append((x, y))
    hfss.modeler.create_rectangle(
        position=[x - port_width / 2, y - port_width / 2, substrate_thickness],
        dimension_list=[port_width, microcoil_thickness],
        axis="Z",
        name=port_name,
        matname="vacuum"
    )

# Create radiation boundary
radiation_boundary_offset = 0.3  # mm (300 micrometers)
hfss.modeler.create_box(
    position=[
        -substrate_size / 2 - radiation_boundary_offset,
        -substrate_size / 2 - radiation_boundary_offset,
        -radiation_boundary_offset
    ],
    dimensions_list=[
        substrate_size + 2 * radiation_boundary_offset,
        substrate_size + 2 * radiation_boundary_offset,
        substrate_thickness + microcoil_thickness + 2 * radiation_boundary_offset
    ],
    name="RadiationBoundary",
    matname="vacuum"
)

# Assign radiation boundary
hfss.assign_radiation_boundary_to_objects(["RadiationBoundary"])

# Assign wave ports
hfss.solution_type = "DrivenModal"
for i, port_name in enumerate(port_names):
    x, y = port_centers[i]
    start_point = [x, y, substrate_thickness]
    end_point = [x, y, substrate_thickness + microcoil_thickness]
    hfss.create_wave_port_from_sheet(
        port_sheet=hfss.modeler[port_name],
        deembed=False,
        integration_line={"start": start_point, "end": end_point},
        num_modes=1,
        port_name=port_name
    )

# Add mesh operations
# Surface approximation for the microcoils
for coil in microcoil_solids:
    hfss.mesh.assign_length_mesh(coil.name, maxlength=microcoil_width / 5)

# Surface approximation for the wave ports
for port_name in port_names:
    hfss.mesh.assign_length_mesh(port_name, maxlength=microcoil_width / 5)

# Skin depth refinement for the microcoils
for coil in microcoil_solids:
    hfss.mesh.assign_skin_depth(
        [coil.name],
        skin_depth=0.0001,  # 0.0001 mm
        num_layers=2,
        frequency="50MHz"
    )

# Set up analysis
setup = hfss.create_setup("Setup1")
setup.props["Frequency"] = "25MHz"
setup.props["MaximumPasses"] = 6
setup.props["MinimumPasses"] = 1
setup.props["MinimumConvergedPasses"] = 1
setup.props["MaxDeltaS"] = 0.02
setup.props["BasisOrder"] = 1
setup.props["UseMatrixConv"] = False
setup.props["PercentRefinement"] = 30
setup.props["DoLambdaRefine"] = True
setup.props["DoMaterialLambda"] = True
setup.props["PortAccuracy"] = 2
setup.props["UseIterativeSolver"] = False
setup.props["SaveAnyFields"] = True
setup.props["AdaptMultipleFreqs"] = True
setup.update()

# Set up frequency sweep
sweep = setup.add_sweep()
sweep.props["RangeType"] = "LinearStep"
sweep.props["RangeStart"] = "1MHz"
sweep.props["RangeEnd"] = "50MHz"
sweep.props["RangeStep"] = "0.1MHz"
sweep.props["Type"] = "Discrete"
sweep.props["SaveFields"] = False
sweep.props["SaveRadFields"] = False
sweep.props["ExtrapToDC"] = False
sweep.update()

# Create reports (S-parameters and Z-parameters)
# S11-parameter
hfss.post.create_report(
    expressions=["dB(S(1,1))"],
    primary_sweep_variable="Freq",
    setup_sweep_name="Setup1 : LastAdaptive",
    plotname="S11_Parameter",
    report_category="Modal Solution Data",
    plot_type="Rectangular Plot"
)

# S21-parameter
hfss.post.create_report(
    expressions=["dB(S(2,1))"],
    primary_sweep_variable="Freq",
    setup_sweep_name="Setup1 : LastAdaptive",
    plotname="S21_Parameter",
    report_category="Modal Solution Data",
    plot_type="Rectangular Plot"
)

# Z11-parameters
hfss.post.create_report(
    expressions=["re(Z(1,1))", "im(Z(1,1))"],
    primary_sweep_variable="Freq",
    setup_sweep_name="Setup1 : LastAdaptive",
    plotname="Z11_Parameter",
    report_category="Modal Solution Data",
    plot_type="Rectangular Plot"
)

# Z21-parameters
hfss.post.create_report(
    expressions=["re(Z(2,1))", "im(Z(2,1))"],
    primary_sweep_variable="Freq",
    setup_sweep_name="Setup1 : LastAdaptive",
    plotname="Z21_Parameter",
    report_category="Modal Solution Data",
    plot_type="Rectangular Plot"
)

# Save the project
hfss.save_project()

# Analyze
hfss.analyze_setup("Setup1")

# Optionally, release the AEDT session
# hfss.release_desktop(close_projects=True, close_desktop=True)