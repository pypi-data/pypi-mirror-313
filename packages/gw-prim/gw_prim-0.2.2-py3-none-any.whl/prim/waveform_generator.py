# import warnings
# warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")

import h5py
import lal
import lalsimulation as lalsim
import numpy as np
import numpy.typing as npt
import phenom
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

try:
    import pyseobnr  # pyright: ignore

    PYSEOBNR_AVAILABLE = True
except ImportError:
    PYSEOBNR_AVAILABLE = False


def td_amp_scale(mtot: float | int, distance: float | int) -> float:
    """
    Computes the amplitude pre-factor for time-domain signals
    given as M*G/c^2 * M_sun / dist

    Parameters
    ----------
    mtot : float | int
        Total mass in solar masses
    distance : float | int
        Distance to source in SI units (metres)

    Returns
    -------
    float
        The scale factor
    """
    return mtot * lal.MRSUN_SI / distance  # pyright: ignore


def gen_td_modes_wf_params(
    m1: int | float = 50,
    m2: int | float = 50,
    S1x: int | float = 0,
    S1y: int | float = 0,
    S1z: int | float = 0,
    S2x: int | float = 0,
    S2y: int | float = 0,
    S2z: int | float = 0,
    distance: int | float = 1,
    deltaT: int | float = 1 / 4096,
    phiRef: int | float = 0.0,
    f_min: int | float = 10,
    f_ref: int | float = 10,
    LALpars: None | lal.Dict = None,
    approximant: str = "SEOBNRv4P",
    lmax_dummy: int = 4,
) -> dict:
    """
    Function to convert the input into a dictionary that can be read by the waveform generator. The
    waveform generator in this case is either `gen_td_modes_wf` which calls
    `SimInspiralChooseTDModes` or `generate_td_modes` from `pyseobnr`.

    Parameters
    ----------
    m1: int | float, default 50
    m2: int | float, default 50
    S1x: int | float, default 0
    S1y: int | float, default 0
    S1z: int | float, default 0
    S2x: int | float, default 0
    S2y: int | float, default 0
    S2z: int | float, default 0
    distance: int | float, default 1
        distance in metres to the source
    deltaT: int | float, default 1 / 4096
    phiRef: int | float, default 0.0
    f_min: int | float, default 10
    f_ref: int | float, default 10
    LALpars: None | lal.Dict, default None
        Used to supply additional parameters to the generator.
        Typically used to set which modes to generate.
    approximant : str, default "SEOBNRv4P"
        The lalsim name of the approximant to generate or if generating
        using pyseobnr then this is either "SEOBNRv5HM" or "SEOBNRv5PHM"
    lmax_dummy : int, default 4
        old option for XLALSimInspiralChooseTDModes
        that sets the max ell mode, this tends to not be used
        as we use ModeArray instead in LALpars.

    Returns
    -------
    dict
        A dictionary with keys that the waveform generator expects.
    """

    if approximant in ["SEOBNRv5HM", "SEOBNRv5PHM"]:
        assert PYSEOBNR_AVAILABLE is True, "pyseobnr not installed"
        # pyseobnr
        distance_Mpc = distance / lal.PC_SI / 1e6
        p = {
            "mass1": m1,
            "mass2": m2,
            "spin1x": S1x,
            "spin1y": S1y,
            "spin1z": S1z,
            "spin2x": S2x,
            "spin2y": S2y,
            "spin2z": S2z,
            "deltaT": deltaT,
            "f22_start": f_min,
            "phi_ref": phiRef,
            "distance": distance_Mpc,
            "inclination": 0,
            # "f_max": 0.5 / deltaT, # this is the default value in pyseobnr i.e. Nyquist
            "approximant": approximant,
        }

    else:
        # lalsuite
        p = dict(
            m1=m1,
            m2=m2,
            S1x=S1x,
            S1y=S1y,
            S1z=S1z,
            S2x=S2x,
            S2y=S2y,
            S2z=S2z,
            phiRef=phiRef,
            r=distance,  # in metres
            deltaT=deltaT,
            f_min=f_min,
            f_ref=f_ref,
            LALpars=LALpars,
            lmax=lmax_dummy,
            approximant=lalsim.GetApproximantFromString(approximant),
        )

    return p


