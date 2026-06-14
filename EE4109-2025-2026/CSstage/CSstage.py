#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:51:17 2020

@author: anton
"""

import SLiCAP as sl
sl.initProject('CSstage')
cir     = sl.makeCircuit('kicad/CSstage/CSstage.kicad_sch')
gain    = sl.doLaplace(cir, pardefs='circuit', source='I1', detector='V_out', 
                       numeric=True)
dBmagZt = sl.plotSweep('dBmagZt.svg', 'dB magnitude', gain, 1, 100e6, 200, 
                       funcType = 'dBmag', sweepScale = 'k', show=True)
phaseZt = sl.plotSweep('phaseZt.svg', 'phase', gain, 1, 100e6, 200, 
                       funcType = 'phase', sweepScale = 'k', show=True)

# HTML Report

sl.htmlPage('CS stage small-signal dynamic behavior')
sl.head2html('Numeric expression')
sl.eqn2html('Z_t', gain.laplace)
sl.head2html('Bode plots')
sl.fig2html(dBmagZt, 600)
sl.fig2html(phaseZt, 600)
sl.htmlPage('LTspice CSstage')
sl.head2html('LTspice circuit')
sl.img2html('CSstageLTspice.svg', 800)
sl.head2html('LTspice Bode plots')
sl.img2html('CSstageLTspiceAC.svg', 800)