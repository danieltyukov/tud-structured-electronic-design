import SLiCAP as sl
import sympy as sp

from g12specifications import global_specs, A1specs

# Select NMOS or PMOS
mosType = False
while not mosType:
    mosType = input("Please select N or P type input CS stage:\n>>> ").upper()
    if mosType != "N" and mosType != "P":
        mosType = False
if mosType == "N":
    cir = sl.makeCircuit("kicad/controller/single_NMOS.kicad_sch")
    img = "single_NMOS.svg"
elif mosType == "P":
    cir = sl.makeCircuit("kicad/controller/single_PMOS.kicad_sch")
    img = "single_PMOS.svg"
sl.img2html(img, 600)

# Specs
sl.specs2html(A1specs.getSpecs())



sl.specs2circuit(A1specs.getSpecs(), cir)
if mosType == "N":
    # NMOS is working in weak inversion, the width does not need to be scaled with the current
    cir.defPar("ID_N", 0.6*cir.getParValue("I_fb"))
elif mosType == "P":
    # PMOS is working in moderate inversion, scale the width with the current
    WP = -0.6*cir.getParValue("I_fb")/cir.getParValue("ID_P")*cir.getParValue("W_P")
    cir.defPar("W_P", WP)
    cir.defPar("ID_P", -0.6*cir.getParValue("I_fb"))
sl.elementData2html(cir)

# params
sl.params2html(cir)

sl.htmlPage('gain plots')
# Plot gain
gain        = sl.doLaplace(cir, pardefs="circuit", numeric=True)
asymptotic  = sl.doLaplace(cir, pardefs="circuit", numeric=True, transfer="asymptotic")
loopgain    = sl.doLaplace(cir, pardefs="circuit", numeric=True, transfer="loopgain")
servo       = sl.doLaplace(cir, pardefs="circuit", numeric=True, transfer="servo")
direct      = sl.doLaplace(cir, pardefs="circuit", numeric=True, transfer="direct")

sl.eqn2html("gain", gain.laplace)
sl.eqn2html("asymptotic", asymptotic.laplace)
sl.eqn2html("loopgain", loopgain.laplace)
sl.eqn2html("servo", servo.laplace)
sl.eqn2html("direct", direct.laplace)


fb_model    = [gain, asymptotic, loopgain, servo, direct]
fbmodel_mag = sl.plotSweep("fb_mag", "Magnitude plots feedback model parameters", fb_model, 10, 10e5, 200)
sl.img2html("fb_mag.svg", width=600)


sl.htmlPage('pole zero plots')
PZgain = sl.doPZ(cir, pardefs="circuit", numeric=True, transfer="gain")
PZasymptotic = sl.doPZ(cir, pardefs="circuit", numeric=True, transfer="asymptotic")
PZloopgain = sl.doPZ(cir, pardefs="circuit", numeric=True, transfer="loopgain")
PZservo = sl.doPZ(cir, pardefs="circuit", numeric=True, transfer="servo")
PZdirect = sl.doPZ(cir, pardefs="circuit", numeric=True, transfer="direct")

sl.plotPZ("PZplotgain", "PZplotgain", PZgain) 
sl.plotPZ("PZplotasymptotic", "PZplotasymptotic", PZasymptotic)
sl.plotPZ("PZplotloopgain", "PZplotloopgain", PZloopgain)
sl.plotPZ("PZplotservo", "PZplotservo", PZservo)
sl.plotPZ("PZplotdirect", "PZplotdirect", PZdirect)

sl.pz2html(PZgain)
sl.img2html("PZplotgain.svg", width=600)
sl.pz2html(PZasymptotic)
sl.img2html("PZplotasymptotic.svg", width=600)
sl.pz2html(PZloopgain)
sl.img2html("PZplotloopgain.svg", width=600)
sl.pz2html(PZservo)
sl.img2html("PZplotservo.svg", width=600)
sl.pz2html(PZdirect)
sl.img2html("PZplotdirect.svg", width=600)


sl.htmlPage('feedback model plots')
fbmodel_phase = sl.plotSweep("fb_phase", "Magnitude plots feedback model parameters", fb_model, 10, 10e5, 200, funcType="phase")
sl.img2html("fb_phase.svg", width=600)


servoData = sl.findServoBandwidth(loopgain.laplace)


L_sym         = sl.doLaplace(cir, transfer="loopgain").laplace
substitutions = {"c_dg_X1":0,"c_gs_X1":0,"c_gb_X1":0,"c_db_X1":0}
L_MB          = sp.simplify(sp.limit(L_sym.subs(substitutions), sp.Symbol("tau_i"), sp.oo))
L_MB_max      = L_MB.subs({sl.ini.laplace:0, sp.Symbol("g_o_X1"):0})
sl.eqn2html("L_MB_max", L_MB_max)


L_MB_max = L_MB_max.subs({"R_i": cir.getParValue("R_i"), "g_m_X1": cir.getParValue("g_m_X1")})
sl.eqn2html("L_MB_max", sp.N(L_MB_max))


PZ = sl.doPoles(cir, pardefs="circuit", numeric=True, transfer="loopgain")
sl.pz2html(PZ)
sl.img2html("PZ.svg", width=600)


# ============================================================================
# Cascode Magnitude Response
# ============================================================================
if mosType == "P":
    # Load the cascode PMOS circuit (starts new HTML section)
    cir_casc = sl.makeCircuit("kicad/controller/cascode_PMOS.kicad_sch", imgWidth=800)

    # Apply specs and scale W/ID same as single PMOS
    sl.specs2circuit(A1specs.getSpecs(), cir_casc)
    WP_casc = -0.6*cir_casc.getParValue("I_fb")/cir_casc.getParValue("ID_P")*cir_casc.getParValue("W_P")
    cir_casc.defPar("W_P", WP_casc)
    cir_casc.defPar("ID_P", -0.6*cir_casc.getParValue("I_fb"))

    sl.elementData2html(cir_casc)
    sl.params2html(cir_casc)

    sl.htmlPage('Cascode Magnitude Response')

    # Feedback model analysis
    casc_gain       = sl.doLaplace(cir_casc, pardefs="circuit", numeric=True)
    casc_asymptotic = sl.doLaplace(cir_casc, pardefs="circuit", numeric=True, transfer="asymptotic")
    casc_loopgain   = sl.doLaplace(cir_casc, pardefs="circuit", numeric=True, transfer="loopgain")
    casc_servo      = sl.doLaplace(cir_casc, pardefs="circuit", numeric=True, transfer="servo")
    casc_direct     = sl.doLaplace(cir_casc, pardefs="circuit", numeric=True, transfer="direct")

    casc_fb_model = [casc_gain, casc_asymptotic, casc_loopgain, casc_servo, casc_direct]
    sl.plotSweep("casc_fb_mag", "Magnitude plots cascode feedback model parameters", casc_fb_model, 10, 10e5, 200)
    sl.img2html("casc_fb_mag.svg", width=600)