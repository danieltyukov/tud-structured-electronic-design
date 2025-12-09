#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
import sympy as sp
SHOW = False

#sl.initProject('transimpedanceCompensatedSource')
cir = sl.makeCircuit('kicad/transimpedanceCompensatedSource/transimpedanceCompensatedSource.kicad_sch')

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
C_s = cir.getParValue('C_s')
# Calculate compensation capacitance
R_phz = sp.N((sp.sqrt(2)*Bw + p_1 + p_2)/C_s/Bw**2/2/sp.pi)
# Pass the value to the circuit
cir.defPar('R_phz', R_phz)
# Print the value of C_phz
print('R_phz = {:9.2e}Ohm\n'.format(R_phz))
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