"""
This module uses e.g. EOB to produce the inspiral (l,m) = (2,2) phase phi_eob_22
which we use as the orbital phase phi_eob_orb = phi_eob_22 / 2
and plug this into the PN complex amplitude modes for non-spinning
systems from Blanchet.

I'm doing this because the LALSimulation version of TaylorTx and SpinTaylorTx
are confusing.

up to 3PN Non-spinning PN amplitudes from Blanchet+ 2008: https://arxiv.org/abs/0802.1249

3.5PN Non-spinning PN amplitude: https://arxiv.org/pdf/1210.2339.pdf
4PN Non-spinning PN amplitude: https://arxiv.org/pdf/2304.11185.pdf


aligned spin terms from [Mike Boyle's
code](https://github.com/moble/PostNewtonian.jl/
blob/7c0a86b573fb4be88ad82637bf2c805ad9a96d04/src/pn_expressions/mode_weights.jl)

"""

import numpy as np
import phenom
from lal import GAMMA
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

from prim.waveform_generator import generate_waveform


def pn_x_fn(orbital_angular_frequency):
    """
    eq 6.5 https://arxiv.org/abs/0802.1249

    x = omega_orb**(2/3)

    although this only approximately the orbital phase.
    more precisely this input to this function is
    the angular frequency of the 22 mode divided by 2
    which we use to approximate the orbital angular frequency.

    see https://arxiv.org/abs/2304.11185 where they talk about
    the GW half-phase psi = phi - log.
    The difference between psi and phi are due to GW tails.
    """
    return orbital_angular_frequency ** (2 / 3)


def delta_fn(eta):
    """
    page 29 https://arxiv.org/abs/0802.1249
    delta = (m_1 - m_2) / (m_1 + m_2)
    delta is either +/- sqrt(1 - 4*eta)
    which depends on the sign of (m_1 - m_2).

    we use the convention that m_1 >= m_2 i.e. m_1 is the primary mass
    so (m_1 - m_2) is positive
    """
    return np.sqrt(1 - 4 * eta)


def get_spin_variables(eta, chi1, chi2):
    """
    variables for spin, assuming M = 1 and m1 >= m2

    Parameters
    ----------
    eta
    chi1
    chi2

    Returns
    -------
    S
        total spin
    Sigma
        spin difference
    delta
        asymmetric mass-ratio
    S0plus
        S0plus spin combination
    S0minus
        S0minus spin combination
    """
    delta = delta_fn(eta)
    m1 = (1 + delta) / 2
    m2 = (1 - delta) / 2
    S1 = chi1 * m1**2
    S2 = chi2 * m2**2
    S = S1 + S2
    Sigma = S2 / m2 - S1 / m1
    S0plus = m1 * chi1 + m2 * chi2
    S0minus = S0plus
    return S, Sigma, delta, S0plus, S0minus


