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
# sl.initProject('NMOS EKV plots') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'mosEKVplotsN_V.cir'

cir = sl.makeCircuit('mosEKVplotsN_V.cir', imgWidth=None)

# Put the plots on a page
sl.htmlPage('CMOS18 EKV model plots')

cir.defPar('V_G', 1.8)
cir.defPar('V_D', 1.8)


stepDict = {'start'  : 0.6,
            'stop'   : 1.8,
            'num'    : 6,
            'method' : 'lin',
            'params' : 'V_G'}

result = sl.doParams(cir, stepdict=stepDict)

fig_Ids_Vds = sl.plotSweep('CMOS18N_V_IdsVds', '$I_{ds}(V_{ds})$', result, 0, 1.8, 50, sweepVar= 'V_D', xUnits = 'V', yVar = 'I_DS_X1', yScale = 'u', yUnits = 'A', funcType = 'param', show = SHOW)
sl.fig2html(fig_Ids_Vds, 600)

stepDict['params'] = 'V_D'

result = sl.doParams(cir, stepdict=stepDict)
fig_Ids_Vgs = sl.plotSweep('CMOS18N_V_IdsVgs', '$I_{ds}(V_{gs})$', result, 0, 1.8, 50, axisType = 'lin', sweepVar= 'V_G', xUnits = 'V', yVar = 'I_DS_X1', yScale = 'u', yUnits = 'A', funcType = 'param', show = SHOW)
sl.fig2html(fig_Ids_Vgs, 600)

fig_Ids_Vgs_Log = sl.plotSweep('CMOS18N_V_IdsVgsLog', '$I_{ds}(V_{gs})$', result, 0.01, 1.8, 50, axisType = 'semilogy', sweepVar= 'V_G', xUnits = 'V', yVar = 'I_DS_X1', yScale = 'u', yUnits = 'A', funcType = 'param', show = SHOW)
sl.fig2html(fig_Ids_Vgs_Log, 600)

fig_gm_Ids  = sl.plotSweep('CMOS18N_V_gmIds', '$g_m(I_{ds})$', result, 0, 1.8, 50, sweepVar= 'V_G', xVar = 'I_DS_X1', xScale = 'u', xUnits = 'A', yVar = 'g_m_X1', yScale = 'u', yUnits = 'S', funcType = 'param', show = SHOW)
sl.fig2html(fig_gm_Ids, 600)

fig_fT_Ids  = sl.plotSweep('CMOS18N_V_fTIds', '$f_{T}(I_{ds})$', result, 0, 1.8, 50, sweepVar= 'V_G', xVar = 'I_DS_X1', xScale = 'u', xUnits = 'A', yVar = 'f_T_X1', yScale = 'G', yUnits = 'Hz', funcType = 'param', show = SHOW)
sl.fig2html(fig_fT_Ids, 600)

fig_CissVg  = sl.plotSweep('CMOS18N_V_CissVg', '$c_{iss}(V_{gs})$', result, 0, 1.8, 50, sweepVar= 'V_G', xScale = '', xUnits = 'V', yVar = 'c_iss_X1', yScale = 'f', yUnits = 'F', funcType = 'param', show = SHOW)
sl.fig2html(fig_CissVg, 600)

LTspiceTraces =  sl.LTspiceData2Traces('nmosChar.txt')
sl.traces2fig(LTspiceTraces, fig_Ids_Vgs)
sl.traces2fig(LTspiceTraces, fig_Ids_Vgs_Log)
fig_Ids_Vgs.plot()
fig_Ids_Vgs_Log.plot()

figLT = sl.plot('LTspiceIdsVgs', 'LTspice $I_{ds}(V_{gs})$', 'lin', LTspiceTraces, xName = '$V_{gs}$', xUnits = 'V', yName = '$I_{ds}$', yUnits = 'A', yScale = 'u', show = SHOW)
sl.fig2html(figLT, 600)
t2=time()
print(t2-t1,'s')
