"""
Old code probably from Cornelius, summarized by Tim.
This module contains beta decay related functions. See also reference:
D.H. Wilkinson, Small terms in the beta-decay spectrum of tritium, Nucl. Phys. A 526 (1991) 131.

Functions
---------
_step
    Step function used in beta_spec.
_condition
    Condition function used in beta_spec.
beta_spec
    Calculates a differential beta spectrum.

fermi
    Fermi function (unscreened Coulomb field).
screening
    Screening of the beta electron.
recoil
    Effect of beta electron moving into a recoiled electric field.
weak_rec
    Nuclear recoil, weak magnetism, V-A.
exchange
    Exchange of an orbital electron with the beta electron.
weak_int
    Effect of finite nuclear size on the solution of the Dirac equation for the electron.
finite_charge
    Convolution of lepton and nucleonic wavefunction through nuclear volume.
radiative
    Radiative correction. 

"""

import numpy as np
from scipy.special import gamma

# from constants import *

from .constants import *


########################################################### general beta decay


def _step(idx):
    """Step function."""
    return 0.5 * (np.sign(idx) + 1)


def _condition(e_kin, endp, m_neutrino=0):
    """Condition function."""
    return ((endp - e_kin) ** 2 - m_neutrino**2) * _step(
        (endp - e_kin) ** 2 - m_neutrino**2
    )


def beta_spec(
    e_kin, endp=ENDPOINT, m_neutrino=0, m_sterile=0, sin2theta=0, smallterms=True
):
    """
    Calculates a differential beta spectrum.

    Parameters
    ----------
    e_kin : 1darray
        Array of energies in eV.
    endp : float, optional
        Spectral endpoint in eV.
    m_neutrino : float, optional
        Neutrino mass in eV. The default is 0.
    m_sterile : float, optional
        Sterile neutrino mass in eV. The default is 0.
    sin2theta : float, optional
        Sterile neutrino mixing matrix element. The default is 0.
    smallterms : bool, optional
        Considers the effect of small term corrections. For details, see reference.
        The default is True.

    Returns
    -------
    spec : 1darray
        Differential beta spectrum.

    """
    cond = e_kin > 0
    e_tot = e_kin[cond] + M_ELECTRON
    momentum = np.sqrt(e_tot**2 - M_ELECTRON**2)
    spec = np.empty(e_kin.shape)

    acti = np.sqrt(
        _step(endp - e_kin[cond] - m_neutrino)
        * (_condition(endp, e_kin[cond], m_neutrino))
    )
    ster = np.sqrt(
        _step(endp - e_kin[cond] - m_sterile)
        * (_condition(endp, e_kin[cond], m_sterile))
    )

    if smallterms:
        corr = (
            screening(e_kin)
            * recoil(e_kin, endp)
            * weak_rec(e_kin)
            * exchange(e_kin)
            * weak_int(e_kin, endp)
            * finite_charge(e_kin)
            * radiative(e_kin, endp)
        )
    else:
        corr = np.ones_like(e_kin)

    spec[cond] = (
        corr[cond]
        * fermi(e_kin[cond])
        * momentum
        * e_tot
        * (endp - e_kin[cond])
        * ((1 - sin2theta) * acti + sin2theta * ster)
    )

    spec[np.invert(cond)] = (
        4
        * np.pi
        * ALPHA
        * A_CONST
        * endp
        * M_ELECTRON**2
        * (
            (1 - sin2theta) * np.sqrt(endp**2 - m_neutrino**2)
            + sin2theta * np.sqrt(endp**2 - m_sterile**2)
        )
    )

    return spec


########################################################### small term corrections
####################################################### For details, see reference


def fermi(e_kin):
    """Fermi function (unscreened Coulomb field)."""
    e_tot = e_kin + M_ELECTRON
    beta = np.sqrt(1 - (M_ELECTRON / e_tot) ** 2)
    yps = 4 * np.pi * ALPHA / beta
    return yps * (A_CONST - B_CONST * beta) / (1 - np.exp(-yps))


def screening(e_kin):
    """Screening of the beta electron."""
    e_tot = e_kin + M_ELECTRON
    W = e_tot / M_ELECTRON
    momentum = np.sqrt(e_tot**2 - M_ELECTRON**2)
    Wbar = W - 1.45 * ALPHA**2
    pbar = np.sqrt(Wbar**2 * M_ELECTRON**2 - M_ELECTRON**2)
    Gamma = np.sqrt(1 - (Z_DAUGHTER * ALPHA) ** 2)
    y = ALPHA * W * M_ELECTRON * Z_DAUGHTER / momentum
    ycomplex = 0 + 1j * y
    ybar = ALPHA * Z_DAUGHTER * Wbar * M_ELECTRON / pbar
    ybarcomplex = 0 + 1j * ybar
    screen = (
        (Wbar / W)
        * (pbar / momentum) ** (-1 + 2 * Gamma)
        * np.exp(np.pi * (ybar - y))
        * (np.absolute(gamma(Gamma + ybarcomplex))) ** 2
        / (np.absolute(gamma(Gamma + ycomplex))) ** 2
    )
    return screen


