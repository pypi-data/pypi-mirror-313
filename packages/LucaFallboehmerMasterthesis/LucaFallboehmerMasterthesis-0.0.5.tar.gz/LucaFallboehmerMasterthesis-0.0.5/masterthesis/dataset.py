import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
from multiprocessing import Pool, cpu_count
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import interp1d


# IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT!
# Rework / rethink how noise is added to spectra with response matrices: Add RM to unfluctuated spectrum and then draw random noise!!!!!
# IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT! IMPORTANT!

# =============================================================================================
# Modifying Datasets =============================================================================================
# =============================================================================================


# ================================================================================    Gaussian Perturbations


def multiple_gaussian_perturbation(x, amplitudes, means, stddevs):
    perturbation = np.zeros_like(x)
    for amplitude, mean, stddev in zip(amplitudes, means, stddevs):
        perturbation += amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev**2))

    return perturbation


def scale_perturbation(perturbation, scale_range=(1, 2)):
    perturbation_min = np.min(perturbation)
    perturbation_max = np.max(perturbation)

    normalized_perturbation = (perturbation - perturbation_min) / (
        perturbation_max - perturbation_min
    )

    min_target, max_target = scale_range
    scaled_perturbation = min_target + normalized_perturbation * (
        max_target - min_target
    )

    return (
        scaled_perturbation,
        perturbation_min,
        perturbation_max,
        min_target,
        max_target,
    )


def check_no_large_difference(peaks, troughs, perturbation, threshold=0.03):
    def ratio_diff(a, b):
        return np.abs(1 - a / b)

    extrema = np.sort(np.concatenate((peaks, troughs)))

    for i in range(1, len(extrema)):
        if (
            ratio_diff(perturbation[extrema[i - 1]], perturbation[extrema[i]])
            > threshold
        ):
            return False

    return True


def check_strict_monotonicity(perturbation):
    is_increasing = np.all(np.diff(perturbation) > 0)
    is_decreasing = np.all(np.diff(perturbation) < 0)

    return is_increasing or is_decreasing


