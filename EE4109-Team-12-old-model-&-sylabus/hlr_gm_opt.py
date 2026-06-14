import SLiCAP as sl
import sympy as sp
import pprint as pp

import sys
sys.setrecursionlimit(10000)

import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import quad

from hlr_specs import global_specs, A1specs
from hlr_source_noise import DIN_A

from pprint import pprint




sl.htmlPage('Transconductance Optimization')
sl.specs2html(A1specs.getSpecs())
cir = sl.makeCircuit("A1_controller_noise_ciss_gm.cir")
sl.elementData2html(cir)
sl.params2html(cir)
sl.specs2circuit(A1specs.getSpecs(), cir)

f_min   = cir.getParValue('f_min')
f_max   = cir.getParValue('f_max')
V_noise = cir.getParValue('V_onoise')
n_SRC   = cir.getParValue('n_SRC')
n_Ri    = cir.getParValue('n_Ri')
sl.img2html('noise_ciss_gm.svg', 700)
pprint(vars(A1specs))
## Selection of input stage type MOS type
# Input NMOS or PMOS CS input stage
mosType = False
while not mosType:
    mosType = input("Please select N or P type input CS stage:\n>>> ").upper()
    if mosType != "N" and mosType != "P":
        mosType = False
if mosType == "N":
    # C18 library global params already imported via .lib C18.lib in .cir file
    cir.defPar("n", "N_s_N18")
    cir.defPar("C_OX", "C_OX_N18")
    cir.defPar("KF", "KF_N18")
    cir.defPar("AF", "AF_N18")
    fT_peak = 50e9
elif mosType == "P":
    # C18 library global params already imported via .lib C18.lib in .cir file
    cir.defPar("n", "N_s_P18")
    cir.defPar("C_OX", "C_OX_P18")
    cir.defPar("KF", "KF_P18")
    cir.defPar("AF", "AF_P18")
    fT_peak = 10e9

## Budgeting of input stage noise contribution

n_M = 0
while n_M > 1-n_SRC - n_Ri or n_M <= 0:
    try:
        n_M = float(input("\nAssign a relative budget for the contribution " +
                          "of the noise of the controller %sMOS input "%(mosType) +
                          "stage to the squared DIN-A weighted RMS output " +
                          "noise (> 0 and < %s):\n>>> "%(sp.N(1 - n_SRC - n_Ri , 3))))
    except ValueError:
        n_M=0
N_required  = V_noise**2 * (n_M + n_SRC + n_Ri)
sl.eqn2html("N_required", N_required, units="V^2")

## Calculation of the unweighted output noise spectrum and variance
# print cir data
sl.head2html("Controller Noise Circuit")
sl.elementData2html(cir)
sl.params2html(cir)
noiseResult = sl.doNoise(cir, pardefs="circuit")
S_onoise    = noiseResult.onoise
sl.eqn2html("S_onoise", sp.N(S_onoise, 4), units="V^2/Hz")

# The variance of the output voltage is obtained after integration 
# over the frequency range of interest. It is a function of $g_m$ and $c_{iss}$:

onoiseVar   = sl.rmsNoise(noiseResult, 'onoise', f_min, f_max)**2
sl.eqn2html("N_obtained", sp.N(onoiseVar, 4), units="V^2")

## Determination of show-stopper values
# Expressing $N_{obtained}$ in the process cut-off frequency $f_T$, 
# shows that the lowest noie is obtaine at the peak $f_T$ of the process:

## Calculation of optimum values
# Valid combinations of $g_m$ and $c_{iss}$ for which $N_{obtained}=N_{required}$ 
# are found from solving $g_m$ from
# $N_{obtained}-N_{required}=0$:


g_m   = sp.Symbol("g_m")
c_iss = sp.Symbol("c_iss")
f_T   = sp.Symbol("f_T")
onoiseVar_fT = onoiseVar.subs(g_m, 2*sp.pi*f_T*c_iss)
sl.eqn2html("N_obtained", sp.N(onoiseVar_fT, 4), units="V^2")

