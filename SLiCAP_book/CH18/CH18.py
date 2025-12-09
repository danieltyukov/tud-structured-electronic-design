#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 29 12:34:51 2021

@author: anton
"""

import SLiCAP as sl 

sl.initProject('CH18')

cir = sl.makeCircuit('cir/NA-2.cir', imgWidth=None)
result = sl.doLaplace(cir)
sl.htmlPage('Results')
sl.head2html('Matrix equation')
sl.matrices2html(result)
sl.head2html('Transimpedance')
sl.eqn2html('Z_t', result.laplace)