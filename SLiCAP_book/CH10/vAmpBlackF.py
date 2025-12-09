#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import SLiCAP as sl

#prj = sl.initProject('vAmpBlackF')
cir = sl.makeCircuit('kicad/vAmpBlackF/vAmpBlackF.kicad_sch', imgWidth=400)
gain = sl.doLaplace(cir).laplace

sl.htmlPage('Voltage amplifier with CCCS controller')
sl.text2html('The gain of the system is obtained as:')
sl.eqn2html('V_3/V_s', gain)
