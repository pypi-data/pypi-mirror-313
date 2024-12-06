import numpy as np
import warnings
from py4vasp import Calculation
from scipy.stats import logistic
from scipy import integrate

warnings.filterwarnings("ignore")


def func_format_dos(file, core_E):
    E_dos_array = np.array(
        [
            Calculation.from_file(f"{file}").dos.to_dict()["energies"]
            + Calculation.from_file(f"{file}").dos.to_dict()["fermi_energy"],
            Calculation.from_file(f"{file}").dos.to_dict()["total"],
        ]
    ).T
    E_dos_array = np.array([x for x in E_dos_array if x[0] >= core_E]).T
    return E_dos_array[0], E_dos_array[1]


# binary search function
def func_binary_search(Te, N, E, dos, bs_E):
    bs_N = [integrate.simpson(logistic.sf(E, Ef, Te) * dos, E) for Ef in bs_E]
    if np.round(bs_N[1], 6) == N:
        return bs_E[1], bs_N[1]
    elif bs_N[1] > N:
        return func_binary_search(Te, N, E, dos, [bs_E[0], np.mean(bs_E[:2]), bs_E[1]])
    elif bs_N[1] < N:
        return func_binary_search(Te, N, E, dos, [bs_E[1], np.mean(bs_E[1:]), bs_E[2]])


# integrated DOS*occ to find the chemical potential for given Te
def func_integrate_for_mu(Te, N, E, dos):
    Ef, Ni = func_binary_search(
        Te, N, E, dos, [np.min(E), np.mean([np.min(E), np.max(E)]), np.max(E)]
    )
    return Ef, Ni


class VaspDOS:
    """
    class VaspDOS gets the energy and dos from a typical vasp DOS calc and also finds the chemical potential based on carrier conservation by integrating the occupations and dos over energy
    """

    def __init__(self, file, Te, N, core_E=-50) -> None:
        """Function returns all E and DOS

        Args:
            file (string): path+file to dos h5 file for py4vasp to post-processes
            Te (float): electronic temperature in eV
            E (array): Energy of VASP DOS from VASP
            N (int): Number of electrons in the calculation
            core_E (float): The energy which below is assumed to be only core contributions and excluded from DOS
            dos (array): Density of states calculated by VASP
            mu (float): The chemical potential found by integrating occupations and dos over energy, while constraining number of carriers
            Ni (float): The number of carriers found from finding the chemical potential, should be VERY close to N

        """
        self.file = file
        self.Te = Te
        self.N = N
        self.core_E = core_E
        self.E, self.dos = func_format_dos(self.file, self.core_E)
        self.mu, self.Ni = func_integrate_for_mu(self.Te, self.N, self.E, self.dos)
