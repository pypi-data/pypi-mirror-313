"""LEGEND HPGe material descriptions for use in geometries."""

from __future__ import annotations

import functools
import math
from typing import Callable

from pint import Quantity, get_application_registry
from pyg4ometry import geant4 as g4

u = get_application_registry()

ge_iso_a: dict = {70: 69.924, 72: 71.922, 73: 72.923, 74: 73.921, 76: 75.921}
"""Molar weight of Germanium isotopes.

Source: `NIST <https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=Ge>`_.
"""

natge_isotopes: dict = {70: 0.2057, 72: 0.2745, 73: 0.0775, 74: 0.3650, 76: 0.0773}
"""Isotopic composition of natural germanium.

Source: `NIST <https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=Ge>`_.
"""

n_avogadro: Quantity = 6.02214076e23 * u("1/mol")
natge_density_meas: Quantity = 5.3234 * u("g/cm^3")
"""Measured density of natural germanium at room temperature."""


def _make_ge_isotopes(
    registry: g4.Registry | None,
) -> dict[int, Callable[[], g4.Isotope]]:
    def make_ge_iso(N: int):
        name = f"Ge{N}"
        if registry is not None and name in registry.materialDict:
            return registry.materialDict[name]
        return g4.Isotope(name, 32, N, ge_iso_a[N], registry)

    return {n: functools.partial(make_ge_iso, n) for n in (70, 72, 73, 74, 76)}


def _number_density_theo() -> Quantity:
    """Calculate the theoretical number density of germanium.

    At room temperature, starting from the measured atomic radius.
    """
    r_ge = 0.122 * u("nm")
    a = 8 * r_ge / math.sqrt(3)
    return (8 / a**3).to("cm^-3")


def _number_density_meas() -> Quantity:
    """Calculate the measured number density of germanium.

    At room temperature, starting from the measured mass density of natural
    germanium.
    """
    a_eff = 0
    for iso, frac in natge_isotopes.items():
        a_eff += ge_iso_a[iso] * u("g/mol") * frac
    return n_avogadro * natge_density_meas / a_eff


def _make_germanium(
    ge_name: str,
    el_symbol: str,
    iso_fracs: dict[int, float],
    density: Quantity,
    reg: g4.Registry | None,
) -> g4.Material:
    if reg is None or ge_name not in reg.materialDict:
        el = g4.ElementIsotopeMixture(
            f"Element{ge_name}", el_symbol, len(iso_fracs), reg
        )

        isos = _make_ge_isotopes(reg)
        for iso, frac in iso_fracs.items():
            el.add_isotope(isos[iso](), frac)
        mat = g4.MaterialCompound(ge_name, density.to("g/cm^3").m, 1, reg)
        mat.add_element_massfraction(el, 1)
        return mat

    return reg.materialDict[ge_name]


def make_natural_germanium(
    registry: g4.Registry | None = None,
) -> g4.Material:
    """Natural germanium material builder."""
    return _make_germanium(
        "NaturalGermanium", "NatGe", natge_isotopes, natge_density_meas, registry
    )


def enriched_germanium_density(ge76_fraction: float = 0.92) -> Quantity:
    """Calculate the density of enriched germanium.

    Starting from the measured density of natural germanium at room
    temperature.

    Parameters
    ----------
    ge76_fraction
        fraction of Ge76 atoms.
    """
    m_eff = (ge_iso_a[76] * ge76_fraction + ge_iso_a[74] * (1 - ge76_fraction)) * u(
        "g/mol"
    )
    return (_number_density_meas() * m_eff / n_avogadro).to("g/cm^3")


def make_enriched_germanium(
    ge76_fraction: float = 0.92,
    registry: g4.Registry | None = None,
) -> g4.Material:
    """Enriched germanium material builder.

    Note
    ----
    The isotopic composition is approximated as a mixture of Ge76 and Ge74.

    Parameters
    ----------
    ge76_fraction
        fraction of Ge76 atoms.
    """
    return _make_germanium(
        f"EnrichedGermanium{ge76_fraction:.3f}",
        f"EnrGe{ge76_fraction:.3f}",
        {74: 1 - ge76_fraction, 76: ge76_fraction},
        enriched_germanium_density(ge76_fraction),
        registry,
    )
