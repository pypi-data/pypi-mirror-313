import numpy as np
from scipy.stats import logistic
from scipy.interpolate import interp1d
from scipy import integrate
import plasmapy.formulary as pp_form
import astropy.units as units
from .constants import *
from .daligault_gamma import DaligaultGamma
from .daligault_gamma import get_mu
from .fermi_gas_dos import FermiGasDOS
from .fermi_gas_params import FGParams
import warnings

warnings.filterwarnings("ignore")


class DaligaultAvgGamma:
    """
    class DaligaultAvgGamma calculates the energy-averaged scattering rate using scattering rates predicted by Eq. 4 in the 2017 Daligault PRL paper
    """

    def __init__(
        self,
        Te,
        N,
        V,
        theta_cutoff=1,
        q_kF_list=np.linspace(1e-3, 10, 1000),
        E=np.linspace(1e-6, 50, 100),
        occ_threshold=1e-8,
    ) -> None:
        """Function returns below parameters

        Args:
            Te (float): electronic temperature in eV
            N (int): Number of electrons in cell
            V (float): Volume of cell in Angstrom cubed (A^3)
            n (float): carrier density of material (1/m^3)
            theta (float): degeneracy parameter
            theta_cutoff (float): Te (eV) cutoff in which we go from quantum to classical chemical potential
            mu (float): chemical potential
            q_kF_list (array): array of q/kF points used for v(q) and G(q/kF), defaults to np.linspace(1e-3, 10, 1000) 1/m
            E (array): Energy array in eV from -500 to 500 eV
            occ_threshold (float): threshold for highest energy to be considered "0" occupation
            E_gamma (2D array): Energy-mu (eV) and Daligault scattering rate (1/fs)
        """
        self.E = E
        self.Te = Te
        self.V = V
        self.N = N
        self.n = N / (V * angstrom**3)
        self.theta = pp_form.quantum_theta(self.Te * units.eV, self.n).value
        self.theta_cutoff = theta_cutoff
        # * get same mu value used in the scattering rate evaluation
        # TODO: clean this up a bit and unify in all scripts in the package
        self.mu = get_mu(self.n, self.theta, self.theta_cutoff) * J_to_eV  # eV
        self.q_kF_list = q_kF_list
        self.occ_threshold = occ_threshold

        daligault_data = DaligaultGamma(self.E, self.Te, self.N, self.V)
        self.E_gamma = daligault_data.get_gamma()

    # get FG dos and then interpolates for data matching
    # The chemical potential should always be 0 eV for the scattering rates that are going to be used with this dos
    def get_fg_dos(self):
        # need this so that there is no interpolation out of range issue when shifting by mu
        E_range = np.linspace(-500, 5000, 1000000)
        fg_dos = FermiGasDOS(E_range, self.V)
        interp_fg_dos = interp1d(
            E_range - self.mu,
            fg_dos.dos,
            fill_value=(0, np.nan),
            bounds_error=False,
        )
        # mu is set to 0 eV
        return interp_fg_dos(self.E_gamma[:, 0])

    # FD distribution
    def get_occ(self):
        occ_condition = True  # turns to false if occ at highest energy does not meat certain threshold
        #! chemical potential should always be set to zero!
        occ = logistic.sf(self.E_gamma[:, 0], 0, self.Te)
        if occ[-1] > self.occ_threshold:
            print(
                f"occupation at {self.E_gamma[:, 0][-1]} eV is {occ[-1]} for Te = {self.Te} eV"
            )
            occ_condition = False  # occ. not zero for highest energy
        return occ, occ_condition

    def daligault_gamma_occ_dos(self):
        E = self.E_gamma[:, 0]
        gamma = self.E_gamma[:, 1]
        occ, occ_condition = DaligaultAvgGamma.get_occ(self)
        dos = DaligaultAvgGamma.get_fg_dos(self)
        return E, gamma, occ, occ_condition, dos

    def avg_daligault_gamma(self):
        (E, gamma, occ, occ_condition, dos) = DaligaultAvgGamma.daligault_gamma_occ_dos(
            self
        )
        avg_gamma = integrate.simpson(gamma * occ * (1 - occ) * dos, E)
        return avg_gamma, occ_condition
