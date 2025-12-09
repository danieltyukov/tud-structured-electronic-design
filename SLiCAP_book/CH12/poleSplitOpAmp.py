#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 12:00:14 2021

@author: anton
"""
import SLiCAP as sl

SHOW = False
#sl.initProject('poleSplitOpamp')
cir = sl.makeCircuit('cir/poleSplitOpamp.cir', imgWidth=None)
denom_1 = sl.doDenom(cir, pardefs='circuit').denom

print("\nCharacteristic equation without pole splitting:\n", denom_1)

poles = sl.doPoles(cir, pardefs='circuit').poles

for i in range(len(poles)):
    print("p_" + str(i+1), '=', poles[i])

# With pole splitting:
denom_2 = sl.doDenom(cir).denom

print("\nCharacteristic equation with pole splitting:\n", denom_2)

cir.defPars({'R_a':'10k', 'C_a':'100p', 'tau':'100u', 'A_0':'100k'})


stepDict = {}
stepDict['params'] = 'C_c'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = 2e-12
stepDict['num']    = 10

poles = sl.doPoles(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
pSplitPZ = sl.plotPZ('pSplitPZ2k', 'Pole splitting', poles, xmin=-5, xmax=0, 
                     ymin =-1, ymax = 1, xscale='M', show=SHOW)

gain  = sl.doLaplace(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
pSplitBode = sl.plotSweep('pSplitBodeMag', 'Pole splitting', gain, 10, 10e6, 
                          200, funcType='dBmag', show=SHOW)
sl.fig2html(pSplitBode, 600)
sl.htmlPage('plots')
sl.fig2html(pSplitPZ, 600)