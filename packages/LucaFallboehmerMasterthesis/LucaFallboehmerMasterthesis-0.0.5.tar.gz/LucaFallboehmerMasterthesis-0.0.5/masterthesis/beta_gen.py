"""Generate and beta spectra using the Gen_spec class. The theory functions are adapted from the TRModel Theo script deta_decay.py

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from multiprocessing import Pool, cpu_count

# from constants import *

# if USE_NUMBA_JIT:
#     from beta_decay_jit import *

#     print("using numbas jit compilation")
# else:
#     from beta_decay import *


from .constants import *
from .beta_decay import *


def process_slice(args):
    """Auxiliary function for the gen_and_rebin method of the Gen_Spec class."""
    key, index, reb_fact, ekin_long, spec_kwargs = args
    high_dim_slice = tuple(
        slice(i * f, (i + 1) * f)
        for i, f in zip(index, np.tile(reb_fact, reps=len(index)))
    )
    # Generate chunk of spectrum (equal to one bin in the final bin width)
    chunk = beta_spec(
        ekin_long[high_dim_slice[1]], ekin_long.max(), *spec_kwargs[key][index[0]]
    )
    # Integration
    return key, index, np.mean(chunk)


class Gen_Spec:
    """
    A class to generate and manipulate binned differential tritium beta decay spectra for neutrino and sterile neutrino experiments.

    Attributes
    ----------
    ekin : ndarray
        Single array of kinetic energy values for all spectra.
    m_neutrino : ndarray
        Array of neutrino mass values.
    m_sterile : ndarray
        Array of sterile neutrino mass values.
    sin2theta : ndarray
        Array of squared sine of the mixing angle values.
    smallterms : boolean ndarray
        Array of bools of wether to apply small correction terms.
    rng : np.random.Generator
        Random number generator initialized with a given seed.

    Methods
    -------
    gen_fast(scale=2e15, **kwargs)
        Generates the spectra for both reference and sterile cases, optionally adding noise and scaling the results.
    scale_spec_stats(spectra, scale)
        Scales the spectral statistics by a given factor.
    gen_and_rebin(num_bins_init, num_bins_fin, scale=2e15, **kwargs)
        Allows integration over a final bin width by rebinning from a very small initial bin width.
    """

    def __init__(self, ekin, m_neutrino, m_sterile, sin2theta, smallterms, seed=42):
        """
        Initializes the Gen_Spec class with provided parameters.

        Parameters
        ----------
        ekin : ndarray
            Single array of kinetic energy values for all spectra.
        m_neutrino : ndarray
            Array of neutrino mass values.
        m_sterile : ndarray
            Array of sterile neutrino mass values.
        sin2theta : ndarray
            Array of squared sine of the mixing angle values.
        smallterms : boolean ndarray
            Array of bools of wether to apply small correction terms.
        seed : int, optional
            Seed for the random number generator (default is 42).
        """
        self.ekin = ekin
        self.m_neutrino = m_neutrino
        self.m_sterile = m_sterile
        self.sin2theta = sin2theta
        self.smallterms = smallterms
        self.rng = np.random.default_rng(seed)

    def scale_spec_stats(self, spectra, scale):
        """
        Scales the spectral statistics by a given factor.

        Parameters
        ----------
        spectra : ndarray
            Array of spectral data to be scaled.
        scale : float
            Scaling factor.

        Returns
        -------
        ndarray
            Scaled spectral data.
        """
        # if self.scale is not None:
        #     return scale * spectra / np.sum(spectra, axis=1, keepdims=True)
        # else:
        #     return [scale * i[:] / i.sum() for i in spectra]
        return [scale * i[:] / np.sum(i) for i in spectra]

    def gen_fast(self, scale=2e15, **kwargs):
        """
        Generates the spectra for both reference and sterile cases, optionally adding noise and scaling the results.

        Parameters
        ----------
        scale : float, optional
            Scaling factor for the spectral statistics (default is 2e15).
        **kwargs : dict, optional
            Keyword arguments specifying the types of spectra to generate. Valid keys are:
            'reference', 'sterile', 'reference_noise', 'sterile_noise'.

        Returns
        -------
        spec_df : dict
            Dictionary containing the generated spectra and parameters.
        """
        self.scale = scale

        if scale is not None:
            spec_df = {
                k: np.zeros((self.m_sterile.shape[0], self.ekin.shape[0]))
                for k in kwargs.keys()
            }
        else:
            spec_df = {
                k: [np.zeros_like(self.ekin) for i in range(self.m_sterile.shape[0])]
                for k in kwargs.keys()
            }

        items_ref = [
            (self.ekin, self.ekin.max(), self.m_neutrino[i], 0, 0, self.smallterms[i])
            for i in range(self.m_sterile.shape[0])
        ]
        items_sterile = [
            (
                self.ekin,
                self.ekin.max(),
                self.m_neutrino[i],
                self.m_sterile[i],
                self.sin2theta[i],
                self.smallterms[i],
            )
            for i in range(self.m_sterile.shape[0])
        ]

        with Pool() as pool:
            for count, (result_ref, result_sterile) in enumerate(
                zip(
                    pool.starmap(beta_spec, items_ref),
                    pool.starmap(beta_spec, items_sterile),
                )
            ):
                for key in kwargs.keys():
                    if key == "reference":
                        spec_df[key][count] = result_ref
                    if key == "sterile":
                        spec_df[key][count] = result_sterile

        if scale is not None:
            for key in ["reference", "sterile"]:
                if key in spec_df:
                    spec_df[key] = self.scale_spec_stats(spec_df[key], scale)

        self._add_noise(spec_df, kwargs, scale)

        spec_df["m_sterile"] = self.m_sterile
        spec_df["sin2theta"] = self.sin2theta

        return pd.DataFrame(spec_df)
        # return spec_df

    def _add_noise(self, spec_df, kwargs, scale):
        """adds binwise poisson noise to the spectra and normalizes them afterards to a chosen statistic (scale)"""
        for key in ["reference_noise", "sterile_noise"]:
            if key in kwargs and kwargs[key]:
                base_key = key.split("_")[0]
                err = np.sqrt(np.abs(spec_df[base_key]))
                noise = self.rng.normal(loc=0.0, scale=err)
                spec_df[key] = spec_df[base_key] + noise
                if scale is not None:
                    spec_df[key] = self.scale_spec_stats(spec_df[key], scale)

    def gen_and_rebin(self, num_bins_init, num_bins_fin, scale=2e15, **kwargs):
        """
        Essentially allows integration over a certain final bin width of the beta spectrum.
        Generate beta spectra with fine binning (using chunks) and rebin to a more coarse binning
        """
        items_ref = [
            (self.m_neutrino[i], 0, 0, self.smallterms[i])
            for i in range(self.m_sterile.shape[0])
        ]
        items_sterile = [
            (
                self.m_neutrino[i],
                self.m_sterile[i],
                self.sin2theta[i],
                self.smallterms[i],
            )
            for i in range(self.m_sterile.shape[0])
        ]
        spectra_kwargs_dict = {
            k: items_ref if k.startswith("reference") else items_sterile
            for k in kwargs.keys()
        }

        assert (
            num_bins_init % num_bins_fin == 0
        ), f"Can't rebin as the number of initial bins ({num_bins_init}) is not divisible by the final number of bins {num_bins_fin}."

        ekin_long = np.linspace(self.ekin.min(), self.ekin.max(), num_bins_init)
        reb_fact = num_bins_init // num_bins_fin

        spec_df_rebinned = {
            k: np.zeros((self.m_sterile.shape[0], num_bins_fin)) for k in kwargs.keys()
        }

        args_list = [
            (key, index, reb_fact, ekin_long, spectra_kwargs_dict)
            for key in spec_df_rebinned.keys()
            for index in np.ndindex(spec_df_rebinned[key].shape)
        ]

        with Pool(processes=cpu_count()) as pool:
            results = pool.map(process_slice, args_list)

        for key, index, value in results:
            spec_df_rebinned[key][index] = value

        if scale is not None:
            for key in ["reference", "sterile"]:
                if key in spec_df_rebinned:
                    spec_df_rebinned[key] = self.scale_spec_stats(
                        spec_df_rebinned[key], scale
                    )

        self._add_noise(spec_df_rebinned, kwargs, scale)
        spec_df_rebinned["m_sterile"] = self.m_sterile
        spec_df_rebinned["sin2theta"] = self.sin2theta

        return pd.DataFrame(spec_df_rebinned)


#  ------------------------------------------------------------------------------------------------------------------------------------------------
# OLD, kept for convenience -----------------------------------------------------------------------------------------------------------------------
#  ------------------------------------------------------------------------------------------------------------------------------------------------


def gen_spectra_fast(
    ekin,
    m_neutrino,
    m_sterile,
    sin2theta,
    smallterms,
    noise=False,
    accurate_noise=False,
):  # makes kernel crash for larger N and custom noise -> TODO Inverstigate but not important now as using accurate noise is favored
    """
    Parallelized version of gen_spectra
    Generates different spectra:
    - a beta spectrum for each m_sterile and sin2theta (called sterile spectrum from now on)
    - one reference spectrum without m_sterile and sin2theta
    - for both of the above a scaled spectrum with bin values scaled s. th. sum(bin_values) = 2e15
    - optionally reference and sterile spectra with custom gaussian noise for training
    - optionally reference and sterile spectra with accurate (stddev = sqrt(bin_value)) gaussian noise for training

    Parameters
    ---------------------------------------------
    e_kin : 1darray
        Array of energies in eV.
    m_neutrino : 1darray
        float, optional
        Neutrino mass in eV. The default is 0.
    m_sterile : 1darray
        float, optional
        Sterile neutrino mass in eV. The default is 0.
    sin2theta : 1darray
        float, optional
        Sterile neutrino mixing matrix element. The default is 0.
    smallterms : 1darray
        bool, optional
        Considers the effect of small term corrections. For details, see reference.
        The default is True.
    noise : ndarray
        float, optional
        Use for custom noise, tensor with different noise for beta spectrum in individual bin
    accurate_noise: bool
        optional
        Creates poisson noise for each bin after scaling spectra, integral of returned spectra equals approx. 2e15

    Returns
    ---------------------------------------------
    spectra : dictionary
        Dictionary of beta spectra with different parameters

    """
    spec_dict = {
        "reference": [],
        "reference_noise": [],
        "sterile": [],
        "sterile_noise": [],
        "m_sterile": [],
        "sin2theta": [],
        "reference_scaled": [],
        "sterile_scaled": [],
    }
    items_ref = [
        (ekin, ekin.max(), m_neutrino[i], 0, 0, smallterms[i])
        for i in range(m_sterile.shape[0])
    ]
    items_sterile = [
        (ekin, ekin.max(), m_neutrino[i], m_sterile[i], sin2theta[i], smallterms[i])
        for i in range(m_sterile.shape[0])
    ]
    shapes_match = m_neutrino.shape == m_sterile.shape == sin2theta.shape
    if shapes_match == True:
        with Pool() as pool:
            for count, (result_ref, result_sterile) in enumerate(
                zip(
                    pool.starmap(beta_spec, items_ref),
                    pool.starmap(beta_spec, items_sterile),
                )
            ):
                spec_dict["reference"].append(result_ref)
                spec_dict["sterile"].append(result_sterile)
                spec_dict["m_sterile"].append(m_sterile[count])
                spec_dict["sin2theta"].append(sin2theta[count])
                spec_dict["reference_scaled"].append(
                    spec_dict["reference"][count][:]
                    * 2e15
                    / spec_dict["reference"][count].sum()
                )
                spec_dict["sterile_scaled"].append(
                    spec_dict["sterile"][count][:]
                    * 2e15
                    / spec_dict["sterile"][count].sum()
                )
            if accurate_noise:
                for count in range(
                    m_sterile.shape[0]
                ):  # parallelizing this doesnt save any time
                    error_ref = np.sqrt(spec_dict["reference_scaled"][count][:])
                    noise_ref = np.random.normal(loc=0.0, scale=error_ref)
                    error_sterile = np.sqrt(spec_dict["sterile_scaled"][count][:])
                    error_sterile[-1] *= -1
                    noise_sterile = np.random.normal(loc=0.0, scale=error_sterile)
                    spec_dict["reference_noise"].append(
                        spec_dict["reference_scaled"][count] + noise_ref
                    )
                    spec_dict["sterile_noise"].append(
                        spec_dict["sterile_scaled"][count] + noise_sterile
                    )
            else:
                if noise.all() != False:
                    for count in range(m_sterile.shape[0]):
                        spec_dict["reference_noise"].append(
                            spec_dict["reference"][count][:] + noise[0][count][:]
                        )
                        spec_dict["sterile_noise"].append(
                            spec_dict["sterile"][count][:] + noise[1][count][:]
                        )
    else:
        print("Input shapes dont match")

    return spec_dict


def gen_spectra(
    ekin,
    m_neutrino,
    m_sterile,
    sin2theta,
    smallterms,
    noise=False,
    accurate_noise=False,
):  # OLD, should not be used anymore, use gen_spectra_fast instead
    """
    OLD, use gen_spectra_fast instead
    Generates different spectra:
    - a beta spectrum for each m_sterile and sin2theta (called sterile spectrum from now on)
    - one reference spectrum without m_sterile and sin2theta
    - for both of the above a scaled spectrum with bin values scaled s. th. sum(bin_values) = 2e15
    - optionally reference and sterile spectra with custom gaussian noise for training
    - optionally reference and sterile spectra with accurate (stddev = sqrt(bin_value)) gaussian noise for training

    Parameters
    ---------------------------------------------
    e_kin : 1darray
        Array of energies in eV.
    m_neutrino : 1darray
        float, optional
        Neutrino mass in eV. The default is 0.
    m_sterile : 1darray
        float, optional
        Sterile neutrino mass in eV. The default is 0.
    sin2theta : 1darray
        float, optional
        Sterile neutrino mixing matrix element. The default is 0.
    smallterms : 1darray
        bool, optional
        Considers the effect of small term corrections. For details, see reference.
        The default is True.
    noise : ndarray
        float, optional
        Use for custom noise, tensor with different noise for beta spectrum in individual bin
    accurate_noise: bool
        optional
        Creates poisson noise for each bin after scaling spectra, integral of returned spectra equals approx. 2e15

    Returns
    ---------------------------------------------
    spectra : dictionary
        Dataframe / Dictionary of beta spectra with different parameters

    """

    shapes_match = m_neutrino.shape == m_sterile.shape == sin2theta.shape
    if shapes_match == True:
        spec_dict = {
            "reference": [],
            "reference_noise": [],
            "sterile": [],
            "sterile_noise": [],
            "m_sterile": [],
            "sin2theta": [],
            "reference_scaled": [],
            "sterile_scaled": [],
        }
        for count in range(m_sterile.shape[0]):
            spec_dict["sterile"].append(
                beta_spec(
                    ekin,
                    m_neutrino=m_neutrino[count],
                    m_sterile=m_sterile[count],
                    sin2theta=sin2theta[count],
                    smallterms=smallterms[count],
                )
            )
            spec_dict["reference"].append(
                beta_spec(
                    ekin,
                    m_neutrino=m_neutrino[count],
                    m_sterile=0,
                    sin2theta=0,
                    smallterms=smallterms[count],
                )
            )
            spec_dict["m_sterile"].append(m_sterile[count])
            spec_dict["sin2theta"].append(sin2theta[count])
            spec_dict["reference_scaled"].append(
                spec_dict["reference"][count][:]
                * 2e15
                / spec_dict["reference"][count].sum()
            )
            spec_dict["sterile_scaled"].append(
                spec_dict["sterile"][count][:]
                * 2e15
                / spec_dict["sterile"][count].sum()
            )
        if accurate_noise:
            for count in range(m_sterile.shape[0]):
                error_ref = np.sqrt(spec_dict["reference_scaled"][count][:])
                error_ref[
                    -1
                ] *= (
                    -1
                )  # this is done as the last bin always somehow has a value of -0.0
                noise_ref = np.random.normal(loc=0.0, scale=error_ref)
                error_sterile = np.sqrt(spec_dict["sterile_scaled"][count][:])
                error_sterile[
                    -1
                ] *= (
                    -1
                )  # this is done as the last bin always somehow has a value of -0.0
                noise_sterile = np.random.normal(loc=0.0, scale=error_sterile)
                spec_dict["reference_noise"].append(
                    spec_dict["reference_scaled"][count] + noise_ref
                )
                spec_dict["sterile_noise"].append(
                    spec_dict["sterile_scaled"][count] + noise_sterile
                )
        else:
            if noise.all() != False:
                for count in range(m_sterile.shape[0]):
                    spec_dict["reference_noise"].append(
                        spec_dict["reference"][count][:] + noise[0][count][:]
                    )
                    spec_dict["sterile_noise"].append(
                        spec_dict["sterile"][count][:] + noise[1][count][:]
                    )
    else:
        print("Input shapes dont match")

    return spec_dict


def plot_sterile_spectra(ekin, spec, rows, cols, size=(15, 15), noise=False):
    fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize=size)
    num_spectra = spec.shape[0]
    i = 0
    if noise == False:
        for row in ax:
            for col in row:
                col.plot(
                    ekin,
                    spec["sterile"][i],
                    label=str(spec["m_sterile"])
                    + " eV & sin^2(theta)"
                    + str(spec["sin2theta"]),
                )
                col.set_title(
                    "m = "
                    + str(int(spec["m_sterile"][i]))
                    + f" eV & $sin^2(t) = $ "
                    + str(float(spec["sin2theta"][i]))
                )
                i += int(num_spectra / (rows * cols))
    if noise == True:
        for row in ax:
            for col in row:
                col.plot(
                    ekin,
                    spec["sterile_noise"][i],
                    label=str(spec["m_sterile"])
                    + " eV & sin^2(theta)"
                    + str(spec["sin2theta"]),
                )
                col.set_title(
                    "m = "
                    + str(int(spec["m_sterile"][i]))
                    + f" eV & $sin^2(t) = $ "
                    + str(float(spec["sin2theta"][i]))
                )
                i += int(num_spectra / (rows * cols))

    plt.show()


def plot_spectra_diff(ekin, spec, rows, cols, size=(15, 15), noise=False):
    fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize=size)
    num_spectra = spec.shape[0]
    i = 0
    if noise == False:
        for row in ax:
            for col in row:
                col.plot(
                    ekin,
                    spec["sterile"][i] - spec["reference"][i],
                    label=str(spec["m_sterile"])
                    + " eV & sin^2(theta)"
                    + str(spec["sin2theta"]),
                )
                col.set_title(
                    "m = "
                    + str(int(spec["m_sterile"][i]))
                    + f" eV & $sin^2(t) = $ "
                    + str(float(spec["sin2theta"][i]))
                )
                i += int(num_spectra / (rows * cols))

    if noise == True:
        for row in ax:
            for col in row:
                col.plot(
                    ekin,
                    spec["sterile_noise"][i] - spec["reference_noise"][i],
                    label=str(spec["m_sterile"])
                    + " eV & sin^2(theta)"
                    + str(spec["sin2theta"]),
                )
                col.set_title(
                    "m = "
                    + str(int(spec["m_sterile"][i]))
                    + f" eV & $sin^2(t) = $ "
                    + str(float(spec["sin2theta"][i]))
                )
                i += int(num_spectra / (rows * cols))

    plt.show()


def plot_spectra_ratio(ekin, spec, rows, cols, size=(15, 15), noise=False):
    fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize=size)
    num_spectra = spec.shape[0]
    i = 0
    if noise == False:
        for row in ax:
            for col in row:
                col.plot(
                    ekin,
                    spec["sterile"][i] / spec["reference"][i],
                    label=str(spec["m_sterile"])
                    + " eV & sin^2(theta)"
                    + str(spec["sin2theta"]),
                )
                col.set_title(
                    "m = "
                    + str(int(spec["m_sterile"][i]))
                    + f" eV & $sin^2(t) = $ "
                    + str(float(spec["sin2theta"][i]))
                )
                i += int(num_spectra / (rows * cols))

    if noise == True:
        for row in ax:
            for col in row:
                col.plot(
                    ekin,
                    spec["sterile_noise"][i] / spec["reference_noise"][i],
                    label=str(spec["m_sterile"])
                    + " eV & sin^2(theta)"
                    + str(spec["sin2theta"]),
                )
                col.set_title(
                    "m = "
                    + str(int(spec["m_sterile"][i]))
                    + f" eV & $sin^2(t) = $ "
                    + str(float(spec["sin2theta"][i]))
                )
                i += int(num_spectra / (rows * cols))

    plt.show()
