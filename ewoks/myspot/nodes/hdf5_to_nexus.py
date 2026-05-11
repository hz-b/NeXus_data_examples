# hdf5_to_nexus.py

from __future__ import annotations

import re
import h5py
import numpy as np
from ewokscore import Task


class HDF5ToNeXusNode(Task):

    @classmethod
    def input_names(cls):
        return [
            "input_h5",
            "nexus_config",
            "output_nexus",
        ]

    @classmethod
    def optional_input_names(cls):
        # return []
        return set()

    def run(self):

        input_h5 = self.inputs["input_h5"]
        output_nexus = self.inputs["output_nexus"]

        with h5py.File(input_h5, "r") as h5, h5py.File(output_nexus, "w") as nx:

            scan_names = self._find_all_scans(h5)

            for scan_name in scan_names:

                print(f"Processing scan: {scan_name}")

                scan_group = h5[scan_name]

                title = scan_group["title"][()].decode()

                mesh_info = self._parse_mesh_title(title)

                if mesh_info is None:
                    continue

                x_motor = mesh_info["x_motor"]
                y_motor = mesh_info["y_motor"]

                nx_points = mesh_info["nx"]
                ny_points = mesh_info["ny"]

                measurement = scan_group["measurement"]

                x_positions = measurement[x_motor][()]

                if y_motor is None:
                    y_positions = np.array([0.0], dtype=np.float32)
                else:
                    y_positions = measurement[y_motor][()]

                spec_scan_number = int(scan_name.split(".")[0])

                mca_group_name = f"scan_{spec_scan_number:05d}"

                if mca_group_name not in h5["mca"]:

                    print(
                        f"WARNING: MCA group '{mca_group_name}' "
                        f"does not exist for scan '{scan_name}'. Skipping."
                    )

                    continue

                mca_group = h5["mca"][mca_group_name]

                point_keys = sorted(mca_group.keys())

                if not point_keys:

                    print(
                        f"WARNING: No spectra found in "
                        f"'{mca_group_name}'. Skipping."
                    )

                    continue

                expected_points = nx_points * ny_points

                first_spectrum = mca_group[point_keys[0]][()]

                nchannels = first_spectrum.shape[0]

                detector_map = np.zeros(
                    (ny_points, nx_points, nchannels),
                    dtype=np.float32,
                )

                for i, key in enumerate(point_keys):

                    if i >= expected_points:
                        break

                    iy = i // nx_points
                    ix = i % nx_points

                    detector_map[iy, ix, :] = mca_group[key][()]

                entry_name = f"entry_{spec_scan_number:05d}"

                entry = nx.create_group(entry_name)
                entry.attrs["NX_class"] = "NXentry"

                instrument = entry.create_group("instrument")
                instrument.attrs["NX_class"] = "NXinstrument"

                detector = instrument.create_group("detector")
                detector.attrs["NX_class"] = "NXdetector"

                detector.create_dataset(
                    "data",
                    data=detector_map,
                    compression="gzip",
                )

                detector.create_dataset(
                    "x_positions",
                    data=x_positions,
                )

                detector.create_dataset(
                    "y_positions",
                    data=y_positions,
                )

                detector["data"].attrs["signal"] = 1
                detector["data"].attrs["interpretation"] = "spectrum"

                print(f"Finished scan: {scan_name}")

    @staticmethod
    def _find_all_scans(h5):

        scans = []

        for key in h5.keys():

            if key[0].isdigit():

                scans.append(key)

        scans = sorted(scans)

        if not scans:
            raise RuntimeError("No SPEC scans found")

        return scans

    @staticmethod
    def _parse_mesh_title(title):

        title = title.strip()

        if title.startswith("ascan"):

            parts = title.split()

            motor = parts[1]

            start = float(parts[2])
            end = float(parts[3])

            npoints = int(parts[4]) + 1

            return {
                "scan_type": "ascan",
                "x_motor": motor,
                "x_start": start,
                "x_end": end,
                "nx": npoints,
                "y_motor": None,
                "ny": 1,
            }

        mesh_re = re.compile(
            r"(mesh|dmesh|eigermesh)\s+"
            r"(\w+)\s+([\d\.-]+)\s+"
            r"([\d\.-]+)\s+(\d+)\s+"
            r"(\w+)\s+([\d\.-]+)\s+"
            r"([\d\.-]+)\s+(\d+)"
        )

        match = mesh_re.search(title)

        if match is not None:

            return {
                "scan_type": "mesh",
                "x_motor": match.group(2),
                "x_start": float(match.group(3)),
                "x_end": float(match.group(4)),
                "nx": int(match.group(5)) + 1,
                "y_motor": match.group(6),
                "y_start": float(match.group(7)),
                "y_end": float(match.group(8)),
                "ny": int(match.group(9)) + 1,
            }

        print(
             f"WARNING: Unsupported scan title: "
             f"' {title}'. Skipping scan."
             )

        return None
