class VaspParam:
    """
    class VaspParam reads and produces all desired parameters from a VASP calcualtion
    """

    def __init__(self, file) -> None:
        """Function reads through VASP output self.outcar (self.outcar) and parses out key parameters

        Args:
            file (string): the path to the OUTCAR file
        Returns:
            file (string): the path to the OUTCAR file
            outcar (list): the OUTCAR file written to a list
            algo (string): GW calculation algorithm
            finite_temp (string): GW calculation type (T/F)
            full_freq (string): GW calculation type (T/F)
            Te (float): Electronic temperature in eV
            Ef (float): Fermi energy of calculation
            volume (float): Volume of cell in A^3
            nelect (float): Total number of electrons
            ispin (int): Spin of system
            N (int): Number of electrons accounting for degeneracy
            num_ion_type (array): Number of each ion species
            pomass (array): Mass of each ion species
            mass (float): Total mass of the cell
            rho (float): Density of the cell in g/cc
            nbands (int): Number of bands in calculation
            nbandsgw (int): Number of bands included in GW calculation
            nkpts (int): Number of irreducible kpoints in calculation
            nkdim (int): Total number of kpoints in calculation
            nomega (int): Number of frequency grid points in GW calculation
            cshift (float): Shift of the Hilbert transformation for GW calculation
        """

        self.file = file
        self.outcar = [line for line in open(self.file, "r")]
        self.algo = [line for line in self.outcar if "ALGO" in line][0].split()[-1]
        self.finite_temp = [line for line in self.outcar if "LFINITE_T" in line][
            -1
        ].split()[-5]
        self.full_freq = [line for line in self.outcar if "LSELFENERGY" in line][
            -1
        ].split()[-7]
        # use Te instead of sigma due to sigma being used for self-energy elsewhere
        self.Te = float(
            [line for line in self.outcar if "SIGMA" in line][0].split()[-1]
        )
        self.Ef = float(
            [line for line in self.outcar if "E-fermi" in line][0].split()[-1]
        )
        self.volume = float(
            [line for line in self.outcar if "volume" in line][0].split()[-1]
        )
        self.nelect = float(
            [line for line in self.outcar if "NELECT" in line][0].split()[2]
        )
        self.ispin = int(
            [line for line in self.outcar if "ISPIN" in line][0].split()[2]
        )
        self.N = int(self.ispin * self.nelect / 2)
        self.num_ion_type = [line for line in self.outcar if "ions per type" in line][
            0
        ].split()[4:]
        self.pomass = [line for line in self.outcar if "POMASS" in line][-1].split()[2:]
        self.mass = sum(
            [
                float(ion) * float(mass)
                for ion, mass in list(zip(self.num_ion_type, self.pomass))
            ]
        )  # Dalton
        self.rho = (self.mass * 1.6605e24) / (self.volume * 1e24)  # g/cc
        self.nbands = int(
            [line for line in self.outcar if "NBANDS" in line][0].split()[-1]
        )
        self.nbandsgw = int(
            [line for line in self.outcar if "NBANDSGW " in line][-1].split()[-10]
        )
        self.nkpts = int(
            [line for line in self.outcar if "NKPTS" in line][0].split()[3]
        )
        self.nkdim = int(
            [line for line in self.outcar if "NKDIM" in line][0].split()[9]
        )
        self.nomega = int(
            [line for line in self.outcar if "NOMEGA" in line][0].split()[-1]
        )
        self.cshift = float(
            [line for line in self.outcar if "CSHIFT" in line][-1].split()[-9]
        )