def get_random_gauss_pert(
    num_gaussians,
    pert_size,
    num_perturbs=20,
    ROI_nbin=186,
    E0=18575.0,
    plot=False,
    seed=42,
    smoothness_parameter=0.0003,
    monotonicity=True,
):
    """Generate a random perturbation from a sum of gaussians with a fixed ampitude and optional constraints"""

    x_pert = (
        np.linspace(0, E0, ROI_nbin + 1)[:-1] + np.linspace(0, E0, ROI_nbin + 1)[1:]
    ) / 2
    scale_range = (1, 1 + pert_size)

    iteration_count = 0
    meets_condition = False
    scaled_perturbations = []
    scaled_perturbations.append(np.ones(len(x_pert)))

    np.random.seed(seed)

    for i in range(num_perturbs):
        meets_condition = False
        iteration_count = 0

        while not meets_condition:
            amplitudes = np.random.uniform(0.8, 1.2, num_gaussians)
            means = np.linspace(-5000, 23000, num_gaussians)
            stddevs = np.random.uniform(1000, 5000, num_gaussians)

            perturbation = multiple_gaussian_perturbation(
                x_pert, amplitudes, means, stddevs
            )
            scaled_perturbation, A, B, C, D = scale_perturbation(
                perturbation, scale_range
            )
            peaks, _ = find_peaks(scaled_perturbation)
            troughs, _ = find_peaks(-scaled_perturbation)

            meets_condition = check_no_large_difference(
                peaks, troughs, scaled_perturbation, threshold=smoothness_parameter
            )
            if monotonicity:
                meets_condition = check_strict_monotonicity(scaled_perturbation)
            iteration_count += 1

        scaled_perturbations.append(scaled_perturbation)
        scaled_perturbation_reversed = scaled_perturbation[::-1]
        scaled_perturbations.append(scaled_perturbation_reversed)

    if plot:
        plt.figure(figsize=(10, 8))
        for i in range(1, 2 * num_perturbs):
            plt.plot(
                x_pert / 1000, scaled_perturbations[i] - 1, linewidth=2
            )  # color='blue',

        plt.grid(True, linewidth=0.5, color="gray", linestyle="--")

        plt.xlabel("Energy (keV)", fontsize=20)
        plt.ylabel("Normalized perturbation", fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax = plt.gca()  # Get the current axis
        ax.yaxis.set_major_locator(
            MaxNLocator(nbins=5)
        )  # Set the number of y-ticks to 5
        ax.set_ylim(0, pert_size * 1.1)

        plt.tight_layout()
        # plt.savefig('perturbation_ref_8gauss_40pert_3.png', dpi=300)
        plt.show()

    return scaled_perturbations


# ================================================================================    Shape factor


def shape_factor(spec_vals, ekin, params):
    """Introduces a polynomial shapefactor to a beta spectrum
    Parameters
    -----------
    spec_vals: array
        Values of the beta spectrum
    ekin: array
        Kinetic energy values
    params: array
        Parameters for the polynomial in order of increasing degree i.e. (1, 2) give 1 + 2*x
    """
    x = (ekin - ekin.max()) / ekin.max()
    p = np.polynomial.polynomial.polyval(x, [1] + list(params))
    return p * spec_vals


# ================================================================================    RM General


def process_spectrum(interp_obj, interp_val, spectrum):
    """Helper function for add_RM"""
    return np.dot(spectrum, interp_obj(interp_val))


def add_RM(spectra, RM_dict, mode="single_RM", context="train", n_jobs=None):
    """Add a response matrix to spectra"""
    if mode == "single_RM":
        return np.dot(spectra, RM_dict["RM"])
    elif mode == "RM_interp":
        if context == "train":
            interp_obj = RM_dict["interp_obj"]
            interp_vals = RM_dict["interp_vals"]

            if n_jobs is None:
                n_jobs = cpu_count()

            with Pool(processes=n_jobs) as pool:
                partial_process = partial(process_spectrum, interp_obj)
                results = pool.starmap(partial_process, zip(interp_vals, spectra))

            return np.array(results)

        if context == "eval":
            interp_obj = RM_dict["interp_obj"]
            interp_vals = RM_dict["interp_vals"]
            return np.array(
                [
                    np.dot(spectrum, interp_obj(interp_vals[i]))
                    for i, spectrum in enumerate(spectra)
                ]
            )


# ================================================================================    MSFE


def calc_msfe_matrix(in_dim, sigma=1.0, num_encodings=32, scales=[0], base=3.0):
    """Calculates the a random matrix with entries drawn from a gaussian used in computing a multi-scale fourier encoding"""
    B = [
        sigma * np.random.randn(in_dim, num_encodings) / pow(base, scale)
        for scale in scales
    ]
    return B


def multi_scale_fourier_encoding(X, B):
    """
    Apply multi-scale Fourier feature encoding to the input data.

    Args:
    X (np.array):   Input data of shape (batch_size, input_dim)
    B (list):       List of fourier encoding matrices

    Returns:
    np.array: Encoded features
    """
    B_combined = np.concatenate(B, axis=1)

    projections = np.dot(X, B_combined)

    sin_features = np.sin(2 * np.pi * projections)
    cos_features = np.cos(2 * np.pi * projections)

    encoded_features = np.concatenate([X, sin_features, cos_features], axis=-1)

    return encoded_features


# ================================================================================    Charge sharing


def response_matrix_cs_raw(
    bin_center,
):
    """raw response for charge sharing, has to be calculated once"""
    bin_step = bin_center[1] - bin_center[0]

    def model_chargecloud(x):
        "simple gauss as 1D charge cloud model"
        return 1.0 / np.sqrt(2.0 * np.pi) * np.exp(-np.power(x, 2.0) / 2.0)

    def get_eta_function(model, eta_min=0.0, eta_max=1.0, plot=False):
        x = np.linspace(-10, 10, 10000)  # uses 10000 points for internal calculation
        dx = x[1] - x[0]
        g = model(x)
        E = np.cumsum(g) * dx
        p = 1.0 / g
        p[E < eta_min] = 0.0
        p[E > eta_max] = 0.0
        return interp1d(E, p, fill_value="extrapolate")

    nbin = len(bin_center)
    mat_cs_raw = np.zeros((nbin, nbin))
    for iE, cs_res in enumerate(mat_cs_raw):
        cs_res[0:iE] = (
            get_eta_function(model_chargecloud, eta_min=0.0, eta_max=1.0)(
                bin_center[0:iE] / bin_center[iE]
            )
            * bin_step
            / bin_center[iE]
            * 2.0
        )
    return mat_cs_raw


def response_matrix_cs_1D(w, R, bin_center):
    """calculates the response from charge sharing."""
    gen_thresh = 100
    w_r = w / R
    cs_mat = response_matrix_cs_raw(bin_center) * w_r
    # normalize
    for iE, cs_res in enumerate(cs_mat):
        y_cum = cs_res.copy()
        y_cum[0 : int(iE / 2)] = 0.0
        y_cum = y_cum.cumsum()
        i_ex = np.where(y_cum > 1.0)[0]
        if len(i_ex) == 0:
            i_crit = int(iE)
        else:
            i_crit = i_ex[0]
        cs_res[i_crit:] = 0.0
        cs_res[i_crit] = 1.0 - y_cum[i_crit - 1]
        cs_res[bin_center < gen_thresh] = 0.0
    # for i in range(0, np.shape(cs_mat)[0]):
    #     print(i, cs_mat[i].sum())
    print("overall norm: ", np.sum(cs_mat) / iE)
    return cs_mat


def response_cs(w, R, bin_center, spectrum):
    nbin = len(bin_center)
    res_2D = np.zeros((nbin, nbin))
    np.fill_diagonal(res_2D, 1)
    res_2D = np.matmul(
        res_2D,
        response_matrix_cs_1D(w=det_ccWidth, R=det_pxRadius, bin_center=bin_center),
    )
    return spectrum @ res_2D


def calc_CS_res2D(
    w,
    R,
    bin_center,
):
    """calculates the 2D charge sharing response matrix
    Parameters:
    ----------
    w: float
        charge cloud width (w_cc)
    R: float
        pixel radius
    bin_center: np.array
        bin centers of beta spectrum

    Example usage:
    -------------
    det_ccWidth  = 20.
    det_pxRadius = 1500.0

    bin_step   = 100
    max_E      = 55000
    e_data     = np.arange(0, max_E, bin_step) + bin_step/2

    RM_CS  = calc_CS_res2D(det_ccWidth, det_pxRadius, e_data,)
    """
    nbin = len(bin_center)
    res_2D = np.zeros((nbin, nbin))
    np.fill_diagonal(res_2D, 1)
    res_2D = np.matmul(
        res_2D,
        response_matrix_cs_1D(w, R, bin_center),
    )
    return res_2D


# =============================================================================================
# Processing Datasets =============================================================================================
# =============================================================================================


class Preprocessing:
    """
    Preprocessing class for preparing training datasets.

    This class provides methods for preprocessing spectra data, including feature standardization,
    min-max normalization, and data modification.

    Attributes:
    -----------
        seed (int): Random seed for reproducibility.
        rng (Generator): Random number generator.
        outputs (str): Type of output data.
        num_ref_spec (int): Number of reference spectra.
        modifications (dict): Dictionary specifying modifications to apply to the data.
        spectrum_type (str): Type of spectrum data.
        ms_range (tuple): Range of sterile mass values.
        s2t_log_range (tuple): Range of sin^2(2*theta) values.
        x_sterile (pd.Series): Sterile spectrum data.
        x_ref (pd.Series): Reference spectrum data.
        bin_width (int): Width of energy bins.
        e_range (tuple): Energy range.
        ekin (np.ndarray): Array of kinetic energies.
        y_sterile (np.ndarray): Labels for sterile spectrum data.
        y_ref (np.ndarray): Labels for reference spectrum data.
        m_s (np.ndarray): Sterile mass values.
        s2t (np.ndarray): Sin^2(2*theta) values.
        x (pd.Series or np.ndarray): Combined spectrum data.
        y (np.ndarray): Combined labels.
        m (np.ndarray): Combined mass values.
        s (np.ndarray): Combined sin^2(2*theta) values.

    Methods:
    --------
        scale(just_var=False): Perform feature standardization.
        min_max_scale(logscale=True): Perform min-max normalization.
        modify(): Apply modifications to the data.
        create_train_test_dataset(validation_split=0.5, scale=True, min_max_scale=True): Create training and validation datasets.
    """

    def __init__(self, spectra_df, use_case, seed=42):

        self.seed = seed
        self.rng = np.random.default_rng(seed)

        self.outputs = use_case["outputs"]
        self.num_ref_spec = use_case["num_ref_spec"]
        self.modifications = use_case["modifications"]
        self.spectrum_type = use_case["spectrum_type"]

        # keep noiseless spectra for case of adding response matrices & shape factors
        self.x_sterile_no_noise = spectra_df["sterile"]
        self.x_ref_no_noise = spectra_df["reference"].iloc[: self.num_ref_spec]

        # self.statistics = np.sum(self.x_ref_no_noise.iloc[0])

        self.ms_range = (
            0,
            18600,
        )  # for parametrized models & correct min / max scaling
        self.s2t_log_range = (
            -8,
            -0.5,
        )  # for parametrized models & correct min / max scaling
        if self.spectrum_type == "both":
            self.x_sterile = spectra_df["sterile_noise"]
            self.x_ref = spectra_df["reference_noise"].iloc[: self.num_ref_spec]
            self.y_sterile = np.ones_like(self.x_sterile)
            self.y_ref = np.zeros_like(self.x_ref)
            self.bins = self.x_sterile.iloc[0].shape[0]
        if self.spectrum_type == "ref":
            self.x_ref = spectra_df["reference_noise"].iloc[: self.num_ref_spec]
            self.y_ref = np.zeros_like(self.x_ref)
            self.bins = self.x_ref.iloc[0].shape[0]
        if self.spectrum_type == "ster":
            self.x_sterile = spectra_df["sterile_noise"]
            self.y_sterile = np.ones_like(self.x_sterile)
            self.bins = self.x_sterile.iloc[0].shape[0]

        for key in use_case.keys():
            if key == "no_noise":
                if use_case[key]:
                    self.x_sterile = self.x_sterile_no_noise
                    self.x_ref = self.x_ref_no_noise

        # self.bin_width = 100  # eV
        self.e_range = (0, 18600)  # eV
        self.bin_width = (self.e_range[1] - self.e_range[0]) / self.bins
        self.ekin = np.linspace(
            self.e_range[0],
            self.e_range[1],
            int((self.e_range[1] - self.e_range[0]) / self.bin_width),
        )

        self.m_s = spectra_df["m_sterile"].to_numpy()
        # self.m_s_ref = np.zeros_like(self.m_s)
        self.s2t = spectra_df["sin2theta"].to_numpy()
        # self.s2t_ref = np.zeros_like(self.s2t)

        # updates after scaling and modification

        if self.spectrum_type == "both":
            self.x = pd.concat([self.x_sterile, self.x_ref]).to_numpy()
            self.y = np.concatenate((self.y_sterile, self.y_ref))
            self.m = np.concatenate([self.m_s, self.m_s])
            self.s = np.concatenate([self.s2t, self.s2t])

        if self.spectrum_type == "ref":
            self.x = self.x_ref.to_numpy()
            self.y = self.y_ref
            self.m = self.m_s
            self.s = self.s2t

        if self.spectrum_type == "ster":
            self.x = self.x_sterile.to_numpy()
            self.y = self.y_sterile
            self.m = self.m_s
            self.s = self.s2t

    def scale(self, just_var=False):
        """
        Performes feature standardization. (Z-score Normalisation). Scales energy bin counts of beta decay spectra to have zero mean and unit variance:
        s = variance of spectrum
        u = mean of spectrum
        x_scaled = (x - u) / s
        if just_var:
            Normalization of data is changed to have unit variance
        """
        # Convert self.x to a 2D NumPy array
        x_2d = np.stack(self.x)

        # Compute standard deviation along the bin axis
        std = np.std(x_2d, axis=1, keepdims=True)

        if just_var:
            x_scaled = x_2d / std
        else:
            # Compute mean along the bin axis
            mean = np.mean(x_2d, axis=1, keepdims=True)
            x_scaled = (x_2d - mean) / std

        # Convert back to the original structure: 1D array of arrays
        self.x = np.array([x_scaled[i] for i in range(len(self.x))])
        # return self.x

    def min_max_scale(self, logscale=True):
        """
        Perform min-max normalization with respect to the full sterile mass and mixing angle range.

        Args:
            logscale (bool, optional): If True, apply log scaling to sin^2(theta). Defaults to True.
        """

        if logscale:
            self.s = np.log10(self.s)

        self.m = -1 + (self.m - self.ms_range[0]) * 2 / (
            self.ms_range[1] - self.ms_range[0]
        )
        self.s = -1 + (self.s - self.s2t_log_range[0]) * 2 / (
            self.s2t_log_range[1] - self.s2t_log_range[0]
        )

    def modify(self, context="train"):
        """
        Apply specified modifications to the spectrum data.

        This method processes the spectrum data (`self.x`) using a variety of modification options provided
        in the `self.modifications` dictionary. Modifications include shape adjustments, energy range shifts,
        response matrix applications, and more. Each type of modification has specific input requirements
        and effects on the data.

        Supported Modifications:
            - **Shape Factor (`shape_factor`)**:
            Adjusts the spectrum shape using a polynomial shape factor. Optionally applies indices
            specified in the `idxs` key. Uses the `shape_factor` function.

            - **Post-Analysis Energy (`PAE`)**:
            Shifts the energy range and modifies spectrum binning. Updates `e_range` and `ekin`.

            - **Smoothing Kernel (`smoothing_kernel`)**:
            Applies a Gaussian smoothing filter with a specified `sigma`.

            - **Response Matrix (`RM`)**:
            Applies a response matrix to the entire dataset. Uses the `add_RM` function.

            - **Response Matrix List (`RM_list`)**:
            Applies a list of response matrices to individual spectra. Each matrix corresponds to one spectrum.

            - **Response Matrix Dictionary (`RM_dict`)**:
            Applies specific response matrices from a dictionary. Keys in the dictionary match spectrum indices.

            - **Interpolated Response Matrix (`RM_interp`)**:
            Applies interpolated response matrices with randomness introduced via `dead_mean` and `dead_sigma`.
            Updates `interp_vals` in the modifications dictionary.

            - **Background Noise (`bg`)**:
            Adds background noise based on a specified scaling factor (`bg_size`). Noise is generated
            proportional to the minimum non-zero spectrum value.

            - **Multi-Scale Fourier Encoding (`multi_scale_fourier_encoding`)**:
            Encodes spectrum data using a Fourier transformation with multiple scales.

            - **Single Perturbation (`perturbation_single`)**:
            Applies a uniform scaling factor to all spectra.

            - **Full Perturbation (`perturbation_full`)**:
            Applies unique scaling factors to each spectrum individually.

        Parameters:
            context (str): Specifies the context for certain modifications (default: "train").

        Returns:
            None
        """
        if self.modifications != None:
            for i in self.modifications.keys():
                if i == "shape_factor":
                    shape_fac_arr = self.modifications["shape_factor"]
                    if "idxs" in self.modifications:
                        shape_fac_arr = shape_fac_arr[self.modifications["idxs"]]
                    self.x = np.array(
                        [
                            shape_factor(
                                self.x[i],
                                self.ekin,
                                shape_fac_arr[i],
                            )
                            for i in range(shape_fac_arr.shape[0])
                        ],
                        dtype=np.float64,
                    )

                if i == "PAE":
                    E_PAE, e_range_post = self.modifications["PAE"]
                    num_bins_prev = int(
                        (self.e_range[1] - self.e_range[0]) / self.bin_width
                    )
                    num_bins_new = int(
                        (e_range_post[1] - e_range_post[0]) / self.bin_width
                    )
                    num_bins_shift = int(E_PAE / self.bin_width)
                    # update energy range
                    self.e_range = e_range_post
                    # update ekin
                    self.ekin = np.linspace(
                        self.e_range[0],
                        self.e_range[1],
                        int((self.e_range[1] - self.e_range[0]) / self.bin_width),
                    )
                    self.x = np.array(
                        [
                            np.concatenate(
                                (
                                    np.zeros(num_bins_shift),
                                    spectrum,
                                    np.zeros(
                                        num_bins_new - num_bins_shift - num_bins_prev
                                    ),
                                )
                            )
                            for spectrum in self.x
                        ],
                        dtype=np.float64,
                    )

                if i == "smoothing_kernel":
                    sigma = self.modifications["smoothing_kernel"]
                    self.x = np.array(
                        [gaussian_filter1d(i, sigma) for i in self.x], dtype=np.float64
                    )

                if i == "RM":
                    self.x = add_RM(self.x, self.modifications, context=context)

                if i == "RM_list":  # slow
                    if len(self.modifications["RM_list"]) == self.x.shape[0]:
                        self.x = np.array(
                            [
                                i @ self.modifications["RM_list"][c]
                                for c, i in enumerate(self.x)
                            ],
                            dtype=np.float64,
                        )

                if i == "RM_dict":
                    keys = self.modifications["RM_dict"]["keys"]
                    if len(keys) == self.x.shape[0]:
                        self.x = np.array(
                            [
                                i @ self.modifications["RM_dict"][keys[c]]
                                for c, i in enumerate(self.x)
                            ],
                            dtype=np.float64,
                        )

                if i == "RM_interp":
                    dead_mean = self.modifications["RM_interp"]["dead_mean"]
                    dead_sigma = self.modifications["RM_interp"]["dead_sigma"]
                    self.modifications["RM_interp"]["interp_vals"] = (
                        dead_mean
                        + dead_sigma * self.rng.standard_normal(self.x.shape[0])
                    )

                    self.x = add_RM(
                        self.x,
                        self.modifications["RM_interp"],
                        mode="RM_interp",
                        context=context,
                    )

                if i == "bg":
                    bg_size = self.modifications["bg"]
                    bg_mean_glob = bg_mean_glob = (
                        np.ma.masked_equal(self.x[0], 0.0, copy=False).min() * bg_size
                    )
                    self.x = np.array(
                        [
                            np.where(
                                i == 0,
                                self.rng.normal(
                                    loc=bg_mean_glob,
                                    scale=np.sqrt(bg_mean_glob),
                                    size=i.shape,
                                ),
                                i,
                            )
                            for i in self.x
                        ],
                        dtype=np.float64,
                    )

                if i == "multi_scale_fourier_encoding":
                    self.scale()
                    self.x = multi_scale_fourier_encoding(
                        self.x, self.modifications["multi_scale_fourier_encoding"]
                    )

                if i == "perturbation_single":
                    self.x = np.array(
                        [spec * self.modifications[i] for spec in self.x],
                        dtype=np.float64,
                    )  # TODO: do i need to scale this to 2e15 again or not?

                if i == "perturbation_full":
                    self.x = np.array(
                        [
                            spec * self.modifications[i][c]
                            for c, spec in enumerate(self.x)
                        ],
                        dtype=np.float64,
                    )

    def create_train_test_dataset(
        self,
        validation_split=0.5,
        scale=True,
        min_max_scale=True,
        chisq=False,
        no_shuffle=False,
    ):
        """
        Create training and validation datasets.

        Args:
            validation_split (float, optional): Fraction of data to use for validation. Defaults to 0.5.
            scale (bool, optional): If True, perform feature standardization. Defaults to True.
            min_max_scale (bool, optional): If True, perform min-max scaling on the additional parameters for a parametrized NN. Defaults to True.
            no_shuffle (bool, optional): If True, the resulting arrays are not shuffled (should be left on False for trainings!)

        Returns:
            tuple: Depending on the specified outputs, returns training and validation datasets.
        """
        if no_shuffle:
            rng_idxs = np.arange(self.x.shape[0])
        else:
            rng_idxs = self.rng.choice(np.arange(self.x.shape[0]), self.x.shape[0])
        rng_idx_val = rng_idxs[: int(self.x.shape[0] * validation_split)]
        rng_idx_train = rng_idxs[int(self.x.shape[0] * validation_split) :]

        if scale:
            self.scale()

        if self.outputs == "xy":
            x_train = self.x[rng_idx_train]
            y_train = self.y[rng_idx_train]
            x_val = self.x[rng_idx_val]
            y_val = self.y[rng_idx_val]
            return (
                x_train,
                y_train,
                x_val,
                y_val,
            )  # maybe need to change this to numpy array

        if self.outputs == "xyms":
            if min_max_scale:
                self.min_max_scale()
            x_train = self.x[rng_idx_train]
            y_train = self.y[rng_idx_train]
            m_s_train = self.m[rng_idx_train]
            s2t_train = self.s[rng_idx_train]
            x_val = self.x[rng_idx_val]
            y_val = self.y[rng_idx_val]
            m_s_val = self.m[rng_idx_val]
            s2t_val = self.s[rng_idx_val]
            return (
                x_train,
                y_train,
                m_s_train,
                s2t_train,
                x_val,
                y_val,
                m_s_val,
                s2t_val,
            )

        if self.outputs == "xy_no_split":
            if chisq:  # failsafe for case of single spectra in chisq scan
                return self.x, self.y

            x = self.x[rng_idxs]
            y = self.y[rng_idxs]
            return x, y

        if self.outputs == "xyms_no_split":
            if min_max_scale:
                self.min_max_scale()
            x = self.x[rng_idxs]
            y = self.y[rng_idxs]
            m = self.m[rng_idxs]
            s = self.s[rng_idxs]
            return x, y, m, s

    def _add_noise(self):
        """adds bin-wise poisson noise"""
        err = np.sqrt(np.abs(self.x))
        noise = self.rng.normal(loc=0.0, scale=err)
        self.x = self.x + noise
        # self._scale_to_statistics()

    def _require_no_noise(self):
        """Chooses non-fluctuated spectra for the output. Has to be applied before to any modifications"""
        if self.spectrum_type == "both":
            self.x_sterile = self.x_sterile_no_noise
            self.x_ref = self.x_ref_no_noise
            self.y_sterile = np.ones_like(self.x_sterile)
            self.y_ref = np.zeros_like(self.x_ref)
            self.bins = self.x_sterile.iloc[0].shape[0]
        if self.spectrum_type == "ref":
            self.x_ref = self.x_ref_no_noise
            self.y_ref = np.zeros_like(self.x_ref)
            self.bins = self.x_ref.iloc[0].shape[0]
        if self.spectrum_type == "ster":
            self.x_sterile = self.x_sterile_no_noise
            self.y_sterile = np.ones_like(self.x_sterile)
            self.bins = self.x_sterile.iloc[0].shape[0]

        if self.spectrum_type == "both":
            self.x = pd.concat([self.x_sterile, self.x_ref]).to_numpy()
            self.y = np.concatenate((self.y_sterile, self.y_ref))
            self.m = np.concatenate([self.m_s, self.m_s])
            self.s = np.concatenate([self.s2t, self.s2t])

        if self.spectrum_type == "ref":
            self.x = self.x_ref.to_numpy()
            self.y = self.y_ref
            self.m = self.m_s
            self.s = self.s2t

        if self.spectrum_type == "ster":
            self.x = self.x_sterile.to_numpy()
            self.y = self.y_sterile
            self.m = self.m_s
            self.s = self.s2t

    # def _scale_to_statistics(self):
    #     np.array([self.statistics * i[:] / np.sum(i) for i in self.x], )


# =============================================================================================
# Creating Datasets =============================================================================================
# =============================================================================================


class Dataset:
    def __init__(self, x, y, seed=42):
        self.x, self.y = x, y

        self.seed = seed
        self.rng = np.random.default_rng(self.seed)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]

    def shuffle(self):
        rng_idxs = self.rng.choice(
            np.arange(self.x.shape[0]), self.x.shape[0], replace=False
        )
        self.x = self.x[rng_idxs]
        self.y = self.y[rng_idxs]


