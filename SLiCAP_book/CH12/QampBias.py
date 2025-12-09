#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl

SHOW = False

#sl.initProject('QampBias')

cir = sl.makeCircuit('kicad/QampBias/QampBias.kicad_sch')
GainUncomp = sl.doLaplace(cir, pardefs='circuit', numeric=True)
GainUncomp.gainType = 'uncomp.'
cir.defPar('C_c','220p')
GainComp = sl.doLaplace(cir, pardefs='circuit', numeric=True)
GainComp.gainType = 'phz comp.'
dBmag = sl.plotSweep('dBmagQamp', 'Biased charge amplifier', 
                     [GainUncomp, GainComp], 100, 10e6, 500, 
                     funcType='dBmag', show=SHOW)
phase = sl.plotSweep('phaseQamp', 'Biased charge amplifier', 
                     [GainUncomp, GainComp], 100, 10e6, 500, 
                     funcType='phase', show=SHOW)
stepDict = {}
stepDict['params'] = 'C_c'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = '220p'
stepDict['num']    = 20

poles = sl.doPoles(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
pPlot = sl.plotPZ('RLqAmp', 'Biased charge amplifier', poles, xmin=-3, xmax=0, 
                   ymin=-1.5, ymax=1.5, xscale='k', yscale='k', show=SHOW)

sl.htmlPage("Results")
sl.fig2html(dBmag, 600)
sl.fig2html(phase, 600)
sl.fig2html(pPlot, 600)