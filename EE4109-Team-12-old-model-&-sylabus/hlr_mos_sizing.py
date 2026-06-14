import SLiCAP as sl
import sympy as sp
from scipy.integrate import quad

from hlr_specs import global_specs, A1specs
from hlr_source_noise import DIN_A

sl.htmlPage('Transistor Sizing')
sl.specs2html(A1specs.getSpecs())

mosType = False
while not mosType:
    mosType = input("Please select N or P type input CS stage:\n>>> ").upper()
    if mosType != "N" and mosType != "P":
        mosType = False
if mosType == "N":
    cir = sl.makeCircuit("A1_controller_noiseWLI_n.cir")
    img = "A1_controller_noiseWLI_n.svg"
elif mosType == "P":
    cir = sl.makeCircuit("A1_controller_noiseWLI_p.cir")
    img = "A1_controller_noiseWLI_p.svg"
sl.elementData2html(cir)
sl.params2html(cir)
sl.img2html(img, 600)


W_finger = 0
while W_finger < 0.18 or W_finger > 50:
    try:
        W_finger = float(input("MOS maximum finger width in [um] (>= 0.18 and <=50):\n>>> "))
    except ValueError:
        W_finger = 0
W_finger *= 1e-6


Le=0
while Le < 0.18:
    try:
        Le = float(input("MOS channel length in [um] (> 0.18):\n>>> "))
    except ValueError:
        Le=0
Le *= 1e-6

sl.specs2circuit(A1specs.getSpecs(), cir)
IC_old = cir.getParValue('IC_X1') # Store the symbolic definition of the inversion coefficient
ICinit = 1

correction = True
while correction:
    # Delete definitions from previous runs
    cir.delPar('IC_X1')
    cir.delPar('W')
    cir.delPar('L')
    cir.delPar('ID')
    IC_X1   = sp.Symbol('IC_X1')
    L       = sp.Symbol('L')
    x_X1    = sp.Symbol('x_X1')

    # Get c_iss as a function of W, L and IC
    ciss_IC  = cir.getParValue('c_iss_X1')
    ciss_W   = ciss_IC.subs({IC_X1: ICinit, L: Le})
    ciss     = cir.getParValue('c_iss%s'%(mosType))
    W        = sp.Symbol('W')

    width    = sp.solve(ciss_W-ciss)[0]

    # round to W_finger
    Mf       = int(width/W_finger)
    if Mf > 0:
        W_sel    = Mf*W_finger
    else:
        W_sel = width
        Mf = 1

    gm       = cir.getParValue('g_m_X1').subs({IC_X1: ICinit, L: Le})
    g_m      = cir.getParValue('g_m%s'%(mosType))
    ID       = sp.solve(gm-g_m)[0]

    # Check the inversion coefficient
    cir.defPar('IC_X1', IC_old)
    cir.defPar('W', W_sel)
    cir.defPar('L', Le)
    cir.defPar('ID', ID)
    IC = cir.getParValue('IC_X1')
    print("IC =", sp.N(IC,3))
    if sp.Abs(1-IC/ICinit) < 0.001:
        correction = False
    else:
        ICinit = IC

f_min          = cir.getParValue('f_min')
f_max          = cir.getParValue('f_max')
noiseResult    = sl.doNoise(cir, pardefs="circuit", numeric=True)
RMS_unweigted  = sl.rmsNoise(noiseResult, 'onoise', 200, 6000)
f              = sl.ini.frequency
func_OnoiseVar = sp.lambdify(f, sp.N(noiseResult.onoise * DIN_A**2))
N_var_dinA     = quad(func_OnoiseVar, f_min, f_max)[0]
RMS_dinA       = sp.sqrt(N_var_dinA)

print("%sMOS design results\n----------------------------"%(mosType))
print("RMS unweighted obtained     :", sp.N(RMS_unweigted, 3), 'V')
print("RMS DIN A weighted obtained :", sp.N(RMS_dinA, 3), 'V')
print("DIN A RMS correction factor :", sp.N(RMS_unweigted/RMS_dinA, 3))
print("Required value of c_iss     :", sp.N(cir.getParValue('c_iss%s'%(mosType)), 3), 'F')
print("Obtained value of c_iss     :", sp.N(cir.getParValue('c_iss_X1'), 3), 'F')
print("Required value of g_m       :", sp.N(cir.getParValue('g_m%s'%(mosType)), 3), 'S')
print("Obtained value of g_m       :", sp.N(cir.getParValue('g_m_X1'), 3), 'S')
print("Selected value of L         :", sp.N(cir.getParValue('L')*1e6, 3), 'um')
print("Obtained value of W         :", sp.N(cir.getParValue('W')*1e3, 3), 'mm')
print("Obtained value of M         :", sp.N(Mf, 3))
print("Selected max. finger width  :", sp.N(W_finger*1e6, 3), "um")
print("Obtained value of ID        :", sp.N(cir.getParValue('ID')*1e6, 3), 'uA')
print("Obtained value of IC        :", sp.N(cir.getParValue('IC_X1'), 3))


A1specs.append("W_%s" % (mosType), "Selected width input stage %sMOS" % (mosType), sp.N(cir.getParValue('W')), "m", "design")
A1specs.append("L_%s" % (mosType), "Selected length input stage %sMOS" % (mosType), sp.N(cir.getParValue('L')), "m", "design")
A1specs.append("g_m_%s_o" % (mosType), "Obtained transconductance input stage %sMOS" % (mosType), sp.N(cir.getParValue('g_m_X1')), "S", "design")
A1specs.append("c_iss_%s_o" % (mosType), "Obtained input capacitance input stage %sMOS" % (mosType), sp.N(cir.getParValue('c_iss_X1')), "F", "design")
A1specs.append("ID_%s" % (mosType), "Operating current input stage %sMOS" % (mosType), sp.N(cir.getParValue('ID')), "A", "design")
A1specs.append("IC_%s" % (mosType), "Inversion coefficient input stage %sMOS" % (mosType), sp.N(cir.getParValue('IC_X1')), "", "design")
A1specs.append("M_%s" % (mosType), "Number of fingers input stage %sMOS" % (mosType), Mf, "", "design")
A1specs.append("W_F_%s" % (mosType), "Finger width input stage %sMOS" % (mosType), W_finger, "m", "design")
A1specs.append("V_onoise_WLI_%s" % (mosType), "DIN A weighted RMS output noise with %sMOS, W, L, and ID" % (mosType), RMS_dinA, "V", "achievements")

sl.specs2html(A1specs.getSpecs())