class DataLoader:
    def __init__(self, dataset, batch_size, device):
        self.ds, self.bs = dataset, batch_size
        self.device = device

    def __iter__(self):
        for i in range(0, len(self.ds), self.bs):
            x, y = self.ds[i : i + self.bs]
            x, y = torch.FloatTensor(x.astype(np.float64)), torch.FloatTensor(
                y.astype(np.float64)
            ).unsqueeze(-1)
            batch = x.to(self.device), y.to(self.device)
            yield batch


class Dataset_Parametrized(Dataset):
    def __init__(self, x, y, m_s, s2t, seed=42):
        super().__init__(x, y, seed)
        self.m_s, self.s2t = m_s, s2t

    def __getitem__(self, i):
        return self.x[i], self.y[i], self.m_s[i], self.s2t[i]

    def shuffle_parametrized(self):
        rng_idxs = self.rng.choice(
            np.arange(self.x.shape[0]), self.x.shape[0], replace=False
        )
        self.x = self.x[rng_idxs]
        self.y = self.y[rng_idxs]
        self.m_s = self.m_s[rng_idxs]
        self.s2t = self.s2t[rng_idxs]


class DataLoader_Parametrized(DataLoader):
    def __init__(self, dataset, batch_size, device):
        super().__init__(dataset, batch_size, device)

    def __iter__(self):
        for i in range(0, len(self.ds), self.bs):
            x, y, m_s, s2t = self.ds[i : i + self.bs]
            x, y, m_s, s2t = (
                torch.FloatTensor(x.astype(np.float64)),
                torch.FloatTensor(y.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(m_s.astype(np.float64)).unsqueeze(-1),
                torch.FloatTensor(s2t.astype(np.float64)).unsqueeze(-1),
            )
            batch = (
                x.to(self.device),
                y.to(self.device),
                m_s.to(self.device),
                s2t.to(self.device),
            )
            yield batch


# old 10.04.24
# class Dataset:
#     def __init__(self, x, y):
#         self.x, self.y = x, y

#     def __len__(self):
#         return len(self.x)

#     def __getitem__(self, i):
#         return self.x[i], self.y[i]


# class DataLoader:
#     def __init__(self, dataset, batch_size, device):
#         self.ds, self.bs = dataset, batch_size
#         self.device = device

#     def __iter__(self):
#         for i in range(0, len(self.ds), self.bs):
#             x, y = self.ds[i : i + self.bs]
#             x, y = torch.FloatTensor(x.astype(np.float64)), torch.FloatTensor(
#                 y.astype(np.float64)
#             ).unsqueeze(-1)
#             batch = x.to(self.device), y.to(self.device)
#             yield batch


# old old
# class Dataset:
#     def __init__(self, x, y):
#         self.x, self.y = x, y

#     def __len__(self):
#         return len(self.x)

#     def __getitem__(self, i):
#         return self.x[i], self.y[i]


# class DataLoader:
#     def __init__(self, dataset, batch_size, device):
#         self.ds, self.bs = dataset, batch_size
#         self.device = device

#     def __iter__(self):
#         for i in range(0, len(self.ds), self.bs):
#             x, y = self.ds[i : i + self.bs]
#             x, y = torch.FloatTensor(x), torch.FloatTensor(y).unsqueeze(-1)
#             batch = x.to(self.device), y.to(self.device)
#             yield batch
