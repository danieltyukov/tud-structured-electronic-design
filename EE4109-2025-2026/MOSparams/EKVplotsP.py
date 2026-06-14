#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:15:00 2020

@author: anton
"""

import SLiCAP as sl

#sl.initProject('PMOS EKV plots') # Creates the SLiCAP libraries and the
                                 # project HTML index page

fileName = 'mosEKVplotsP.cir'

cir = sl.makeCircuit(fileName)

# Put the plots on a page
sl.htmlPage('CMOS18 EKV model plots')

result = sl.doParams(cir)

fig_Ids_Vgs = sl.plotSweep('IdsVgs', '$V_{gs}(I_{ds})$', result, -0.001, -35, 200, 
                           sweepVar= 'I_D', sweepScale = 'u', yVar = 'I_D', 
                           yUnits = 'A', yScale = 'u',  xVar = 'V_GS_X1', 
                           xUnits = 'V', funcType = 'param', show = True)
sl.fig2html(fig_Ids_Vgs, 600)

fig_gm_Ids  = sl.plotSweep('gmIds', '$g_m(I_{ds})$', result, -0.001, -35, 100, 
                           sweepVar= 'I_D', sweepScale = 'u', xUnits = 'A', 
                           yVar = 'g_m_X1', yScale = 'u', yUnits = 'S', 
                           funcType = 'param', show = True)
sl.fig2html(fig_gm_Ids, 600)

fig_fT_Ids  = sl.plotSweep('fTIds', '$f_{T}(I_{ds})$', result, -0.001, -35, 100, 
                           sweepVar= 'I_D', sweepScale = 'u', xUnits = 'A', 
                           yVar = 'f_T_X1', yScale = 'G', yUnits = 'Hz', 
                           funcType = 'param', show = True)
sl.fig2html(fig_fT_Ids, 600)

fig_CissVg  = sl.plotSweep('CissVg', '$c_{iss}(V_{gs})$', result, -0.001, -35, 100, 
                           sweepVar= 'I_D', sweepScale="u", xVar = "V_GS_X1", 
                           xScale = '', xUnits = 'V', yVar = 'c_iss_X1', 
                           yScale = 'f', yUnits = 'F', funcType = 'param', 
                           show = True)
sl.fig2html(fig_CissVg, 600)