def recoil(e_kin, endpoint):
    """Effect of beta electron moving into a recoiled electric field."""
    e_tot = e_kin + M_ELECTRON
    W = e_tot / M_ELECTRON
    W_0 = endpoint / M_ELECTRON
    momentum = np.sqrt(e_tot**2 - M_ELECTRON**2)
    B = (1 - LAMBDA_T**2) / (1 + 3 * LAMBDA_T**2)
    Q = 1 - np.pi * ALPHA * Z_DAUGHTER * M_ELECTRON / (
        M_HE * (momentum / M_ELECTRON)
    ) * (1 + B * (W_0 - W) / (3 * W))
    return Q


def weak_rec(e_kin):
    """Nuclear recoil, weak magnetism, V-A."""
    W = (e_kin + M_ELECTRON) / M_ELECTRON
    a = 2 * M_ELECTRON * (5 * LAMBDA_T**2 + 2 * LAMBDA_T * MU_DIFF + 1) / M_HE
    b = 2 * M_ELECTRON * LAMBDA_T * (LAMBDA_T + MU_DIFF) / M_HE
    c = 1 + 3 * LAMBDA_T**2 - b * W
    R = 1 + (a * W - b / W) / c
    return R


def exchange(e_kin):
    """Exchange of an orbital electron with the beta electron."""
    e_tot = e_kin + M_ELECTRON
    momentum = np.sqrt(e_tot**2 - M_ELECTRON**2)
    eta = -2 * ALPHA * M_ELECTRON / momentum
    Alpha = eta**4 * np.exp(2 * eta * np.arctan(-2 / eta)) / (1 + 0.25 * eta**2) ** 2
    exch = 1 + 2.462 * Alpha**2 + 0.905 * Alpha
    return exch


def weak_int(e_kin, endpoint):
    """Effect of finite nuclear size on the solution of the Dirac equation for the electron."""
    W = (e_kin + M_ELECTRON) / M_ELECTRON
    W_0 = endpoint / M_ELECTRON
    C_0 = (
        -233 * (ALPHA * Z_DAUGHTER) ** 2 / 630
        - (W_0 * R_HE) ** 2 / 5
        + 2 * (W_0 * R_HE * ALPHA * Z_DAUGHTER) / 35
    )
    C_1 = -21 * (R_HE * ALPHA * Z_DAUGHTER) / 35 + 4 * (W_0 * R_HE**2) / 9
    C_2 = -4 * R_HE**2 / 9
    deltaC = C_0 + C_1 * W + C_2 * W**2
    return deltaC + 1


def finite_charge(e_kin):
    """Convolution of lepton and nucleonic wavefunction through nuclear volume."""
    W = (e_kin + M_ELECTRON) / M_ELECTRON
    Gamma = np.sqrt(1 - (ALPHA * Z_DAUGHTER) ** 2)
    L = (
        1
        + (13 / 60) * (ALPHA * Z_DAUGHTER) ** 2
        - W * R_HE * ALPHA * Z_DAUGHTER * ((41 - 26 * Gamma) / (15 * (2 * Gamma - 1)))
        - ALPHA
        * Z_DAUGHTER
        * R_HE
        * Gamma
        * ((17 - 2 * Gamma) / (30 * W * (2 * Gamma - 1)))
    )
    return L


def radiative(e_kin, endpoint):
    """Radiative correction."""
    W = endpoint / M_ELECTRON + 1
    W_0 = e_kin / M_ELECTRON + 1
    beta = np.sqrt(W_0**2 - 1) / W_0
    tbeta = (1 / (2 * beta)) * np.log((1 + beta) / (1 - beta)) - 1
    diffW = W - W_0
    diffW[np.where(diffW < 0)[0]] = 0
    G = diffW ** (2 * ALPHA * tbeta / np.pi) * (
        1
        + (2 * ALPHA / np.pi)
        * (
            tbeta * (np.log(2) - 1.5 + (W - W_0) / W_0)
            + 0.25
            * (tbeta + 1)
            * (2 * (1 + beta**2) + 2 * np.log(1 - beta) + (W - W_0) ** 2 / (6 * W_0**2))
            - 2
            + 0.5 * beta
            - (17 / 36) * beta**2
            + (5 / 6) * beta**3
        )
    )
    return G
