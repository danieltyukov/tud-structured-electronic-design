#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 08:59:59 2020

@author: anton
"""
import SLiCAP as sl
import sympy as sp
from time import time

t1 = time()

#sl.initProject('Vamp bias project')

cir = sl.makeCircuit('kicad/VampFeedbackBiasTotal/VampFeedbackBiasTotal.kicad_sch',
                     imgWidth = 600)

V_outDC = sl.doDC(cir, transfer=None).laplace

sl.htmlPage('Feedback biasing')
sl.text2html('The DC output voltage $V_{outDC}$ is:')
sl.eqn2html('V_outDC', V_outDC)

sigma_Vout = sp.sqrt(sl.assumeRealParams(sl.doDCvar(cir, transfer=None).ovar))

# Laplace transfer function

transfer = sl.doLaplace(cir).laplace
sl.text2html('The voltage transfer $A_v$ from source to load is:')
sl.eqn2html('A_v(s)', transfer)
hf = sp.limit(transfer, sl.ini.laplace, 'oo')
sl.text2html('For high frequencies this can be written as:')
sl.eqn2html('A_v(oo)', hf)
sl.text2html('The standard deviation of the output voltage equals that of ' +
             'the reference voltage::')
sl.eqn2html('sigma_Vout', sigma_Vout)
t2 = time()
print('\n', t2-t1, 's')