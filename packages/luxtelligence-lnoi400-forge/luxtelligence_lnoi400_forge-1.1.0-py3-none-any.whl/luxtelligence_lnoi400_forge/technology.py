from .utils import cpw_spec

import tidy3d as td
import photonforge as pf


_Medium = td.components.medium.MediumType


def lnoi400(
    *,
    ln_thickness: float = 0.4,
    slab_thickness: float = 0.2,
    sidewall_angle: float = 13,
    box_thickness: float = 4.7,
    tl_thickness: float = 0.9,
    tl_separation: float = 1,
    include_substrate: bool = False,
    include_top_opening: bool = False,
    sio2: _Medium = td.material_library["SiO2"]["Palik_Lossless"],
    si: _Medium = td.material_library["cSi"]["Li1993_293K"],
    ln: _Medium = td.material_library["LiNbO3"]["Zelmon1997"](optical_axis=1),
    tl_metal: _Medium = td.material_library["Au"]["JohnsonChristy1972"],
    opening: _Medium = td.Medium(permittivity=1.0, name="Opening"),
) -> pf.Technology:
    """Create a technology for the LNOI400 PDK.

    Args:
        ln_thickness (float): LiNbO₃ layer thickness.
        slab_thickness (float): Partially etched slab thickness in LiNbO₃.
        sidewall_angle (float): Sidewall angle (in degrees) for LiNbO₃
          etching.
        box_thickness (float): Thickness of the bottom oxide clad.
        tl_thickness (float): TL layer thickness.
        tl_separation (float): Separation between the LiNbO₃ and TL layers.
        include_substrate (bool): Flag indicating whether or not to include
          the silicon substrate.
        include_top_opening (bool): Flag indicating whether or not to
          include the open region above the last extrusion layer.
        sio2 (Medium): Oxide and background medium.
        si (Medium): Silicon medium.
        ln (Medium): LiNbO₃ medium.
        tl_metal (Medium): TL and heater metal medium.
        opening (Medium): Medium for openings.

    Returns:
        Technology: E-Beam PDK technology definition.
    """
    # Layers
    layers = {
        "LN_RIDGE": pf.LayerSpec(
            layer=(2, 0), description="LN etch (ridge)", color="#7d57de18", pattern="//"
        ),
        "LN_SLAB": pf.LayerSpec(
            layer=(3, 0), description="LN etch (full)", color="#00008018", pattern="\\"
        ),
        "SLAB_NEGATIVE": pf.LayerSpec(
            layer=(3, 1), description="Slab etch negative", color="#6750bf18", pattern="\\"
        ),
        "LABELS": pf.LayerSpec(
            layer=(4, 0), description="Labels (LN etch)", color="#5179b518", pattern="/"
        ),
        "CHIP_CONTOUR": pf.LayerSpec(
            layer=(6, 0), description="Usable floorplan area", color="#ffc6b818", pattern="\\"
        ),
        "CHIP_EXCLUSION_ZONE": pf.LayerSpec(
            layer=(6, 1), description="Final chip boundaries", color="#00fe9c18", pattern="/"
        ),
        "TL": pf.LayerSpec(
            layer=(21, 0), description="Metal transmission lines", color="#3503fc18", pattern="\\"
        ),
        "HT": pf.LayerSpec(
            layer=(21, 1), description="Metal heaters", color="#a3c50318", pattern="."
        ),
        "ALIGN": pf.LayerSpec(
            layer=(31, 0), description="Alignment markers (LN etch)", color="#ba29c218", pattern="/"
        ),
        "DOC": pf.LayerSpec(
            layer=(201, 0),
            description="Labels for GDS layout (not fabricated)",
            color="#80a8ff18",
            pattern=".",
        ),
    }

    # Extrusion specifications
    bounds = pf.MaskSpec()  # Empty mask for all chip bounds
    full_ln_mask = pf.MaskSpec([(2, 0), (4, 0), (31, 0)], [], "+")
    slab_etch_mask = pf.MaskSpec((3, 1), (3, 0), "-")
    tl_mask = pf.MaskSpec((21, 0))
    ht_mask = pf.MaskSpec((21, 1))

    z_tl = ln_thickness + tl_separation
    z_top = z_tl + tl_thickness

    extrusion_specs = [
        pf.ExtrusionSpec(bounds, ln, (0, slab_thickness), 0),
        pf.ExtrusionSpec(full_ln_mask, ln, (0, ln_thickness), sidewall_angle),
        pf.ExtrusionSpec(slab_etch_mask, sio2, (0, ln_thickness), -sidewall_angle),
        pf.ExtrusionSpec(tl_mask, tl_metal, (z_tl, z_top)),
        pf.ExtrusionSpec(ht_mask, tl_metal, (z_tl, z_top)),
    ]

    if include_substrate:
        extrusion_specs.append(pf.ExtrusionSpec(bounds, si, (-pf.Z_INF, -box_thickness)))

    if include_top_opening:
        extrusion_specs.append(pf.ExtrusionSpec(bounds, opening, (z_top, pf.Z_INF)))

    rwg_port_gap = min(1.5, box_thickness)
    rwg_port_limits = (-rwg_port_gap, ln_thickness + rwg_port_gap)
    swg_port_gap = min(2.1, box_thickness)
    swg_port_limits = (-swg_port_gap, slab_thickness + swg_port_gap)

    ports = {
        "RWG1000": pf.PortSpec(
            description="LN single mode ridge waveguide for C-band, TE mode",
            width=5,
            limits=rwg_port_limits,
            num_modes=2,
            target_neff=2.2,
            path_profiles=((1, 0, (2, 0)), (10, 0, (3, 0))),
        ),
        "RWG3000": pf.PortSpec(
            description="LN multimode mode ridge for C-band, TE mode",
            width=8,
            limits=rwg_port_limits,
            num_modes=5,
            target_neff=2.2,
            path_profiles=((3, 0, (2, 0)), (12, 0, (3, 0))),
        ),
        "SWG250": pf.PortSpec(
            description="LN strip waveguide for C-band, TE mode",
            width=10,
            limits=swg_port_limits,
            num_modes=1,
            target_neff=2.2,
            path_profiles=((0.25, 0, (3, 0)), (12, 0, (3, 1))),
        ),
        "UniCPW": cpw_spec(),
        "UniCPW-EO": cpw_spec(10, 4, 180),
    }

    return pf.Technology("LNOI400", "1.1.0", layers, extrusion_specs, ports, sio2)
