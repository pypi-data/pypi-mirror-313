# About
This repository contains the source code, data and figures made available for the article [Blob-B-Gone: a lightweight framework for removing blob artifacts from 2D/3D MINFLUX single-particle tracking data](https://doi.org/10.3389/fbinf.2023.1268899) published in *Frontiers in Bioinformatics*.

# Blob-B-Gone
### Basic Usage
```python
from blobBgone import blobBgone

BBEG = blobBgone.from_npy('path/to/dir/')        # <- from files
BBEG = blobBgone.from_pointCloud(Dict[int,np.ndarray])  # <- from point cloud

BBEG.run()                                              # <- run the algorithm

blob_IDs = BBEG.blob_IDs()                              # <- get the blob IDs
free_IDs = BBEG.free_IDs()                              # <- get the free IDs

BBEG.plot_PCA()                                         # <- plot the PCA
```

### Advanced Usage
```python
from blobBgone import blobBgone

# create an instance of the blobBgone class #

# create a dictionary with the custom weights
custom_weights_2D = {MAX_DIST: float, CV_AREA:float, SPHE:float, ELLI:float, CV_DENSITY:float}
custom_weights_3D = {MAX_DIST: float, CV_VOL:float, SPHE:float, ELLI:float, CV_DENSITY:float}

# set custom weights depending on the dimensionality of your data
BBEG.custom_weights = custom_weights_2D/custom_weights_3D 
```

# Installation
### Via pip
```bash
pip install blobBgone
```

### From source
```bash
git clone
pip install .
```


## Python Environment
To run the notebooks found within this repository, you may need to create a conda environment with the required dependencies. The `dev_env.yml` file contains the necessary dependencies to run the code.

Requirements: [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [anaconda](https://www.anaconda.com/products/distribution) installed.
Dont forget that you can "**skip registration**" even when installing anaconda don't get confused by the [dark pattern](https://en.wikipedia.org/wiki/Dark_pattern) they put up. 

### Create the environment
Open a terminal or anaconda prompt and navigate to the root of the repository. Then run the following command:
```bash
conda env create -f dev_env.yml
```
After that you can activate the environment with:
```bash
conda activate BBEG
```

# Examples
The `notebooks` folder contains a series of Jupyter notebooks that demonstrate the use of and explain the logic behind the `blobBgone` package. 

# Repository Structure
The code is organized in a Python package called `blobBgone` and the data used in the article is available in the `Example_Data` folder. The figures appearing in the main text are available in the `Figures` folder.

```bash
C:.
├───blobBgone
│   └───__pycache__
├───blobBgone.egg-info
├───build
│   ├───bdist.win-amd64
│   └───lib
│       └───blobBgone
├───dist
├───Example_Data
│   ├───Additional_MFX_Data
│   │   ├───Labelled_Data
│   │   │   ├───blob
│   │   │   └───free
│   │   └───Labelled_Thumbnails
│   │       ├───blob
│   │       └───free
│   ├───MINFLUX Data
│   │   ├───Blob_GQ23nm_2D_Tracks
│   │   ├───Blob_GQ23nm_3D_Tracks
│   │   └───MINFLUX Tracking Sequences
│   └───Simulation
│       ├───2D_Mix_dynamicSTD
│       └───3D_Mix_dynamicSTD
├───Figures
│   ├───In Paper
│   │   ├───Main Text
│   │   └───Supplementary
│   └───Raw
│       ├───Additional
│       └───Initial
├───notebooks
└───__pycache__
```