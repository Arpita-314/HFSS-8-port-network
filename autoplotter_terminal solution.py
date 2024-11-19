import skrf as rf
import numpy as np
import matplotlib.pyplot as plt

# Load the Touchstone file
file_path = 'C:/Users/go29lap/code/ansys/microcoils/terminal solution/try without s parameter/Ag-Pd/400/microcoils_terminal_wavePd20Ag1000_2.aedtexport/HFSSDesign1/Setup1/Sweep_DV11185.s8p'  # Update this to the file path in your environment
network = rf.Network(file_path)

# Define a helper function to convert S-parameters to impedance
def s_to_impedance(network, z0=50):
    """Calculate terminal impedance from S-parameters."""
    s = network.s  # S-parameter matrix
    z = network.z  # Terminal impedance matrix (from skrf directly)
    return z

# Plot the S-parameter Magnitude (dB) and Phase (Degrees)
def plot_s_parameters(network):
    plt.figure(figsize=(12, 8))
    # Plot magnitude (dB)
    for m in range(network.s.shape[1]):
        for n in range(network.s.shape[2]):
            network.plot_s_db(m=m, n=n, label=f"S{m+1}{n+1}")
    plt.title("S-Parameter Magnitude (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()
    
    # Plot phase (degrees)
    plt.figure(figsize=(12, 8))
    for m in range(network.s.shape[1]):
        for n in range(network.s.shape[2]):
            network.plot_s_deg(m=m, n=n, label=f"S{m+1}{n+1}")
    plt.title("S-Parameter Phase (Degrees)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (Degrees)")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

# Plot Terminal Impedance (Z) for each port
def plot_terminal_impedance(network):
    z = s_to_impedance(network)  # Calculate terminal impedance
    frequencies = network.f * 1e-9  # Convert frequency to GHz for plotting
    
    plt.figure(figsize=(12, 8))
    for i in range(z.shape[1]):
        plt.plot(frequencies, np.abs(z[:, i, i]), label=f"Z{str(i+1)}{str(i+1)} (Ohms)")
    plt.title("Terminal Impedance |Z| (Ohms)")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Impedance (Ohms)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot Characteristic Impedance (Z0) for each port
def plot_characteristic_impedance(network):
    z0 = network.z0  # Characteristic impedance from skrf
    frequencies = network.f * 1e-9  # Convert frequency to GHz for plotting
    
    plt.figure(figsize=(12, 8))
    for i in range(len(z0[0])):  # Plot each Z0 for the different ports
        plt.plot(frequencies, np.real(z0[:, i]), label=f"Z0 Port {i+1}")
    plt.title("Characteristic Impedance Z0 (Ohms)")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Characteristic Impedance (Ohms)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the Scattering Parameters (S) in Polar format (Smith Chart)
def plot_smith_chart(network):
    plt.figure(figsize=(10, 8))
    for m in range(network.s.shape[1]):
        for n in range(network.s.shape[2]):
            network.plot_s_smith(m=m, n=n, label=f"S{m+1}{n+1}")
    plt.title("Smith Chart - Scattering Parameters")
    plt.legend(loc='upper right')
    plt.show()

# TDR plot using inverse Fourier Transform of S-parameters
def plot_tdr(network):
    # Time step and frequency sweep setup
    t, s11_t = network.s11.s_time_domain(window=('kaiser', 6), inverse=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t * 1e9, np.abs(s11_t))  # Convert time to nanoseconds for easier interpretation
    plt.title("Time Domain Reflectometry (TDR) Plot for S11")
    plt.xlabel("Time (ns)")
    plt.ylabel("Reflection Magnitude (|S11|)")
    plt.grid(True)
    plt.show()

# Execute plotting functions
plot_s_parameters(network)
plot_terminal_impedance(network)
plot_characteristic_impedance(network)
plot_smith_chart(network)
plot_tdr(network)
