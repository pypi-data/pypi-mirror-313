import numpy as np
import math
import warnings
from .constants import *

warnings.filterwarnings("ignore")


class FLGamma:
    """
    class FLGamma generates all necessary parameters and outputs for analysis
    """

    def __init__(self, E, Te, N, V) -> None:
        """Function returns all parameters

        Args:
            E (array): Energy array in eV
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
            a3 (float): alpha parameters in a.u.
            xi3 (float): xi3 parameters in a.u.
        """
        self.E = E
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
        self.a3 = np.pi**2 * self.N0 / (self.kf**2 * self.rs)
        self.xi3 = np.sqrt((self.a3 * self.rs) / (4 * np.pi)) * math.atan(
            np.sqrt(np.pi / (self.a3 * self.rs))
        ) + 1 / (2 * (1 + np.pi / (self.a3 * self.rs)))

    def gamma(self):
        """
        Function calculates Vignale FL gamma
        Returns:
            E_qph (2D array): Energy-mu and total quasiparticle and quasihole scattering rates
            E_qh (2D array): Energy-mu and  quasihole scattering rates
            E_qp (2D array): Energy-mu and  quasiparticle scattering rates
        """
        qh_gamma = (
            np.pi
            / (8 * hbar_eVfs * self.Ef)
            * ((self.mu - self.E) ** 2 + (np.pi * self.Te) ** 2)
            / (1 + np.exp(-(self.mu - self.E) / self.Te))
            * self.xi3
        )
        qp_gamma = (
            np.pi
            / (8 * hbar_eVfs * self.Ef)
            * ((self.E - self.mu) ** 2 + (np.pi * self.Te) ** 2)
            / (1 + np.exp(-(self.E - self.mu) / self.Te))
            * self.xi3
        )

        E_qph = np.array([self.E - self.mu, qh_gamma + qp_gamma]).T
        E_qh = np.array([self.E - self.mu, qh_gamma]).T
        E_qp = np.array([self.E - self.mu, qp_gamma]).T
        return E_qph, E_qh, E_qp
