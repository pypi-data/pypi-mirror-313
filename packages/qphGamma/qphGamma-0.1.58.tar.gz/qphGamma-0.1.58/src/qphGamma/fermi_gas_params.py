import numpy as np
import plasmapy.formulary as pp_form
import astropy.units as units
import math
from .constants import *
import warnings

warnings.filterwarnings("ignore")


class FGParams:
    """
    class FLParams generates Fermi gas parameters
    """

    def __init__(self, Te, N, V) -> None:
        """Function returns all parameters

        Args:
            Te (float): electronic temperature in eV
            N (int): Number of electrons in cell
            V (float): Volume of cell in Angstrom cubed
            Ef (float): Fermi energy of free electron gas in eV
            mu (float): Chemical potential of free electron gas in eV
            V_au (float): Volume in atomic units
            n_au (float): particle density (N/V) in a.u.
            kf (float): Fermi wave vector in a.u.
            rs (float): Wigner-Seitz radius in a.u.
            N0 (float): DOS at Ef in a.u.
        """
        self.Te = Te
        self.N = int(N)
        self.V = V
        self.Ef = (
            hbar_Js**2
            / (2 * m_e)
            * (3 * np.pi**2 * self.N / (self.V * 1e-30)) ** (2 / 3)
        ) * J_to_eV
        self.mu = self.Ef * (1 - 1 / 3 * ((np.pi * self.Te) / (2 * self.Ef)) ** 2)
        # Use atomic units:  hbar = m = e = 1  a.u
        self.V_au = self.V * (1.88973) ** 3  # a0^3
        self.n_au = self.N / self.V_au
        self.kf = (3 * np.pi**2 * self.n_au) ** (1 / 3)
        self.rs = (3 / (4 * np.pi * self.n_au)) ** (1 / 3)
        self.N0 = 3 * self.n_au / (self.kf**2)
