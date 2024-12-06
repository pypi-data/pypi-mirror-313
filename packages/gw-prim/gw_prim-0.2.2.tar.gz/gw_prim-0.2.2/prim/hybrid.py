import copy

import lmfit
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

from prim import waveform


def MultimodeHybridModel(x, dt, dphi, dpsi, waveform_nr, modes):
    """
    This function is designed to be used with lmfit.
    It can fit multiple modes by concatenating them.

    Use this to help
    https://lmfit.github.io/lmfit-py/faq.html#how-can-i-fit-multiple-data-sets

    input:
        x: time arrray to evaluate model on
        dt: time shift parameter to estimate
        dphi: orbital phase shift parameter to estimate
        dpsi: polarisation angle parameter to estimate
        waveform_nr: an instance of the waveform.Waveform class
            containing the NR data.
            Specifically, all that is needed are the times
            'waveform_nr.times' and
            the dictionary complex multipoles 'waveform_nr.hlms'
        modes: list of (l,m) modes to use in the fit

    returns:
        array where all hlm_nr_y multipole data has been
        concatenated, selecting only the input `x` times
        with the time, phase and polarisation shift applied.
    """
    # assert type(waveform_nr) == waveform.Waveform, 'must be of type waveform.Waveform'
    # waveform_nr = copy.deepcopy(waveform_nr)
    i_hlm_real = {}
    i_hlm_imag = {}
    for k in modes:
        i_hlm_real[k] = IUS(waveform_nr.times, waveform_nr.hlms[k].real, ext=3)
        i_hlm_imag[k] = IUS(waveform_nr.times, waveform_nr.hlms[k].imag, ext=3)

    zs = []
    for k in modes:
        m = k[1]
        z = i_hlm_real[k](x + dt) + 1.0j * i_hlm_imag[k](x + dt)
        z *= np.exp(1.0j * m * dphi)
        z *= np.exp(1.0j * dpsi)
        zs.append(z)

    return np.concatenate(zs)


def fit_hybrid(wf_pn, wf_nr, win1, win2, modes, time_shift_guess, n_tries=5, max_nfev=None):
    """
    wf_pn: an instance of the waveform.Waveform class
            containing the PN data.
        This waveform could also be called waveform_1, the fixed waveform or the 'left' waveform.
        During the fitting process we leave this waveform fixed / untransformed.
        It's called wf_pn but the waveform doesn't have to be from PN
    wf_nr: an instance of the waveform.Waveform class
            containing the NR data.
        This is the 'right' waveform. In this code we apply transformations to this
        waveform to align it with wf_pn.
        It's called wf_nr but the waveform doesn't have to be from NR.
    win1: start time of hybrid window, in pn times
    win2: end time of hybrid window, in pn times
    modes: list of tuples of which modes to use to fit
    """
    wf_pn = copy.deepcopy(wf_pn)
    wf_nr = copy.deepcopy(wf_nr)

    ##############################
    # prepare PN data
    wf_pn.mask(start_time=win1, end_time=win2)
    x_fit = wf_pn.times
    y_fit = np.concatenate([wf_pn.hlms[k] for k in modes])
    #
    ##############################

    # need to fit each waveform multiple times
    # with either dpsi fixed to either 0 or pi
    # and then with random dphis to avoid local minima
    # pick the model with smallest redchis

    # it's 0 or pi because we define it as exp(i*psi0)

    # psi=0
    results_psi_0 = []
    chisq_psi_0 = []

    # psi=pi
    results_psi_pi = []
    chisq_psi_pi = []

    model = lmfit.Model(
        MultimodeHybridModel,
        independent_vars="x",
        param_names=["dt", "dphi", "dpsi"],
        waveform_nr=wf_nr,
        modes=modes,
    )

    # parallelise this loop?
    for i in range(n_tries):
        # psi=0
        params = model.make_params(
            dt=dict(value=time_shift_guess),
            dphi=dict(value=np.random.uniform(0, 2 * np.pi), min=0, max=2 * np.pi),
            dpsi=dict(value=0, vary=False),
        )

        result = model.fit(y_fit, params, x=x_fit, max_nfev=max_nfev)
        results_psi_0.append(result)
        chisq_psi_0.append(result.redchi)

        # psi=pi
        params = model.make_params(
            dt=dict(value=time_shift_guess),
            dphi=dict(value=np.random.uniform(0, 2 * np.pi), min=0, max=2 * np.pi),
            dpsi=dict(value=np.pi, vary=False),
        )

        result = model.fit(y_fit, params, x=x_fit, max_nfev=max_nfev)
        results_psi_pi.append(result)
        chisq_psi_pi.append(result.redchi)

    psi_0_best_idx = np.argmin(chisq_psi_0)
    psi_0_best_value = chisq_psi_0[psi_0_best_idx]

    psi_pi_best_idx = np.argmin(chisq_psi_pi)
    psi_pi_best_value = chisq_psi_pi[psi_pi_best_idx]

    # return model with smallest chisquare
    if psi_0_best_value <= psi_pi_best_value:
        return results_psi_0[psi_0_best_idx]
    else:
        return results_psi_pi[psi_pi_best_idx]