def gen_td_modes_wf(p: dict, modes: list[tuple[int, int]] = [(2, 2)]) -> tuple[npt.NDArray, dict]:
    """
    Function to generate waveform modes using lalsimulation's
    SimInspiralChooseTDModes function.

    Parameters
    ----------
        p : dict
            normally the output of gen_td_modes_wf_params
        modes : list[tuple[int,int]], default [(2,2)]
            modes to generate
            Note: Depending on the waveform model used
            you might need to explicitly provide both positive and
            negative modes.
            To supply multiple modes you do [(2,2), (2,1), (3,3), ...]

    Returns
    -------
        times : npt.NDArray
            The time grid that the waveform is evaluated at in units of seconds
        hlms: dict
            contains time domain complex hlm modes. The keys are given by the
            input modes.
    """
    p = p.copy()

    if (2, 2) not in modes:
        raise NotImplementedError(
            "(2,2) mode not in modes.\
Currently we assume that this mode exists."
        )

    if p["LALpars"] is None:
        p["LALpars"] = lal.CreateDict()

    # amplitude order?
    # lalsim.SimInspiralWaveformParamsInsertPNAmplitudeOrder(p['LALpars'], -1)

    ma = lalsim.SimInspiralCreateModeArray()
    for ell, mm in modes:
        lalsim.SimInspiralModeArrayActivateMode(ma, ell, mm)
    lalsim.SimInspiralWaveformParamsInsertModeArray(p["LALpars"], ma)

    # M = p["m1"] + p["m2"]
    p.update({"m1": p["m1"] * lal.MSUN_SI})
    p.update({"m2": p["m2"] * lal.MSUN_SI})

    hlms_lal = lalsim.SimInspiralChooseTDModes(**p)

    hlms = {}

    for ell, mm in modes:
        tmp = lalsim.SphHarmTimeSeriesGetMode(hlms_lal, ell, mm)
        if ell == 2 and mm == 2:
            length_22 = tmp.data.length
            dt_22 = tmp.deltaT
            epoch_22 = tmp.epoch
        hlms.update({(ell, mm): tmp.data.data})

    assert (
        p["deltaT"] == dt_22  # pyright: ignore
    ), f"input deltaT = {p['deltaT']} does not match waveform dt = {dt_22}."  # pyright: ignore

    t = np.arange(length_22) * dt_22 + float(epoch_22)  # pyright: ignore

    return t, hlms


def get_hdf5_strain(nr_hdf5_filename: str, modes: list[tuple[int, int]], dt: int | float) -> dict:
    """
    Load NR modes from a LAL compatible hdf5 file and return the output as a dictionary.
    The data is interpolated onto a time grid with spacing given by the input dt in units
    of M (total mass).

    Parameters
    ----------
    nr_hdf5_filename: str
        The path the the NR hdf5 file to load.
    modes: list[tuple[int,int]]
        List of modes to load. e.g. [(2,2), (2,-2), (2, 1), (2, -1), ...]
    dt: int | float
        The grid spacing for use for the output time array in units of M (total mass)

    Returns
    -------
    dict
        The output dict has the following keys:
            - t: npt.NDArray
                The times the waveform is defined at in units of M (total mass)
            - hlm:dict
                Contains time domain complex hlm modes. The keys are given by the
                input modes.
            - metadata:dict
                A dictionary that contains some of the NR metadata such as masses,
                spins and filename.
    """
    f = h5py.File(nr_hdf5_filename, "r")

    # eta = f.attrs["eta"]
    # this try/except is here because the GTech waveforms
    # use 'irreducible_mass1' instead of 'mass1'..
    try:
        q = float(f.attrs["mass1"]) / float(f.attrs["mass2"])
        Mtotal = float(f.attrs["mass1"]) + float(f.attrs["mass2"])
    except KeyError:
        q = float(f.attrs["irreducible_mass1"]) / float(f.attrs["irreducible_mass2"])
        Mtotal = float(f.attrs["irreducible_mass1"]) + float(f.attrs["irreducible_mass2"])

    # print((f.attrs.keys()))
    spin1z = f.attrs["spin1z"]
    spin2z = f.attrs["spin2z"]

    amp_x = {}
    amp_y = {}
    phase_x = {}
    phase_y = {}
    for lm in modes:
        amp_tmp = f["amp_l{0}_m{1}".format(lm[0], lm[1])]
        amp_x[lm] = amp_tmp["X"][()]
        amp_y[lm] = amp_tmp["Y"][()]

        phase_tmp = f["phase_l{0}_m{1}".format(lm[0], lm[1])]
        phase_x[lm] = phase_tmp["X"][()]
        phase_y[lm] = phase_tmp["Y"][()]

    f.close()

    t1 = max(amp_x[2, 2][0], phase_x[2, 2][0])
    t2 = min(amp_x[2, 2][-1], phase_x[2, 2][-1])

    times = np.arange(t1, t2, dt)

    hlm = {}
    for lm in modes:
        amp_i = IUS(amp_x[lm], amp_y[lm])
        phase_i = IUS(phase_x[lm], phase_y[lm])

        amp = amp_i(times)
        phase = phase_i(times)

        hlm[lm] = amp * np.exp(1.0j * phase)

    # TODO: output f.attrs as metadata
    metadata = {
        "q": q,
        "filename": nr_hdf5_filename,
        "M": Mtotal,
        "spin1z": spin1z,
        "spin2z": spin2z,
    }
    wf = dict(t=times, hlm=hlm, metadata=metadata)
    return wf


