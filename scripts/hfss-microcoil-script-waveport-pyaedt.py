from pyaedt import Hfss
import os

def create_8port_network():
    # Initialize HFSS
    hfss = Hfss(specified_version="2024.1")
    
    # Design parameters
    substrate_size = 4  # mm
    substrate_thickness = 0.5  # mm
    microcoil_width = 0.01  # mm
    microcoil_thickness = 0.0002  # mm
    
    # Create ground plane
    hfss.modeler.create_box(
        position=[-2, -2, 0],
        dimensions=[4, 4, 0.001],
        name="GndPlane",
        matname="copper"
    )
    
    # Create diamond substrate
    hfss.modeler.create_box(
        position=[-2, -2, 0],
        dimensions=[4, 4, 0.5],
        name="Diamond",
        matname="diamond"
    )
    
    # Import DXF file
    dxf_path = "C:/Users/go29lap/code/ansys/microcoils_v3.dxf"
    if os.path.exists(dxf_path):
        hfss.modeler.import_dxf(
            file_path=dxf_path,
            layer="0",
            scale_factor=0.001,
            model_units="mm"
        )
    
    # Move imported objects up
    height_increase = 0.5
    for obj in hfss.modeler.get_objects_in_group("Sheets"):
        if obj.startswith("0"):
            hfss.modeler.move(obj, [0, 0, height_increase])
    
    # Unite imported sheets
    sheet_objects = [obj for obj in hfss.modeler.get_objects_in_group("Sheets") if obj.startswith("0")]
    if len(sheet_objects) > 1:
        hfss.modeler.unite(sheet_objects)
    
    # Create wave ports
    port_positions = [
        (2, -1.170478567), (1.201158763, 2), (0, 2),
        (-1.019214464, 2), (-2, 1.201158763),
        (-2, -1.019214464), (-1.201158763, -2),
        (1.050351405, -2)
    ]
    
    for i, (x, y) in enumerate(port_positions):
        port_name = f"WavePort_{i+1}"
        hfss.modeler.create_rectangle(
            position=[x - microcoil_width/2, y - microcoil_width/2, height_increase],
            dimension_list=[microcoil_width, microcoil_width],
            name=port_name,
            axis="Z"
        )
        
        # Assign wave ports
        hfss.create_wave_port(
            name=port_name,
            terminal_references=[port_name],
            port_number=i+1,
            num_modes=1,
            renormalize=True,
            line_integration_method=True,
            start_point=[x, y, height_increase],
            end_point=[x, y + microcoil_width, height_increase]
        )
    
    # Create and assign radiation boundary
    radiation_boundary_offset = 0.3
    rad_box = hfss.modeler.create_box(
        position=[-substrate_size/2 - radiation_boundary_offset,
                 -substrate_size/2 - radiation_boundary_offset,
                 0],
        dimensions=[substrate_size + 2*radiation_boundary_offset,
                   substrate_size + 2*radiation_boundary_offset,
                   substrate_thickness + 2*height_increase + 2*radiation_boundary_offset],
        name="RadiationBoundary",
        matname="vacuum"
    )
    
    hfss.assign_radiation_boundary_to_objects("Rad1", ["RadiationBoundary"])
    
    # Mesh operations
    # For microcoils
    hfss.mesh.assign_length_mesh(
        ["0"],
        maxlength=microcoil_width,
        maxelements=1000,
        name="Length_Microcoils"
    )
    
    # For wave ports
    for i in range(1, 9):
        port_name = f"WavePort_{i}"
        hfss.mesh.assign_length_mesh(
            [port_name],
            maxlength=microcoil_width/5,
            maxelements=1000,
            name=f"Length_{port_name}"
        )
    
    # Analysis setup
    setup = hfss.create_setup("Setup1")
    setup.props["Frequency"] = "25MHz"
    setup.props["MaxDeltaS"] = 0.02
    setup.props["MaximumPasses"] = 6
    setup.props["MinimumPasses"] = 1
    
    # Frequency sweep
    sweep = setup.add_sweep(
        sweep_name="Sweep",
        sweep_type="LinearStep",
        start_freq="1MHz",
        stop_freq="50MHz",
        step_size="1MHz",
        type="Interpolating"
    )
    
    # Create reports
    # S-parameters
    s_params = ["dB(S(1,1))", "dB(S(2,1))", "dB(S(2,2))"]
    for param in s_params:
        hfss.post.create_report(
            "Modal Solution Data",
            "Rectangular Plot",
            solution_name="Setup1 : Sweep",
            primary_sweep="Freq",
            expressions=[param]
        )
    
    # Z-parameters
    z_params = [["re(Z(1,1))", "im(Z(1,1))"], ["re(Z(2,1))", "im(Z(2,1))"]]
    for param_pair in z_params:
        hfss.post.create_report(
            "Modal Solution Data",
            "Rectangular Plot",
            solution_name="Setup1 : Sweep",
            primary_sweep="Freq",
            expressions=param_pair
        )
    
    # Save project
    hfss.save_project()
    
    # Analyze
    hfss.analyze_setup("Setup1")
    
    return hfss

if __name__ == "__main__":
    hfss = create_8port_network()