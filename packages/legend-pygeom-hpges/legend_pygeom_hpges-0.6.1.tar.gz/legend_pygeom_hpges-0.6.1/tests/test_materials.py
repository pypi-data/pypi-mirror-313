from __future__ import annotations

import pytest
from pyg4ometry import geant4 as g4

from legendhpges import materials


def test_number_density_meas():
    assert materials._number_density_meas().to("1/cm^3").m == pytest.approx(
        4.41752e22, rel=1e-3
    )


def test_enriched_ge_density():
    assert materials.enriched_germanium_density(1).to("g/cm^3").m == pytest.approx(
        5.569, rel=1e-3
    )
    assert materials.enriched_germanium_density(0).to("g/cm^3").m == pytest.approx(
        5.422, rel=1e-3
    )


def test_g4_materials():
    assert (
        materials.make_enriched_germanium(0.92).density
        == materials.enriched_germanium_density(0.92).to("g/cm^3").m
    )
    assert (
        materials.make_natural_germanium().density
        == materials.natge_density_meas.to("g/cm^3").m
    )


def test_g4_materials_on_reg():
    reg = g4.Registry()

    # ensure that all materials, elements and isotopes are actually registered with the registry.
    mat92_1 = materials.make_enriched_germanium(0.92, reg)
    for mat in (
        "Ge74",
        "Ge76",
        "EnrichedGermanium0.920",
        "ElementEnrichedGermanium0.920",
    ):
        assert mat in reg.materialDict
    # lazy-loaded isotopes should not exist.
    for mat in ("Ge70", "Ge72", "Ge73"):
        assert mat not in reg.materialDict

    # ensure we get the same instance back, without duplication errors.
    mat92_2 = materials.make_enriched_germanium(0.92, reg)
    assert mat92_1 is mat92_2

    # ensure that we can create different enrichments, without duplication errors.
    materials.make_enriched_germanium(0.90, reg)
    for mat in ("ElementEnrichedGermanium0.900", "EnrichedGermanium0.900"):
        assert mat in reg.materialDict

    # ensure that natural germanium also works.
    materials.make_natural_germanium(reg)
    for mat in ("Ge70", "Ge72", "Ge73", "NaturalGermanium", "ElementNaturalGermanium"):
        assert mat in reg.materialDict
