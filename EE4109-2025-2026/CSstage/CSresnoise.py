#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 23:00:31 2020

@author: anton
"""

import SLiCAP as sl
import sympy as sp

sl.initProject('CS stage noise with resistive source')

cir = sl.makeCircuit('kicad/CSresNoise/CSresNoise.kicad_sch')

# Set the drain current at critical inversion
I_D     = cir.getParValue('ID')
IC      = cir.getParValue('IC_X1')
IC_CRIT = cir.getParValue('IC_CRIT_X1')
I_D     = I_D*IC_CRIT/IC

cir.defPar('ID', I_D)

noise_result = sl.doNoise(cir, pardefs="circuit", numeric=True, source="V1", detector="V_out")
sl.plotSweep('Inoise', 'Source-referred noise spectrum', noise_result, 1e8, 1e11, 100, funcType = 'inoise', show=True)

# Calculate the noise figure at critical inversion and the given width
tot_inoise     = sl.rmsNoise(noise_result, 'inoise', 1e9, 5e9)
tot_inoise_src = sl.rmsNoise(noise_result, 'inoise', 1e9, 5e9, 
                             source="I_noise_R1")
NF             = 20*sp.log(tot_inoise/tot_inoise_src)/sp.log(10)
print("The noise figure equals: %s [dB]."%(sp.N(NF, sl.ini.disp)))

# We will now calculate the width W at which we will have the best noise performance.
# Define the variable 'W' in the notebook environment
Width = cir.getParValue("W")
W     = sp.Symbol('W')
cir.delPar('W')        # delete the numeric definition of the width
# We will keep the inversion coefficient at critical inversion, hence we scale the
# current with the width.
# Please know that not scaling the current results in expressions that cannot be integrated symbolically.
# We will then need numeric methods for determination of the optimum width.
cir.defPar('ID', I_D*W/Width)
# calculate the noise spectra as a function of W and f
noise_w = sl.doNoise(cir, pardefs="circuit", numeric=True, source="V1", detector="V_out") 
# Calculate the noise figure as a function of W over a frequency range from 'fmin' to 'fmax':
f_min = sp.Symbol('f_min')
f_max = sp.Symbol('f_max')
rms_noise_w        = sl.rmsNoise(noise_w, 'inoise', f_min, f_max)
rms_noise_w_source = sl.rmsNoise(noise_w, 'inoise', f_min, f_max, 
                              source="I_noise_R1")
# We will now calculate the noise figure as a function of 'W', 'f_min' and 'f_max':
# We will use the variance instead of the RMS value:
NF_W  = (rms_noise_w/rms_noise_w_source)**2
# We will now calculate the optimum width as a function of 'fmin' and 'fmax':
W_opt = sp.solve(sp.diff(NF_W, W), W)
# The sympy solve function returns a list with solutions, we will print the positive ones
# that are positive over a frequency range of interest.
for w in W_opt:
    w = sp.N(w.subs([(f_min, 1e9), (f_max, 5e9)]), sl.ini.disp)
    if w > 0:
        W = w
        print(W)

# Create a plot of the noise figure versus the with for different values of f_max and f_min = 1G
# Define the plot parameters, 'fw', 'W' and 'fmax'
cir.defPar('W', W)
cir.defPar('f_max', '10G')
cir.defPar('NF', 10*sp.log(NF_W.subs([(f_min, 2e8)]))/sp.log(10))
# Define the step parameters
stepDict = {"params"  : "f_max",
            "start"   : "2G",
            "stop"    : "10G",
            "method"  : "lin",
            "num"     : 5}
result = sl.doParams(cir, pardefs="circuit", numeric=True, stepdict=stepDict)
# Plot the function
fig_NF_W = sl.plotSweep('NF_W', 'Noise Figure versus width, $f_{min}$ = 200MHz', 
                        result, 10, 200, 50, sweepVar = 'W', sweepScale = 'u', 
                        funcType = 'param', xUnits = 'm', yVar = 'NF', 
                        yUnits = 'dB', show = True)