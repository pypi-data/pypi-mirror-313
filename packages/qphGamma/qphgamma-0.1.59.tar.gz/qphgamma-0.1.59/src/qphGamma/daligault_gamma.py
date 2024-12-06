import numpy as np
from scipy import integrate
from scipy.stats import logistic
import plasmapy.formulary as pp_form
import astropy.units as units
from .constants import *
import warnings
from .fermi_gas_dos import FermiGasDOS

warnings.filterwarnings("ignore")


#!---------------------------------------------------------------
# * Start of density- and theta-dependent parameter section


def get_kF(n):
    return (3 * np.pi**2 * n) ** (1 / 3)


def get_T_from_theta(n, theta):
    Ef = pp_form.quantum.Ef_(n * units.m**-3).value
    return theta * Ef / kB


def get_mu_quantum(n, theta):
    T = get_T_from_theta(n, theta)
    Ef = pp_form.quantum.Ef_(n * units.m**-3).value
    return Ef * (1 - 1 / 3 * ((np.pi * kB * T) / (2 * Ef)) ** 2)


# Eq. 5.26 on pp. 40 in Fetter and Walecka
def get_mu_classical(n, theta):
    T = get_T_from_theta(n, theta)
    mu = kB * T * np.log(n / 2 * pp_form.quantum.lambdaDB_th_(T * units.K).value ** 3)
    return mu


def get_mu(n, theta, theta_cutoff=1):
    if theta < theta_cutoff:
        mu = get_mu_quantum(n, theta)
    elif theta >= theta_cutoff:
        mu = get_mu_classical(n, theta)
    return mu


def get_omega_p(n):
    return pp_form.plasma_frequency(n * units.m**-3, particle="e-").value


# * End of density-dependent parameter section
#!---------------------------------------------------------------

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
# * Start of Eq. (4) section


def get_u_integral(u, k_kF, q_kF, theta, sq_mu):
    integral_first_term = (1 / (1 - np.exp(((2 * q_kF) / theta) * u))) * (
        1
        / (
            1
            + np.exp((-(2 * q_kF) / theta) * u)
            * np.exp((1 / theta) * (sq_mu - k_kF**2))
        )
    )
    integral_second_term = np.log(
        (1 + np.exp((1 / theta) * (sq_mu - (u + q_kF / 2) ** 2)))
        / (1 + np.exp((1 / theta) * (sq_mu - (-u + q_kF / 2) ** 2)))
    )

    return integral_first_term * integral_second_term


def get_G(k_kF, q_kF, theta, sq_mu, F_12, F_n12):

    integral, error = integrate.quad(
        get_u_integral,
        q_kF / 2 - k_kF,
        q_kF / 2 + k_kF,
        args=(k_kF, q_kF, theta, sq_mu),
    )

    G = (
        (9 * np.pi / (16 * np.sqrt(2)))
        * (theta ** (5 / 2))
        * (F_12 / F_n12) ** (3 / 2)
        * (q_kF / k_kF)
        * integral
    )

    return G, error


# * End of Eq. (4) section
#!---------------------------------------------------------------

#!---------------------------------------------------------------
# * Start of v(q) section


def get_k_sc(n, theta, F_12, F_n12):
    T = get_T_from_theta(n, theta)
    k_DH = 1 / pp_form.lengths.Debye_length(T * units.K, n * units.m**-3).value  # 1/m
    k_sc = k_DH * np.sqrt(F_n12 / F_12)  # 1/m

    return k_sc


def get_v(q, k_sc):
    v = 1 / (q**2 + k_sc**2)
    return v


# * End of v(q) section
#!---------------------------------------------------------------


#!---------------------------------------------------------------
# * Start of Eq. (3) section


def get_q_integrand(q, q_kF, k_kF, k_sc, theta, sq_mu, F_12, F_n12):
    v2 = np.abs(get_v(q, k_sc)) ** 2
    G = get_G(k_kF, q_kF, theta, sq_mu, F_12, F_n12)[0]

    q_integrand = v2 * G
    return q_integrand


def get_Eq_3(q_list, kF, k_kF, k_sc, theta, sq_mu, F_12, F_n12):

    q_integrand = np.array(
        [
            get_q_integrand(q, q / kF, k_kF, k_sc, theta, sq_mu, F_12, F_n12)
            for q in q_list
        ]
    )
    q_integral = integrate.cumtrapz(q_integrand, q_list, initial=0)[-1]

    return k_sc**3 * q_integral


