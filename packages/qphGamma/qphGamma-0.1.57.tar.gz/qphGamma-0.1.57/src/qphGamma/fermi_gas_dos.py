import numpy as np
import warnings
from .constants import *

warnings.filterwarnings("ignore")


class FermiGasDOS:
    """
    class FermiGasDOS calculates and returns the DOS predicted by the Fermi gas model
    """

    def __init__(self, E, V) -> None:
        """Function returns all E and DOS

        Args:
            E (array): Energy array in eV
            V (float): Volume of cell in Angstrom cubed
            dos (array): Density of states predicted by FG and all nan is turned into 0

        """
        self.E = E
        self.V = V
        self.dos = np.nan_to_num(
            np.array(
                (
                    ((self.V * 1e-30) / (2 * np.pi**2))
                    * (2 * m_e / (hbar_Js**2)) ** (3 / 2)
                )
                / J_to_eV ** (3 / 2)
                * np.sqrt(self.E)
            )
        )
