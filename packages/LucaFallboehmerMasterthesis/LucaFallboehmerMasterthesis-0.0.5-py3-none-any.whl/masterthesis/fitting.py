"""Important fitting functions and theoretical models"""

import torch
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import sys
import os
import scipy
from iminuit import Minuit

# from constants import *
# from beta_gen import *
# from models import *
# from dataset import *
# from model_eval import *
# from model_pipeline import *

# if USE_NUMBA_JIT:
#     from beta_decay_jit import *

#     print("using numbas jit compilation")
# else:
#     from beta_decay import *
from .constants import *
from .beta_decay import *
from .beta_gen import *
from .models import *
from .dataset import *
from .model_eval import *
from .model_pipeline import *

# ================================================================================================
# Fitting Backbone ================================================================================================
# ================================================================================================


def scale_spec_stats(spectra, N_tot):
    return np.array(
        [N_tot * i[:] / i.sum() for i in spectra], dtype=np.float64
    )  # have to be ints for poissonian ll


def neg_log_likelihood_gauss(y, y_error, model):
    """the function that is minimized for a fit with gaussian errors.
    This is the chi2 function, and corresponds to -2*log(lh).
    """
    return np.sum(np.square((model - y) / y_error))


def neg_log_likelihood_poisson(counts, model):
    """
    Approximation for the -2log(lh) for Poissonian counts assuming expectation
    values given by model. Implemented by Andrea
    """
    return np.sum(
        np.square((model - counts) / np.where(counts > 0, np.sqrt(counts), 1))
    )


def neg_log_likelihood_cov(y, cov_inv, model):
    """the function that is minimized for a fit with covariance matrix.
    This is the chi2 function, and corresponds to -2*log(lh).
    """
    return np.sum(np.dot((model - y), np.matmul(cov_inv, (model - y))))


def residuals_poisson(counts, model):  # pull terms
    """
    Residuals belonging to neg_log_likelihood_poisson.

    """
    return (model - counts) / np.where(counts > 0, np.sqrt(counts), 1)


def minimize_minuit(nll, p0, keys_free, limitsdict, verbose=0):
    """
    minimize a function using minuit.
    nll: callable,    function to be minimized, nll(*p)
    p0: dict,         start parameters for the minimization
    keys_free: list,  keys of the parameters which are free
    limitsdict: dict, can contain limits for each parameter fo the form {key: (min,max)}
    verbose: int      amount of log output. can be 0, 1 or 2

    Returns a dictionary with useful output of the minimization
    """
    keys_fixed = [key for key in p0.keys() if key not in keys_free]
    m = Minuit(nll, name=list(p0.keys()), **p0)
    m.errordef = 1
    for key in keys_fixed:
        m.fixed[key] = True
    for key, limits in limitsdict.items():
        m.limits[key] = limits
    m.migrad()
    if verbose > 0:
        print(m)
    params = {k: v for k, v in zip(m.parameters, m.values)}
    rdict = {}
    rdict["params"] = params
    rdict["m"] = m
    return rdict


