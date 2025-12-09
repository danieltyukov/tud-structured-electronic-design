#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""
import SLiCAP as sl
from CSstageLTspice import LTmag, LTphase
SHOW = False
# Obtain the values of the small-signal parameters from the EKV model
# Alternatively, you could obtain them from a looup table or a SPICE .OP run
from CSstageEKV import gm, go, cgs, cgb, cdg, cdb
# Uncomment the next line if you want to overwrite the main html index page
#prj = initProject('CSstageSmallSignal');

# Generate netlist
#makeNetlist('CSstageComponents.asc', 'CS stage hybrid-pi small-signal model');

cir = sl.makeCircuit('kicad/CSstageComponents/CSstageComponents.kicad_sch')
# This creates an new index page in the html report and links to new pages
# will now be placed on this index page
cir.defPar('g_m', gm)
cir.defPar('g_o', go)
cir.defPar('c_gs', cgs)
cir.defPar('c_gb', cgb)
cir.defPar('c_dg', cdg)
cir.defPar('c_db', cdb)

sl.htmlPage('CS stage small-signal dynamic behavior')

gainComponents = sl.doLaplace(cir, pardefs='circuit', numeric=True)

sl.head2html('Numeric expression')
sl.eqn2html('Z_t', sl.normalizeRational(gainComponents.laplace))

sl.head2html('Bode plots')
magZtComponents = sl.plotSweep('magZtComponents', 'magnitude', gainComponents, 1, 100e9, 200, funcType = 'mag', show = SHOW)
sl.traces2fig(LTmag, magZtComponents)
magZtComponents.plot()
sl.fig2html(magZtComponents, 600)
phaseZtComponents = sl.plotSweep('phaseZtComponents', 'phase', gainComponents, 1, 100e9, 200, funcType = 'phase', show = SHOW)
sl.traces2fig(LTphase, phaseZtComponents)
phaseZtComponents.plot()
sl.fig2html(phaseZtComponents, 600)

pzComponents = sl.doPZ(cir, pardefs='circuit', numeric=True)
sl.pz2html(pzComponents)

