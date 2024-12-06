from scipy import constants


hbar_eVfs = (
    constants.hbar
    / constants.physical_constants["electron volt-joule relationship"][0]
    * 1e15
)  # eV/fs
J_to_eV = 1 / constants.physical_constants["electron volt-joule relationship"][0]
eV_to_au = 1 / constants.physical_constants["Hartree energy in eV"][0]
K_to_eV = 1 / constants.physical_constants["electron volt-kelvin relationship"][0]
eV_to_K = 1 / K_to_eV
eV_to_au = 1 / constants.physical_constants["Hartree energy in eV"][0]
# From KGCollection.cpp
hbar_Js = constants.hbar
m_e = constants.m_e
angstrom = constants.angstrom
charge_e = constants.elementary_charge
eV = constants.electron_volt
ohm_to_cgs = 0.11111111111111e-11
m_to_cgs = 1e2
hbar_eVs = (
    constants.hbar / constants.physical_constants["electron volt-joule relationship"][0]
)
c_cgs = 2.99792458e10
m_to_a0 = 1 / constants.physical_constants["Bohr radius"][0]
kB = constants.Boltzmann
