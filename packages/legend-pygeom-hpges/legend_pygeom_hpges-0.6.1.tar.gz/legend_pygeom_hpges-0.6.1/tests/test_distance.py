from __future__ import annotations

import pathlib

import numpy as np
import pytest
from legendmeta import TextDB
from legendtestdata import LegendTestData
from pyg4ometry import geant4

from legendhpges import make_hpge

configs = TextDB(pathlib.Path(__file__).parent.resolve() / "configs")


@pytest.fixture(scope="session")
def test_data_configs():
    ldata = LegendTestData()
    ldata.checkout("2553a28")
    return ldata.get_path("legend/metadata/hardware/detectors/germanium/diodes")


@pytest.fixture(params=["r", "n"])
def reg(request):
    return geant4.Registry() if request.param == "r" else None


def test_not_implemented(reg):
    ppc = make_hpge(configs.P00664B, registry=reg)

    with pytest.raises(NotImplementedError):
        ppc.distance_to_surface([[1, 0, 0]])


def test_bad_dimensions(test_data_configs, reg):
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg)

    with pytest.raises(ValueError):
        gedet.distance_to_surface([[1, 0, 0, 0]])


def test_output(test_data_configs, reg):
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg)
    dist = gedet.distance_to_surface([[0, 0, 0], [1, 3, 3], [0, 0, 0]])

    assert np.shape(dist == (3,))
    assert np.all(dist >= 0)

    dist_indices = gedet.distance_to_surface(
        [[0, 0, 0], [1, 3, 3], [0, 0, 0]], surface_indices=[0, 3]
    )
    assert np.all(dist_indices >= dist)


def test_inside_not_implemented(reg):
    ppc = make_hpge(configs.P00664B, registry=reg)

    with pytest.raises(NotImplementedError):
        ppc.is_inside([[1, 0, 0]])


def test_inside_bad_dimensions(test_data_configs, reg):
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg)

    with pytest.raises(ValueError):
        gedet.is_inside([[1, 0, 0, 0]])


def test_inside_output(test_data_configs, reg):
    gedet = make_hpge(test_data_configs + "/B99000A.json", registry=reg)
    r, z = gedet._decode_polycone_coord()

    # detetor is a simple bege
    # p+ at 0-7.5 mm
    # groove at 10-12 mm 2mm deep
    # radius and height 40mm

    theta = 33
    cos = np.cos(np.deg2rad(theta))
    sin = np.sin(np.deg2rad(theta))

    # 1) on axis inside
    # 2) below outside
    # 3) inside groove
    # 4) above groove
    # 5) outside side
    # 6) exactly on the side
    # 7) far above top

    coords = np.array(
        [
            [0, 0, 10],
            [5 * cos, 5 * sin, -0.1],
            [11 * cos, 11 * sin, 1],
            [11 * cos, 11 * sin, 4],
            [50 * cos, 50 * sin, 10],
            [40 * cos, 40 * sin, 10],
            [20, 20, 1000],
        ]
    )

    is_in = gedet.is_inside(coords, tol=1e-11)

    assert np.all(is_in == np.array([True, False, False, True, False, True, False]))
