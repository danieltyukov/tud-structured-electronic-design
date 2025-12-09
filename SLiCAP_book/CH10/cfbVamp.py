#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import SLiCAP as sl
import sympy as sp

#sl.initProject('cfbVamp')       
cir = sl.makeCircuit('kicad/cfbVamp/cfbVamp.kicad_sch', imgWidth=600) 

# Calculation of the gain using MNA
gain = sl.doLaplace(cir).laplace

V_ell, V_s, A_f                = sp.symbols('V_ell, V_s, A_f')
L_G1, rho_G1, S_G1, A_infty_G1 = sp.symbols('L_G1, rho_G1, S_G1, A_oo_G1')
L_H1, rho_H1, S_H1, A_infty_H1 = sp.symbols('L_H1, rho_H1, S_H1, A_oo_H1')

# Calculations with H1 as loop gain reference

AG1 = sl.doLaplace(cir, transfer='asymptotic', lgref='G1').laplace
LG1 = sl.doLaplace(cir, transfer='loopgain', lgref='G1').laplace
SG1 = sl.doLaplace(cir, transfer='servo', lgref='G1').laplace
DG1 = sl.doLaplace(cir, transfer='direct', lgref='G1').laplace

sl.htmlPage('Asymptotic-gain model G1 ref')
sl.text2html('The gain of the circuit is obtained as:')
sl.eqn2html(V_ell/V_s, gain)

sl.text2html('The asymptotic-gain $A_{\\infty_G1}$ is found as:')
sl.eqn2html(A_infty_G1, AG1)

sl.text2html('The loop gain $L_{G1}$ is found as:')
sl.eqn2html(L_G1, LG1)

sl.text2html('The servo function $S_{G1}$ is found as:')
sl.eqn2html(S_G1, SG1)

sl.text2html('The direct transfer $\\rho_{G1}$ is found as:')
sl.eqn2html(rho_G1, DG1)

sl.text2html('The gain $A_f$ calculated from $A_{\\infty_{G1}}$, $S_{G1}$ and  $\\rho_{G1}$ is obtained as:')
sl.eqn2html(A_f, sp.simplify(AG1*SG1 + DG1/(1-LG1)))

# Calculations with H1 as loop gain reference

AH1 = sl.doLaplace(cir, transfer='asymptotic', lgref='H1').laplace
LH1 = sl.doLaplace(cir, transfer='loopgain', lgref='H1').laplace
SH1 = sl.doLaplace(cir, transfer='servo', lgref='H1').laplace
DH1 = sl.doLaplace(cir, transfer='direct', lgref='H1').laplace

sl.htmlPage('Asymptotic-gain model H1 ref')
sl.text2html('The gain of the circuit is obtained as:')
sl.eqn2html(V_ell/V_s, gain)

sl.text2html('The asymptotic-gain $A_{\\infty_{H1}}$ is found as:')
sl.eqn2html(A_infty_H1, AH1)

sl.text2html('The loop gain $L_{H1}$ is found as:')
sl.eqn2html(L_H1, LH1)

sl.text2html('The servo function $S_{H1}$ is found as:')
sl.eqn2html(S_H1, SH1)

sl.text2html('The direct transfer $\\rho_{H1}$ is found as:')
sl.eqn2html(rho_H1, DH1)

sl.text2html('The gain $A_f$ calculated from $A_{\\infty_G1}$, $S_{G1}$ and  $\\rho_{G1}$ is obtained as:')
sl.eqn2html(A_f, sp.simplify(AH1*SH1 + DH1/(1-LH1)))
