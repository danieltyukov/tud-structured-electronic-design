#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""

import SLiCAP as sl
from CSstageLTspice import LTmag, LTphase

# Obtain the values of the small-signal parameters from the EKV model
# Alternatively, you could obtain them from a looup table or a SPICE .OP run
from CSstageEKV import gm, go, cgs, cgb, cdg, cdb
SHOW = False
# Uncomment the next line if you want to overwrite the main html index page
#sl.initProject('CSstageSmallSignal');
cir = sl.makeCircuit('kicad/CSstageModel/CSstageModel.kicad_sch')

cir.defPar('g_m', gm)
cir.defPar('g_o', go)
cir.defPar('c_gs', cgs)
cir.defPar('c_gb', cgb)
cir.defPar('c_dg', cdg)
cir.defPar('c_db', cdb)

sl.htmlPage('CS stage small-signal dynamic behavior')
gainModel = sl.doLaplace(cir, pardefs='circuit', numeric=True)

sl.head2html('Numeric expression')
sl.eqn2html('Z_t', sl.normalizeRational(gainModel.laplace))

sl.head2html('Bode plots')
magZtModel = sl.plotSweep('magZtModel', 'magnitude', gainModel, 1, 100e9, 200, funcType = 'mag', show = SHOW)
sl.traces2fig(LTmag, magZtModel)
magZtModel.plot()
sl.fig2html(magZtModel, 600)
phaseZtModel = sl.plotSweep('phaseZtModel', 'phase', gainModel, 1, 100e9, 200, funcType = 'phase', show = SHOW)
sl.traces2fig(LTphase, phaseZtModel)
phaseZtModel.plot()
sl.fig2html(phaseZtModel, 600)

pzModel = sl.doPZ(cir, pardefs='circuit', numeric=True)
sl.pz2html(pzModel)
