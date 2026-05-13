### Create a Python Environment

```
python -m venv ewoks-env
source ewoks-env/bin/activate
```


### Install Required Packages
```
pip install -e .
```

Or manually:

```
pip install ewokscore silx h5py numpy pynxtools
```

### Organize Your Input Data

```
experiment/
├── 2022-09-30_scans.spec
├── mca/
│   ├── 2022-09-30_scans_00003_00001.mca
│   ├── 2022-09-30_scans_00003_00002.mca
│   ├── ...
```

Important:

all `.mca` files must be inside `mca/`directory and
naming must follow:

```
<basename>_<scan>_<point>.mca
```

Example:

```
2022-09-30_scans_00003_00521.mca
```

### Edit EWOKS Workflow Paths

Open `workflows/nexus_conversion.json` and edit paths of input and output:
```
{
  "spec_file": "/absolute/path/to/2022-09-30_scans.spec",
  "mca_dir": "/absolute/path/to/mca",
  "output_h5": "/absolute/path/to/intermediate.h5"
}
```

### Run the Workflow
```
ewoks execute workflows/nexus_conversion.json
```
If successful, you should see geneated files: `intermediate.h5` and `output.nxs`

### Verify the generated files
```
h5ls -r output.nxs
```

You should see somthing like:
```
/entry
/entry/instrument
/entry/instrument/detector
/entry/instrument/detector/data
```

### Complete NeXus structure
```
├── 1.1  # silx converter structure unchange
|   ├── instrument
|   ├── measurement
|   ├── start_time
|   ├── title 
├── 2.1
├── 3.1
├── ...
├── mca/
|   ├── spectra_scans_00001
│       ├── ENTRY_1
│           ├── title
|           ├── start_time
|           ├── definition (`NXfluo`)
|           ├── INSTRUMENT
|               ├── SOURCE
|                   ├── type
|                   ├── name
|                   ├── probe (`x-ray`)
|               ├── monochromator
|                   ├── wavelength
|               ├── fluoroscence
|                   ├── data
|                   ├── energy
|           ├── SAMPLE
|           ├── MONITOR
|           ├── data
|               ├── energy (`/entry/instrument/fluorescence/energy`)
|               ├── data (`entry/instrument/fluorescence/data`)
│       ├── ENTRY_2
│       ├── ENTRY_3
│       ├── ...
│   ├── spectra_scans_00002
│   ├── spectra_scans_00003
|   ├── ...
├── mca_process
|   ├── map_scans_00001
|       ├── program
|       ├── version
|       ├── NOTE
|       ├── PARAMETERS
|       ├── DATA
|   ├── map_scans_00002
|   ├── map_scans_00003
|   ├── ....

```


