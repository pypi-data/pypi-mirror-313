from __future__ import annotations

import pathlib

import pytest
from legendmeta import TextDB
from legendtestdata import LegendTestData
from pyg4ometry import geant4

from legendhpges import (
    P00664B,
    PPC,
    V02160A,
    V02162B,
    V07646A,
    BEGe,
    InvertedCoax,
    SemiCoax,
    make_hpge,
    materials,
)

configs = TextDB(pathlib.Path(__file__).parent.resolve() / "configs")


@pytest.fixture(scope="session")
def test_data_configs():
    ldata = LegendTestData()
    ldata.checkout("5f9b368")
    return ldata.get_path("legend/metadata/hardware/detectors/germanium/diodes")


@pytest.fixture
def reg():
    return geant4.Registry()


@pytest.fixture(params=["r", "n"])
def reg_or_none(request):
    return geant4.Registry() if request.param == "r" else None


@pytest.fixture
def natural_germanium(reg):
    return materials.make_natural_germanium(reg)


def test_icpc(test_data_configs, reg, natural_germanium):
    InvertedCoax(
        test_data_configs + "/V99000A.json", material=natural_germanium, registry=reg
    )


def test_bege(test_data_configs, reg, natural_germanium):
    BEGe(test_data_configs + "/B99000A.json", material=natural_germanium, registry=reg)


def test_ppc(test_data_configs, reg, natural_germanium):
    PPC(test_data_configs + "/P99000A.json", material=natural_germanium, registry=reg)


def test_semicoax(test_data_configs, reg, natural_germanium):
    SemiCoax(
        test_data_configs + "/C99000A.json", material=natural_germanium, registry=reg
    )


def test_v07646a(reg, natural_germanium):
    V07646A(configs.V07646A, material=natural_germanium, registry=reg)


def test_p00664p(reg, natural_germanium):
    P00664B(configs.P00664B, material=natural_germanium, registry=reg)


def test_v02162b(reg, natural_germanium):
    V02162B(configs.V02162B, material=natural_germanium, registry=reg)


def test_v02160a(reg, natural_germanium):
    V02160A(configs.V02160A, material=natural_germanium, registry=reg)


def test_make_icpc(test_data_configs, reg_or_none):
    gedet = make_hpge(test_data_configs + "/V99000A.json", registry=reg_or_none)
    assert isinstance(gedet, InvertedCoax)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def test_make_bege(test_data_configs, reg_or_none):
    gedet = make_hpge(test_data_configs + "/B99000A.json", registry=reg_or_none)
    assert isinstance(gedet, BEGe)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def test_make_ppc(test_data_configs, reg_or_none):
    gedet = make_hpge(test_data_configs + "/P99000A.json", registry=reg_or_none)
    assert isinstance(gedet, PPC)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def test_make_semicoax(test_data_configs, reg_or_none):
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg_or_none)
    assert isinstance(gedet, SemiCoax)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def make_v07646a(reg_or_none):
    gedet = make_hpge(configs.V07646A, registry=reg_or_none)
    assert isinstance(gedet, V07646A)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def test_make_p00664b(reg_or_none):
    gedet = make_hpge(configs.P00664B, registry=reg_or_none)
    assert gedet.mass
    assert isinstance(gedet, P00664B)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1

    gedet = make_hpge(
        configs.P00664B,
        name="P00664B_bis",
        allow_cylindrical_asymmetry=False,
        registry=reg_or_none,
    )
    assert isinstance(gedet, PPC)
    assert not isinstance(gedet, P00664B)
    assert isinstance(gedet.solid, geant4.solid.GenericPolycone)


def test_make_v02162b(reg_or_none):
    gedet = make_hpge(configs.V02162B, registry=reg_or_none)
    assert gedet.mass
    assert isinstance(gedet, V02162B)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def test_make_v02160a(reg_or_none):
    gedet = make_hpge(configs.V02160A, registry=reg_or_none)
    assert gedet.mass
    assert isinstance(gedet, V02160A)

    assert len(gedet._decode_polycone_coord()[0]) == len(gedet.surfaces) + 1


def test_null_enrichment(reg_or_none):
    metadata = configs.V07646A
    metadata.production.enrichment = None
    with pytest.raises(ValueError):
        make_hpge(metadata, registry=reg_or_none, name="my_gedet")
