#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mosPoleSplitting.py
"""
import SLiCAP as sl
import sympy as sp
SHOW = False
sl.initProject('mosPoleSplitting')
cir = sl.makeCircuit('kicad/mosPoleSplitting/mosPoleSplitting.kicad_sch')
sl.htmlPage('Pole splitting in CS stage:')

poles = sl.doPoles(cir, pardefs='circuit', numeric=True).poles
sp.symbols('p_1 p_2')
sumOfPoles = poles[0] + poles[1]
sl.text2html('The sum of the poles in [rad/s] with $c_{dg}=300$fF equals:')
sl.eqn2html('p_1+p_2', sumOfPoles)
cir.defPar('c_dg', 0);

poles = sl.doPoles(cir, pardefs='circuit', numeric=True).poles
sumOfPoles = poles[0] + poles[1]
sl.text2html('The sum of the poles in [rad/s] with $c_{dg}=0$ equals:')
sl.eqn2html('p_1+p_2', sumOfPoles)
sl.htmlPage('Pole splitting with $c_{dg}$')
cir.defPar('c_dg', 20.44e-15);
poles = sl.doPoles(cir, pardefs='circuit', numeric=True).poles
sumOfPoles = poles[0] + poles[1]
sl.text2html('The sum of the poles in [rad/s] with $c_{dg}=20.44$fF equals:')
sl.eqn2html('p_1+p_2', sumOfPoles)

stepDict = {}
stepDict['params'] = 'c_dg'
stepDict['start']  = 0
stepDict['stop']   = '50f'
stepDict['num']    = 100
stepDict['method'] = 'lin'

polesStepped = sl.doPoles(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
figPZ = sl.plotPZ('poleSplitting', 'Poles vs $c_{d_g}$', polesStepped, show = SHOW)
sl.fig2html(figPZ, 500)
