from __future__ import annotations

import math

from .base import HPGe
from .build_utils import make_pplus


class V02162B(HPGe):
    """An inverted-coaxial point contact germanium detector V02162B with a special detector geometry."""

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

        if c.taper.bottom.height_in_mm > 0:
            r += [
                c.radius_in_mm
                - c.taper.bottom.height_in_mm * _tan(c.taper.bottom.angle_in_deg),
                c.radius_in_mm,
            ]

            z += [
                0,
                c.taper.bottom.height_in_mm,
            ]

            surfaces += ["nplus", "nplus"]
        else:
            r += [c.radius_in_mm]
            z += [0]
            surfaces += ["nplus"]

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
        # top groove
        r += [c.extra.topgroove.radius_in_mm, c.extra.topgroove.radius_in_mm]

        z += [c.height_in_mm, c.height_in_mm - c.extra.topgroove.depth_in_mm]

        surfaces += ["nplus", "nplus"]

        # borehole
        r += [c.borehole.radius_in_mm, c.borehole.radius_in_mm, 0]

        z += [
            c.height_in_mm - c.extra.topgroove.depth_in_mm,
            c.height_in_mm - c.borehole.depth_in_mm,
            c.height_in_mm - c.borehole.depth_in_mm,
        ]
        surfaces += ["nplus", "nplus", "nplus"]

        self.surfaces = surfaces

        return r, z
