In our efforts to achieve FAIR data practices at BESSY II, we are leveraging the NeXus standard [[1](https://www.nexusformat.org)], a common data exchange format for data obtained in the fields of neutron, muon, and X-ray science. Two core components of this standard are its base classes and application definitions. NeXus base classes serve as building blocks, offering community-agreed names and data structures for all devices required to run an experiment, including those on the beamline. Built upon these base classes, NeXus application definitions specify the minimal required structures and data elements necessary to represent a given experimental technique. In this work, we present preliminary results from the development of an application definition for a multi-modal experiment conducted at the mySpot beamline of BESSY II. This versatile beamline supports measurements with multiple techniques - XRD, SAXS, XRF, EXAFS, and XANES performed simultaneously under in-operando conditions. For the data conversion process, we use pynxtools [[2](https://github.com/FAIRmat-NFDI/pynxtools)], a tool designed to facilitate FAIR experimental data. Additionally, we discuss the perspective of this development for the Bluesky NeXus package [[3](https://codebase.helmholtz.cloud/hzb/bluesky/core/source/bluesky_nexus
)], developed at BESSY II, which enables the automated export of NeXus-compliant HDF5 files for Blueksy-based experiments and beamlines.


## Figure 8 — BESSY-II Techniques and NeXus Mapping

Mapping of current experiment techniques at BESSY-II to NeXus application
definitions. The number in brackets indicates the number of beamlines
performing a given experimental technique.

[Source: S. Patel et al., ICALEPCS 2025, TUPD111, pp. 758–762](https://pure.mpg.de/rest/items/item_3684708_2/component/file_3684709/content)

<iframe
  src="../assets/figure8_interactive.html"
  width="100%"
  height="880px"
  style="border:none; border-radius:8px;"
></iframe>



