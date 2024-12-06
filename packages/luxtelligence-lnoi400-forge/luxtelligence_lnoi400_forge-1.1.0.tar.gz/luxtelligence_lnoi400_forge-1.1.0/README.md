# Luxtelligence LNOI400

This python module implements the [Luxtelligence](https://luxtelligence.ai/)
LNOI400 PDK as components and technology specification for
[PhotonForge](https://docs.flexcompute.com/projects/photonforge/)


## Installation

Installation via `pip`:

    pip install luxtelligence-lnoi400-forge


### PhotonForge Web UI

1. [Download from
   PyPI](https://pypi.org/project/luxtelligence-lnoi400-forge/#files) the
   latest wheel file: `luxtelligence_lnoi400_forge-*-py3-none-any.whl`.

2. In the PhotonForge web interface, upload that file to load the LNOI400 PDK.


## Usage

The simplest way to use the this PDK in PhotonForge is to set its technology as
default:

    import photonforge as pf
    import luxtelligence_lnoi400_forge as lxt

    tech = lxt.lnoi400()
    pf.config.default_technology = tech


The `lnoi400` function creates a parametric technology and accepts a number of
parameters to fine-tune the technology.

PDK components are available in the `component` submodule. The list of
components can be discovered by:

    dir(lxt.component)
    
    pdk_component = lxt.component.mmi1x2()


Utility functions `cpw_spec` and `place_edge_couplers` are also available for
generating CPW port specifications and placing edge couplers at chip boudaries.

More information can be obtained in the documentation for each function:

    help(lxt.lnoi400)

    help(lxt.component.mmi1x2)

    help(lxt.place_edge_couplers)


## Warnings

Please note that the 3D structures obtained by extrusion through this module's
technologies are a best approximation of the intended fabricated structures,
but the actual final dimensions may differ due to several fabrication-specific
effects. In particular, doping profiles are represented with hard-boundary,
homogeneous solids, but, in practice will present process-dependent variations
with smooth boundaries.
