import numpy as np
from scipy import integrate
from scipy.stats import logistic
from scipy.interpolate import interp1d
import math
import warnings
from .constants import *
from .fermi_gas_params import FGParams
from .fermi_gas_dos import FermiGasDOS

warnings.filterwarnings("ignore")


#!---------------------------------------------------------------
# * Start getting the chemical potential by integrating over the occ*DOS section


# binary search function
def binary_search(Te, N, E, dos, bs_E):
    bs_N = [integrate.simpson(logistic.sf(E, Ef, Te) * dos, E) for Ef in bs_E]
    if np.round(bs_N[1], 6) == N:
        return bs_E[1], bs_N[1]
    elif bs_N[1] > N:
        return binary_search(Te, N, E, dos, [bs_E[0], np.mean(bs_E[:2]), bs_E[1]])
    elif bs_N[1] < N:
        return binary_search(Te, N, E, dos, [bs_E[1], np.mean(bs_E[1:]), bs_E[2]])


# integrated DOS*occ to find the chemical potential for given Te
def integrate_for_mu(Te, N, E, dos, search_min=-10000, search_max=10000):
    Ef, Ni = binary_search(Te, N, E, dos, [search_min, 0, search_max])
    return Ef, Ni


# * End getting the chemical potential by integrating over the occ*DOS section
#!---------------------------------------------------------------

#!---------------------------------------------------------------
# * Start gamma sections


def get_qh_gamma(E, mu, Te, Ef, xi3):
    qh_gamma = (
        np.pi
        / (8 * hbar_eVfs * Ef)
        * ((mu - E) ** 2 + (np.pi * Te) ** 2)
        / (1 + np.exp(-(mu - E) / Te))
        * xi3
    )
    return qh_gamma


def get_qp_gamma(E, mu, Te, Ef, xi3):
    qp_gamma = (
        np.pi
        / (8 * hbar_eVfs * Ef)
        * ((E - mu) ** 2 + (np.pi * Te) ** 2)
        / (1 + np.exp(-(E - mu) / Te))
        * xi3
    )
    return qp_gamma


def get_avg_gamma(gamma, dos, occ, E):
    return integrate.simpson(gamma * dos * occ, E)


# * End gamma sections
#!---------------------------------------------------------------


class VignaleGamma:
    """
    class VignaleGamma generates all necessary parameters and outputs for analysis
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
        fg_params = FGParams(self.Te, self.N, self.V)
        self.Ef = fg_params.Ef
        self.model_mu = fg_params.mu
        self.V_au = fg_params.V_au
        self.kf = fg_params.kf
        self.rs = fg_params.rs
        self.N0 = fg_params.N0
        self.a3 = np.pi**2 * self.N0 / (self.kf**2 * self.rs)
        self.xi3 = np.sqrt((self.a3 * self.rs) / (4 * np.pi)) * math.atan(
            np.sqrt(np.pi / (self.a3 * self.rs))
        ) + 1 / (2 * (1 + np.pi / (self.a3 * self.rs)))
        #! Here, think about how to handle below
        fg_dos = FermiGasDOS(self.E, self.V)
        self.dos = fg_dos.dos
        self.mu = integrate_for_mu(self.Te, self.N, self.E, self.dos)[0]
        self.occ = logistic.sf(self.E, self.mu, self.Te)
        self.qh_gamma = get_qh_gamma(self.E, self.mu, self.Te, self.Ef, self.xi3)
        self.qp_gamma = get_qp_gamma(self.E, self.mu, self.Te, self.Ef, self.xi3)
        self.total_gamma = self.qh_gamma + self.qp_gamma
        self.avg_gamma = get_avg_gamma(self.qp_gamma, self.dos, self.occ, self.E)
        self.E_mu = self.E - self.mu
