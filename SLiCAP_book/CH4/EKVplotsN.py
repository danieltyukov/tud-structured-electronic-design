#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:15:00 2020

@author: anton
"""

import SLiCAP as sl
from time import time
t1 = time()
SHOW = False
#sl.initProject('NMOS EKV plots') # Creates the SLiCAP libraries and the
                             # project HTML index page

cir = sl.makeCircuit('mosEKVplotsN.cir', imgWidth=None)

result = sl.doParams(cir)
# Put the plots on a page
sl.htmlPage('CMOS18 EKV model plots')

fig_Ids_Vgs  = sl.plotSweep('CMOS18N_IdsVgs', '$V_{gs}(I_{ds})$', result, 1e-3, 150, 200, sweepVar= 'I_D', sweepScale = 'u', yVar = 'I_D', yUnits = 'A', yScale = 'u',  xVar = 'V_GS_X1', xUnits = 'V', funcType = 'param', show = SHOW)
sl.fig2html(fig_Ids_Vgs, 600)

fig_gm_Ids  = sl.plotSweep('CMOS18N_gmIds', '$g_m(I_{ds})$', result, 0, 150, 100, sweepVar= 'I_D', sweepScale = 'u', xUnits = 'A', yVar = 'g_m_X1', yScale = 'u', yUnits = 'S', funcType = 'param', show = SHOW)
sl.fig2html(fig_gm_Ids, 600)

fig_fT_Ids  = sl.plotSweep('CMOS18N_fTIds', '$f_{T}(I_{ds})$', result, 0, 150, 100, sweepVar= 'I_D', sweepScale = 'u', xUnits = 'A', yVar = 'f_T_X1', yScale = 'G', yUnits = 'Hz', funcType = 'param', show = SHOW)
sl.fig2html(fig_fT_Ids, 600)

LTspiceTraces =  sl.LTspiceData2Traces('NMOS-gm-testbench.txt')
sl.traces2fig(LTspiceTraces, fig_gm_Ids)
fig_gm_Ids.plot()

LTspiceTraces =  sl.LTspiceData2Traces('NMOS-fT-testbench.txt')
sl.traces2fig(LTspiceTraces, fig_fT_Ids)
fig_fT_Ids.plot()

t2=time()
print(t2-t1,'s')
