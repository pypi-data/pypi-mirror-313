import numpy as np
from scipy.interpolate import interp1d
from scipy import integrate
from scipy.stats import logistic
from .gw_gamma import GWGamma
from .vasp_param import VaspParam
from .vasp_dos import VaspDOS
from .fermi_gas_dos import FermiGasDOS
from .fermi_gas_params import FGParams
import warnings

warnings.filterwarnings("ignore")

# TODO: add in warning when temperatures lead to core energy contributions!


class GWAvgGamma:
    """
    class GWAvgGamma calculates the energy-averaged scattering rate
    """

    def __init__(self, file, core_E, dos_file=None) -> None:
        """Function returns below parameters

        Args:
            file (string): directory and name of VASP OUTCAR file
            dos_file (string, optional): directory and name of VASP DOS .h5 file
            core_E (float): cutoff (below) energy in eV that gets rid of core states - needed for integration
            E_gamma_occ (2D array - nkpts*nbands x 3): GW data of KS energies - Ef, scattering rate, and occupation values (0 to 1) sorted in ascending order of KS energies
            Te (float): electronic temperature in eV
            V (float): Volume of cell in A^3
            N (int): Number of electrons accounting for degeneracy

        """
        self.file = file
        self.dos_file = dos_file
        self.core_E = core_E  # eV
        params = VaspParam(file)
        gw_data = GWGamma(file, self.core_E)
        self.E_gamma_occ = gw_data.get_finite_Te_self_energy()
        self.Te = params.Te  # eV
        self.N = params.N
        self.V = params.volume

    # Function checks to ensure that the occupation of the core energy does not contribute to thermal excitations
    def check_core_E_contribution(self):
        core_E_occ = logistic.sf(self.core_E, 0, self.Te)
        if core_E_occ < 0.9999:
            print(
                f"States below the core_E of {self.core_E} contribute since the occupation of {core_E_occ} is less than 0.9999!"
            )

    # Function gets the DOS predicted by VASP then interpolates for data matching
    # The chemical potential should always be 0 eV for the scattering rates that are going to be used with this dos
    def get_vasp_dos(self):
        # gets tet. method DOS
        if self.dos_file != None:
            data = VaspDOS(self.dos_file, self.Te, self.N)
            # mu is set to 0 eV
            interp_vasp_dos = interp1d(data.E - data.mu, data.dos)
            return interp_vasp_dos(self.E_gamma_occ[:, 0])
        else:
            print("\n\nNo VASP DOS .h5 file included in GWAvgGamma! Goodbye!\n\n")
            exit()

    def gw_gamma_occ_vasp_dos(self):
        E = self.E_gamma_occ[:, 0]
        gamma = self.E_gamma_occ[:, 1]
        occ = self.E_gamma_occ[:, 2]
        dos = GWAvgGamma.get_vasp_dos(self)
        return E, gamma, occ, dos

    def avg_gw_gamma_vasp_dos(self):
        E, gamma, occ, dos = GWAvgGamma.gw_gamma_occ_vasp_dos(self)
        avg_gamma = integrate.simpson(gamma * occ * (1 - occ) * dos, E)
        GWAvgGamma.check_core_E_contribution(self)
        return avg_gamma

    # get FG dos and then interpolates for data matching
    # The chemical potential should always be 0 eV for the scattering rates that are going to be used with this dos
    def get_fg_dos(self):
        # need this so that there is no interpolation out of range issue when shifting by mu
        E_range = np.linspace(-500, 5000, 1000000)
        fg_params = FGParams(self.Te, self.N, self.V)
        fg_dos = FermiGasDOS(E_range, self.V)
        interp_fg_dos = interp1d(E_range - fg_params.mu, fg_dos.dos)
        # mu is set to 0 eV
        return interp_fg_dos(self.E_gamma_occ[:, 0])

    def gw_gamma_occ_fg_dos(self):
        E = self.E_gamma_occ[:, 0]
        gamma = self.E_gamma_occ[:, 1]
        occ = self.E_gamma_occ[:, 2]
        dos = GWAvgGamma.get_fg_dos(self)
        return E, gamma, occ, dos

    def avg_gw_gamma_fg_dos(self):
        E, gamma, occ, dos = GWAvgGamma.gw_gamma_occ_fg_dos(self)
        avg_gamma = integrate.simpson(gamma * occ * (1 - occ) * dos, E)
        GWAvgGamma.check_core_E_contribution(self)
        return avg_gamma
