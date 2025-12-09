#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import SLiCAP as sl

SHOW = False
#sl.initProject('cfbVampExtended') 
cir = sl.makeCircuit('kicad/cfbVampExtended/cfbVampExtended.kicad_sch', imgWidth=800)                        

G = sl.doLaplace(cir, transfer='gain', pardefs='circuit', numeric=True)
A = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
S = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
D = sl.doLaplace(cir, transfer='direct', pardefs='circuit', numeric=True)

figdBmag = sl.plotSweep('cfbVampdBmag.svg', 'dB magnitude plots asymptotic-gain model', 
                        [G,A,L,S,D], 1e4, 1e9, 200, funcType='dBmag', show=SHOW)
figPhase = sl.plotSweep('cfbVampPhase.svg', 'Phase plots asymptotic-gain model', 
                        [G,A,L,S,D], 1e4, 1e9, 200, funcType='phase', show=SHOW)

sl.htmlPage('Bode plots')
sl.fig2html(figdBmag, 800)
sl.fig2html(figPhase, 800)

sl.htmlPage('Symbolic asymptotic-gain')
A = sl.doLaplace(cir, transfer='asymptotic').laplace
sl.text2html('The asymptotic-gain is found as:')
sl.eqn2html('A_f_oo', A)
