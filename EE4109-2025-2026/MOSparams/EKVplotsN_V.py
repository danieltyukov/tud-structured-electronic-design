#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:15:00 2020

@author: anton
"""

import SLiCAP as sl

#sl.initProject('NMOS EKV plots') # Creates the SLiCAP libraries and the
                                 # project HTML index page

fileName = 'mosEKVplotsN_V.cir'

cir = sl.makeCircuit(fileName)

# Put the plots on a page
sl.htmlPage('CMOS18 EKV model plots')


cir.defPar('V_G', 1.8)
cir.defPar('V_D', 1.8)

# Create the step instruction (dictionary)
step_dict = {"params": "V_G",
             "method": "lin",
             "start" :  0.6,
             "stop"  :   1.8,
             "num"   : 3}


result = sl.doParams(cir, stepdict=step_dict)

fig_Ids_Vds = sl.plotSweep('IdsVds', '$I_{ds}(V_{ds})$', result, 0, 1.8, 50, 
                           sweepVar= 'V_D', xUnits = 'V', yVar = 'I_DS_X1', 
                           yScale = 'u', yUnits = 'A', funcType = 'param', 
                           show = True)
sl.fig2html(fig_Ids_Vds, 600)

step_dict['params'] = 'V_D'
result = sl.doParams(cir, stepdict=step_dict)

fig_Ids_Vgs = sl.plotSweep('IdsVgs', '$I_{ds}(V_{gs})$', result, 0, 1.8, 50, 
                           axisType = 'lin', sweepVar= 'V_G', xUnits = 'V', 
                           yVar = 'I_DS_X1', yScale = 'u', yUnits = 'A', 
                           funcType = 'param', show = True)
sl.fig2html(fig_Ids_Vgs, 600)

fig_gm_Ids  = sl.plotSweep('gmIds', '$g_m(I_{ds})$', result, 0, 1.8, 50, 
                           sweepVar= 'V_G', xVar = 'I_DS_X1', xScale = 'u', 
                           xUnits = 'A', yVar = 'g_m_X1', yScale = 'u', 
                           yUnits = 'S', funcType = 'param', show = True)
sl.fig2html(fig_gm_Ids, 600)

fig_fT_Ids  = sl.plotSweep('fTIds', '$f_{T}(I_{ds})$', result, 0, 1.8, 50, 
                           sweepVar= 'V_G', xVar = 'I_DS_X1', xScale = 'u', 
                           xUnits = 'A', yVar = 'f_T_X1', yScale = 'G', 
                           yUnits = 'Hz', funcType = 'param', show = True)
sl.fig2html(fig_fT_Ids, 600)

fig_CissVg  = sl.plotSweep('CissVg', '$c_{iss}(V_{gs})$', result, 0, 1.8, 50, 
                           sweepVar= 'V_G', xScale = '', xUnits = 'V', 
                           yVar = 'c_iss_X1', yScale = 'f', yUnits = 'F', 
                           funcType = 'param', show = True)
sl.fig2html(fig_CissVg, 600)