def do_fit(y_exp, keys_free, model, p0, limdict, pulls=None):
    """ " Fits gridpoint data to a model (contained in the loss function)

    Parameters
    ----------
    lossfun: callable
        function to perform the fit on
    y_exp: numpy.ndarray
        spectrum at the gridpoint to be evaluated
    p0: dict
        start parameters for the minimization
    keys_free: list,
        keys of the parameters which are free
    model: callable
        model for the fit, also contained in lossfun
    limitsdict: dict,
        can contain limits for each parameter fo the form {key: (min,max)}

    """

    # Local model to use for the fit
    def model_local(*p):
        kwargs = {ki: pi for ki, pi in zip(p0.keys(), p)}
        return model(**kwargs)

    # Setting up Pull Terms, NOT YET IMPLEMENTED: Pulls for m_s, s2t, norm: just need to change p[2:] to e.g. p[:] if all three should have pulls
    if pulls is not None:
        p_t, p_s = pulls["true"], pulls["sigma"]

    # Loss function to minimize
    def nll(*p):
        if pulls is not None:
            return neg_log_likelihood_poisson(y_exp, model_local(*p)) + np.sum(
                [((i - p_t[c]) / p_s[c]) ** 2 for c, i in enumerate(p[3:])]
            )
        else:
            return neg_log_likelihood_poisson(y_exp, model_local(*p))

    # fit
    res = minimize_minuit(nll, p0, keys_free=keys_free, limitsdict=limdict)

    # fit info
    res["nll"] = res["m"].fval
    # res["nll"] = nll(*res['params'].values())
    chi2 = res["nll"]
    ndof = len(y_exp) - len(p0)
    rchi2 = chi2 / ndof
    pvalue = np.float64(1.0 - scipy.stats.chi2.cdf(chi2, df=ndof))
    model_out = model(**res["params"])
    residuals = (model_out - y_exp) / np.where(y_exp > 0, np.sqrt(y_exp), 1)
    errs = np.where(y_exp > 0, np.sqrt(y_exp), 1)

    return {
        "full_res": res,
        "chi2": chi2,
        "ndof": ndof,
        "rchi2": rchi2,
        "pvalue": pvalue,
        "model_out": model_out,
        "residuals": residuals,
        "fit_valid": res["m"].valid,
        "fit_accurate": res["m"].accurate,
        "errs": errs,
    }


# ================================================================================================
# Models ================================================================================================
# ================================================================================================


def shape_factor_fit(spec_vals, ekin, **kwargs):
    x = (ekin - ekin.max()) / ekin.max()
    p = 1
    for c, (k, v) in enumerate(kwargs.items()):
        p += v * x ** (c + 1)
    shaped_beta = p * spec_vals
    return shaped_beta


def beta_theo(m_s, s2t):
    ekin = np.linspace(0, 18600, 186)
    return (
        beta_spec(
            ekin,
            ekin.max(),
            m_neutrino=1,
            m_sterile=m_s,
            sin2theta=s2t,
            smallterms=True,
        )
        * 2e15
        / np.sum(
            beta_spec(
                ekin,
                ekin.max(),
                m_neutrino=1,
                m_sterile=m_s,
                sin2theta=s2t,
                smallterms=True,
            )
        )
    )


def beta_theo_norm(m_s, s2t, norm):
    ekin = np.linspace(0, 18600, 186)
    return (
        norm
        * beta_spec(
            ekin,
            ekin.max(),
            m_neutrino=1,
            m_sterile=m_s,
            sin2theta=s2t,
            smallterms=True,
        )
        / np.sum(
            beta_spec(
                ekin,
                ekin.max(),
                m_neutrino=1,
                m_sterile=m_s,
                sin2theta=s2t,
                smallterms=True,
            )
        )
    )


def beta_theo_norm_sf(m_s, s2t, norm, **kwargs):
    ekin = np.linspace(0, 18600, 186)
    return (
        norm
        * shape_factor_fit(
            beta_spec(
                ekin,
                ekin.max(),
                m_neutrino=1,
                m_sterile=m_s,
                sin2theta=s2t,
                smallterms=True,
            ),
            ekin,
            **kwargs
        )
        / np.sum(
            shape_factor_fit(
                beta_spec(
                    ekin,
                    ekin.max(),
                    m_neutrino=1,
                    m_sterile=m_s,
                    sin2theta=s2t,
                    smallterms=True,
                ),
                ekin,
                **kwargs
            )
        )
    )


# ================================================================================================
# Special Versions for Contour Interpolation ================================================================================================
# ================================================================================================


def calc_zero(a, b):
    return -a / b


def linear(x, a, b):
    return a + x * b


