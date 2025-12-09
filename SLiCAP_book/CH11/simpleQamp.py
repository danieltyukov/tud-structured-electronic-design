#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
import sympy as sp
SHOW = False
#sl.initProject('simpleQamp')

cir = sl.makeCircuit('cir/simpleQamp.cir', imgWidth=None)
sl.htmlPage('High-pass cut-off design')
exprServo = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True).laplace
sl.eqn2html('S', exprServo)

gain, numerCoeffs, denomCoeffs = sl.coeffsTransfer(exprServo)
order          = len(denomCoeffs) - 1
omegaLow       = denomCoeffs[0]/denomCoeffs[-1]
f_l            = 1e3
A0min          = sp.solve(omegaLow - (2*sp.pi*f_l)**(1/order))[0]

A_min = sp.Symbol('A_min')
sl.text2html('In order to meet the requirement for $f_{\\ell}$ we need a minimum value $A_{\\min}$ for the DC gain $A_0$ of the controller:')
sl.eqn2html(A_min, A0min)

cir.defPar('A_0', A0min)
sl.htmlPage('Bode plots simpleQamp')

S = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
A = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
D = sl.doLaplace(cir, transfer='direct', pardefs='circuit', numeric=True)
G = sl.doLaplace(cir, transfer='gain', pardefs='circuit', numeric=True)
figMag = sl.plotSweep('magQamp', 'Magnitude characteristics', [A, L, S, D, G], 10, 10e6, 200, funcType='mag', show = SHOW)
sl.fig2html(figMag, 600)
figPhase = sl.plotSweep('phaseQamp', 'Magnitude characteristics', [A, L, S, D, G], 10, 10e6, 200, funcType='phase', show = SHOW)
sl.fig2html(figPhase, 600);
