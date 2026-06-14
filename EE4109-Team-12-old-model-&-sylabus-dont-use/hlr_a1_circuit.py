import SLiCAP as sl
import sympy as sp
from time import time

import numpy as np
from scipy.integrate import quad

from numpy import geomspace
from SLiCAP import trace, plot, float2rational, initProject, head2html, htmlPage, text2html
from sympy import Symbol, lambdify, sqrt

from hlr_specs import global_specs, A1specs


# A1 amplifier Design
fileName = "kicad/nullorcir/A1_design.kicad_sch"
cir = sl.makeCircuit(fileName, imgWidth = 800)
sl.elementData2html(cir)
sl.params2html(cir)
# sl.img2html("A1-design.svg", width = 800)
head2html("Design Equation for Integration Capacitor $C_i$")
Ci_eq = 1/ ((sp.Symbol('(R_i + R_s)', positive = True)) * sp.Symbol('62.4e3'))
sl.eqn2html(sp.Symbol('C_i', positive = True), Ci_eq, label = 'CC1', labelText = 'Design equation for $C_i$')

# In order to calculate the Ri and Ci of the feedback network, we make noise budget


htmlPage('Noise Specifications')
# Specifications A1
tau_i           = 1/6.24e4    # A1 integration time constant
f_min           = 600      # Low 3dB cut off frequency
f_max           = 6000     # High 3dB cut-off frequency
f_ref           = 1000     # Reference frequency for receive coil sensitivity
f_fp            = 5000     # Max. full-power frequency
Vi_ADC          = 0.9      # Peak-peak input voltage ADC
SPLref          = 20E-6    # 0dB SPL level in Pa
mic_dB_Pa       = -35.5    # microphone sensitivity in dBV/Pa
SPL_noise       = 30       # Allowed SPL noise level
SPL_max         = 110      # Max sound pressure level
SPL_ref         = 90       # dB/(A/m) inductive loop reference
SPL_sens        = -60.2    # dBV/(A/m) receive coil sensitivity at f_ref with termination
V_noise         = 20E-6 * 10**((mic_dB_Pa + SPL_noise)/20)
Rs              = 875      # Source reistance
Ls              = 0.12     # Source inductance
F_crest         = 3        # Signal crest factor
Vi_pp           = 2 * F_crest * 10**((SPL_sens + SPL_max - SPL_ref)/20)*f_fp/f_ref
P_max           = 1e-3     # Maximum power dissipation at maximum supply voltage 
V_DD            = 0.9      # Maximum supply voltage   


# source electrical specification

# Performance specifications
A1specs.append("L_s", "Source inductance", Ls, "H", "performance")
A1specs.append("R_s", "Source resistance", Rs, "Omega", "performance")
A1specs.append("R_t", "Termination resistance", 10e3, "Omega", "performance")

# Source signal specification
A1specs.append("Vi_pp", "Maximum peak-peak input voltage", Vi_pp, "", "performance")
A1specs.append("f_fp", "Maximum full-power frequency", f_fp, "Hz", "performance")

# Performance requirements (Range, Bandwidth, Resolution)
A1specs.append("tau_i", "Integration time constant", tau_i, "s", "performance")
A1specs.append("f_min", "-3dB high-pass cut-off frequency", f_min, "Hz", "performance")
A1specs.append("f_max", "-3dB low-pass cut-off frequency", f_max, "Hz", "performance")
A1specs.append("V_onoise", "DIN A weighted output voltage noise", V_noise, "V", "performance")
A1specs.append("Vi_ADC", "Peak-peak input voltage ADC", Vi_ADC, "V", "performance")
A1specs.append("P_max", "Maximum power dissipation at maximum supply voltage", P_max, "W", "performance")
A1specs.append("V_DD", "Maximum supply voltage", V_DD, "V", "performance")

sl.specs2html(A1specs.getSpecs())

# Performance specifications
A1specs.append("C_s", "Source capacitance", 1 / (0.12 * 4 * (np.pi**2) * (150e3**2)), "F", "performance")