def generate_spliced_pn_waveform(
    q,
    modes=None,
    M=50,
    f_min=30,
    S1z=0,
    S2z=0,
    approximant="SEOBNRv4HM_PA",  # pyright: ignore
    deltaT=1 / 4096,
):
    """
    this generates the 22 mode phase from the given `approximant` model which is SEOBNRv4PHM by
    default. We use this to estimate the orbital phase as phi_orb = phi_22/2. phi_orb is then used
    in the PN amplitude expressions.

    we also compute the post-newtonian parameter `x` from the frequency.
    """
    available_modes = [
        (2, 2),
        (2, 1),
        (2, 0),
        (3, 3),
        (3, 2),
        (3, 0),
        (4, 4),
        (4, 3),
        (5, 5),
        (5, 4),
    ]
    if modes is None:
        modes = available_modes
    for mode in modes:
        assert (
            mode in available_modes
        ), f"{mode} mode not available, available modes are {available_modes}"
    eta = phenom.eta_from_q(q)

    wf = generate_waveform(
        q,
        [(2, 2)],
        M,
        f_min,
        S1z,
        S2z,
        approximant,
        deltaT,
    )
    t_M = wf["t"].copy()

    # get half GW phase (phi_22) - used in PN modes
    # note the minus sign for convention reasons
    phi_22 = -np.unwrap(np.angle(wf["hlm"][2, 2]))
    # and then divide by 2 which we estiamte to be the orbital phase
    phi_orb = phi_22 / 2
    # interpolate and computer derivative to get estimate for orbital angular frequency
    orbital_angular_frequency = IUS(wf["t"], phi_orb).derivative()(wf["t"])

    # push PN up to the peak of the EOB data.
    # we expect the PN modes to become inaccurate before this point.
    mask = wf["t"] < 0
    t_M = t_M[mask]
    phi_orb = phi_orb[mask]
    orbital_angular_frequency = orbital_angular_frequency[mask]

    # use omega here because of sign convention: used in PN modes
    x = pn_x_fn(orbital_angular_frequency)

    pn_hlm = {}

    pn_mode_funcs = {
        (2, 2): pn_h_22,
        (2, 1): pn_h_21,
        (2, 0): pn_h_20,
        (3, 3): pn_h_33,
        (3, 2): pn_h_32,
        (3, 1): pn_h_31,
        (3, 0): pn_h_30,
        (4, 4): pn_h_44,
        (4, 3): pn_h_43,
        (5, 5): pn_h_55,
        (5, 4): pn_h_54,
    }

    for mode in modes:
        pn_hlm[mode] = pn_mode_funcs[mode](x, eta, phi_orb, S1z, S2z)

    wf_pn = dict(t=t_M, hlm=pn_hlm)

    return wf_pn


def pn_h_pre_factor(eta, x):
    """
    e.g 9.3a https://arxiv.org/abs/0802.1249
    """
    return 2 * eta * x


def psi_fn(phi, x, x0=1):
    """
    e.g. eq. 8.8 in https://arxiv.org/abs/0802.1249
    or eq. 16 in https://arxiv.org/abs/1210.2339
    or eq 7 in https://arxiv.org/abs/2304.11185
    """
    return phi - 3 * x ** (3 / 2) * np.log(x / x0)


