import SLiCAP as sl
import sympy as sp
from time import time

import numpy as np
from scipy.integrate import quad

from numpy import geomspace
from SLiCAP import trace, plot, float2rational, initProject, head2html, htmlPage, text2html
from sympy import Symbol, lambdify, sqrt

from g12specifications import global_specs, A1specs



# A1 amplifier Design
fileName = "kicad/nullorcir/A1_design.kicad_sch"
cir = sl.makeCircuit(fileName, update = True, imgWidth = 800)
# sl.img2html("A1-design.svg", width = 800)


head2html("The design equation for $C_i$:")
cir.defPar("R_i", A1specs.getSpec("R_i"))
Ci  = 1/ ((cir.getParValue('R_i') + cir.getParValue('R_s')) * 62.4e3) # In this case there is only one solution
Ci_eq = 1/ ((sp.Symbol('(R_i + R_s)', positive = True)) * sp.Symbol('62.4e3'))
sl.eqn2html(sp.Symbol('C_i', positive = True), Ci_eq, label = 'CC1', labelText = 'Design equation for $C_i$')
cir.defPar('C_i', Ci)


htmlPage('Plots')
head2html('Amplifier Design A1 - analysis')

# Let us now evaluate the transfer function of this network.
gain = sl.doLaplace(cir)
# The laplace transform can now be found in the attribute 'laplace' of 'gain'.
sl.eqn2html('V_out/V_1', gain.laplace, label = 'gainLaplace', labelText = 'Laplace transfer function')
print(sl.ini.laplace)
numGain = sl.doLaplace(cir, pardefs='circuit')
head2html('Frequency domain plots')
figMag = sl.plotSweep('RCmag', 'Magnitude characteristic', numGain, 10, '100k', 100, yUnits = '-', show = False)
# This will put the figure on the HTML page with a width of 800 pixels, a caption and a label:
sl.fig2html(figMag, 600, caption = 'Magnitude characteristic of the RC network.', label = 'figMag')
figPol = sl.plotSweep('RCpolar', 'Polar plot', numGain, 10, '100k', 100, axisType = 'polar', show = False)
sl.fig2html(figPol, 600, caption = 'Polar plot of the transfer of the RC network.', label = 'figPolar')
figdBmag = sl.plotSweep('RCdBmag', 'dB magnitude characteristic', numGain, 10, '100k', 100, funcType = 'dBmag', show = False)
sl.fig2html(figdBmag, 600, caption = 'dB Magnitude characteristic of the RC network.', label = 'figdBmag')
figPhase = sl.plotSweep('RCphase', 'Phase characteristic', numGain, 10, '100k', 100, funcType = 'phase', show = False)
sl.fig2html(figPhase, 600, caption = 'Phase characteristic of the RC network.', label = 'figPhase')
figDelay = sl.plotSweep('RCdelay', 'Group delay characteristic', numGain, 10, '100k', 100, yScale = 'u', funcType = 'delay')
sl.fig2html(figDelay, 600, caption = 'Group delay characteristic of the RC network.', label = 'figDelay')
pzResult = sl.doPZ(cir)
pzGain = sl.doPZ(cir, pardefs = 'circuit')
htmlPage('Poles and zeros')
sl.pz2html(pzResult, label = 'PZlistSym', labelText = 'Symbolic values of the poles and zeros of the network')
sl.pz2html(pzGain, label = 'PZlist', labelText = 'Poles and zeros of the network')
head2html("Complex frequency domain plots")
figPZ = sl.plotPZ('PZ', 'Poles and zeros of the RC network', pzGain)
figPZ = sl.plotPZ('PZ', 'Poles and zeros of the RC network', pzGain, xmin = -1.9, xmax = 0.1, ymin = -1, ymax = 1, xscale = 'k', yscale = 'k')
sl.fig2html(figPZ, 600, caption = 'Poles and zeros of the RC network.', label = 'figPZ')
numStep = sl.doStep(cir, pardefs="circuit")
figStep = sl.plotSweep('step', 'Unit step response', numStep, 0, 1, 50, sweepScale='m', show = False)
# Let us put this plot on the page with the plots. You can get a list with page names by typing: 'ini.htmlPages'
sl.ini.htmlPage = 'myFirstRCnetwork_Plots.html'
head2html('Time domain plots')
sl.fig2html(figStep, 600, caption = 'Unit step response of the RC network.', label = 'figStep')

