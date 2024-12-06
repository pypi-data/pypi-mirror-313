from __future__ import annotations

import math

from .base import HPGe
from .build_utils import make_pplus


class V07646A(HPGe):
    """An inverted-coaxial point contact germanium detector V07646A with a special geometry."""

    def _decode_polycone_coord(self) -> tuple[list[float], list[float]]:
        c = self.metadata.geometry

        def _tan(a):
            return math.tan(math.pi * a / 180)

        r = []
        z = []
        surfaces = []

        r_p, z_p, surface_p = make_pplus(c)
        r += r_p
        z += z_p
        surfaces += surface_p

        bottom_cylinder = c.extra.bottom_cylinder

        if c.taper.bottom.height_in_mm > 0:
            r += [
                bottom_cylinder.radius_in_mm
                - c.taper.bottom.height_in_mm * _tan(c.taper.bottom.angle_in_deg),
                bottom_cylinder.radius_in_mm,
            ]

            z += [
                0,
                c.taper.bottom.height_in_mm,
            ]
            surfaces += ["nplus", "nplus"]
        else:
            r += [bottom_cylinder.radius_in_mm]
            z += [0]
            surfaces += ["nplus"]

        r += [bottom_cylinder.radius_in_mm, c.radius_in_mm]
        z += [
            bottom_cylinder.height_in_mm,
            bottom_cylinder.height_in_mm + bottom_cylinder.transition_in_mm,
        ]
        surfaces += ["nplus", "nplus"]

        if c.taper.top.height_in_mm > 0:
            r += [
                c.radius_in_mm,
                c.radius_in_mm
                - c.taper.top.height_in_mm * _tan(c.taper.top.angle_in_deg),
            ]

            z += [
                c.height_in_mm - c.taper.top.height_in_mm,
                c.height_in_mm,
            ]
            surfaces += ["nplus", "nplus"]
        else:
            r += [c.radius_in_mm]
            z += [c.height_in_mm]
            surfaces += ["nplus"]

        if c.taper.borehole.height_in_mm > 0:
            r += [
                c.borehole.radius_in_mm
                + c.taper.borehole.height_in_mm * _tan(c.taper.borehole.angle_in_deg),
                c.borehole.radius_in_mm,
            ]

            z += [c.height_in_mm, c.height_in_mm - c.taper.borehole.height_in_mm]
            surfaces += ["nplus", "nplus"]

        else:
            r += [c.borehole.radius_in_mm]
            z += [c.height_in_mm]
            surfaces += ["nplus"]

        if c.taper.borehole.height_in_mm != c.borehole.depth_in_mm:
            r += [
                c.borehole.radius_in_mm,
                0,
            ]

            z += [
                c.height_in_mm - c.borehole.depth_in_mm,
                c.height_in_mm - c.borehole.depth_in_mm,
            ]
            surfaces += ["nplus", "nplus"]

        else:
            r += [0]

            z += [c.height_in_mm - c.borehole.depth_in_mm]

            surfaces += ["nplus"]

        self.surfaces = surfaces

        return r, z
