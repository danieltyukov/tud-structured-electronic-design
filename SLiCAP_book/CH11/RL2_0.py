#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import SLiCAP as sl
SHOW = False
fileName = 'RL2_0'
sl.initProject(fileName)
cir = sl.makeCircuit(sl.ini.cir_path + fileName + '.cir', imgWidth=None)
sl.htmlPage('Root locus plot: ', fileName)
pzL = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
stepDict = {}
stepDict['params'] = 'A_0'
stepDict['method'] = 'lin'
stepDict['start']  = 0
stepDict['stop']   = 20
stepDict['num']    = 500
plsS = sl.doPoles(cir, transfer='servo', pardefs='circuit', numeric=True, 
                  stepdict=stepDict)
figPZ = sl.plotPZ(fileName, fileName, [plsS, pzL], xmin=-100, xmax=0, ymin=-100, ymax=100, show = SHOW)
sl.fig2html(figPZ, 500)