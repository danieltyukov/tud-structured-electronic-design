#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 13:02:51 2025

@author: anton
"""
import SLiCAP as sl
import sympy as sp
from scipy.optimize import fsolve
from copy import deepcopy

g_m, c_iss = sp.symbols("g_m, c_iss")
VARIABLES  = {1/c_iss: 'alpha', 1/g_m: 'beta', c_iss/g_m: 'gamma', c_iss**2/g_m: 'delta', 1 : 'epsilon'}
        
class process():
    def __init__(self):
        self.name     = ""     # Subcircuit name of "noisy nullor" with MOS noise sources
        self.IG       = 0      # DC gate current [A]
        self.W_min    = 0      # Minimum channel width [m]
        self.W_finger = 50e-6  # Maximum finger width [m]
        self.W_max    = 1      # Maximum channel width [m] (number of fingers * width per finger)
        self.L_min    = 0      # Minimum channel length [m]
        self.L_max    = 1      # Maximum channel length [m]
        self.channel  = None   # Channel type "P" or "N" must correspond with subcircuit name
        self.subckt   = None   # Spice noisy nullor subcircuit
        self.bias     = None   # MOS bias circuit
        
class specObject():
    def __init__(self):    
        self.noiseRMS = None # RMS output noise budget (source, feedback network, input stage transistor)
        self.f_min    = None # Lower limit of frequency range of interest [Hz]
        self.f_max    = None # Upper limit of frequency range of interest [Hz]
        self.ID_spec  = None # Specified current budget for methods W,L@I_DS [A]
        self.IC_max   = None # IC for minimum noise (maximum fT)
        self.gmID     = None # gmID for noise design according to specs
        self.gmID_min = None # gmID for minimum noise (maximum fT)
        self.VDS      = None # VDS; always positive
    
def _noisyNullorCircuit(file_name, model, lib=None, par_defs={}):
    cir = sl.makeCircuit(file_name)
    file_name_parts = file_name.replace("\\", "/").split("/")
    cir_name = file_name_parts[-1].split('.')[0]
    f = open(sl.ini.cir_path + cir_name + ".cir", "r")
    lines = f.readlines()
    f.close()
    found = False
    error = False
    new_lines = []
    for line in lines:
        if not found:
            if line[0] == "N":
                line = "X" + line[1:-2] + model.name + " W={W} L={L} ID={ID} IG={IG}\n"
                found = True
            new_lines.append(line)
        elif line[0] == "N":
            error = True
            print("Error: Found multiple nullors in the circuit.")
        else:
            new_lines.append(line)
    if lib != None:
        new_lines[-1] = ".lib {}\n".format(lib)
        new_lines.append(".end")
    if found and not error:
        f = open(sl.ini.cir_path + cir_name + "_" + model.name + ".cir", "w")
        f.writelines(new_lines)
        f.close()
        cir = sl.makeCircuit(cir_name + "_" + model.name + ".cir")
        cir.defPars(par_defs)
    else:
        cir = None
        if not found:
            print("Error: did not find a nullor in the circuit.")
    return cir

def _update_inversion_levels(cir, specs, model):
    # If IC is not specified, calculate it from gmID
    if specs.IC == None or specs.IC < 0 :
        if specs.gmID == None:
            print("Error: missing gm/ID or IC specification")
            cir = None
        elif specs.gmID <= 0:
            print("Error1: invalid IC or gm/ID ratio.")
            cir = None
        else:
            if model.channel.upper() == "P":
                gmID = -specs.gmID
            else:
                gmID = specs.gmID
            specs.IC = _IC(cir, gmID)
    # if gmID is not specified, calculate it from IC
    if specs.gmID == None or specs.gmID < 0:
        specs.gmID = _gmID(cir, specs.IC)
        if model.channel.upper() == "P":
            specs.gmID = -specs.gmID
    # If IC_max is not specified, calculate it from gmID_min
    if specs.IC_max == None or specs.IC_max < 0 :
        if specs.gmID_min == None:
            print("Error: missing gm/ID or IC specification")
            cir = None
        elif specs.gmID_min <= 0:
            print("Error2: invalid IC or gm/ID ratio.")
            cir = None
        else:
            if model.channel.upper() == "P":
                gmID_min = -specs.gmID_min
            else:
                gmID_min = specs.gmID_min
            specs.IC_max = _IC(cir, gmID_min)
    # if gmID_min is not specified, calculate it from IC_max
    if specs.gmID_min == None or specs.gmID_min < 0:
        specs.gmID_min = _gmID(cir, specs.IC_max)
        if model.channel.upper() == "P":
            specs.gmID_min = -specs.gmID_min   
    return specs
                         
def _getCoeffs(cir, IC_spec, f_min, f_max):
    out = {}
    g_m, c_iss, IC = sp.symbols("g_m, c_iss, IC")
    gm   = cir.getParValue("g_m_X1", substitute = False)
    ciss = cir.getParValue("c_iss_X1", substitute=False)
    #ig   = cir.getParValue("IG", substitute=False)
    ic   = cir.getParValue("IC_X1", substitute=False)
    cir.defPar("c_iss_X1", c_iss) # Use symbolic definition of c_iss
    cir.defPar("g_m_X1", g_m)     # Use symbolic definition of g_m
    cir.defPar("IG", 0)           # Ignore gate shot noise (leakage current)
    cir.defPar("IC_X1", IC_spec) # Use symbolic definition of IC
    # Express the output noise spectrum in c_iss, g_m, and f
    onoise   = sl.doNoise(cir, pardefs='circuit', numeric=True).onoise
    # Wtite the output noise as a sum of products of numerically calculated integrals and 
    # coefficients in the form of (g_m^x * c_iss^y), where x and y are positive or negative integers.
    # The coefficient "1" (x=0 and y=0) is the noise with a noise-free controller.
    coeffs   = sl.integrated_monomial_coeffs(sp.expand(onoise), (g_m, c_iss), sl.ini.frequency, f_min, f_max)
    keys      = coeffs.keys()
    for key in VARIABLES.keys():
        if key not in keys:
            coeffs[key] = 0
    for key in coeffs.keys():
        out[VARIABLES[key]] = sp.factor(sp.expand(coeffs[key]))
        cir.defPar("g_m_X1", gm)
    cir.defPar("g_m_X1", gm)
    cir.defPar("c_iss_X1", ciss)
    #cir.defPar("IG", ig)
    cir.defPar("IC_X1", ic)
    return out
    
def _g_c_opt(coeffs, specs):
    """
    Returns g_min and c_iss@g_min for which the noise requirements are met with
    minimum transconductance g_m.
    """
    if len(coeffs.keys()) > 0:
        c_iss_min = coeffs["alpha"]/specs.noiseRMS**2
        x = sp.Symbol('x')
        gm = (x/(x*specs.noiseRMS**2 - coeffs['alpha']))*(coeffs['beta']+x*coeffs['gamma']+x**2*coeffs['delta'])
        num, den = sp.diff(gm, x).as_numer_denom()
        sols = sp.solve(num)
        for sol in sols:
            if sp.re(sol) > c_iss_min and (sp.im(sol) == 0 or sp.Abs(sp.re(sol)/sp.im(sol)) > 1e12):
                c_iss_min = sp.re(sol)
        g_min = gm.subs(x, c_iss_min)
    else:
        g_min = None
        c_iss_min = None
    return g_min, c_iss_min

def _gc_opt(coeffs, specs):
    """
    Returns g_min and c_iss@g_min for which the noise requirements are met with
    minimum product of transconductance g_m and input capacitance C_iss.
    """
    if len(coeffs.keys()) > 0:
        c_iss_min = coeffs["alpha"]/specs.noiseRMS**2
        x = sp.Symbol('x')
        gmc = (x**2/(x*specs.noiseRMS**2 - coeffs['alpha']))*(coeffs['beta']+x*coeffs['gamma']+x**2*coeffs['delta'])
        num, den = sp.diff(gmc, x).as_numer_denom()
        sols = sp.solve(num)
        for sol in sols:
            if sp.re(sol) > c_iss_min and (sp.im(sol) == 0 or sp.Abs(sp.re(sol)/sp.im(sol)) > 1e12):
                c_iss_min = sp.re(sol)
        g_min = (gmc/x).subs(x, c_iss_min)
    else:
        g_min = None
        c_iss_min = None
    return g_min, c_iss_min

def _g_c_i(coeffs, specs, model):
    """
    Returns a dict with keys = gm value and value is a list with c values
    """
    out = {}
    if len(coeffs.keys()) > 0:
        c_iss_min = coeffs["alpha"]/specs.noiseRMS**2
        x = sp.Symbol('x')
        gm = (x/(x*specs.noiseRMS**2-coeffs['alpha']))*(coeffs['beta']+x*coeffs['gamma']+x**2*coeffs['delta'])
        ID = gm/specs.gmID
        I_spec = specs.ID_spec
        if model.channel.upper() == "P":
            I_spec = -I_spec 
            ID     = -ID
        num, den = ID.as_numer_denom()
        sols = sp.solve(num - I_spec*den, x)
        cs = []
        for sol in sols:
            if sp.re(sol) > c_iss_min and (sp.im(sol) == 0 or sp.Abs(sp.re(sol)/sp.im(sol)) > 1e12):
                cs.append(sp.re(sol))
        if len(cs):
            out[gm.subs(x, cs[0])] = cs
    return out
    
def _WLI(cir, g_min, c_iss_min, IC_spec, model):
    """
    Returns W, L, and I, from circuit object, g_min, and c_iss_min

    """
    W, L, ID = sp.symbols("W, L, ID")
    IC  = cir.getParValue("IC_X1")
    cir.defPar("IC_X1", IC_spec)
    chi = cir.getParValue("chi_X1")
    for name in cir.parDefs.keys():
        if str(name)[0:5] == "C_OX_":
            COX = cir.getParValue(str(name))
        elif str(name)[0:5] == "CGBO_":
            CGBO = cir.getParValue(str(name))
        elif str(name)[0:5] == "CGSO_":
            CGSO = cir.getParValue(str(name))
        elif str(name)[0:4] == "I_0_":
            I0 = cir.getParValue(str(name))
    gm    = cir.getParValue("g_m_X1", numeric=True)
    a     = chi * COX
    b     = 2 * CGSO
    c     = 2 * CGBO
    d     = I0 * gm/ID * IC_spec
    if model.channel.upper() == "P":
        d = -d
    if b == 0 and c == 0:
        W = sp.N(sp.sqrt(g_min*c_iss_min/a/d))
        L = sp.N(sp.sqrt(d*c_iss_min/a/g_min))
    else:
        term1 = c*d+2*b*g_min
        term2 = term1/2/a*(sp.sqrt(1+4*a*d*g_min*c_iss_min/(term1)**2)-1)
        W     = sp.N(term2/d)
        L     = sp.N(term2/g_min) 
    if sp.im(W) == 0 and sp.re(W) > 0 and sp.im(L) == 0 and sp.re(L) > 0:
        IDS   = sp.N(sp.solve(gm - g_min, ID)[0])
        out = {"W": W, "L": L, "ID": IDS, "c_iss_spec": c_iss_min, "g_m_spec": g_min, "IC_spec": IC_spec}
    else:
        out = {}
    cir.defPar("IC_X1", IC)
    return out

def _IC(cir, gm_ID):
    """
    Returns IC for a given gm/ID ratio.
    """
    IC, ID = sp.symbols("IC, ID")
    ICX1   = cir.getParValue("IC_X1", substitute = False)
    cir.defPar("IC_X1", IC)
    gmID = cir.getParValue("g_m_X1")/ID
    try:
        IC = sp.solve(gmID - sp.Rational(gm_ID), IC)[0]
    except IndexError:
        print("Error: invalid gm/ID ratio")
    cir.defPar("IC_X1", ICX1)
    return sp.N(IC)

def _gmID(cir, IC_num):
    """"
    Returns gm/ID ratio for a given IC.
    """
    # Save the value of the lateral field velocity saturation and set it to infinite

    IC, ID = sp.symbols("IC, ID")
    ICX1 = cir.getParValue("IC_X1", substitute = False)
    cir.defPar("IC_X1", IC_num)
    gmID = cir.getParValue("g_m_X1")/ID
    cir.defPar("IC_X1", ICX1)

    return gmID

def _minN(cir, specs, model):
    """
    Returns dictionary with MOS design data for minimum noise at specified
    IC_max or gmID_min.

    """
    # define minimum geometry
    cir.defPar("W", model.W_min)
    cir.defPar("L", model.L_min)
    # get definition inversion coefficient
    IC_old = cir.getParValue("IC_X1", substitute = False)
    # Calculate current at maximum inverson level
    IC_ID = cir.getParValue("IC_X1")
    
    func_IC_ID = sp.lambdify(sp.Symbol("ID"), sp.N(IC_ID) - specs.IC_max)
    start = 1e-6
    if model.channel.upper() == "P":
        start = - start
    ID = fsolve(func_IC_ID, start)[0]
    cir.defPar("ID", ID)
    fT_max       = cir.getParValue("f_T_X1", numeric=True)
    coeffs       = _getCoeffs(cir, specs.IC_max, specs.f_min, specs.f_max)
    c_iss_opt    = sp.N(sp.sqrt((2*sp.pi*fT_max*coeffs["alpha"] + coeffs["beta"])/coeffs["delta"]))
    g_m_opt      = sp.N(2*sp.pi*fT_max*c_iss_opt)
    cir.delPar("W")
    cir.delPar("L")
    cir.delPar("ID")
    out               = _WLI(cir, g_m_opt, c_iss_opt, specs.IC_max, model)
    out["c_iss_spec"] = c_iss_opt
    out["g_m_spec"]   = g_m_opt
    out["IC_spec"]    = specs.IC_max
    cir.defPar("IC_X1", IC_old)
    return out

def _min_fT(cir, coeffs, specs, model):
    fT        = sp.Symbol("fT")
    x         = sp.Symbol('x')
    ovar_fT   = coeffs["alpha"]/x + coeffs["beta"]/(2*sp.pi*fT*x) + (coeffs["gamma"] + coeffs["delta"]*x)/(2*sp.pi*fT) + coeffs["epsilon"]
    fT_ciss   = sp.solve(ovar_fT - specs.noiseRMS**2, fT)[0]
    num, den  = fT_ciss.as_numer_denom()
    c_iss_min = sp.solve(den, x)[0]
    dFT_dciss = sp.diff(fT_ciss, x)
    num, den  = dFT_dciss.as_numer_denom()
    sols      = sp.solve(num, x)
    for sol in sols:
        if sp.re(sol) > c_iss_min and (sp.im(sol) == 0 or sp.Abs(sp.re(sol)/sp.im(sol)) > 1e12):
            c_iss_min = sp.re(sol)
    g_min = fT_ciss.subs(x, c_iss_min)*sp.pi*2*c_iss_min
    out = _WLI(cir, g_min, c_iss_min, specs.IC, model)
    out["g_m_spec"]   = sp.N(g_min)
    out["IC_spec"]    = specs.IC
    return out

def _c_g_fT(coeffs, fT):
    ciss_opt = sp.N(sp.sqrt((2*sp.pi*fT*coeffs['alpha'] + coeffs['beta'])/coeffs['delta']))
    gm_opt = sp.N(fT*2*sp.pi*ciss_opt)
    return gm_opt, ciss_opt

def _mosParams(file_name, specs, model, par_defs = {}):
    print("\n=============================================================")
    print("Model: {}".format(model.name))
    print("=============================================================\n")
    # Create output dictionary
    out = {}
    # Create the noisy nullor circuit from the nullor circuit
    cir = _noisyNullorCircuit(file_name, model, lib="SLiCAP_C18.lib", par_defs=par_defs)
    if cir != None:
        # store symbolic definition of IC
        ic  = cir.getParValue("IC_X1", substitute=False) 
        for name in cir.parDefs.keys():
            if str(name)[0:7] == "E_CRIT_":
                ecrit  = cir.getParValue(name)
                cir.defPar(str(name), sp.oo)
                break
        specs = _update_inversion_levels(cir, specs, model)                    
    if cir != None:
        # Calculate the coefficients 'alpha' ... 'epsilon' of the noise equation
        coeffs   = _getCoeffs(cir, specs.IC, specs.f_min, specs.f_max)
        # Method mininum noise
        out["N_min"] = _minN(cir, specs, model)
        #cir.defPar("IC_X1", specs.IC)
        # Calculate the optimum c_iss and minimum g_m from the coefficients and the specs
        g_min, c_iss_min =  _g_c_opt(coeffs, specs)
        if g_min != None and c_iss_min != None:
            # Calculate W, L, and ID from 'g_min' and 'c_iss_min'
            cir.defPar("IC_X1", specs.IC)
            # Method minimum current
            out["I_min"] = _WLI(cir, g_min, c_iss_min, specs.IC, model)
            cir.defPar("IC_X1", ic)
        # Method minimum fT
        out["min_fT"] = _min_fT(cir, coeffs, specs, model)
        # Method minimum product of g_m and c_iss
        g_min, c_iss_min =  _gc_opt(coeffs, specs)
        if g_min != None and c_iss_min != None:
            # Calculate W, L, and ID from 'g_min' and 'c_iss_min'
            cir.defPar("IC_X1", specs.IC)
            # Method minimum current
            out["g*c_min"] = _WLI(cir, g_min, c_iss_min, specs.IC, model)
            cir.defPar("IC_X1", ic)
        # Method WL at given IC and IDS
        cir.defPar("IC_X1", specs.IC)
        limits = _g_c_i(coeffs, specs, model)
        for key in limits.keys():
            for i in range(len(limits[key])):
                out["Ispec_" + str(i)] = _WLI(cir, key, limits[key][i], specs.IC, model)
        cir.defPar("IC_X1", ic)
        if coeffs["epsilon"] > specs.noiseRMS**2:
            print("\nFATAL ERROR: no noise budget left for MOS transistor")
            print("             RMS noise exceeds specified budget in all cases!")
            print("=============================================================\n")
         
    for name in cir.parDefs.keys():
        if str(name)[0:7] == "E_CRIT_":
            cir.defPar(str(name), ecrit)
            break
    return out, cir

def _checkNoise(cir, specs, pardefs):
    cir.defPars(pardefs)
    cir.defPar("IG", 0)
    Sout = sl.doNoise(cir, pardefs="circuit", numeric=True)
    RMSnoise = sl.rmsNoise(Sout, "onoise", specs.f_min, specs.f_max)
    return RMSnoise, cir

def _checkNoiseSpice(baseFileName, model, specs, ID, W, L, spice_params=None):
    M  = int(W/ model.W_finger) + 1
    W  = W/M
    params = [("W", W), ("L", L), ("ID", ID), ("M", M), ("VDS", specs.VDS)]
    biascir = model.bias.replace("\\", "/")
    biascir = biascir.split("/")[-1].split(".")[0]
    biasinfo = sl.ngspice2traces(sl.ini.cir_path + biascir, "OP", {"VGS": "V(g1)", "VDS": "V(d1)"}, parList=params)
    params = [("W", W), ("L", L), ("ID", ID), ("M", M), ("VDS", biasinfo["VDS"]), ("VGS", biasinfo["VGS"])]
    if type(spice_params) == list:
        params += spice_params
    simCmd = "OP"
    names  = {"V_in": "V(in)", "V_out": "V(out)", "I_DS": "@M.X1.M1[id]", "V_GS": "@M.X1.M1[vgs]", "g_m": "@M.X1.M1[gm]", "c_iss": "@M.X1.M1[cgg]"}
    cirFile = baseFileName + "NoisyNullor{}.kicad_sch".format(model.channel.upper())
    sl.makeCircuit(cirFile, language="SPICE")
    netlist = cirFile.split("/")[-1].split(".")[0]
    out    = sl.ngspice2traces(sl.ini.cir_path + netlist, simCmd, names, parList=params)
    out["L"] = L
    out["W"] = W
    out["M"] = M
    names  = {"V_no": "onoise_total"}
    
    ## ADD SOURCE
    
    simCmd = "NOISE V(out) V1 dec 50 " + str(specs.f_min) + " " + str(specs.f_max)
    noise  = sl.ngspice2traces(sl.ini.cir_path + netlist, simCmd, names, parList=params)
    for key in noise.keys():
        out[key] = noise[key]
    return out

def _printResults(results, cir, specs, model, kicad_sch, printAll=True, spice=False, par_defs={}):
    if spice:
        print("\nUpdating library sub circuit definitions.\n")
        sl.makeCircuit(model.bias, language="SPICE")
        sl.makeCircuit(model.subckt, language="SPICE")
        spice_params = []
        for key in par_defs.keys():
            try:
                spice_params.append( (str(key), float(par_defs[key])) )
            except TypeError:
                print("Error: cannot calculate numeric value of {}.".format(str(key)))
                #spice = False
    for key in results.keys():
        errors        = False
        RMSnoise, cir = _checkNoise(cir, specs, results[key])
        gm            = cir.getParValue("g_m_X1", numeric=True)   # Realized g_m
        ID            = cir.getParValue("ID", numeric=True)       # Realized ID
        if model.channel.upper() == "P":
            ID = -ID
        W             = cir.getParValue("W", numeric=True)        # Realized W
        L             = cir.getParValue("L", numeric=True)        # Realized L
        gmID          = gm/ID                                     # Realized gm/ID 
        print("\nMethod:", key, model.name)
        print("============================================")
        if key == "N_min":
            if RMSnoise > specs.noiseRMS:
                print("RMS noise  : {:.2e} uV ** Error: too high!".format(RMSnoise*1e6))
                errors = True
            else:
                print("RMS noise  : {:.2e} uV".format(RMSnoise*1e6))
        elif sp.im(RMSnoise) != 0:
            print("RMS noise  : ** Error: invalid!")
            errors = True
        else:
            print("RMS noise  : {:.2e} uV".format(RMSnoise*1e6))
        print("ID         : {:.2e} uA".format(ID*1e6))
        if W < model.W_min:
            print("W          : {:.2e} um ** Error: too small!".format(W*1e6))
            errors = True
        elif W > model.W_max:
            print("W          : {:.2e} um ** Error: too large!".format(W*1e6))
            errors = True
        else:
            print("W          : {:.2e} um".format(W*1e6))
        if L < model.L_min:
            print("L          : {:.2e} um ** Error: too small!".format(L*1e6))
            errors = True
        elif L > model.L_max:
            print("L          : {:.2e} um ** Error: too large!".format(L*1e6))
            errors = True
        else:
            print("L          : {:.2e} um".format(L*1e6))
        print("gm/ID      : {:.2g} 1/V".format(gmID))
        if printAll:
            IC_spec       = results[key]["IC_spec"]                   # Target IC
            IC            = cir.getParValue("IC_X1", numeric=True)    # Realized IC
            gm_spec       = results[key]["g_m_spec"]                  # target g_m
            ciss_spec     = results[key]["c_iss_spec"]                # Traget c_iss
            ciss          = cir.getParValue("c_iss_X1", numeric=True) # Realized c_iss
            print("area       : {:.2g} um_sq".format(W*L*1e12))
            print("g_m_spec   : {:.2g} uS".format(gm_spec*1e6))
            print("g_m        : {:.2g} uS".format(gm*1e6))
            print("c_iss_spec : {:.2g} pF".format(ciss_spec*1e12))
            print("c_iss      : {:.2g} pF".format(ciss*1e12))
            print("IC_spec    : {:.2g} -".format(IC_spec))
            print("IC         : {:.2g} -".format(IC))
            print("f_T        : {:.2g} MHz".format(sp.N(gm/2/sp.pi/ciss/1e6)))
        if not errors and spice:
            try:
                print("\n------------ SPICE verification ------------\n")
                baseFileName = kicad_sch.replace("\\", "/").split(".")[0]
                spiceResults = _checkNoiseSpice(baseFileName, model, specs, ID, W, L, spice_params=spice_params)
                if len(spiceResults.keys()):
                    print("\nRMS noise  : {:.2e} uV".format(spiceResults["V_no"]*1e6))
                    print("ID         : {:.2g} uA".format(spiceResults["I_DS"]*1e6))
                    print("W          : {:.2g} um".format(spiceResults["W"]*1e6))
                    print("L          : {:.2g} um".format(spiceResults["L"]*1e6))
                    print("M          : {:.2g} -".format(spiceResults["M"]))
                    print("VGS        : {:.2g} V".format(spiceResults["V_GS"]))
                    print("c_iss      : {:.2g} pF".format(spiceResults["c_iss"]*1e12))
                    print("g_m        : {:.2g} uS".format(spiceResults["g_m"]*1e6))
                    print("g_m/ID     : {:.2g} 1/V".format(spiceResults["g_m"]/spiceResults["I_DS"]))
                    print("f_T        : {:.2g} MHz".format(sp.N(spiceResults["g_m"]/spiceResults["c_iss"]/2/sp.pi)/1e6))
                    try:
                        print("\nBias results\n------------")
                        print("V_out_DC   : {:.2g} uV".format(spiceResults["V_out"]*1e6))
                        print("V_in_DC    : {:.2g} uV".format(spiceResults["V_in"]*1e6))
                        print("------------")
                    except KeyError():
                        pass
            except:
                pass
    
def doMOSnoiseDesign(kicad_sch, specs, models, printAll=True, spice=False, par_defs={}):
    all_results = {}
    for model in models:
        results, cir = _mosParams(kicad_sch, specs, model, par_defs=par_defs)
        if len(results.keys()) != 0:
            if spice:
                par_defs = {}
                for key in cir.parDefs.keys():
                    par_defs[key] = sl.fullSubs(cir.parDefs[key], cir.parDefs)
            _printResults(results, cir, specs, model, kicad_sch, printAll=printAll, spice=spice, par_defs=par_defs)
            all_results[model.name] = (deepcopy(results), deepcopy(cir))
    return all_results