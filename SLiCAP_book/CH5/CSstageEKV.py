#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""

import SLiCAP as sl
from CSstageLTspice import LTmag, LTphase
SHOW = False
#sl.initProject('CSstageSmallSignal');
cir = sl.makeCircuit('kicad/CSstageEKV/CSstageEKV.kicad_sch')

# Obtain the values of the small-signal parameters according to the EKV model,
# the C18 process parameters and the device geometry. They are calculated
# using the model equations in the subcircuit X1: CMOS18N
# We will pass these values to other circuits.
# 
# You could also obtain these values from a lookup table and correct them for 
# the device geometry and operating conditions

gm = cir.getParValue('g_m_X1', numeric=True)
go = cir.getParValue('g_o_X1', numeric=True)
cgs = cir.getParValue('c_gs_X1', numeric=True)
cgb = cir.getParValue('c_gb_X1', numeric=True)
cdg = cir.getParValue('c_dg_X1', numeric=True)
cdb = cir.getParValue('c_db_X1', numeric=True)

sl.htmlPage('CS stage small-signal dynamic behavior')
gainEKV = sl.doLaplace(cir, pardefs='circuit', numeric=True)

sl.head2html('Numeric expression')
sl.eqn2html('Z_t', sl.normalizeRational(gainEKV.laplace))

sl.head2html('Bode plots')
magZtEKV = sl.plotSweep('magZtEKV', 'magnitude', gainEKV, 1, 100e9, 200, funcType = 'mag', show = SHOW)
sl.traces2fig(LTmag, magZtEKV)
magZtEKV.plot()
sl.fig2html(magZtEKV, 600)
phaseZtEKV = sl.plotSweep('phaseZtEKV', 'phase', gainEKV, 1, 100e9, 200, funcType = 'phase', show = SHOW)
sl.traces2fig(LTphase, phaseZtEKV)
phaseZtEKV.plot()
sl.fig2html(phaseZtEKV, 600)

pzEKV = sl.doPZ(cir, pardefs='circuit', numeric=True)
sl.pz2html(pzEKV)
