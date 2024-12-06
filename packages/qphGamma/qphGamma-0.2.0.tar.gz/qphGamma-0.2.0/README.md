# qphGamma - Python package for analyzing qp (e-) and qh (h+) scattering rates

This package is used to calculate, post-process, and analyze qp and qh scattering rates.  Currently, it supports calculating the scattering rate from a finite-temperature *GW* calculation, through the relation between the imaginary part of the electron-self energy and the scattering rate. It also allows for one to calculate the scattering rate predicted by the Vignale Fermi-liquid (FL) approximation.

Currently, this package will do the following
- Energy- and electronic temperature-dependent scattering rate
- Energy averaged scattering rate
  - Found by integrating total (qp+qh) gamma, occ., 1-occ., and dos over energy
  - Choice of gamma, dos, and occ. must be made
