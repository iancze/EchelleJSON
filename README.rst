EchelleJSON
===========

A JSON format for storing spectra taken with echelle spectrographs (astronomy)

While FITS seems to be an industry standard for storing echelle spectra, the formats by which it is stored inside of this file can often be quite disparate and confusing to read, leaving IRAF as the only "sure-to-work" means of reading spectra from disk. To eliminate this dependency and store only the minimal amount of information necessary for a spectroscopic fitting routine (e.g., [Starfish](https://github.com/iancze/Starfish/)), we propose this simple, human-readable format in JSON.

The advantages of JSON is that it is a widely used format that is easily readable by nearly every programming language. In this package we provide Python scripts for the writing and reading of the format. If you develop scripts in other languages, pull requests are definitely welcome!

Echelle Spectra
=================

In contrast to single-order spectra at lower resolution, echelle spectra consist of multiple spectroscopic *orders*, where each order typically covers a different wavelength range. These orders may or may not have regions of wavelength overlap, and may or may not contain the same number of pixels. Therefore a simple 2D array of ```(norders, nlambda)`` may not always work as a storage format for echelle spectra from a particular instrument.

Therefore, each spectral order is stored as a separate 1D array in the ``EchelleJSON`` format. Single-order spectra can also be stored in the ``EchelleJSON`` format as if they were taken from a 1-order echelle.

Format
======

Wavelengths and Fluxes
----------------------

At minimum, (optical and infrared) spectra are the flux density ``[ergs/s/cm^2/Ang]`` as a unit of wavelength ``[Ang]``. If you're telescope reduction pipeline was generous, there might also be information from the telescope about the uncertainties in the spectral extraction (the "error" spectrum), and a binary mask for bad pixels. Therefore the spectrum should provide
::
    wl : a 1D array of length nlam, in units of [Ang]
    fl : a 1D array of length nlam, in units of [ergs/s/cm^2/Ang], or otherwise dimensionless if the spectra are unnormalized

and optionally provides
::
    sigma : a 1D array of length nlam
    mask: a boolean array of length nlam, true for good pixels, false for bad pixels

Routines that read in files without ``sigma`` defined might estimate it from ``sqrt(fl)```, if ``fl`` happens to be counts. Routines that read in files without ```mask`` defined would assume the mask is ```true`` everywhere.

Orders
------

Each order of the spectrum contains 1D arrays of ``wl`` and ``fl`` (and optionally ``sigma`` and ```mask``) as described above. Each order is stored top-level by a key, ```order_[name]```. ``name`` can be anything the user wants, as long as the name for each order is different, e.g. ```order_red`` and ```order_blue`` or ``order_01``, ``order_02``, ```order_03``, etc. And of course ```nlam`` may be different for each order.

Header
------

It is important to sufficiently document the provenance of a spectrum so that subsequent routines have all of the available information necessary to manipulate it during analysis. That said, many of the headers that are intrinsic to a ```FITS`` file may be superfluous to a spectroscopic fitting code. We recommend but do not enforce the following header fields
::
    BCV: 0.0 # [km/s] Barycentric correction, should default to 0.0 if not provided
    NAME: star # the name of your target
    DATE: 2016-02-26 # the date of your observation, in ISO format


``DATE`` should strive to be in [ISO format](http://stackoverflow.com/questions/10286204/the-right-json-date-format).

Python implementation
=====================

Unfortunately, there does not yet exist a built-in way to encode ``numpy`` arrays directly to JSON and vice-versa. Fortunately, ``astropy`` has provided a wonderful [encoder class](https://astropy.readthedocs.org/en/stable/api/astropy.utils.misc.JsonCustomEncoder.html) that nicely provides this functionality.
