from __future__ import annotations

from collections.abc import Mapping


def make_pplus(geometry: Mapping) -> tuple[list, list, list]:
    """Make the pplus contact for BeGe and some ICPC.

    Methods to avoid duplicating code.

    Parameters
    ----------
    geometry
        dictionary with the geometry information.

    Returns
    -------
        Tuple ``(r,z,surfaces)`` of lists of r,z coordinates and surface names.
    """
    r = []
    z = []
    surfaces = []

    if geometry.pp_contact.depth_in_mm > 0:
        r += [
            0,
            geometry.pp_contact.radius_in_mm,
            geometry.pp_contact.radius_in_mm,
            geometry.groove.radius_in_mm.inner,
        ]
        z += [
            geometry.pp_contact.depth_in_mm,
            geometry.pp_contact.depth_in_mm,
            0,
            0,
        ]
        surfaces += ["pplus", "passive", "passive"]

    elif geometry.pp_contact.radius_in_mm < geometry.groove.radius_in_mm.inner:
        r += [
            0,
            geometry.pp_contact.radius_in_mm,
            geometry.groove.radius_in_mm.inner,
        ]
        z += [0, 0, 0]
        surfaces += ["pplus", "passive"]
    else:
        r += [0, geometry.pp_contact.radius_in_mm]
        z += [0, 0]
        surfaces += ["pplus"]

    r += [
        geometry.groove.radius_in_mm.inner,
        geometry.groove.radius_in_mm.outer,
        geometry.groove.radius_in_mm.outer,
    ]

    z += [
        geometry.groove.depth_in_mm,
        geometry.groove.depth_in_mm,
        0,
    ]
    surfaces += ["passive", "passive", "passive"]

    return (r, z, surfaces)
