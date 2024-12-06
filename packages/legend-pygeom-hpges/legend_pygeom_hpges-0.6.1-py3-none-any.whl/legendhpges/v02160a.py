from __future__ import annotations

import math

from pint import get_application_registry
from pyg4ometry import geant4

from .base import HPGe
from .build_utils import make_pplus

u = get_application_registry()


class V02160A(HPGe):
    """An inverted-coaxial point contact germanium detector V02160A with a special geometry.

    Note
    ----
        The center of the cut plane faces the positive x-direction with a certain angle with respect to xz-plane.
    """

    def _g4_solid(self):
        c = self.metadata.geometry

        # return ordered r,z lists, default unit [mm]
        r, z = self._decode_polycone_coord()

        # build generic polycone, default [mm]
        uncut_hpge = geant4.solid.GenericPolycone(
            "uncrack_" + self.name, 0, 2 * math.pi, r, z, self.registry
        )

        # build the cut plane
        r_cp = c.extra.crack.radius_in_mm
        angle_cp = c.extra.crack.angle_in_deg * math.pi / 180

        px_cp = r_cp * math.cos(angle_cp) * 2
        py_cp = 2 * c.radius_in_mm
        pz_cp = r_cp / math.sin(angle_cp) * 2

        cut_plane = geant4.solid.Box(
            "cut_plane_" + self.name, px_cp, py_cp, pz_cp, self.registry
        )

        # build the subtraction solid
        return geant4.solid.Subtraction(
            self.name,
            uncut_hpge,
            cut_plane,
            [
                [0, angle_cp, 0],
                [c.radius_in_mm - r_cp + px_cp / 2 / math.cos(angle_cp), 0, 0],
            ],
            self.registry,
        )

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

        if c.taper.borehole.height_in_mm > 0:
            r += [
                c.borehole.radius_in_mm
                + c.taper.borehole.height_in_mm * _tan(c.taper.borehole.angle_in_deg),
                c.borehole.radius_in_mm,
            ]

            z += [
                c.height_in_mm,
                c.height_in_mm - c.taper.borehole.height_in_mm,
            ]
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

    @property
    def volume(self):
        c = self.metadata.geometry

        # volume of the full solid without cut
        full_volume = 0
        pr, pz = self._decode_polycone_coord()
        r1 = pr[-1]
        z1 = pz[-1]
        for i in range(len(pz)):
            r2 = pr[i]
            z2 = pz[i]
            full_volume += (r1 * r1 + r1 * r2 + r2 * r2) * (z2 - z1)
            r1 = r2
            z1 = z2
        full_volume = 2 * math.pi * abs(full_volume) / 6

        # calculate the volume of the cut
        r = c.radius_in_mm
        angle_cut = c.extra.crack.angle_in_deg * math.pi / 180
        h_cut = c.extra.crack.radius_in_mm * math.tan(angle_cut)

        theta = 2 * math.acos(1 - h_cut / r * math.tan(angle_cut))

        def _sin(x):
            return math.sin(x)

        def _cos(x):
            return math.cos(x)

        prefactor = (
            theta
            - _sin(theta) * (_cos(theta) + 2)
            - 2 * math.log(_cos(theta / 2) - _sin(theta / 2))
            + 2 * math.log(_sin(theta / 2) + _cos(theta / 2))
        )

        cut_volume = theta / 2 * r * r * h_cut - prefactor * r**3 / (
            32 * math.tan(angle_cut)
        )

        return (full_volume - cut_volume) * u.mm**3
