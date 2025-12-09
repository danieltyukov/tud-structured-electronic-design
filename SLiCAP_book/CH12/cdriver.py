#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:58:54 2021

@author: anton
"""
import SLiCAP as sl
#sl.initProject('cdriver')
cir = sl.makeCircuit('kicad/cdriver/cdriver.kicad_sch', imgWidth=600)

polesL = sl.doPoles(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(polesL)

zerosL = sl.doZeros(cir, transfer='loopgain', pardefs='circuit', numeric=True)
sl.listPZ(zerosL)

loopgain = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', 
                        numeric=True).laplace
servoData = sl.findServoBandwidth(loopgain)
for key in servoData.keys():
    print(key,":", servoData[key])
gain, numerCoeffs, denomCoeffs = sl.coeffsTransfer(loopgain)

print("\nGain factor:", gain)
print("\nNumerator coefficients of s:\n----------------------------")
for i in range(len(numerCoeffs)):
    print(i, numerCoeffs[i])
print("\nDenominator coefficients of s:\n------------------------------")
for i in range(len(denomCoeffs)):
    print(i, denomCoeffs[i])

polesG = sl.doPoles(cir, transfer='gain', pardefs='circuit', numeric=True)
sl.listPZ(polesG);