# For the selected MOS type we have:
sl.eqn2html("f_Tmax", fT_peak, units="Hz")

# With this value we obtain:
onoiseVar_fTpeak = onoiseVar_fT.subs(f_T, fT_peak)
sl.eqn2html("N_obtained", sp.N(onoiseVar_fTpeak, 4), units="V^2")

# This expression has a minimum for:
_ciss_solutions = sp.solve(sp.diff(onoiseVar_fTpeak, c_iss))
c_iss_best = None
for _sol in _ciss_solutions:
    _val = complex(sp.N(_sol))
    if _val.real > 0 and abs(_val.imag) < 1e-6 * max(abs(_val.real), 1e-30):
        if c_iss_best is None or _val.real > c_iss_best:
            c_iss_best = _val.real
c_iss_best = float(c_iss_best)
sl.eqn2html("c_iss_Opt", sp.N(c_iss_best, 4), units="F")

## Calculation of optimum values
# Valid combinations of $g_m$ and $c_{iss}$ for which $N_{obtained}=N_{required}$ are found from solving $g_m$ from
# $N_{obtained}-N_{required}=0$:
onoiseVar = sl.assumePosParams(onoiseVar)
g_m       = sp.Symbol('g_m', positive = True)
gm_ciss   = sp.solve(onoiseVar - N_required, g_m)[0]
sl.eqn2html("gm_ciss", sp.N(gm_ciss, 4), units="S")

# The denominator of this expression must be positive. This yields a minimum value for $c_{iss}$:
num, den     = gm_ciss.as_numer_denom()
ciss_min     = float(sp.solve(den)[0])
sl.eqn2html("c_issMin", sp.N(ciss_min, 4), units="F")

# The optimum value for the lowest $g_m$ == lowest current consumption is found at a much larger value of $c_{iss}$. This can be seen from the plot!
gm_ciss_func = sp.lambdify(sp.Symbol("c_iss"), gm_ciss)
ciss_num     = np.geomspace(ciss_min * 1.1, c_iss_best/10, 500)
gm_func_ciss = gm_ciss_func(ciss_num)
trc          = sl.trace([ciss_num, gm_func_ciss])
trc.label    = "gm_ciss"
sl.plot("gm_ciss", "Required $g_m$ versus $c_{iss}$", "log", {"gm_ciss": trc}, show=False, xScale="p", xUnits="F", yUnits="S")
sl.img2html("gm_ciss.svg", width=700)

# The minimum value of $g_m$ is found from solving the derivative of gm_ciss for $c_{iss} > c_{issMin}$. We will determine the derivative symbolically and solve it for $c_{iss}$ numerically:
c_iss                = sp.Symbol('c_iss', positive = True)
diff_gm_ciss         = sp.diff(gm_ciss, c_iss)
func_diff_gm_ciss    = sp.lambdify(c_iss, diff_gm_ciss)
ciss_gm_min          = fsolve(func_diff_gm_ciss, float(ciss_min) + 1e-15)[0]
gm_min               = gm_ciss.subs(c_iss, ciss_gm_min)
sl.eqn2html("g_mMin", sp.N(gm_min, 4), units="S")

## Solution for minimum costs
# The product of $c_{iss}$ and $g_m$ can be taken as a measure for the costs: 
# the product of the current consumtion and the area. We obtain minimum cost when $c_{iss}=c_{issMinCosts}$ satisfies $\frac{d\,g_m c_{iss}}{d\,c_{iss}} = 0$. The corresponsing value of $g_{mMinCosts}$ is obtained after substitution of $c_{issMinCosts}$ in $gm_{ciss}$:

costs                = gm_ciss * c_iss
diff_costs_ciss      = sp.diff(costs, c_iss)
func_diff_costs_ciss = sp.lambdify(c_iss, diff_costs_ciss)
ciss_costs_min       = fsolve(func_diff_costs_ciss, float(ciss_min) + 1e-15)[0]
gm_costs_min         = gm_ciss.subs(c_iss, ciss_costs_min)
sl.eqn2html("c_issMinCosts", sp.N(ciss_costs_min, 4), units="F")

