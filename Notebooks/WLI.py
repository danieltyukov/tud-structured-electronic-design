#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 18:04:52 2025

@author: anton
"""
import sympy as sp

def updateModel(cir, IC):
    g_m, c_iss = sp.symbols("g_m, c_iss")
    IC_sym     = cir.getParValue("IC_X1", substitute=False)
    for name in cir.parDefs.keys():
        if str(name)[0:7] == "E_CRIT_":
            ecrit  = cir.getParValue(name)
            cir.defPar(str(name), sp.oo)
            break
    gm_sym     = cir.getParValue("g_m_X1", substitute=False)
    cir.defPar("IC_X1", IC)
    cir.defPar("g_m_X1", g_m)
    cir.defPar("c_iss_X1", c_iss)
    return (cir, IC_sym, gm_sym)
    

def WLI(cir, g_min, c_iss_min, gm_sym, IC, channel):
    cir.delPar("W")
    cir.delPar("L")
    cir.delPar("ID")
    cir.defPar("g_m_X1", gm_sym)
    W, L, ID = sp.symbols("W, L, ID")
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
    d     = I0 * gm/ID * IC
    if channel.upper() == "P":
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
    return (W, L, IDS)