def minimize_minuit_scan_int(nll, p0, keys_free, limitsdict, verbose=0):
    """
    minimize a function using minuit.
    nll: callable,    function to be minimized, nll(*p)
    p0: dict,         start parameters for the minimization
    keys_free: list,  keys of the parameters which are free
    limitsdict: dict, can contain limits for each parameter fo the form {key: (min,max)}
    verbose: int      amount of log output. can be 0, 1 or 2

    Returns a dictionary with useful output of the minimization
    """
    keys_fixed = [key for key in p0.keys() if key not in keys_free]
    m = Minuit(nll, name=list(p0.keys()), **p0)
    m.errordef = 1
    for key in keys_fixed:
        m.fixed[key] = True
    for key, limits in limitsdict.items():
        m.limits[key] = limits
    m.migrad()
    if verbose > 0:
        print(m)
    params = {k: v for k, v in zip(m.parameters, m.values)}
    rdict = {}
    rdict["params"] = params
    rdict["m"] = m
    return rdict


def do_fit_scan_int(
    x_data,
    y_exp,
    errors,
    keys_free,
    model,
    p0,
    limdict,
    pulls=None,
    use_cov=None,
    method="gauss",
):
    """ " Fits gridpoint data to a model (contained in the loss function)

    Parameters
    ----------
    lossfun: callable
        function to perform the fit on
    y_exp: numpy.ndarray
        spectrum at the gridpoint to be evaluated
    p0: dict
        start parameters for the minimization
    keys_free: list,
        keys of the parameters which are free
    model: callable
        model for the fit, also contained in lossfun
    limitsdict: dict,
        can contain limits for each parameter fo the form {key: (min,max)}

    """

    # Local model to use for the fit
    def model_local(x_data, *p):
        kwargs = {ki: pi for ki, pi in zip(p0.keys(), p)}
        return model(x_data, **kwargs)

    # Setting up Pull Terms, NOT YET IMPLEMENTED: Pulls for m_s, s2t, norm: just need to change p[2:] to e.g. p[:] if all three should have pulls
    if pulls is not None:
        p_t, p_s = pulls["true"], pulls["sigma"]

    if use_cov is not None:
        # add epsilon to diagonal to ensure invertibility
        eps = np.diag(np.full((use_cov.shape[0]), np.finfo(float).eps))
        cov_inv = np.linalg.inv(use_cov + eps)

    # Loss function to minimize
    def nll(*p):
        if method == "gauss":
            return neg_log_likelihood_gauss(y_exp, errors, model_local(x_data, *p))
        else:
            if use_cov is None:
                if pulls is not None:
                    return neg_log_likelihood_poisson(y_exp, model_local(*p)) + np.sum(
                        [((i - p_t[c]) / p_s[c]) ** 2 for c, i in enumerate(p[3:])]
                    )
                else:
                    return neg_log_likelihood_poisson(y_exp, model_local(*p))
            else:
                if pulls is not None:
                    return neg_log_likelihood_cov(
                        y_exp, cov_inv, model_local(*p)
                    ) + np.sum(
                        [((i - p_t[c]) / p_s[c]) ** 2 for c, i in enumerate(p[3:])]
                    )
                else:
                    return neg_log_likelihood_cov(y_exp, cov_inv, model_local(*p))

    # fit
    res = minimize_minuit_scan_int(nll, p0, keys_free=keys_free, limitsdict=limdict)

    # fit info
    res["nll"] = res["m"].fval
    # res["nll"] = nll(*res['params'].values())
    chi2 = res["nll"]
    ndof = len(y_exp) - len(p0)
    rchi2 = chi2 / ndof
    pvalue = np.float64(1.0 - scipy.stats.chi2.cdf(chi2, df=ndof))
    model_out = model(x_data, **res["params"])
    if method == "gauss":
        residuals = (model_out - y_exp) / errors
        errs = errors
    else:
        residuals = (model_out - y_exp) / np.where(y_exp > 0, np.sqrt(y_exp), 1)
        errs = np.where(y_exp > 0, np.sqrt(y_exp), 1)

    return {
        "full_res": res,
        "chi2": chi2,
        "ndof": ndof,
        "rchi2": rchi2,
        "pvalue": pvalue,
        "model_out": model_out,
        "residuals": residuals,
        "fit_valid": res["m"].valid,
        "fit_accurate": res["m"].accurate,
        "errs": errs,
    }


