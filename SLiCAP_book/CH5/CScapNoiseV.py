#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CScapNoiseV.py
"""
import SLiCAP as sl
import sympy as sp
SHOW = False
#sl.initProject('CScapNoiseV')
cir = sl.makeCircuit('kicad/CScapNoiseV/CScapNoiseV.kicad_sch', imgWidth = 400)
# Discard 1/f noise
cir.defPar('KF_N18', 0)
# print important operating point parameters
sl.text2html('The inversion coefficient $IC$ equals: ' +
             '%s'%(sp.N(cir.getParValue('IC_X1'), sl.ini.disp)))
sl.text2html('The critical inversion coefficient $IC_{CRIT}$ equals: ' +
             '%s'%(sp.N(cir.getParValue('IC_CRIT_X1'), sl.ini.disp)))
sl.text2html('The transconductance $g_m$ equals: ' +
             '%s'%(sp.N(cir.getParValue('g_m_X1'), sl.ini.disp)))
# calculate source referred noise spectrum
noiseResult = sl.doNoise(cir, pardefs='circuit', numeric = True)
sl.head2html('Source referred noise')
iNoise = sp.sqrt(noiseResult.inoise)
sl.text2html('The spectrum of the source-referred voltage noise [V/rt(Hz)] ' +
          'is: %s'%(sp.N(iNoise, sl.ini.disp)))
sl.text2html('The plot below shows the source-referred noise spectrum ' +
          'from  100MHz to 100GHz; as expected, it does not depend on ' +
          'the frequency.');
figSin = sl.plotSweep('CScapNoiseVspectrum','Input noise spectrum', noiseResult,
                   1e8, 1e11, 100, funcType='inoise', show = SHOW)
sl.fig2html(figSin,  500)
# Find the width for the lowest noise
sl.htmlPage('Noise performance optimization')
# Delete the numeric definition of W so we can calculate the optimum value
# symbolically
cir.delPar('W')
# Keep IC at IC_CRIT
cir.defPar('ID', '7.44m*W/66u');
Svi_f_W = sl.doNoise(cir, pardefs='circuit', numeric = True).inoise
W = sp.Symbol('W')
# Find optimum value of W
W_opt = sp.solve(sp.diff(Svi_f_W, W), W)
for w in W_opt:
    if w > 0:
        cir.defPar('W', w)
        print(sp.N(w))
sl.text2html('The optimum device width $W_{opt}$ is found as: ' +
          '%s'%(sp.N(cir.getParValue('W'), sl.ini.disp)) + ' [m].')
sl.text2html('At this width we have in input capacitance $c_{iss}$ of: ' +
          '%s'%(sp.N(cir.getParValue('c_iss_X1'), sl.ini.disp)) + ' [F],')
sl.text2html('a drain current $I_{DS}$ of: %s'%(sp.N(cir.getParValue('ID'),
          sl.ini.disp)) + ' [A],')
sl.text2html('and a transadmittance $g_m$ of: %s'%(sp.N(cir.getParValue('g_m_X1'),
          sl.ini.disp)) + ' [S]')
sl.text2html('The plot below shows the total source referred noise over a ' +
          'frequency range from 0.1GHZ to 1GHz as a function of the ' +
          'device width, with the inversion coefficient held constant at ' +
          '$IC_{CRIT}$.')
f_max = 1e9
f_min = 1e8
B = f_max-f_min
cir.defPar('Vni', sp.sqrt(Svi_f_W*B))
# Redefine the width so it can be used as sweep variable, any value is K
cir.defPar('W', 0)
result = sl.doParams(cir)
fig_Vni_W = sl.plotSweep('Vni_W', 'Source-referred noise voltage versus ' +
                      'width: 0.1GHz-1GHz',
                     result, 10, 200, 200, sweepVar = 'W', sweepScale = 'u',
                     funcType = 'param', xUnits = 'm', yVar = 'Vni',
                     yUnits = 'V', yScale='u', show = SHOW)
sl.fig2html(fig_Vni_W, 500)