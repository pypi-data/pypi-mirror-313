import numpy as np
from scipy.interpolate import interp1d
from scipy import integrate
from scipy.stats import logistic
from .vasp_param import VaspParam
from .vasp_dos import VaspDOS
from .fermi_gas_dos import FermiGasDOS
from .fermi_gas_params import FGParams
from .constants import *
import warnings

warnings.filterwarnings("ignore")


def get_finite_Te_self_energy(outcar, algo, nkpts, Ef, core_E):
    """Function gets the energy and e-e scattering rates from the GW calculation
    Returns:
        E_gamma_occ (2D array - nkpts*nbands x 3): GW data of KS energies - Ef, scattering rate, and occupation values (0 to 1) sorted in ascending order of KS energies

    """

    ncol = 11
    head_string = "QP shifts evaluated in"
    tail_string = "Energies using frozen"
    header_num = [
        line_num for line_num, line in enumerate(outcar) if head_string in line
    ]
    tail_num = [line_num for line_num, line in enumerate(outcar) if tail_string in line]
    # For non-single shot calculations
    if algo.lower() == "gwr" or algo.lower() == "scgwr":
        tail_string_gwr = "ROTSIGMA"
        tail_num_gw = [
            line_num for line_num, line in enumerate(outcar) if tail_string_gwr in line
        ]
        tail_num = [tail_num[0]] + tail_num_gw

    def get_clean_data(data):
        return (
            np.array(
                [
                    [
                        x.split()
                        for x in [x.strip() for x in data if len(x.split()) == ncol]
                    ]
                ]
            )
            .flatten()
            .astype(float)
        )

    finite_data = [
        get_clean_data(outcar[head:tail])
        for head, tail in list(zip(header_num, tail_num))
    ]

    nbands = int(len(finite_data[0]) / (nkpts * ncol))

    KS_energies = np.array(
        [
            x[1::ncol].reshape(nkpts, nbands, int(len(x) / nkpts / nbands / ncol))
            for x in finite_data
        ]
    ).flatten()
    occ = (
        np.array(
            [
                x[7::ncol].reshape(nkpts, nbands, int(len(x) / nkpts / nbands / ncol))
                for x in finite_data
            ]
        ).flatten()
        / 2
    )
    gamma = (
        -2
        / hbar_eVfs
        * np.array(
            [
                x[8::ncol].reshape(nkpts, nbands, int(len(x) / nkpts / nbands / ncol))
                for x in finite_data
            ]
        ).flatten()
    )
    # sort in order of KS-energies
    E_gamma_occ = np.array(
        sorted(np.array([KS_energies - Ef, gamma, occ]).T, key=lambda x: x[0])
    )

    # get rid of any core states
    E_gamma_occ = np.array([x for x in E_gamma_occ if x[0] >= core_E])

    return E_gamma_occ[:, 0], E_gamma_occ[:, 1], E_gamma_occ[:, 2]


#!---------------------------------------------------------------
# * Start DOS and <gamma> section


def check_core_E_contribution(Te, core_E):
    core_E_occ = logistic.sf(core_E, 0, Te)
    if core_E_occ < 0.9999:
        print(
            f"\nFor Te = {Te:.2f} eV, states below the core_E of {core_E} contribute since the occupation of {core_E_occ} is less than 0.9999!\n"
        )


# Function gets the DOS predicted by VASP then interpolates for data matching
# The chemical potential should always be 0 eV for the scattering rates that are going to be used with this dos
def get_vasp_dos(Te, N, E, dos_file):
    # gets tet. method DOS
    if dos_file != None:
        data = VaspDOS(dos_file, Te, N)
        # mu is set to 0 eV
        interp_vasp_dos = interp1d(data.E - data.mu, data.dos)
        return interp_vasp_dos(E)
    else:
        print("\n\nNo VASP DOS .h5 file included in GWAvgGamma! Goodbye!\n\n")
        return [0] * len(E)


def avg_gamma_vasp_dos(Te, N, E, gamma, occ, dos_file, core_E):
    dos = get_vasp_dos(Te, N, E, dos_file)
    avg_gamma = integrate.simpson(gamma * occ * dos, E)
    check_core_E_contribution(Te, core_E)
    return avg_gamma


# get FG dos and then interpolates for data matching
# The chemical potential should always be 0 eV for the scattering rates that are going to be used with this dos
def get_fg_dos(Te, N, V, E):
    # need this so that there is no interpolation out of range issue when shifting by mu
    E_range = np.linspace(-500, 5000, 1000000)
    fg_params = FGParams(Te, N, V)
    fg_dos = FermiGasDOS(E_range, V)
    interp_fg_dos = interp1d(E_range - fg_params.mu, fg_dos.dos)
    # mu is set to 0 eV
    return interp_fg_dos(E)


def avg_gamma_fg_dos(Te, N, V, E, gamma, occ, core_E):
    dos = get_fg_dos(Te, N, V, E)
    avg_gamma = integrate.simpson(gamma * occ * dos, E)
    check_core_E_contribution(Te, core_E)
    return avg_gamma


# * End DOS and <gamma> section
#!---------------------------------------------------------------


class GWGamma:
    """
    class GWGamma generates all necessary parameters and outputs for analysis
    """

    def __init__(self, file, core_E, dos_file=None) -> None:
        """Function returns all parameters

        Args:
            file (string): the path to the OUTCAR file
            outcar (list): the OUTCAR file written to a list
            nkpts (int): the number of symmetry reduced KPOINTS
            algo (string): GW calculation algorithm
            Ef (float): Fermi energy of calculation, treated as the chemical potential
            core_E (float): cutoff (below) energy in eV that gets rid of core states - needed for integration
        """
        self.file = file
        self.outcar = [line for line in open(self.file, "r")]
        self.nkpts = int(
            [line for line in self.outcar if "NKPTS" in line][0].split()[3]
        )
        self.algo = [line for line in self.outcar if "ALGO" in line][0].split()[-1]
        self.Ef = float(
            [line for line in self.outcar if "E-fermi" in line][0].split()[-1]
        )
        self.core_E = core_E  # eV
        params = VaspParam(file)
        self.Te = params.Te  # eV
        self.N = params.N
        self.V = params.volume
        E_mu, gamma, occ = get_finite_Te_self_energy(
            self.outcar, self.algo, self.nkpts, self.Ef, self.core_E
        )
        self.E_mu = E_mu
        self.occ = occ
        self.gamma = gamma * (1 - occ)
        self.qh_gamma = gamma * occ
        self.total_gamma = gamma
        self.avg_vasp_gamma = avg_gamma_vasp_dos(
            params.Te, params.N, E_mu, gamma * (1 - occ), occ, dos_file, core_E
        )
        self.qh_avg_vasp_gamma = avg_gamma_vasp_dos(
            params.Te, params.N, E_mu, gamma * occ, (1 - occ), dos_file, core_E
        )
        self.avg_fg_gamma = avg_gamma_fg_dos(
            params.Te,
            params.N,
            params.volume,
            E_mu,
            gamma * (1 - occ),
            occ,
            core_E,
        )
        self.qh_avg_fg_gamma = avg_gamma_fg_dos(
            params.Te,
            params.N,
            params.volume,
            E_mu,
            gamma * occ,
            (1 - occ),
            core_E,
        )
