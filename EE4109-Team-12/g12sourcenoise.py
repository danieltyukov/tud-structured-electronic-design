import SLiCAP as sl
import sympy as sp
import numpy as np

from SLiCAP import trace, plot, float2rational, initProject, head2html, htmlPage, text2html
from scipy.integrate import quad
from sympy import Symbol, lambdify, sqrt
from numpy import geomspace

from g12specifications import A1specs

cir2 = sl.makeCircuit("kicad/A1_R_noise_without_Ri.kicad_sch", imgWidth = 800)
sl.elementData2html(cir2)
sl.params2html(cir2)

sl.img2html("A1_R_noise_without_Ri.svg", width = 800)

# DIN_A
htmlPage('DIN A weighting curve')
print("Calculating DIN A weighting curve")

f            = Symbol("f")
DIN_A        = 12194**2*f**4/((f**2+20.6**2)*(f**2+12194**2)*sqrt((f**2+107.7**2)*(f**2+737.9**2)))
# normalized the weighting function w.r.t. 1kHz
DIN_A        = float2rational(DIN_A/DIN_A.subs(f,1000))

# Plot the DIN A weighting curve
x            = geomspace(20, 20000, num=200)
y            = lambdify(f,DIN_A)
tr           = trace([x, y(x)])
tr.label     = "DIN A"
DINA_plot    = plot("DINA", "DIN A normalized at 1kHz", 'log', {"DINA":tr}, xName='frequency', xUnits='Hz', yName='Weight', show=False)

sl.img2html("DINA.svg", width = 800)

htmlPage("Noise budget")
# Load circuit parameters from specifications


text2html('The noise budget is calculated by the following formula:')
print("Calculating noise budget")

sl.specs2html(A1specs.getSpecs())
sl.specs2circuit(A1specs.getSpecs(), cir2)
# sl.elementData2html(cir2)



noiseResult1 = sl.doNoise(cir2, pardefs="circuit")
S_onoise     = noiseResult1.onoise
sl.eqn2html("S_onoise", sp.N(S_onoise, 4), units = "V^2/Hz")


S_o_weighted = sp.simplify(DIN_A**2*S_onoise)
sl.eqn2html("S_o_weighted", sp.N(S_o_weighted, 4), units = "V^2/Hz")


f_min           = cir2.getParValue('f_min')
f_max           = cir2.getParValue('f_max')
V_noise         = cir2.getParValue('V_onoise')
f               = sl.ini.frequency
func_OnoiseVar  = sp.lambdify(f, S_o_weighted)
N_var_1_dinA    = quad(func_OnoiseVar, f_min, f_max)[0]
RMS_1           = np.sqrt(N_var_1_dinA)
n_SRC           = N_var_1_dinA/V_noise**2
sl.eqn2html("n_SRC", n_SRC, units = "")

A1specs.append("SRCnoise", "DIN A weighted RMS output noise, source + termination", RMS_1, "V", "design")
A1specs.append("n_SRC", "Relative contribution of source noise to the squared DIN-A weighted RMS output noise", n_SRC, "", "budgets")

sl.specs2html(A1specs.getSpecs(), types=["budgets", "design"])