import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

def show_fields(network:dict, field = 'T', slice_index = 2, title = None):
    """
    Plotting a field across sliced 3D data
    Parameters
    ----------
    network: Network.network object
    field: which field to show

    Returns
    -------
    """
    if field not in network:
        raise KeyError(f"Field '{field}' not found in the network.")
    data = network[field][slice_index, :, :]  # Slice the 3D data along the first axis

    # Generate X and Y grid for the data
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    X, Y = np.meshgrid(x, y)

    # Flatten X, Y, and Z for Triangulation
    Z = data.flatten()
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    triang = Triangulation(X_flat, Y_flat)

    contour = plt.tricontourf(triang, Z)
    cbar = plt.colorbar(contour, orientation='horizontal')
    cbar.ax.tick_params(labelsize=14)  # Increase font size for colorbar ticks
    plt.xlabel("X-axis", fontsize=16)
    plt.ylabel("Y-axis", fontsize=16)
    plt.title(f"Tricontourf Plot for Field: {field}" if title is None else title, fontsize=18)
    plt.gca().set_aspect('equal')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()


def calculate_fields(network, field = 'Q'):
    pass