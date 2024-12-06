from __future__ import annotations

import math

from pint import get_application_registry
from pyg4ometry import geant4

from .base import HPGe

u = get_application_registry()


class P00664B(HPGe):
    """A p-type point contact germanium detector P00664B with a special detector geometry.

    Note
    ----
        The normal vector of the cut plane is in the positive x-direction.
    """

    def _g4_solid(self):
        c = self.metadata.geometry

        # return ordered r,z lists, default unit [mm]
        r, z = self._decode_polycone_coord()

        x_cut_plane = c.extra.crack.radius_in_mm

        # build generic polycone, default [mm]
        uncut_hpge = geant4.solid.GenericPolycone(
            "uncut" + self.name, 0, 2 * math.pi, r, z, self.registry
        )

        px_sliced = c.radius_in_mm - x_cut_plane
        py_sliced = 2 * c.radius_in_mm

        cut_plane = geant4.solid.Box(
            "cut_plane_" + self.name,
            px_sliced,
            py_sliced,
            c.height_in_mm,
            self.registry,
        )

        return geant4.solid.Subtraction(
            self.name,
            uncut_hpge,
            cut_plane,
            [[0, 0, 0], [x_cut_plane + px_sliced / 2, 0, c.height_in_mm / 2]],
            self.registry,
        )

    def _decode_polycone_coord(self):
        c = self.metadata.geometry

        def _tan(a):
            return math.tan(math.pi * a / 180)

        r = []
        z = []
        surfaces = []

        if c.pp_contact.depth_in_mm > 0:
            r += [0, c.pp_contact.radius_in_mm, c.pp_contact.radius_in_mm]
            z += [c.pp_contact.depth_in_mm, c.pp_contact.depth_in_mm, 0]
            surfaces += ["pplus", "passive"]

        else:
            r += [0, c.pp_contact.radius_in_mm]
            z += [0, 0]
            surfaces += ["pplus"]

        if c.taper.bottom.height_in_mm > 0:
            r += [
                c.radius_in_mm
                - c.taper.bottom.height_in_mm * _tan(c.taper.bottom.angle_in_deg),
                c.radius_in_mm,
            ]
            z += [0, c.taper.bottom.height_in_mm]
            surfaces += ["passive", "nplus"]

        else:
            r += [c.radius_in_mm]
            z += [0]
            surfaces += ["passive"]

        if c.taper.top.height_in_mm > 0:
            r += [
                c.radius_in_mm,
                c.radius_in_mm
                - c.taper.top.height_in_mm * _tan(c.taper.top.angle_in_deg),
            ]
            z += [c.height_in_mm - c.taper.top.height_in_mm, c.height_in_mm]
            surfaces += ["nplus", "nplus"]
        else:
            r += [c.radius_in_mm]
            z += [c.height_in_mm]
            surfaces += ["nplus"]

        r += [0]
        z += [c.height_in_mm]
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
        r_cut = c.extra.crack.radius_in_mm
        h_bot_taper = c.taper.bottom.height_in_mm
        angle_bot_taper = c.taper.bottom.angle_in_deg * math.pi / 180

        theta = math.acos(r_cut / r)

        # part above the bottom taper
        cut_volume_top = (theta * r * r - r * math.sin(theta) * r_cut) * (
            c.height_in_mm - h_bot_taper
        )

        # part along the bottom taper
        r2 = r - h_bot_taper * math.tan(angle_bot_taper)

        cut_volume_bot = theta * (
            r * r + r * r2 + r2 * r2
        ) * h_bot_taper / 3 - math.sin(2 * theta) / (6 * math.tan(angle_bot_taper)) * (
            r**3 - (r - h_bot_taper * math.tan(angle_bot_taper)) ** 3
        )

        cut_volume = cut_volume_top + cut_volume_bot

        return (full_volume - cut_volume) * u.mm**3
