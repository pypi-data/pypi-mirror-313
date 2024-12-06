from __future__ import annotations

import json
from pathlib import Path

from legendmeta import AttrsDict
from pyg4ometry import geant4

from .bege import BEGe
from .invcoax import InvertedCoax
from .materials import make_enriched_germanium
from .p00664b import P00664B
from .ppc import PPC
from .semicoax import SemiCoax
from .v02160a import V02160A
from .v02162b import V02162B
from .v07646a import V07646A


def make_hpge(
    metadata: str | dict | AttrsDict,
    registry: geant4.Registry | None,
    allow_cylindrical_asymmetry: bool = True,
    **kwargs,
) -> geant4.LogicalVolume:
    """Construct an HPGe detector logical volume based on the detector metadata.

    Parameters
    ----------
    metadata
        LEGEND HPGe configuration metadata file containing
        detector static properties.
    registry
        pyg4ometry Geant4 registry instance.
    allow_cylindrical_asymmetry
        if true, use derived classes for detectors that break cylindrical
        symmetry. Otherwise, just build them using the base class (i.e.
        ignoring the non-symmetric features).

    Other Parameters
    ----------------
    **kwargs
        Additionally, the following arguments are allowed for
        overriding the name and the material from the metadata:

        name
            name to attach to the detector. Used to name
            solid and logical volume.
        material
            pyg4ometry Geant4 material for the detector.

    Examples
    --------
        >>> gedet = make_hpge(metadata, registry)

        >>> gedet = make_hpge(metadata, registry, name = "my_det", material = my_material)

    """
    if not isinstance(metadata, (dict, AttrsDict)):
        with Path(metadata).open() as jfile:
            gedet_meta = AttrsDict(json.load(jfile))
    else:
        gedet_meta = AttrsDict(metadata)

    material = kwargs.get("material")
    name = kwargs.get("name")

    if registry is None:
        registry = geant4.Registry()

    if material is None:
        if gedet_meta.production.enrichment is None:
            msg = "The enrichment argument in the metadata is None."
            raise ValueError(msg)
        # representation of enrichment data changed in legend-exp/legend-detectors PR #43 to
        # value and uncertainty.
        if isinstance(gedet_meta.production.enrichment, float):
            enrichment = gedet_meta.production.enrichment
        else:
            enrichment = gedet_meta.production.enrichment.val
        kwargs["material"] = make_enriched_germanium(enrichment, registry)

    if name is None:
        if gedet_meta.name is None:
            msg = "The name of the detector in the metadata is None."
            raise ValueError(msg)
        kwargs["name"] = gedet_meta.name

    if gedet_meta.type == "ppc":
        # asymmetric detector
        if allow_cylindrical_asymmetry and gedet_meta.name == "P00664B":
            gedet = P00664B(gedet_meta, registry=registry, **kwargs)
        else:
            gedet = PPC(gedet_meta, registry=registry, **kwargs)

    elif gedet_meta.type == "bege":
        gedet = BEGe(gedet_meta, registry=registry, **kwargs)

    elif gedet_meta.type == "icpc":
        if gedet_meta.name == "V07646A":
            gedet = V07646A(gedet_meta, registry=registry, **kwargs)
        # asymmetric detector
        elif allow_cylindrical_asymmetry and gedet_meta.name == "V02160A":
            gedet = V02160A(gedet_meta, registry=registry, **kwargs)
        elif gedet_meta.name == "V02162B":
            gedet = V02162B(gedet_meta, registry=registry, **kwargs)
        else:
            gedet = InvertedCoax(gedet_meta, registry=registry, **kwargs)

    elif gedet_meta.type == "coax":
        gedet = SemiCoax(gedet_meta, registry=registry, **kwargs)

    return gedet
