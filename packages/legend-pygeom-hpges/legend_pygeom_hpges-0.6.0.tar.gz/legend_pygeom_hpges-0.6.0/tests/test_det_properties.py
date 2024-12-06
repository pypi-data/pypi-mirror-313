from __future__ import annotations

import pathlib

import numpy as np
import pytest
from legendmeta import TextDB
from legendtestdata import LegendTestData
from pyg4ometry import geant4

from legendhpges import (
    make_hpge,
)
from legendhpges.materials import make_natural_germanium

reg = geant4.Registry()
natural_germanium = make_natural_germanium(reg)
configs = TextDB(pathlib.Path(__file__).parent.resolve() / "configs")


@pytest.fixture(scope="session")
def test_data_configs():
    ldata = LegendTestData()
    ldata.checkout("5f9b368")
    return ldata.get_path("legend/metadata/hardware/detectors/germanium/diodes")


def test_surface_area(test_data_configs):
    reg = geant4.Registry()
    gedet = make_hpge(test_data_configs + "/C99000A.json", registry=reg)

    assert len(gedet.surface_area(surface_indices=[])) == 0
    assert np.sum(gedet.surface_area(surface_indices=None)) > 0
