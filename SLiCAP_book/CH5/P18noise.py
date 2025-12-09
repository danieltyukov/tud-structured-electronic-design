#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P18noise.py
"""
import SLiCAP as sl
import sympy as sp
SHOW = False
#sl.initProject('P18noise')

cir = sl.makeCircuit('kicad/P18noise/P18noise.kicad_sch')
# Plot S_vi for ID=-10uA, step W and L, while keeping W/L=1
cir.defPar('ID','-10u')
sl.htmlPage('Voltage noise PMOS')
stepDict = {}
stepDict['params'] = 'W'
stepDict['method'] ='list'
stepDict['values']   = [1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6]

noiseResult = sl.doNoise(cir, pardefs='circuit', numeric=True, stepdict=stepDict)

SvP18mos = sl.plotSweep('SvP18mos', 'Svi V/rt(Hz) PMOS W/L=1 ID=-10uA',
                        noiseResult, 10, 100e6, 200, funcType='inoise', 
                        show = SHOW)
sl.fig2html(SvP18mos, 800)

# Another method is to calculate S_vi(f, W), define it as a circuit parameter
# and plot this parameter.
# Calculate the function and define it as a circuit parameter
cir.delPar('W') # Delete the definition of W, this keeps it a symbolic variable
inoise_f_W = sl.doNoise(cir, pardefs='circuit').inoise # calculate S_vi(f,W)
cir.defPar('Si_f_W', inoise_f_W) # define a circuit parameter for this function
cir.defPar('W', '1u')  # Redefine the parameter W otherwise it cannot be stepped
cir.defPar('f', 1)     # Define the parameter f otherwise it cannot be swept
result = sl.doParams(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
S_vi_f_W_P = sl.plotSweep('S_vi_f_W_P', 'Svi V/rt(Hz) noise PMOS W/L=1 ID=-10uA',
                          result, 10, 100e6, 200, funcType='param', 
                          axisType='log', sweepVar='f', xUnits='Hz', 
                          yVar='Si_f_W', yUnits='$V^2/Hz$', show = SHOW)
sl.fig2html(S_vi_f_W_P, 800)
# Plot f_T and f_l versus W for W/L=1 and ID=-10uA (dataType = 'params')
result = sl.doParams(cir, pardefs='circuit', numeric=True)
f_T_f_L_P = sl.plotSweep('f_T_f_L_P', '$f_T,\\, f_{\\ell}, PMOS W/L=1 ID=-10uA$', 
                         result, 2e-6, 500e-6, 200, funcType='param', 
                         axisType='log', sweepVar='W', xUnits='m', xScale='u',
                         yVar=['f_T_X1', 'f_ell_X1'], yScale='G', yUnits='Hz',
                         show = SHOW)
sl.fig2html(f_T_f_L_P, 800)
cir.delPar('f')      # Remove the numeric definition of the frequency
# Plot S_vi for W = L = 50u while stepping ID
cir.defPar('W', '200u')
stepDict['params'] = 'ID'
stepDict['values'] = [-10e-6, -20e-6, -50e-6, -100e-6, -1e-3, -2e-3, -5e-3]
noiseResult = sl.doNoise(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
SvP18mos200u = sl.plotSweep('SvP18mos50u', 'Svi V/rt(Hz) noise W=50u', 
                            noiseResult, 1, 1e6, 200, funcType='inoise', 
                            show = SHOW)
sl.fig2html(SvP18mos200u, 800)