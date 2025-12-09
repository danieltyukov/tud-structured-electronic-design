#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N18noise.py
"""
import SLiCAP as sl
import sympy as sp
SHOW = False
#sl.initProject('N18noise');

cir = sl.makeCircuit('kicad/N18noise/N18noise.kicad_sch')
# Plot S_vi for ID=10uA, step W and L, while keeping W/L=1
cir.defPar('ID','10u')
sl.htmlPage('Voltage noise NMOS')
stepDict = {}
stepDict['params'] = 'W'
stepDict['method'] ='list'
stepDict['values']   = [0.2e-6, 0.5e-6, 1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6]

noiseResult = sl.doNoise(cir, pardefs='circuit', numeric=True, stepdict=stepDict)

SvN18mos = sl.plotSweep('SvN18mos', 'Svi V/rt(Hz) NMOS W/L=1 ID=10uA',
                        noiseResult, 10, 100e6, 200, funcType='inoise', 
                        show = SHOW)
sl.fig2html(SvN18mos, 800)

# Another method is to calculate S_vi(f, W), define it as a circuit parameter
# and plot this parameter.
# Calculate the function and define it as a circuit parameter
cir.delPar('W') # Delete the definition of W, this keeps it a symbolic variable
inoise_f_W = sl.doNoise(cir, pardefs = 'circuit').inoise   # calculate S_vi(f,W)

cir.defPar('Si_f_W', inoise_f_W) # define a circuit parameter for this function
cir.defPar('W', '1u') # Redefine the parameter W otherwise it cannot be stepped
cir.defPar('f', 1)    # Define the parameter f otherwise it cannot be swept

result = sl.doParams(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
S_vi_f_W_N = sl.plotSweep('S_vi_f_W_N', 'Svi V/rt(Hz) noise NMOS W/L=1 ID=10uA',
                          result, 10, 100e6, 200, funcType='param', 
                          axisType='log', sweepVar='f', xUnits='Hz', 
                          yVar='Si_f_W', yUnits='$V^2/Hz$', show = SHOW)
sl.fig2html(S_vi_f_W_N, 800)
# Plot f_T and f_l versus W for W/L=1 and ID=10uA
result = sl.doParams(cir, pardefs='circuit', numeric=True)
f_T_f_L_N = sl.plotSweep('f_T_f_L_N', '$f_T,\\, f_{\\ell}, NMOS W/L=1 ID=10uA$', 
                         result, 0.2e-6, 50e-6, 200, funcType='param', 
                         axisType='log', sweepVar='W', xUnits='m', xScale='u',
                         yVar=['f_T_X1', 'f_ell_X1'], yScale='G', yUnits='Hz',
                         show = SHOW)
sl.fig2html(f_T_f_L_N, 800)

cir.delPar('f')      # Remove the numeric definition of the frequency
# Plot S_vi for W = L = 50u while stepping ID
cir.defPar('W', '50u')

stepDict['params'] = 'ID'
stepDict['method'] ='list'
stepDict['values'] = [10e-6, 20e-6, 50e-6, 100e-6, 1e-3, 2e-3, 5e-3]

noiseResult = sl.doNoise(cir, pardefs='circuit', numeric=True, stepdict=stepDict)
SvN18mos50u = sl.plotSweep('SvN18mos50u', 'Svi V/rt(Hz) noise W=50u', 
                           noiseResult, 1, 1e6, 200, funcType='inoise', 
                           show = SHOW)
sl.fig2html(SvN18mos50u, 800)