# ================================================================================================
# Contour ================================================================================================
# ================================================================================================


def contour_fit(
    model, scan_params, scan_df, keys_free, limdict, p0, pulls=None, use_cov=None, CL=95
):

    pvalue_matrix = np.zeros((scan_params[0].shape[0], scan_params[1].shape[0]))
    chi2_matrix = np.zeros((scan_params[0].shape[0], scan_params[1].shape[0]))
    rchi2_matrix = np.zeros((scan_params[0].shape[0], scan_params[1].shape[0]))

    param_values = {k: v for k, v in zip(scan_params[0], scan_params[1])}
    residuals_matrix = {k: v for k, v in zip(scan_params[0], scan_params[1])}
    for i in param_values.keys():
        param_values[i] = {
            k_nested: v_nested
            for k_nested, v_nested in zip(scan_params[1], scan_params[1])
        }
        residuals_matrix[i] = {
            k_nested: v_nested
            for k_nested, v_nested in zip(scan_params[1], scan_params[1])
        }

    s2t_scan_matrix = np.zeros_like(pvalue_matrix)
    m_s_scan_matrix = np.zeros_like(pvalue_matrix)

    with trange(len(scan_params[0]), unit="m_s") as iterable:
        for count_ms in iterable:
            # for count_ms, ms in enumerate(scan_params[0]):
            ms = scan_params[0][count_ms]

            for count_s2t, s2t in enumerate(scan_params[1]):

                # filter scan data frame
                y_mask1 = scan_df.m_sterile == ms
                s1 = scan_df[y_mask1]
                y_mask2 = s1.sin2theta == s2t
                s2 = s1[y_mask2]

                # p0 = {"m_s": ms, "s2t": s2t}
                # p0 = {"m_s": 0, "s2t": 0, "norm": 2e15}   # -> p0 now passed as argument

                # sterile spectrum ("measured / experimental spectrum")
                y_exp_uns = [s2["sterile"].iloc[0]]
                y_exp = scale_spec_stats(y_exp_uns, 2e15)[0]

                # perform the fit
                res = do_fit(
                    y_exp=y_exp,
                    keys_free=keys_free,
                    model=model,
                    p0=p0,
                    limdict=limdict,
                    pulls=pulls,
                    use_cov=use_cov,
                )

                pvalue_matrix[count_ms][count_s2t] = res["pvalue"]
                chi2_matrix[count_ms][count_s2t] = res["chi2"]
                rchi2_matrix[count_ms][count_s2t] = res["rchi2"]
                param_values[ms][s2t] = res["full_res"]["params"]
                residuals_matrix[ms][s2t] = res["residuals"]

                # get matrix of scan data
                s2t_scan_matrix[count_ms][count_s2t] = s2t
                m_s_scan_matrix[count_ms][count_s2t] = ms

    ndof = res["ndof"]

    # getting the contour:
    s2t_contour = []
    m_s_contour = []
    z_value_chisq = scipy.stats.chi2.ppf(CL / 100, df=2)

    for r, row in enumerate(s2t_scan_matrix):
        flag = 0
        for c, column in enumerate(row):
            if flag == 0:
                if chi2_matrix[r][c] <= (z_value_chisq):
                    s2t_contour.append(s2t_scan_matrix[r][c])
                    m_s_contour.append(m_s_scan_matrix[r][c])
                    flag = 1

    out_dict = {
        "contour_ms": m_s_contour,
        "contour_s2t": s2t_contour,
        "pvalue_matrix": pvalue_matrix,
        "chi2_matrix": chi2_matrix,
        "rchi2_matrix": rchi2_matrix,
        "param_values_matrix": param_values,
        "residuals_matrix": residuals_matrix,
    }
    return out_dict
