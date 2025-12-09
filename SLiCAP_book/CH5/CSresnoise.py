#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSresnoise.py
"""
import SLiCAP as sl
import sympy as sp
SHOW = False
#sl.initProject('CS stage noise with resistive source')
cir = sl.makeCircuit('kicad/CSresNoise/CSresNoise.kicad_sch', imgWidth = 400)
# Set value of 1/f noise to zero, and I_D to critical inversion
cir.defPar('KF_N18', 0)
I_D     = cir.getParValue('ID')
IC      = cir.getParValue('IC_X1')
IC_CRIT = cir.getParValue('IC_CRIT_X1')
I_D     = I_D*IC_CRIT/IC
cir.defPar('ID', I_D)
# Print some important noise parameters to an HTML page
sl.htmlPage('Operating point parameters')
R_N     = cir.getParValue('R_N_X1')
R_s     = cir.getParValue('R_s')
f_T     = cir.getParValue('f_T_X1')
g_m     = cir.getParValue('g_m_X1')
Width   = cir.getParValue('W')
sl.text2html('Device width:')
sl.eqn2html('W', Width)
sl.text2html('Dain current at critical inversion:')
sl.eqn2html('I_D', I_D)
sl.text2html('Effective noise resistance $R_N$:')
sl.eqn2html('R_N', R_N)
sl.text2html('Cut-off frequency $f_T$:')
sl.eqn2html('f_T', f_T)
noise_result   = sl.doNoise(cir, pardefs='circuit')
figInoise      = sl.plotSweep('Inoise', 'Source-referred noise spectrum',
                           noise_result, 1e8, 1e11, 100, funcType = 'inoise',
                           show = SHOW)
# Calculate the noise figure at critical inversion and the given width
tot_inoise     = sl.rmsNoise(noise_result, 'inoise', 1e9, 5e9)

# Calculate the noise figure
tot_inoise_src = sl.rmsNoise(noise_result, 'inoise', 1e9, 5e9,
                           source = "I_noise_R1")

NF             = 20*sp.log(tot_inoise/tot_inoise_src)/sp.log(10)
# Estimation of the corner frequency f_c:
f_c            = f_T*sp.sqrt(R_N/R_s)
sl.htmlPage("Noise analysis-1")
sl.text2html("The figure below shows the spectrum of the source-referred " +
          "voltage noise.")
sl.fig2html(figInoise, 500)
sl.text2html("The source-referred RMS noise voltage over this frequency range " +
          "equals: %s [$\\mu$V]."%(sp.N(1e6*tot_inoise, sl.ini.disp)))
sl.text2html("The noise figure equals: %s [dB]."%(sp.N(NF, sl.ini.disp)))
sl.text2html("The estimated conrner frequency $f_c$" +
          ": %s [GHz]."%(sp.N(f_c*1e-9, sl.ini.disp)))
# Calculate the width W at which we will have the best noise performance.
W               = sp.Symbol('W') # 'W' in the Python environment
cir.delPar('W')        # delete the numeric definition of the width
# We will keep the inversion coefficient at critical inversion, hence we scale
# the current with the width.
cir.defPar('ID', I_D*W/Width)
# calculate the noise spectra as a function of W and f
noise_w = sl.doNoise(cir, pardefs='circuit', numeric=True) 
# We now calculate the noise as a function of W over a frequency range
# 'fmin' to 'fmax':
f_min = sp.Symbol('f_min')
f_max = sp.Symbol('f_max')
rms_noise_w        = sl.rmsNoise(noise_w, 'inoise', f_min, f_max)
rms_noise_w_source = sl.rmsNoise(noise_w, 'inoise', f_min, f_max, 
                                 source="I_noise_R1")
# We now calculate the noise figure as a function of 'W', 'f_min' and 'f_max':
# Use the variance instead of the RMS value (simpler equation for later use)
NF_W               = (rms_noise_w/rms_noise_w_source)**2
# We now calculate the optimum width as a function of 'fmin' and 'fmax':
W_opt              = sp.solve(sp.diff(sp.N(NF_W), W), W)
# The sympy solve function returns a list with solutions, we will print the
# positive one.
for w in W_opt:
    w = sp.N(w.subs([(f_min, 1e9), (f_max, 5e9)]), sl.ini.disp)
    if w > 0:
        W = w
print(W)
# Create a plot of the noise figure versus the with for different values of
# f_max and f_min = 1G
# Define the plot parameters, 'fw', 'W' and 'fmax'
cir.defPar('W', W)
cir.defPar('f_max', '10G')
# Define the noise figure as a function of f_max:
cir.defPar('NF', 10*sp.log(NF_W.subs([(f_min, 2e8)]))/sp.log(10))
# Define the step parameters
stepDict = {}
stepDict['params'] = 'f_max'
stepDict['start']  = '2G'
stepDict['stop']   = '10G'
stepDict['method'] = 'lin'
stepDict['num']    = 5
result = sl.doParams(cir, pardefs='circuit', stepdict=stepDict, numeric=True)
# Plot the function
fig_NF_W = sl.plotSweep('NF_W', 'Noise Figure versus width, $f_{min}$ = 200MHz',
                     result, 10, 200, 50, sweepVar = 'W', sweepScale = 'u',
                     funcType = 'param', xUnits = 'm', yVar = 'NF',
                     yUnits = 'dB', show = SHOW)
# Put it all on an HTML page
sl.htmlPage("Noise analysis-2")
sl.text2html("The lowest noise figure over a frequency range from 1GHz to 5GHz " +
          "and at critical inversion is achieved at a width " +
          "of: %s [um]"%(sp.N(W*1e6, sl.ini.disp)))
sl.text2html("The figure below shows the noise figure as a function of the " +
          "width and at critical inversion for diferent values of the " +
          "maximum frequency $f_{max}$, and $f_{min}$=200MHz.")
sl.fig2html(fig_NF_W, 500)