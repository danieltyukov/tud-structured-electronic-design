#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl

SHOW = False

fileName = 'RLvAmp_3_2'
#sl.initProject(fileName)       
cir = sl.makeCircuit('cir/' + fileName + '.cir', imgWidth=None)

stepDict           = {}
stepDict['params'] = 'A_0'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = '1M'
stepDict['num']    = 100

RL              = sl.doPoles(cir, transfer='servo', pardefs='circuit', 
                             numeric=True, stepdict=stepDict)
polesGain       = sl.doPoles(cir, transfer='gain', pardefs='circuit', 
                             numeric=True)
polesAsymptotic = sl.doPoles(cir, transfer='asymptotic', pardefs='circuit', 
                             numeric=True)
polesLoopGain   = sl.doPoles(cir, transfer='loopgain', pardefs='circuit', 
                             numeric=True)
zerosLoopGain   = sl.doZeros(cir, transfer='loopgain', pardefs='circuit', 
                             numeric=True)
plots           = [RL, zerosLoopGain, polesLoopGain, polesAsymptotic, polesGain]
fig_PZ          = sl.plotPZ('RL_' + fileName, fileName, plots, xmin=-2, xmax=0, 
                            ymin=-1, ymax=1, xscale='k', yscale='k', show=SHOW)

sl.htmlPage('Root locus')
sl.fig2html(fig_PZ, 600)

# Print poles and zeros of the gain
pzGain        = sl.doPZ(cir, transfer='gain', pardefs='circuit', numeric=True)
sl.listPZ(pzGain)

# Calculate the phase margin
L  = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
pm = sl.phaseMargin(L.laplace)
uF = pm[1] # unity-gain frequency
pM = pm[0] # phase margin

print('Loop gain: phase margin = {:3.2f}deg at f = {:8.2e}Hz'.format(pM, uF))

# Generate Bode plots
sl.htmlPage('Bode plots')
S = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
G = sl.doLaplace(cir, transfer='gain', pardefs='circuit', numeric=True)
A = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
plots = [A, L, S, G]
BodeMag  = sl.plotSweep('dBmag_' + fileName, fileName, plots, 1, 1e4, 200, 
                        funcType='dBmag', show=SHOW)
BodePhas = sl.plotSweep('Phase_' + fileName, fileName, plots, 1, 1e4, 200, 
                        funcType='phase', show=SHOW)
sl.fig2html(BodeMag, 600)
sl.fig2html(BodePhas,600)