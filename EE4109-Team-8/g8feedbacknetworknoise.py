import SLiCAP as sl
import sympy as sp
import numpy as np

from SLiCAP import trace, plot, float2rational, initProject, head2html, htmlPage, text2html
from scipy.integrate import quad

from g8sourcenoise import DIN_A
from g8specifications import A1specs

cir = sl.makeCircuit("kicad/A1_R_noise_with_Ri.kicad_sch")
sl.img2html("A1_R_noise_with_Ri.svg", 500)

sl.specs2circuit(A1specs.getSpecs(), cir)
R_i                 = sp.Symbol("R_i")
f_min               = cir.getParValue('f_min')
f_max               = cir.getParValue('f_max')
V_noise             = cir.getParValue('V_onoise')
tau_i               = cir.getParValue('tau_i')
f_fp                = cir.getParValue('f_fp')
Vi_ADC              = cir.getParValue('Vi_ADC')
n_SRC               = cir.getParValue('n_SRC')
SRCnoise            = cir.getParValue('SRCnoise')
P_max               = cir.getParValue('P_max')
V_DD                = cir.getParValue('V_DD')
C_s                 = cir.getParValue('C_s')
C_i                 = cir.getParValue('C_i')

noiseResult2 = sl.doNoise(cir, pardefs="circuit")
S_onoise     = noiseResult2.onoise

sl.eqn2html("S_onoise", sp.N(S_onoise, 4), units = "V^2/Hz")

n_Ri = 0
while n_Ri > 1 - n_SRC or n_Ri <= 0:
    try:
        n_Ri = float(input("\nPlease assign a budget for the relative contribution of " +
                           "the noise of the integrator resistance to the "+
                           "squared DIN-A weighted RMS output noise " +
                           "(> 0 and < %s):\n>>> "%(sp.N(1-n_SRC,3))))
    except ValueError:
        n_Ri = 0
sl.eqn2html("n_Ri", n_Ri, units = "")

N_var_required  = V_noise**2 * (n_Ri + n_SRC)
sl.eqn2html("N_var_required", sp.N(N_var_required, 4), units = "V^2/Hz")
RMS_2_sq        = sl.rmsNoise(noiseResult2, "onoise", f_min, f_max)**2
sl.eqn2html("RMS_2_sq", sp.N(RMS_2_sq, 4), units = "V^2/Hz")
try:
    Ri_max      = sp.solve(RMS_2_sq - N_var_required, R_i)[0]
except IndexError:
    i = 2
    Ri_max = 0
sl.eqn2html("Ri_max", sp.N(Ri_max, 4), units = "Ohm")


S_weighted      = sp.simplify(S_onoise.subs(R_i, Ri_max) * DIN_A**2)
sl.eqn2html("S_weighted", sp.N(S_weighted, 4), units = "V^2/Hz")

func_S_weighted = sp.lambdify(sl.ini.frequency, S_weighted)
N_var_obtained  = quad(func_S_weighted, f_min, f_max)[0]

sl.eqn2html("N_var_obtained", sp.N(N_var_obtained, 4), units = "V^2/Hz")

correction      = N_var_required/N_var_obtained
sl.eqn2html("correction", sp.N(correction, 4), units = "")

N_var_corrected = N_var_obtained
while np.abs(1-correction) > 0.001:
    Ri_max          = sp.solve(RMS_2_sq - N_var_corrected, R_i)[0]
    S_weighted      = S_onoise.subs(R_i, Ri_max) * DIN_A**2
    func_S_weighted = sp.lambdify(sl.ini.frequency, S_weighted)
    N_var_obtained  = quad(func_S_weighted, f_min, f_max)[0]
    correction = N_var_required/N_var_obtained
    N_var_corrected *= correction
    print(correction)
sl.eqn2html("Ri_max", sp.N(Ri_max, 4), units = "Ohm")

I_max     = P_max/2/V_DD
Ri_min    = V_DD/I_max
if Ri_max < Ri_min:
    print("Conflicting requirements between power dissipation and noise performance")
    conflict = True
else:
    print("Found no conflict between power dissipation and noise performance")
    conflict = False

Ri = 0
while Ri > Ri_max or Ri < Ri_min or conflict:
    try:
        Ri = float(input("\nPlease assign a value to the integrator resistance R_i " +
                         "(>= %sOhm, and <= %s Ohm):\n>>> "%(sp.N(Ri_min,5), sp.N(Ri_max,5))))
    except ValueError:
        Ri = 0
sl.eqn2html("R_i", sp.N(Ri, 4), units = "Ohm")


Ci = tau_i/(Ri + cir.getParValue('R_s'))
ZL_min          = sp.sqrt(Ri**2 + 1/(2*sp.pi*f_fp*Ci)**2)
IL_fb_max       = sp.N(Vi_ADC/ZL_min)

S_weighted      = S_onoise.subs(R_i, Ri) * DIN_A**2
func_S_weighted = sp.lambdify(sl.ini.frequency, S_weighted)
N_var_obtained  = quad(func_S_weighted, f_min, f_max)[0]
n_Ri_obtained   = (N_var_obtained - SRCnoise**2)/V_noise**2

A1specs.append("n_Ri", "Relative contribution of R_i noise to the squared DIN-A weighted RMS output noise", n_Ri, "", "budgets")
A1specs.append("Ri_max", "Max. value of integrator resistor", Ri_max, "Omega", "design")
A1specs.append("R_i", "Selected value of integrator resistor", Ri, "Omega", "design")
A1specs.append("Ri_min", "Min. value of integrator resistor", Ri_min, "Omega", "design")
A1specs.append("C_i", "Required value of integrator capacitor", Ci, "F", "design")
A1specs.append("I_fb", "Maximum peak-peak current through feedback network", IL_fb_max, "A", "design")
A1specs.append("S_Ri", "Squared DIN A weighted RMS output noise due to source and feedback network", N_var_obtained, "V^2/Hz", "design")
A1specs.append("n_Ri_obtained", "Relative contribution of source and feedback network to squared DIN A weighted output noise", n_Ri_obtained, "", "design")

sl.specs2html(A1specs.getSpecs(), types=["budgets", "design"])