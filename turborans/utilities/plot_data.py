import pyvista as pv
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

#script to plot mean pressure from the Periodic Hill VTR data, with the option to also plot mean streamwise velocity and turbulence kinetic energy if available. The script identifies the solid region based on the pressure data and masks it in the plots to visually highlight the hill geometry. 
# Works if in th same folder as the data, or you can specify the path to the mean.vtr file using the --file argument.

def plot_data(filepath):
    # Read the mean VTR file
    mesh = pv.read(filepath)
    
    # Coordinates
    dims = mesh.dimensions
    X = mesh.x
    Y = mesh.y
    z_idx = dims[2] // 2 if dims[2] > 1 else 0

    # Helper function to extract and reshape 2D slice
    def get_slice(mesh_obj, array_name):
        if array_name not in mesh_obj.array_names:
            return None
        data = mesh_obj[array_name]
        data_reshaped = data.reshape(dims, order='F')
        return data_reshaped[:, :, z_idx]

    # Masking arrays
    is_solid = None

    # Get Pressure
    p_key = next((k for k in mesh.array_names if 'p' in k.lower() or 'pressure' in k.lower()), None)
    if p_key:
        p_slice = get_slice(mesh, p_key)
        # Find solid region based on pressure data
        is_solid = np.isnan(p_slice) | (p_slice == 0.0)
        p_masked = np.ma.masked_where(is_solid, p_slice)
    else:
        p_masked = None

    # Get Velocity (Streamwise)
    u_key = next((k for k in mesh.array_names if 'umean' in k.lower() or 'u' == k.lower()), None)
    if u_key and is_solid is not None:
        u_slice = get_slice(mesh, u_key)
        u_masked = np.ma.masked_where(is_solid, u_slice)
    else:
        u_masked = None

    # Check for TKE in rms_1.vtr
    rms1_path = filepath.replace('mean.vtr', 'rms_1.vtr')
    tke_masked = None
    if os.path.exists(rms1_path) and is_solid is not None:
        rms_mesh = pv.read(rms1_path)
        uu = get_slice(rms_mesh, 'UUMEAN')
        vv = get_slice(rms_mesh, 'VVMEAN')
        ww = get_slice(rms_mesh, 'WWMEAN')
        if uu is not None and vv is not None and ww is not None:
            # TKE = 0.5 * (u'u' + v'v' + w'w')
            tke_slice = 0.5 * (uu + vv + ww)
            tke_masked = np.ma.masked_where(is_solid, tke_slice)

    # Combine available plots
    plots = []
    if p_masked is not None:
        plots.append((f'Mean Pressure ({p_key})', p_masked, 'turbo'))
    if u_masked is not None:
        plots.append((f'Mean Streamwise Velocity ({u_key})', u_masked, 'coolwarm'))
    if tke_masked is not None:
        plots.append(('Turbulence Kinetic Energy (TKE)', tke_masked, 'plasma'))
        
    if not plots:
        print("No plotable data found.")
        return

    # Create subplots
    fig, axes = plt.subplots(len(plots), 1, figsize=(10, 4 * len(plots)))
    if len(plots) == 1:
        axes = [axes]
        
    for ax, (title, data_masked, cmap) in zip(axes, plots):
        # Fill the solid region so the hill geometry stands out visually
        solid_mask = np.ma.masked_where(~is_solid, is_solid)
        ax.pcolormesh(X, Y, solid_mask.T, color='gray', shading='auto', alpha=0.5)
        
        # Plot the data
        im = ax.contourf(X, Y, data_masked.T, levels=100, cmap=cmap)
        ax.set_title(title)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_aspect('equal')
        fig.colorbar(im, ax=ax, label=title)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot mean pressure from Periodic Hill VTR data.")
    # Default to the known location if available
    default_path = os.path.join(
        os.path.dirname(__file__) if '__file__' in locals() else '.', 
        "alph05-4071-4048", "mean.vtr"
    )
    
    parser.add_argument("--file", type=str, default=default_path, help="Path to the mean.vtr file")
    
    args = parser.parse_args()
    
    if os.path.exists(args.file):
        plot_data(args.file)
    else:
        print(f"File not found: {args.file}")
        print("Please provide the correct path using --file <path_to_mean.vtr>")