def get_gamma_omega_p(q_kF_list, k_kF_list, n, theta, mu):
    # * Assign values independent of k and q
    kF = get_kF(n)
    sq_mu = mu / pp_form.quantum.Ef_(n * units.m**-3).value
    F_12 = np.real(pp_form.mathematics.Fermi_integral(sq_mu / theta, 1 / 2))
    F_n12 = np.real(pp_form.mathematics.Fermi_integral(sq_mu / theta, -1 / 2))
    k_sc = get_k_sc(n, theta, F_12, F_n12)
    q_list = q_kF_list * get_kF(n)
    k_list = k_kF_list * get_kF(n)

    gamma_omega_p = np.array(
        [get_Eq_3(q_list, kF, k / kF, k_sc, theta, sq_mu, F_12, F_n12) for k in k_list]
    )

    return gamma_omega_p


# * End of Eq. (3) section
#!---------------------------------------------------------------

#!---------------------------------------------------------------
# * Start of Gamma section


def get_gamma(E, n, mu, theta, q_kF_list):
    """
    Function calculates Daligault gamma
    Returns:
        E_mu (1D array): Energy-mu (eV)
        gamma (1D array):  Daligault scattering rate (1/fs)
        dos (1D array): Fermi gas DOS
        occ (1D array): Fermi dirac occupation values
    """

    k_kF_list = (np.sqrt(2 * m_e * E / J_to_eV) / hbar_Js) / get_kF(n)

    gamma = (
        np.array(get_gamma_omega_p(q_kF_list, k_kF_list, n, theta, mu / J_to_eV))
        * get_omega_p(n)
        * 1e-15
    )
    # 1/fs

    return gamma


def get_avg_gamma(gamma, dos, occ, E_mu):
    return integrate.simpson(gamma * dos * occ, E_mu)


# * End of Gamma section
#!---------------------------------------------------------------


class DaligaultGamma:
    """
    class DaligaultGamma generates all necessary parameters and outputs for analysis
    """

    def __init__(
        self, E, Te, N, V, theta_cutoff=1, q_kF_list=np.linspace(1e-3, 10, 1000)
    ) -> None:
        """Function returns all parameters

        Args:
            E (array): Energy array in eV
            Te (float): electronic temperature in eV
            N (int): Number of electrons in cell
            V (float): Volume of cell in Angstrom cubed (A^3)
            n (float): carrier density of material (1/m^3)
            theta (float): degeneracy parameter
            theta_cutoff (float): Te (eV) cutoff in which we go from quantum to classical chemical potential
            q_kF_list (array): array of q/kF points used for v(q) and G(q/kF), defaults to np.linspace(1e-3, 10, 1000) 1/m
            model_mu (float): Chemical potential in eV obtained from either a FG or classical model depending on theta
            dos (array): Array of Fermi gas density of states
            mu (float): Chemical potential in eV obtained by integrating the DOS*occupation over energy and constraining by N
            occ (array): Fermi Dirac occupation values, where the chemical potential is set to 0 eV
            gamma (array): Daligualt method of estimating gamma(E)
            avg_gamma (float): gamma*occ*dos integrated over energy
            E_mu (array): Energy array minus mu in eV
        """
        self.E = E
        self.Te = Te
        self.N = N
        self.V = V
        self.n = N / (V * angstrom**3)
        self.theta = pp_form.quantum_theta(self.Te * units.eV, self.n).value
        self.theta_cutoff = theta_cutoff
        self.q_kF_list = q_kF_list
        self.model_mu = get_mu(self.n, self.theta, self.theta_cutoff) * J_to_eV
        fg_dos = FermiGasDOS(self.E, self.V)
        self.dos = fg_dos.dos
        self.mu = integrate_for_mu(self.Te, self.N, self.E, self.dos)[0]
        self.occ = logistic.sf(self.E, self.mu, self.Te)
        self.gamma = get_gamma(self.E, self.n, self.mu, self.theta, self.q_kF_list)
        self.avg_gamma = get_avg_gamma(self.gamma, self.dos, self.occ, self.E)
        self.E_mu = self.E - self.mu