def generate_waveform(
    q: int | float,
    modes: list[tuple[int, int]],
    M: int | float = 50,
    f_min: int | float = 30,
    S1z: int | float = 0,
    S2z: int | float = 0,
    approximant: str = "SpinTaylorT1",
    deltaT: int | float = 1 / 4096,
    phiRef: int | float = 0,
    f_ref: int | float | None = None,
):
    """
    Main function to generate waveforms.
    Returns a dictionary with keys 't' and 'hlm' where
    'hlm' is a dictionary with keys (l,m).
    the time is in units of M. The hlm data are also normalised
    by the time domain scaling factor.

    Parameters
    ----------
    q: int | float
        The mass-ratio. We use the convention that q >= 1.
    modes: list[tuple[int, int]],
        list of [(l,m)] modes to include. E.g. [(2,2), (2,1), (3,3), ...]
    M: int | float, default 50
        total mass in solar masses
    f_min: int | float, default 30
        start frequency in Hz
    S1z: int | float, default 0
        Z component of body 1 spin
    S2z: int | float, default 0
        Z component of body 2 spin
    approximant: str, default "SpinTaylorT1"
        The name of the approximant. Usually the lalsimulation name.
        If either "SEOBNRv5HM" or "SEOBNRv5PHM" provided then this generated using
        pyseobnr.
    deltaT: int | float, default 1 / 4096
        The time spacing to generate the waveform at. Also the inverse sample rate.
    phiRef: int | float, default 0
        The reference phase. This can be defined differently depending on the approximant.
        But it typically should be the value of the 2,2 GW phase at the reference frequency.
    f_ref: int | float | None, default None
        The reference frequency in Hz. If None then this is set to f_min.


    Returns
    -------
    dict
        The output dict has the following keys:
            - t: npt.NDArray
                The times the waveform is defined at in units of M (total mass)
            - hlm : dict
                Contains time domain complex hlm modes. The keys are given by the
                input modes. The amplitude of the hlm data have been divided by the
                comman time domain amplitude scaling factor.
    """
    assert q >= 1, f"Input mass-ratio q is {q}. We use the convention that q >= 1"
    if f_ref is None:
        f_ref = f_min
    m1, m2 = phenom.m1_m2_M_q(M, q)
    p = gen_td_modes_wf_params(
        approximant=approximant,
        m1=m1,
        m2=m2,
        f_min=f_min,
        f_ref=f_ref,
        phiRef=phiRef,
        S1z=S1z,
        S2z=S2z,
        deltaT=deltaT,
    )

    if approximant in ["SEOBNRv5HM", "SEOBNRv5PHM"]:
        assert PYSEOBNR_AVAILABLE is True, "pyseobnr not installed"
        # pyseobnr
        p.update({"mode_array": modes})
        wfm_gen = pyseobnr.generate_waveform.GenerateWaveform(p)
        # Generate mode dictionary
        t, hlm = wfm_gen.generate_td_modes()
        # convert Mpc to metres
        r = p["distance"] * lal.PC_SI * 1e6
    else:
        # lalsuite
        t, hlm = gen_td_modes_wf(p, modes=modes)
        r = p["r"]

    amp_scale = td_amp_scale(M, r)  # pyright: ignore
    for lm in hlm.keys():
        hlm[lm] = hlm[lm] / amp_scale
    t_M = phenom.StoM(t, M)
    wf = dict(t=t_M, hlm=hlm)
    return wf
