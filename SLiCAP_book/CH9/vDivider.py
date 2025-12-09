#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 08:59:59 2020

@author: anton
"""
import SLiCAP as sl
from time import time
t1 = time()

#sl.initProject('Vamp bias project') 

cir = sl. makeCircuit('kicad/vDivider/vDivider.kicad_sch', imgWidth=700) 
result = sl.doDCvar(cir)

sl.htmlPage('DC variance analysis')
sl.dcVar2html(result)
t2 = time()
print('\n', t2-t1, 's')