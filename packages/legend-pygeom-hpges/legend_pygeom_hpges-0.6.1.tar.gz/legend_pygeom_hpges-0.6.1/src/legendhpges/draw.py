from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from pyg4ometry.visualisation import VtkViewer

from .base import HPGe


def plot_profile(
    hpge: HPGe, axes: plt.Axes = None, split_by_type: bool = False, **kwargs
) -> tuple[plt.Figure, plt.Axes]:
    """Plot the HPGe profile with :mod:`matplotlib`.

    Parameters
    ----------
    hpge
        detector.
    axes
        pre-existing axes where the profile will be plotted.
    split_by_type
        boolean to separate surfaces of different types.
    **kwargs
        any keyword argument supported by :func:`matplotlib.pyplot.plot`.

    """
    # data
    r, z = hpge.get_profile()

    # set options
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    fig = None
    if axes is None:
        fig, axes = plt.subplots()
        fig.tight_layout()
        axes.axis("equal")
        axes.set_xlabel("r [mm]")
        axes.set_ylabel("z [mm]")
        axes.grid()

    default_kwargs = {
        "marker": "o",
        "markersize": 2,
        "markeredgecolor": colors[1],
        "markerfacecolor": colors[1],
        "linewidth": 2,
    }
    default_kwargs |= kwargs

    if not split_by_type:
        x = r + [-x for x in reversed(r)]
        y = z + list(reversed(z))

        axes.plot(x, y, **default_kwargs)
    else:
        surfaces = np.array(hpge.surfaces)
        unique_surfaces = np.unique(surfaces)

        dr = np.array([np.array([r1, r2]) for r1, r2 in zip(r[:-1], r[1:])])
        dz = np.array([np.array([z1, z2]) for z1, z2 in zip(z[:-1], z[1:])])

        for idx, u in enumerate(unique_surfaces):
            drs_tmp = dr[surfaces == u]
            dzs_tmp = dz[surfaces == u]

            first = True
            for r_tmp, z_tmp in zip(drs_tmp, dzs_tmp):
                if first:
                    axes.plot(
                        r_tmp, z_tmp, color=colors[idx + 2], label=u, **default_kwargs
                    )
                    first = False
                    axes.plot(-r_tmp, z_tmp, color=colors[idx + 2], **default_kwargs)
                else:
                    axes.plot(r_tmp, z_tmp, color=colors[idx + 2], **default_kwargs)
                    axes.plot(-r_tmp, z_tmp, color=colors[idx + 2], **default_kwargs)
        axes.legend(loc="upper right")
    return fig, axes


def visualize(hpge: HPGe, viewer: VtkViewer = None) -> VtkViewer:
    """Visualize the HPGe with :class:`pyg4ometry.visualisation.VtkViewer`.

    Parameters
    ----------
    viewer
        pre-existing VTK viewer.
    """
    if viewer is None:
        viewer = VtkViewer()
    viewer.addLogicalVolume(hpge)
    viewer.setSurface()
    viewer.view(interactive=True)

    return viewer
