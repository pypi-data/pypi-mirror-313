# plotting.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.axes as maxes
from matplotlib.colorbar import Colorbar
from matplotlib.colors import ListedColormap


def colorbar(fig, divider, mappable, label, nrows=1, total_cbars=2) -> Colorbar:
    last_axes = plt.gca()
    base_pad = 0.1
    num_colorbars = (len(fig.axes) - nrows) % total_cbars
    pad = base_pad + num_colorbars * 0.6
    cax = divider.append_axes("right", size="4%", pad=pad, axes_class=maxes.Axes)
    cbar = fig.colorbar(mappable, cax=cax, label=label)
    plt.sca(last_axes)
    return cbar


def get_turner_cmap() -> ListedColormap:
    n_colors = 256
    viridis = plt.get_cmap('viridis', n_colors)
    newcolors = viridis(np.linspace(0, 1, n_colors))

    red, yellow, green, blue = np.array([1, 0, 0, 1]), np.array([1, 1, 0, 1]), np.array([0, 1, 0, 1]), np.array([0, 0, 1, 1])
    newcolors[:int(256 * 0.125)] = red
    newcolors[int(256 * 0.125):int(256 * 0.375)] = yellow
    newcolors[int(256 * 0.375):int(256 * 0.625)] = green
    newcolors[int(256 * 0.625):int(256 * 0.875)] = blue
    newcolors[int(256 * 0.875):] = red

    return ListedColormap(newcolors)
