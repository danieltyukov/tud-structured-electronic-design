#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
SHOW = False
fileName = 'RL1_R'
sl.initProject(fileName)
cir = sl.makeCircuit(sl.ini.cir_path + fileName + '.cir', imgWidth=None)
sl.htmlPage('Root locus plot: ', fileName)
pzL = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
stepDict = {}
stepDict['params'] = 'A_0'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = 3
stepDict['num']    = 100
plsS = sl.doPoles(cir, transfer='servo', pardefs='circuit', numeric=True, 
                  stepdict=stepDict)
figPZ = sl.plotPZ(fileName, fileName, [plsS, pzL], xmin=-200, xmax=0, ymin=-1, ymax=1, show = SHOW)
sl.fig2html(figPZ, 500)