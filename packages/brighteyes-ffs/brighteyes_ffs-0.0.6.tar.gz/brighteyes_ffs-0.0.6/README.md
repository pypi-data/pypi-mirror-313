# BrightEyes-FFS

A toolbox for analysing Fluorescence Correlation Spectroscopy (FCS) and Fluorescence Fluctuation Spectroscopy (FFS) data with array detectors.
The fcs module contains libraries for:

* Calculating autocorrelations and cross-correlations of raw FCS/FFS data (i.e. photon counts vs. time)
* Fitting correlations to various 2D and 3D diffusion models
* Calibration-free FCS/FFS analysis such as circular-scanning FCS and iMSD analysis
* Miscellaneous tools

The fcs_gui module contains libraries for:

* Storing and loading FCS/FFS analysis sessions, as used in the GUI

The dataio module contains libraries for:

* Fitting various models to data (polynomial, Gaussian, power law, etc.)
* Stokes-Einstein relation
* Save/load 2D arrays to/from .csv files
* Save data to .tiff file
* Miscellaneous tools

----------------------------------

## Installation

You can install `brighteyes-ffs` via [pip] directly from GitHub:

    pip install git+https://github.com/VicidominiLab/BrightEyes-FFS

or using the version on [PyPI]:

    pip install brighteyes-ffs
	
or:
	
	pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple brighteyes-ffs

It requires the following Python packages

    h5py
	joblib
	matplotlib>=3.3.2
	multipletau>=0.3.3
	numpy>=1.19.4
	pandas>=1.1.4
	scipy
	tifffile>=2020.9.29
	seaborn
	imutils
	PyQt5
	qdarkstyle
	nbformat

## License

Distributed under the terms of the [GNU GPL v3.0] license,
"BrightEyes-FFS" is free and open source software

## Contributing

You want to contribute? Great!
Contributing works best if you creat a pull request with your changes.

1. Fork the project.
2. Create a branch for your feature: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'My new feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request!
