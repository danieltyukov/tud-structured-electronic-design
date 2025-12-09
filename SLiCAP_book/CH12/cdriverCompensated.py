#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:58:54 2021

@author: anton
"""
import SLiCAP as sl

SHOW = False

#sl.initProject('cdriverCompensated')
cir = sl.makeCircuit('kicad/cdriverCompensated/cdriverCompensated.kicad_sch')

stepDict = {}
stepDict['params'] = 'R_phz'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = 0.25
stepDict['num']    = 5

polesServo = sl.doPoles(cir, transfer='servo', pardefs='circuit', numeric=True,
                        stepdict=stepDict)
locusR_phz = sl.plotPZ('RootLocusRphz', 'Root locus Rphz', polesServo, 
                       xmin=-200, xmax=100, ymin=-150, ymax=150, xscale='k', 
                       yscale='k', show=SHOW)

sl.fig2html(locusR_phz, 600)

ZoutPassiveESR = sl.doLaplace(cir, pardefs='circuit')
ZoutPassiveESR.gainType = 'passiveESR'

ZoutPassive = sl.doLaplace(cir, source='I2', detector='V_out2', 
                           pardefs='circuit')
ZoutPassive.gainType = 'passive'

# Active phantom zero #########################################################

cir = sl.makeCircuit('kicad/activePHZ/activePHZ.kicad_sch')

pzGain = sl.doPZ(cir, pardefs='circuit', numeric=True)
sl.listPZ(pzGain)

pzLG = sl.doPZ(cir, pardefs='circuit', transfer='loopgain', numeric=True)
sl.listPZ(pzLG)

loopgain = sl.doLaplace(cir, pardefs='circuit', transfer='loopgain').laplace
servoData = sl.findServoBandwidth(loopgain)

for key in servoData.keys():
    print(key,":", servoData[key])
    
stepDict['params'] = 'A_0'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = '300k'
stepDict['num']    = 100

RLservo = sl.doPoles(cir, pardefs='circuit', transfer='servo', numeric=True,
                     stepdict=stepDict)
sl.plotPZ('RLactive', 'RootLocus', RLservo, xmin=-2, xmax=2, ymin=-2, ymax=2, 
       xscale='M', yscale='M', show = SHOW)


ZoutActive = sl.doLaplace(cir, pardefs='circuit')
ZoutActive.gainType = 'active'
Zout = sl.plotSweep('Z-out', 'Z-out', [ZoutPassive, ZoutPassiveESR, ZoutActive]
                    , 1, 10e6, 200, yUnits='$\\Omega$', show=SHOW);
sl.fig2html(Zout, 600);