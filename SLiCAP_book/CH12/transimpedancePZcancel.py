#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
import sympy as sp
SHOW = False

sl.initProject('transimpedancePZcancel')
cir = sl.makeCircuit('kicad/transimpedancePZcancel/transimpedancePZcancel.kicad_sch')

poles = sl.doPoles(cir, transfer='loopgain', pardefs='circuit', numeric=True)
# Display the DC value and poles and zeros of the loop gain
sl.listPZ(poles)

# Display zeros
zeros = sl.doZeros(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(zeros)

# Display, poles, zeros and DC gain
pz = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(pz)

# Calculate the phase margin
L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
loopGain = L.laplace
pmResults = sl.phaseMargin(loopGain)

uF = pmResults[1]
pM = pmResults[0]

print('Loop gain: phase margin = {:3.2f}deg at f = {:8.2e}Hz\n'.format(pM, uF))

# Show the poles, zeros and DC value of the gain
pzG = sl.doPZ(cir, transfer='gain', pardefs='circuit', numeric=True)
sl.listPZ(pzG)

# Modified compensation
print('=== Modified compensation C_z = 200p. ===\n')
cir.defPar('C_z', '200p')

L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
loopGain = L.laplace
pmResults = sl.phaseMargin(loopGain)

uF = pmResults[1]
pM = pmResults[0]

print('Loop gain: phase margin = {:3.2f}deg at f = {:8.2e}Hz\n'.format(pM, uF))

pzL = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(pzL)

stepDict           = {}
stepDict['params'] = 'C_z'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = '200p'
stepDict['num']    = 100

result = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', 
                      numeric=True, stepdict=stepDict)

PM = [result.stepList, sl.phaseMargin(result.laplace)[0]]

plotData = {'PhaseMargin vs C_z': PM}
figPM = sl.plot('PM', 'Phase margin versus C_z', 'lin', plotData, 
                xName = stepDict['params'], xScale = 'p', 
                xUnits = 'F', yName = 'Phase margin', yUnits = 'deg', show=SHOW)

stepDict['start']  = '50p'
stepDict['num']    = 4
result = sl.doStep(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
stepPZcancel = sl.plotSweep('stepPZcancel', 'Unit step response lag compensation', 
                            result, 0, 3, 200, sweepScale='u', yScale='k', 
                            show=SHOW)

result = sl.doLaplace(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
dBmagStepped = sl.plotSweep('dBmagSteppedCancelPZ', 'Lag compensation', result,
                            1, 10e3, 200, sweepScale='k', show = SHOW)
phaseStepped = sl.plotSweep('PhaseSteppedCancelPZ', 'Lag compensation', result,
                            1, 10e3, 200, sweepScale='k', funcType='phase', 
                            show=SHOW)


stepDict['params'] = 'A_0'
stepDict['method'] = 'log'
stepDict['start']  = 1
stepDict['stop']   = 1e6
stepDict['num']    = 500

polesS = sl.doPoles(cir, transfer='servo', pardefs='circuit', numeric=True, 
                    stepdict=stepDict)

zerosL = sl.doZeros(cir, transfer='loopgain', pardefs='circuit', numeric=True)
pzRLpzComp = sl.plotPZ('pzRLpzComp', 'Lag compensation root locus', 
                       [polesS, zerosL], xmin=-2, xmax=0, ymin=-1, 
                       ymax=1, xscale='M', yscale='M', show=SHOW)
pzRLpzCompZoom = sl.plotPZ('pzRLpzCompZoom', 'Lag compensation root locus', 
                           [polesS, zerosL], xmin=-0.5, xmax=0, ymin=-0.25, 
                           ymax=0.25, xscale='M', yscale='M', show=SHOW)

pzGain = sl.doPZ(cir, transfer='gain', pardefs='circuit', numeric=True)
sl.listPZ(pzGain)