#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CScapNoiseI.py
"""
import SLiCAP as sl
import sympy as sp
SHOW = False
#sl.initProject('CScapNoiseI')
cir = sl.makeCircuit('kicad/CScapNoiseI/CScapNoiseI.kicad_sch', imgWidth = 400)
# Discard 1/f noise
cir.defPar('KF_N18', 0)
noiseResult = sl.doNoise(cir, pardefs='circuit')
sl.head2html('Source referred noise');
sl.text2html('The figure below shows the source referred noise spectrum ' +
          'from  100MHz to 100GHz for $W=W_{opt}$ and at $IC=IC_{CRIT}$.')
figSin = sl.plotSweep('CScapNoiseIspectrum', 'Input noise spectrum', 
                      noiseResult, 1e8, 1e11, 100, funcType='inoise', 
                      show = SHOW)
sl.fig2html(figSin,  500)
IniRMS = sl.rmsNoise(noiseResult, 'inoise', 100e6, 1e9);
sl.text2html('The total source referred RMS current noise $i_{ni}$ amounts: ' +
             '%s [A]'%(sp.N(IniRMS, sl.ini.disp)))