def get_window_times(wf, n_cycles_before_window=2, n_cycles_in_window=6):
    wf = copy.deepcopy(wf)
    wf.compute_phase()

    # estimate derivative of phase using the first half of the data
    idx_half = int(len(wf.phases[2, 2]) // 2)
    phi = wf.phases[2, 2][:idx_half]
    avg_sign = np.mean(np.diff(phi))
    if avg_sign < 0:
        phi_win1 = wf.phases[2, 2][0] - 2 * np.pi * n_cycles_before_window
        phi_win2 = phi_win1 - 2 * np.pi * n_cycles_in_window
        win1 = wf.times[wf.phases[2, 2] >= phi_win1][-1]
        win2 = wf.times[wf.phases[2, 2] >= phi_win2][-1]
    else:
        phi_win1 = wf.phases[2, 2][0] + 2 * np.pi * n_cycles_before_window
        phi_win2 = phi_win1 + 2 * np.pi * n_cycles_in_window
        win1 = wf.times[wf.phases[2, 2] <= phi_win1][-1]
        win2 = wf.times[wf.phases[2, 2] <= phi_win2][-1]

    return win1, win2


def blending_function(t, win1, win2):
    """
    https://arxiv.org/abs/1812.07865
    """
    tau = np.zeros(len(t))
    mask = np.where((t >= win1) & (t <= win2))

    frac = (t[mask] - win1) / (win2 - win1)

    tau[mask] = np.sin(0.5 * np.pi * frac) ** 2
    mask = np.where(t > win2)
    tau[mask] = 1
    return tau


def build_hybrid(wf_pn, wf_nr, dt, dphi, dpsi, win1, win2, delta_t=None):
    """
    delta_t: output delta_t for hybrid, default None. If None then will use PN delta_t/4
    """
    wf_pn = copy.deepcopy(wf_pn)
    wf_nr = copy.deepcopy(wf_nr)

    (wf_nr.apply_time_shift(-dt).apply_phase_shift(dphi).apply_polarisation_shift(dpsi))

    # loop over all modes in waveform dict
    # apply hybridisation to each mode
    # todo: apply global time and phase shift

    modes = wf_nr.modes

    # use 2,2 mode to get common time array
    wf_pn_x = wf_pn.times
    wf_nr_x_shifted = wf_nr.times

    t_start = np.min([wf_pn_x[0], wf_nr_x_shifted[0]])
    t_end = np.max([wf_pn_x[-1], wf_nr_x_shifted[-1]])
    if delta_t is None:
        delta_t = (wf_pn_x[1] - wf_pn_x[0]) / 4
    times = np.arange(t_start, t_end, delta_t)

    # window/blending function
    tau = blending_function(times, win1, win2)

    wf_hybrid = {}
    wf_hybrid["hlm"] = {}

    for i, mode in enumerate(modes):
        ell = mode[0]
        mm = mode[1]

        # get PN waveform
        wf_pn_x = wf_pn.times
        wf_pn_y = wf_pn.hlms[ell, mm]

        # get NR waveform and apply time, phase and polarisation shifts
        wf_nr_x_shifted = wf_nr.times
        wf_nr_y_shifted = wf_nr.hlms[ell, mm]

        # interpolate real and imag PN and NR waveforms
        # by setting the extrapolation behaviour like this
        # we can easily zero pad the left and right to the same time array
        # and then easily multiply the window function

        hybrid_pn_real = IUS(wf_pn_x, wf_pn_y.real, ext=1)(times) * (1 - tau)
        hybrid_nr_real = IUS(wf_nr_x_shifted, wf_nr_y_shifted.real, ext=1)(times) * tau
        hybrid_real = hybrid_pn_real + hybrid_nr_real

        hybrid_pn_imag = IUS(wf_pn_x, wf_pn_y.imag, ext=1)(times) * (1 - tau)
        hybrid_nr_imag = IUS(wf_nr_x_shifted, wf_nr_y_shifted.imag, ext=1)(times) * tau
        hybrid_imag = hybrid_pn_imag + hybrid_nr_imag

        wf_hybrid["hlm"][mode] = hybrid_real + 1.0j * hybrid_imag

    # time shift peak sum
    # amps = []
    # for mode in modes:
    #     amps.append(np.abs(wf_hybrid['hlm'][mode]))
    # amps = np.array(amps)
    # t_peak = times[np.argmax(amps.sum(0))]

    # wf_hybrid['t'] = times - t_peak
    wf_hybrid["t"] = times

    wf_hybrid = waveform.Waveform(wf_hybrid["t"], hlms=wf_hybrid["hlm"])

    return wf_hybrid
