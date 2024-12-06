import numpy as np
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


class GWGamma:
    """
    class GWGamma generates all necessary parameters and outputs for analysis
    """

    def __init__(self, file, core_E) -> None:
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
        E_mu, gamma, occ = get_finite_Te_self_energy(
            self.outcar, self.algo, self.nkpts, self.Ef, self.core_E
        )
        self.E_mu = E_mu
        self.gamma = gamma
        self.occ = occ
