#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
import sympy as sp
SHOW = False

#sl.initProject('transimpedanceCompensated')
cir = sl.makeCircuit('kicad/transimpedanceCompensated/transimpedanceCompensated.kicad_sch')

result = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
# Display the DC value and poles and zeros of the loop gain
sl.listPZ(result)
polesLG = result.poles
# Extract data for compensation
p_1 = polesLG[0]/2/sp.pi
p_2 = polesLG[1]/2/sp.pi
L_0 = result.DCvalue
# Calculate achievable bandwidth
Bw = sp.sqrt(sp.Abs((1-L_0)*p_1*p_2))
R_f = cir.getParValue('R_f')
# Calculate compensation capacitance
C_phz = sp.N((sp.sqrt(2)*Bw + p_1 + p_2)/R_f/Bw**2/2/sp.pi)
# Pass the value to the circuit
cir.defPar('C_phz', C_phz)
# Print the value of C_phz
print('C_phz = {:9.2e}F\n'.format(C_phz))
# Display the DC value and poles and zeros of the loop gain
LGpz = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(LGpz)
# Display the DC value and poles and zeros of the gain
Gpz = sl.doPZ(cir, transfer='gain', pardefs='circuit', numeric=True)
sl.listPZ(Gpz)

# Create the Bode plots
G = sl.doLaplace(cir, transfer='gain', pardefs='circuit', numeric=True)
A = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
S = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
D = sl.doLaplace(cir, transfer='direct', pardefs='circuit', numeric=True)
dbMagPlot = sl.plotSweep('transimpedanceCompensatedBodeDBmag', 'transimpedance',
                         [A,L,S,D,G], 1e4, 10e9, 200, funcType='dBmag', show=SHOW)
phasePlot = sl.plotSweep('transimpedanceCompensatedBodePhase', 'transimpedance', 
                         [A,L,S,D,G], 1e4, 10e9, 200, funcType='phase', show=SHOW)

sl.htmlPage('Phantom zero compensation')
sl.fig2html(dbMagPlot, 600)
sl.fig2html(phasePlot, 600)

# limitation of the bandwidth to 200kHz #######################################
print('=== Bandwidth limitation to 200kHz ===')
cir.defPar('C_phz', '1/2/pi/2e5/R_f')
# Display the DC value and poles and zeros of the asymptotic gain model
ApzLim = sl.doPZ(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
sl.listPZ(ApzLim)

LpzLim = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(LpzLim)

SpzLim = sl.doPZ(cir, transfer='servo', pardefs='circuit', numeric=True)
sl.listPZ(SpzLim)

GpzLim = sl.doPZ(cir, transfer='gain', pardefs='circuit', numeric=True)
sl.listPZ(GpzLim)

# Generate the Bode plots
GR = sl.doLaplace(cir, transfer='gain', pardefs='circuit', numeric=True)
AR = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
LR = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
SR = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
DR = sl.doLaplace(cir, transfer='direct', pardefs='circuit', numeric=True)

dbMagPlotR = sl.plotSweep('transimpedanceCompensatedBodeDBmag200kHz', 
                          'transimpedance B=200kHz', [AR, LR, SR, DR, GR], 
                          1e4, 10e9, 200, funcType='dBmag', show=SHOW)
phasePlotR = sl.plotSweep('transimpedanceCompensatedBodePhase200kHz', 
                          'transimpedance B=200kHz', [AR, LR, SR, DR, GR], 
                          1e4, 10e9, 200, funcType='phase', show=SHOW)
sl.fig2html(dbMagPlotR, 600)
sl.fig2html(phasePlotR, 600)

# generate root locus plot
pA = sl.doPoles(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
pL = sl.doPoles(cir, transfer='loopgain', pardefs='circuit', numeric=True)
zL = sl.doZeros(cir, transfer='loopgain', pardefs='circuit', numeric=True)
pG = sl.doPoles(cir, transfer='gain', pardefs='circuit', numeric=True)

stepDict = {}
stepDict['params'] = 'A_0'
stepDict['method'] = 'log'
stepDict['start']  = 0.01
stepDict['stop']   = 1e6
stepDict['num']    = 2000

RL = sl.doPoles(cir, transfer='servo', pardefs='circuit', numeric=True, 
                stepdict=stepDict)
figRL = sl.plotPZ('transimpedanceCompensatedRL200kHz.svg', 'Root Locus', 
                  [pA, pL, zL, pG, RL], xmin=-0.4, xmax=0, ymin=-0.2, ymax=0.2,
                  xscale='M', yscale='M', show=SHOW)
sl.fig2html(figRL, 600)