def pn_h_22(x, eta, phi, chi1, chi2):
    """
    Compute the PN (l,m) = (2,2) multipole amplitude.
    We assume the total mass is 1.

    3PN Non-spinning PN hlm: https://arxiv.org/abs/0802.1249
    3.5PN Non-spinning PN hlm: https://arxiv.org/abs/1210.2339
    4PN Non-spinning PN hlm: https://arxiv.org/abs/2304.11185

    1.5PN and 2PN aligned spin terms from [Mike Boyle's
      code](https://github.com/moble/PostNewtonian.jl/
      blob/7c0a86b573fb4be88ad82637bf2c805ad9a96d04/src/pn_expressions/mode_weights.jl)

    Parameters
    ----------
    x
        post-newtonian parameter related to orbital frequency
    eta
        symmetric mass ratio
    phi
        orbital phase
    chi1
        dimensionless aligned spin of primary black hole
    chi2
        dimensionless aligned spin of secondary black hole


    Returns
    -------
    complex array
    """
    mm = 2

    S, Sigma, delta, S0plus, S0minus = get_spin_variables(eta, chi1, chi2)

    # 0pn: x**0
    hatHlm_0PN = 1
    # 1pn: x
    hatHlm_1PN = (-107 / 42) + (55 * eta / 42)
    # 1.5pn: x**(3/2)
    hatHlm_1_5PN_non_spin = 2 * np.pi
    hatHlm_1_5PN_spin = -2 * S + 2.0 / 3.0 * Sigma * delta
    hatHlm_1_5PN = hatHlm_1_5PN_non_spin + hatHlm_1_5PN_spin
    # 2pn: x**2
    hatHlm_2PN_non_spin = (-2173 / 1512) - (1069 * eta / 216) + (2047 * eta**2 / 1512)
    hatHlm_2PN_spin = S0plus * S0minus
    hatHlm_2PN = hatHlm_2PN_non_spin + hatHlm_2PN_spin
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = (-107 * np.pi / 21) - 24 * 1.0j * eta + (34 * np.pi * eta / 21)
    # 3pn: x**3
    hatHlm_3PN = (
        (27027409 / 646800)
        - (856 * GAMMA / 105)
        + (428 * 1.0j * np.pi / 105)
        + (2 * np.pi**2 / 3)
        + (-(278185 / 33264) + (41 * np.pi**2 / 96)) * eta
        - (20261 * eta**2 / 2772)
        + (114635 * eta**3 / 99792)
        - (428 / 105) * np.log(16 * x)
    )
    # 3.5pn: x**(7/2)
    hatHlm_3_5PN = (
        -2173 * np.pi / 756
        + (-2495 * eta / 378 + 14333 * 1.0j / 162) * eta
        + (40 * np.pi / 27 - 4066 * 1.0j / 945) * eta**2
    )
    # 4pn: x**4
    hatHlm_4PN = (
        -846557506853 / 12713500800
        + 45796 / 2205 * GAMMA
        - 22898 * 1.0j * np.pi / 2205
        - 107 * np.pi**2 / 63
        + 22898 / 2205 * np.log(16 * x)
        + (
            -336005827477 / 4237833600
            + 15284 / 441 * GAMMA
            - 219314 * 1.0j * np.pi / 2205
            - 9755 * np.pi**2 / 32256
            + 7642 * np.log(16 * x) / 441
        )
        * eta
        + (256450291 / 7413120 - 1025 * np.pi**2 / 1008) * eta**2
        - 81579187 / 15567552 * eta**3
        + 26251249 / 31135104 * eta**4
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += hatHlm_0PN
    hatHlm += x * hatHlm_1PN
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x**3 * hatHlm_3PN
    hatHlm += x ** (7 / 2) * hatHlm_3_5PN
    hatHlm += x**4 * hatHlm_4PN

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_21(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249
    """
    mm = 1

    S, Sigma, delta, _, _ = get_spin_variables(eta, chi1, chi2)

    # eq 9.4b https://arxiv.org/abs/0802.1249 For the non-spinning terms we do factor out this
    # pre-factor.
    pre_factor = 1 / 3 * 1.0j * delta
    # For the spinning terms we divide by the pre_factor because the expression for the spin terms
    # comes from MBs code and he doesn't factor out this pre-factor.

    # 0.5pn: x**(1/2)
    hatHlm_0_5PN = 1
    # 1pn: x
    hatHlm_1PN_spin = 1.0j / 2.0 * Sigma
    hatHlm_1PN = hatHlm_1PN_spin / pre_factor
    # 1.5pn: x**(3/2)
    hatHlm_1_5PN = -(17 / 28) + (5 * eta / 7)
    # 2pn: x**2
    hatHlm_2PN_non_spin = np.pi + 1.0j * (-0.5 - 2 * np.log(2))
    hatHlm_2PN_spin = 1.0j / 42 * (-86 * S * delta + Sigma * (139 * eta - 79))
    hatHlm_2PN = hatHlm_2PN_non_spin + hatHlm_2PN_spin / pre_factor
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = -(43 / 126) - (509 * eta / 126) + (79 * eta**2 / 168)
    # 3pn: x**3
    hatHlm_3PN = (
        -(17 * np.pi / 28)
        + (3 * np.pi * eta / 14)
        + 1.0j * (17 / 56 + eta * (-(353 / 28) - (3 * np.log(2) / 7)) + (17 * np.log(2) / 14))
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x ** (1 / 2) * hatHlm_0_5PN
    hatHlm += x * hatHlm_1PN
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_20(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249

    chi1, chi2 not used but kept for interface consistency
    """
    mm = 0
    hatHlm = -5 / (14 * np.sqrt(6))

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)
    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_33(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249
    """
    mm = 3

    S, Sigma, delta, _, _ = get_spin_variables(eta, chi1, chi2)

    pre_factor = -0.75 * 1.0j * np.sqrt(15 / 14) * delta

    # similarly for the 21 mode we divide the spinning terms
    # by pre_factor. See 21 mode for details.

    # 0.5pn: x**(1/2)
    hatHlm_0_5PN = 1
    # 1.5pn: x**(3/2)
    hatHlm_1_5PN = -4 + 2 * eta
    # 2pn: x**2
    hatHlm_2PN_non_spin = 3 * np.pi + 1.0j * (-21 / 5 + 6 * np.log(3 / 2))
    hatHlm_2PN_spin = 3.0j / 112 * np.sqrt(210) * (7 * S * delta - 3 * Sigma * (3 * eta - 1))
    hatHlm_2PN = hatHlm_2PN_non_spin + hatHlm_2PN_spin / pre_factor
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = 123 / 110 - 1838 * eta / 165 + 887 * eta**2 / 330
    # 3pn: x**3
    hatHlm_3PN = (
        -12 * np.pi
        + 9 * np.pi * eta / 2
        + 1.0j * (84 / 5 - 24 * np.log(3 / 2) + eta * (-48103 / 1215 + 9 * np.log(3 / 2)))
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x ** (1 / 2) * hatHlm_0_5PN
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_32(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249
    """
    mm = 2

    S, Sigma, delta, _, _ = get_spin_variables(eta, chi1, chi2)
    pre_factor = 1 / 3 * np.sqrt(5 / 7)

    # similarly for the 21 mode we divide the spinning terms
    # by pre_factor. See 21 mode for details.

    # 1pn: x
    hatHlm_1PN = 1 - 3 * eta
    # 1.5pn: x**(3/2)
    hatHlm_1_5PN_spin = 2 * np.sqrt(35) / 21 * (S + Sigma * delta)
    hatHlm_1_5PN = hatHlm_1_5PN_spin / pre_factor
    # 2pn: x**2
    hatHlm_2PN = -193 / 90 + 145 * eta / 18 - 73 * eta**2 / 18
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = 2 * np.pi - 6 * np.pi * eta + 1.0j * (-3 + 66 * eta / 5)
    # 3pn: x**3
    hatHlm_3PN = -1451 / 3960 - 17387 * eta / 3960 + 5557 * eta**2 / 220 - 5341 * eta**3 / 1320

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x * hatHlm_1PN
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_31(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249

    chi1, chi2 not used but kept for interface consistency
    """
    mm = 1
    delta = delta_fn(eta)
    pre_factor = 1.0j * delta / (12 * np.sqrt(14))

    # 0.5pn: x**(1/2)
    hatHlm_0_5PN = 1
    # 1.5pn: x**(3/2)
    hatHlm_1_5PN = -8 / 3 - 2 * eta / 3
    # 2pn: x**2
    hatHlm_2PN = np.pi + 1.0j * (-7 / 5 - 2 * np.log(2))
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = 607 / 198 - 136 * eta / 99 - 247 * eta**2 / 198
    # 3pn: x**3
    hatHlm_3PN = (
        -8 * np.pi / 3
        - 7 * np.pi * eta / 6
        + 1.0j * (56 / 15 + 16 * np.log(2) / 3 + eta * (-1 / 15 + 7 * np.log(2) / 3))
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x ** (1 / 2) * hatHlm_0_5PN
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_30(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249

    chi1, chi2 not used but kept for interface consistency
    """
    mm = 0

    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = -2 / 5 * 1.0j * np.sqrt(6 / 7) * eta

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_44(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249

    chi1, chi2 not used but kept for interface consistency
    """
    mm = 4
    # delta = delta_fn(eta)
    pre_factor = -8 / 9 * np.sqrt(5 / 7)

    # 1pn: x
    hatHlm_1PN = 1 - 3 * eta
    # 2pn: x**2
    hatHlm_2PN = -593 / 110 + 1273 * eta / 66 - 175 * eta**2 / 22
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = (
        4 * np.pi
        - 12 * np.pi * eta
        + 1.0j * (-42 / 5 + eta * (1193 / 40 - 24 * np.log(2)) + 8 * np.log(2))
    )
    # 3pn: x**3
    hatHlm_3PN = (
        1068671 / 200200 - 1088119 * eta / 28600 + 146879 * eta**2 / 2340 - 226097 * eta**3 / 17160
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x * hatHlm_1PN
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_43(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249
    """
    mm = 3

    S, Sigma, delta, _, _ = get_spin_variables(eta, chi1, chi2)

    pre_factor = -9 * 1.0j * delta / (4 * np.sqrt(70))

    # similarly for the 21 mode we divide the spinning terms
    # by pre_factor. See 21 mode for details.

    # 1.5pn: x**(3/2)
    hatHlm_1_5PN = 1 - 2 * eta
    # 2pn: x**(2)
    hatHlm_2PN_spin = 9.0j * np.sqrt(70) / 112 * (-S * delta + 3 * Sigma * eta - Sigma)
    hatHlm_2PN = hatHlm_2PN_spin / pre_factor
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = -39 / 11 + 1267 * eta / 132 - 131 * eta**2 / 33
    # 3pn: x**3
    hatHlm_3PN = (
        3 * np.pi
        - 6 * np.pi * eta
        + 1.0j * (-32 / 5 + eta * (16301 / 810 - 12 * np.log(3 / 2)) + 6 * np.log(3 / 2))
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x ** (2) * hatHlm_2PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_55(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249

    chi1, chi2 not used but kept for interface consistency
    """
    mm = 5
    delta = delta_fn(eta)
    pre_factor = 625 * 1.0j * delta / (96 * np.sqrt(66))

    # 1.5pn: x**(3/2)
    hatHlm_1_5PN = 1 - 2 * eta
    # 2.5pn: x**(5/2)
    hatHlm_2_5PN = -263 / 39 + 688 * eta / 39 - 256 * eta**2 / 39
    # 3pn: x**3
    hatHlm_3PN = (
        5 * np.pi
        - 10 * np.pi * eta
        + 1.0j * (-181 / 14 + eta * (105834 / 3125 - 20 * np.log(5 / 2) + 10 * np.log(5 / 2)))
    )

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x ** (3 / 2) * hatHlm_1_5PN
    hatHlm += x ** (5 / 2) * hatHlm_2_5PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm


def pn_h_54(x, eta, phi, chi1, chi2):
    """
    https://arxiv.org/abs/0802.1249

    chi1, chi2 not used but kept for interface consistency
    """
    mm = 4
    # delta = delta_fn(eta)
    pre_factor = -32 / (9 * np.sqrt(165))

    # 2pn: x**2
    hatHlm_2PN = 1 - 5 * eta * 5 * eta**2
    # 3pn: x**3
    hatHlm_3PN = -4451 / 910 + 3619 * eta / 130 - 521 * eta**2 / 13 + 339 * eta**3 / 26

    # initialise
    hatHlm = np.zeros(len(x), dtype=np.complex128)
    hatHlm += x**2 * hatHlm_2PN
    hatHlm += x ** (3) * hatHlm_3PN

    hatHlm *= pre_factor

    # psi = psi_fn(phi, x)
    # Hlm = np.sqrt(16*np.pi/5) * hatHlm * np.exp(-1.j*mm*psi)

    Hlm = np.sqrt(16 * np.pi / 5) * hatHlm * np.exp(-1.0j * mm * phi)

    return pn_h_pre_factor(eta, x) * Hlm
