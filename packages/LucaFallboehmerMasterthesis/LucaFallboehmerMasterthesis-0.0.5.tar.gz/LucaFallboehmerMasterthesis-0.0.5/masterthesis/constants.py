import numpy as np

# --------------------------------------------------------------------
# Numba jit compilation
USE_NUMBA_JIT = False

# --------------------------------------------------------------------
# beta decay constants
# D.H. Wilkinson, Small terms in the beta-decay spectrum of tritium
# Nucl. Phys. A 526 (1991) 131.

M_ELECTRON = 510998.95  # electron mass, eV
ALPHA = 7.2973525698e-3  # fine-structure constant
ENDPOINT = 18575  # endpoint energy, eV
A_CONST = 1.002037  # constant, see reference
B_CONST = 0.001427  # constant, see reference


# --------------------------------------------------------------------
# small term corrections

Z_DAUGHTER = 2  # daughter nucleus charge
LAMBDA_T = 1.265  # ratio of axial vector to vector coupling
MU_DIFF = 5.106588  # difference of magnetic moments between tritium and helium
R_HE = 2.8840e-3  # helium nuclear radius, unitless (in units of electronmass)

M_T2 = 3 * 1837 * M_ELECTRON
M_HE = M_T2


# --------------------------------------------------------------------
# Tritium half life and activity
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4877155/
TRITIUM_HALF_LIFE = 4500.0 * 24.0 * 60.0 * 60.0  # 4500 days in seconds
TRITIUM_DECAY_CONST = (
    np.log(2) / TRITIUM_HALF_LIFE
)  # counts per second per tritium atom


# --------------------------------------------------------------------
# detector model constants
EPSILON = 3.6  # electron-hole pair energy (eV)
FANOF = 0.115  # fano factor silicon


# --------------------------------------------------------------------
# Detector pixel geometry
PX_SIDELENGTH = 1.649  # mm (side length of hexagonal pixel)
PX_RADIUS = 1.500  # mm (radius of circle with approximately same area)
PX_AREA_MM2 = 3 / 2 * np.sqrt(3) * PX_SIDELENGTH**2  # mm^2 (hexagonal pixel area)
PX_AREA_CM2 = PX_AREA_MM2 * 0.01  # cm^2 (hexagonal pixel area)
PX_PER_MODULE = 166
PX_PHASE_1 = PX_PER_MODULE * 9
PX_PHASE_2 = PX_PER_MODULE * 21