sl.eqn2html("g_mMinCosts", sp.N(gm_costs_min, 4), units="S")

## Calculation of the weighted variance at minimum costs
# After substitution of the optimum cost values for $c_{iss}$ and $g_m$, 
# in the expression for the output noise voltage spectrum ([11]), we hsve the output variance 
S_onoise     = sl.assumePosParams(S_onoise)
S_weighted   = S_onoise.subs({c_iss: ciss_costs_min, g_m: gm_costs_min}) * DIN_A**2
S_weighted_f = sp.lambdify(sl.ini.frequency, S_weighted)
N_weighted   = quad(S_weighted_f, f_min, f_max)[0]

## Correction for DIN-A weighting
# We will adjust the requirement and re-run the above instructions until the DIN-A weighted 
# noise equals the initial requirement.
correction = N_required/N_weighted
sl.eqn2html("correction", sp.N(correction, 4))

N_corrected = correction * N_required
while np.abs(1 - correction) > 0.001:
    gm_ciss              = sp.solve(onoiseVar - N_corrected, g_m)[0]
    costs                = gm_ciss * c_iss
    diff_costs_ciss      = sp.diff(costs, c_iss)
    func_diff_costs_ciss = sp.lambdify(c_iss, diff_costs_ciss)
    ciss_costs_min       = fsolve(func_diff_costs_ciss, float(ciss_min) + 1e-15)[0]
    gm_costs_min         = gm_ciss.subs(c_iss, ciss_costs_min)
    S_weighted           = S_onoise.subs({c_iss: ciss_costs_min, g_m: gm_costs_min}) * DIN_A**2
    S_weighted_f         = sp.lambdify(sl.ini.frequency, S_weighted)
    N_weighted           = quad(S_weighted_f, f_min, f_max)[0]
    correction           = N_required/N_weighted
    N_corrected          = correction * N_required
    print(correction)

## Summary of results
print("\n%sMOS design results:\n--------------------"%(mosType))
print("RMS DIN A weighted required :", sp.N(sp.sqrt(N_required), 4), 'V')
print("RMS DIN A weighted obtained :", sp.N(sp.sqrt(N_weighted), 4), 'V')
print("DIN A RMS correction factor :", sp.N(correction, 4))
print("Selected value of c_iss MOS :", sp.N(ciss_costs_min, 4), 'F')
print("Required value of g_m MOS   :", sp.N(gm_costs_min, 4), 'S')


A1specs.append("n_M%s" % (mosType), "Relative contribution controller %sMOS input stage noise to the squared DIN-A weighted RMS output noise" % (mosType), n_M, "", "budgets")
A1specs.append("c_iss%s" % (mosType), "Selected input capacitance %sMOS" % (mosType), ciss_costs_min, "F", "design")
A1specs.append("g_m%s" % (mosType), "Selected transconductance input stage %sMOS" % (mosType), gm_costs_min, "S", "design")
A1specs.append("g_m_min%s" % (mosType), "Minimum transconductance input stage %sMOS" % (mosType), gm_min, "S", "design")
A1specs.append("c_iss_g_m_min%s" % (mosType), "Required c_issN at g_m_min%s" % (mosType), ciss_gm_min, "F", "design")
A1specs.append("c_iss_costs_min%s" % (mosType), "Required c_iss %sMOS for minimum costs" % (mosType), ciss_costs_min, "F", "design")
A1specs.append("g_m_costs_min%s" % (mosType), "g_m %sMOS for minimum costs" % (mosType), gm_costs_min, "S", "design")
A1specs.append("V_onoise_gmCiss%s" % (mosType), "DIN A weighted RMS output noise with %sMOS and selected g_m and c_iss" % (mosType), sp.sqrt(N_weighted), "V", "achievements")

sl.specs2html(A1specs.getSpecs())