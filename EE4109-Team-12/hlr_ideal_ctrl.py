import SLiCAP as sl
import sympy as sp


from SLiCAP import trace, plot, float2rational, initProject, head2html, htmlPage, text2html
from hlr_specs import A1specs
from hlr_fb_noise import Ci, Ri


file = 'kicad/A1_Ideal_Controller.kicad_sch'
cir = sl.makeCircuit(file)
sl.elementData2html(cir)

cir.defPar("C_i", Ci)

sl.head2html('Source-to-Input Transfer Functions')
sl.head3html('Infinite Input Impedance Case')
cir.defPar("R_i", 1e12)
# Plot gain
gain        = sl.doLaplace(cir, pardefs="circuit", numeric=True)
sl.eqn2html("gain", gain.laplace)
# params
sl.params2html(cir)
fb_model    = [gain]
fbmodel_mag = sl.plotSweep("fb_mag_sm", "Magnitude plots feedback model parameters", fb_model, 10, 10e5, 200)
sl.img2html("fb_mag_sm.svg", width=600)


sl.head3html('Finite Input Impedance Case')
cir.defPar("R_i", Ri)
gain        = sl.doLaplace(cir, pardefs="circuit", numeric=True)
sl.eqn2html("gain", gain.laplace)
# params
sl.params2html(cir)
fb_model    = [gain]
fbmodel_mag = sl.plotSweep("fb_mag2", "Magnitude plots feedback model parameters", fb_model, 10, 10e5, 200)
sl.img2html("fb_mag2.svg", width=600)


file = 'kicad/nullorcir/A1_design copy.kicad_sch'
cir = sl.makeCircuit(file)
sl.elementData2html(cir)
sl.params2html(cir)

sl.specs2circuit(A1specs.getSpecs(), cir)

htmlPage('Transfer Characteristics')
head2html('A1 Stage Transfer Analysis')

# Let us now evaluate the transfer function of this network.
gain = sl.doLaplace(cir)
# The laplace transform can now be found in the attribute 'laplace' of 'gain'.
sl.eqn2html('V_out/V_1', gain.laplace, label = 'gainLaplace', labelText = 'Laplace transfer function')
print(sl.ini.laplace)
numGain = sl.doLaplace(cir, pardefs='circuit')
head2html('Frequency Response')
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
htmlPage('Pole-Zero Distribution')
sl.pz2html(pzResult, label = 'PZlistSym', labelText = 'Symbolic values of the poles and zeros of the network')
sl.pz2html(pzGain, label = 'PZlist', labelText = 'Poles and zeros of the network')
head2html("Complex Frequency Analysis")
figPZ = sl.plotPZ('PZ', 'Poles and zeros of the RC network', pzGain)
figPZ = sl.plotPZ('PZ', 'Poles and zeros of the RC network', pzGain, xmin = -1.9, xmax = 0.1, ymin = -1, ymax = 1, xscale = 'k', yscale = 'k')
sl.fig2html(figPZ, 600, caption = 'Poles and zeros of the RC network.', label = 'figPZ')
numStep = sl.doStep(cir, pardefs="circuit")
figStep = sl.plotSweep('step', 'Unit step response', numStep, 0, 1, 50, sweepScale='m', show = False)
# Let us put this plot on the page with the plots. You can get a list with page names by typing: 'ini.htmlPages'
sl.ini.htmlPage = 'myFirstRCnetwork_Plots.html'
head2html('Time Domain Response')
sl.fig2html(figStep, 600, caption = 'Unit step response of the RC network.', label = 'figStep')
