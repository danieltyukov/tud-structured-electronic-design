#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  14 15:36:50 2020

@author: anton
"""

import SLiCAP as sl
import numpy as np
SHOW = False

#sl.initProject('Phantom Zero Bandwidth limitation')

fileName = 'PhZbwLimit'

cir = sl.makeCircuit('kicad/PhZbwLimit/PhZbwLimit.kicad_sch')

# Define the circuit parameters
A    = -20e6    # small-signal DC gain opamp
f_p2 = 1e9      # frequency of second pole
R_f  = 10e3     # value of transimpedance
C_s  = 300e-12  # value of source capacitance
C_f  = 0        # value of phantom zero capacitance

cir.defPar('A', A)
cir.defPar('tau_2', 1/2/np.pi/f_p2)
cir.defPar('R_f', R_f)
cir.defPar('C_s', C_s)
cir.defPar('C_f', C_f)

# Perform the analysis
ag     = sl.doLaplace(cir, transfer = 'asymptotic', pardefs='circuit')
lg     = sl.doLaplace(cir, transfer = 'loopgain', pardefs='circuit')
direct = sl.doLaplace(cir, transfer = 'direct', pardefs='circuit')
servo  = sl.doLaplace(cir, transfer = 'servo', pardefs='circuit')
gain   = sl.doLaplace(cir, transfer = 'gain', pardefs='circuit')
figdBmagUncomp = sl.plotSweep('Uncomp', 'Uncompensated transimpedance', 
                              [ag, lg, servo, gain, direct], 1e3, 1e7, 200, 
                              show=SHOW)

# Compensate the amplifier
servoData = sl.findServoBandwidth(lg.laplace)
Bf = servoData['lpf']
f_phz = Bf**2/(np.sqrt(2)*Bf - 1/(2*np.pi*R_f*C_s))
C_phz = 1/(2*np.pi*f_phz*R_f)
cir.defPar('C_f', C_phz)

# Perform the analysis
ag     = sl.doLaplace(cir, transfer = 'asymptotic', pardefs='circuit')
lg     = sl.doLaplace(cir, transfer = 'loopgain', pardefs='circuit')
direct = sl.doLaplace(cir, transfer = 'direct', pardefs='circuit')
servo  = sl.doLaplace(cir, transfer = 'servo', pardefs='circuit')
gain   = sl.doLaplace(cir, transfer = 'gain', pardefs='circuit')
figdBmagComp = sl.plotSweep('Comp', 'Compensated transimpedance', 
                            [ag, lg, servo, gain, direct], 1e3, 1e7, 200, 
                            show=SHOW)

# Limit bandwidth stepwise to 10kHz:
f_max = 10e3
C_max = 1/(f_max*2*np.pi*R_f)

stepDict = {}
stepDict['params'] = 'C_f'
stepDict['method'] = 'log'
stepDict['start']  = C_phz
stepDict['stop']   = C_max
stepDict['num']    = 10

gain = sl.doLaplace(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
figdBmagBWL = sl.plotSweep('BWL', 'Bandwidth limited transimpedance',
                           gain, 1e3, 1e7, 200, show=SHOW)

loopgain = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', 
                        numeric=True, stepdict=stepDict)
figdBmagBWLL = sl.plotSweep('BWLloopgain', 
                         'Loop gain bandwidth limited transimpedance', 
                         loopgain, 1e3, 1e7, 200, show=SHOW)


stepDict['num'] = 100
pServoCf = sl.doPoles(cir, pardefs='circuit', transfer='servo', numeric=True, 
                      stepdict=stepDict)

# Root-locus plots
cir.defPar('C_f', C_phz)
stepDict['params'] = 'A'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = A
stepDict['num']    = 100

servoPolesC_phz    = sl.doPoles(cir, transfer='servo', pardefs='circuit',
                                numeric=True, stepdict=stepDict)

cir.defPar('A_0',A)
loopgainZerosC_phz = sl.doZeros(cir, transfer='loopgain', pardefs='circuit',
                                numeric=True)

figPservoCphz = sl.plotPZ('RL_C_phz', 'Poles $C_f=C_{phz}$.', 
                          [servoPolesC_phz, loopgainZerosC_phz], 
                          xmin=-1, xmax=0, ymin=-0.5, ymax = 0.5, 
                          xscale='M', yscale='M', show=SHOW)

cir.defPar('C_f', C_max)
loopgainZerosC_max = sl.doZeros(cir, transfer='loopgain', pardefs='circuit',
                                numeric=True)

servoPolesC_max = sl.doPoles(cir, transfer='servo', pardefs='circuit',
                                numeric=True, stepdict=stepDict)

figPservoCmax = sl.plotPZ('pRL_C_max', 'Poles $C_f=C_{max}$.', 
                       [servoPolesC_max, loopgainZerosC_max], xmin=-4, xmax=0, 
                       ymin=-2, ymax = 2, xscale='M', yscale='M', show=SHOW)

stepDict['num']    = 1000
stepDict['stop']   = -5e5
servoPolesC_max    = sl.doPoles(cir, transfer='servo', pardefs='circuit',
                                numeric=True, stepdict=stepDict)
figPservoZoom = sl.plotPZ('pRL_C_max_Zoom', 'Poles $C_f=C_{max}$.', 
                          [servoPolesC_max, loopgainZerosC_max], 
                          xmin=-20, xmax=0, ymin=-10, ymax = 10, xscale='k', 
                          yscale='k', show=SHOW)

figPservoCf = sl.plotPZ('pServo', 'Poles step $C_f$.', pServoCf, xmin=-4, 
                        xmax=0, ymin=-2, ymax = 2, xscale='M', yscale='M', 
                        show=SHOW)

sl.htmlPage('Asymptotic-gain model plots')
sl.fig2html(figdBmagUncomp, 800)
sl.fig2html(figdBmagComp, 800)
sl.htmlPage('Bandwidth limitation plots')
sl.fig2html(figdBmagBWL, 800)
sl.fig2html(figdBmagBWLL, 800)
sl.htmlPage('Root locus plots')
sl.fig2html(figPservoCphz, 800)
sl.fig2html(figPservoCmax, 800)
sl.fig2html(figPservoZoom, 800)
sl.fig2html(figPservoCf, 800)
