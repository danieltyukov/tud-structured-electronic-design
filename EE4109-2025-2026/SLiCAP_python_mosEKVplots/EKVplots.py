#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:15:00 2020

@author: anton
"""

import SLiCAP as sl

sl.initProject('NMOS EKV plots') # Creates the SLiCAP libraries and the
                             # project HTML index page

cir = sl.makeCircuit('kicad/mosEKVplots/mosEKVplots.kicad_sch')

stepData = {'params': 'V_G',
            'start' : 0.001,
            'stop'  : 1.8,
            'num'   : 10,
            'method': 'lin'}

result = sl.doParams(cir, stepdict=stepData)


# Put the plots on a page
sl.htmlPage('CMOS18 EKV model plots')

fig_Ids_Vds = sl.plotSweep('IdsVds', '$I_{ds}(V_{ds})$', result, 0, 1.8, 50, sweepVar= 'V_D', xUnits = 'V', yVar = 'I_DS_X1', yScale = 'u', yUnits = 'A', funcType = 'param', show = True)
sl.fig2html(fig_Ids_Vds, 600)

stepData['params'] = 'V_D'
result = sl.doParams(cir, stepdict=stepData)

fig_Ids_Vgs = sl.plotSweep('IdsVgs', '$I_{ds}(V_{gs})$', result, 0, 1.8, 50, sweepVar= 'V_G', xUnits = 'V', yVar = 'I_DS_X1', yScale = 'u', yUnits = 'A', funcType = 'param', show = True)
sl.fig2html(fig_Ids_Vgs, 600)

fig_gm_Ids  = sl.plotSweep('gmIds', '$g_m(I_{ds})$', result, 0, 1.8, 50, sweepVar= 'V_G', xVar = 'I_DS_X1', xScale = 'u', xUnits = 'A', yVar = 'g_m_X1', yScale = 'u', yUnits = 'S', funcType = 'param', show = True)
sl.fig2html(fig_gm_Ids, 600)

fig_fT_Ids  = sl.plotSweep('fTIds', '$f_{T}(I_{ds})$', result, 0, 1.8, 50, sweepVar= 'V_G', xVar = 'I_DS_X1', xScale = 'u', xUnits = 'A', yVar = 'f_T_X1', yScale = 'G', yUnits = 'Hz', funcType = 'param', show = True)
sl.fig2html(fig_fT_Ids, 600)

fig_CissVg  = sl.plotSweep('CissVg', '$c_{iss}(V_{gs})$', result, 0, 1.8, 50, sweepVar= 'V_G', xScale = '', xUnits = 'V', yVar = 'c_iss_X1', yScale = 'f', yUnits = 'F', funcType = 'param', show = True)
sl.fig2html(fig_CissVg, 600)