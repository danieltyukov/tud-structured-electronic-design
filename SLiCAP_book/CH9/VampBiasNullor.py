#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:59:59 2020

@author: anton
"""
import SLiCAP as sl
import sympy as sp
from time import time
t1 = time()

#sl.initProject('Vamp bias project')

cir = sl.makeCircuit('kicad/VampBiasNullor/VampBiasNullor.kicad_sch', 
                     imgWidth=400)
DCvalue    = sl.doDC(cir, transfer=None).laplace
DCresult   = sl.doDCsolve(cir)
DCsolution = DCresult.dcSolve
DCvector   = DCresult.Dv

sl.htmlPage('DC analysis')
sl.text2html('The DC voltage $V_6$ is obtained as:')
sl.eqn2html('V_6', DCvalue, units = 'V')
sl.text2html('The DC solution of the network is:')
sl.eqn2html(DCvector, DCsolution)

t2 = time()
print('\n', t2-t1, 's')