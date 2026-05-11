from __future__ import annotations

import glob
import os
import re
from pathlib import Path

import h5py
import numpy as np
from ewokscore import Task
from silx.io.convert import write_to_h5


MCA_PATTERN = re.compile(r".*_(\d{5})_(\d{5})\.mca$")


class SpecToHDF5Node(Task):
 
    @classmethod
    def input_names(cls):
        return ["spec_file", "mca_dir", "output_h5"]

    @classmethod
    def output_names(cls):
        return ["hdf5_file"]

    @classmethod
    def optional_output_names(cls):
        return []
    

    # input_names = ["spec_file", "mca_dir", "output_h5"]
    # output_names = ["hdf5_file"]

    def run(self):
        #spec_file = self.inputs.spec_file
        spec_file = self.inputs["spec_file"]
        # mca_dir = self.inputs.mca_dir
        mca_dir = self.inputs["mca_dir"]
        #output_h5 = str(Path(self.inputs.output_h5).absolute())
        output_h5 = self.inputs["output_h5"]

        with h5py.File(output_h5, "w") as h5:
            write_to_h5(spec_file, h5)

        mca_files = sorted(glob.glob(os.path.join(mca_dir, "*.mca")))

        with h5py.File(output_h5, "a") as h5:
            mca_group = h5.require_group("mca")

            for mca_file in mca_files:
                filename = os.path.basename(mca_file)

                match = MCA_PATTERN.match(filename)
                if match is None:
                    continue

                scan_number = int(match.group(1))
                point_number = int(match.group(2))

                spectrum = self._read_mca_spectrum(mca_file)

                scan_group = mca_group.require_group(
                    f"scan_{scan_number:05d}"
                )

                dset_name = f"point_{point_number:05d}"

                if dset_name in scan_group:
                    del scan_group[dset_name]

                dset = scan_group.create_dataset(
                    dset_name,
                    data=spectrum,
                    compression="gzip",
                )

                dset.attrs["source_file"] = filename
                dset.attrs["scan_number"] = scan_number
                dset.attrs["point_number"] = point_number

        #self.outputs.hdf5_file = output_h5
        # self.outputs["hdf5_file"] = output_h5
        # self.outputs._variables["hdf5_file"].value


    @staticmethod
    def _read_mca_spectrum(mca_file: str) -> np.ndarray:
	    """
	    Read SPEC-style MCA spectrum.

	    Handles lines like:
	
	    @A 12 34 56 ...
	    """

	    values = []

	    with open(mca_file, "r") as f:

	        for line in f:

	            line = line.strip()

	            if not line:
	                continue

	            # Skip comments
	            if line.startswith("#"):
	                continue

	            # Remove SPEC MCA marker
	            if line.startswith("@A"):
	                line = line[2:].strip()

	            parts = line.split()

	            for p in parts:

	                try:
	                    values.append(float(p))

	                except ValueError:
	                    # Ignore malformed tokens
	                    continue

	    return np.asarray(values, dtype=np.float32)
