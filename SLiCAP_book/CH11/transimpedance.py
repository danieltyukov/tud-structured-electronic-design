#!/usr/bin/env python3
import SLiCAP as sl
import sympy as sp
SHOW = False
sl.initProject('transimpedance')
cir = sl.makeCircuit('kicad/transimpedance/transimpedance.kicad_sch', imgWidth=600)

sl.htmlPage('Example controller GB product requirements')

Lsym = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True).laplace

#
gain, numerCoeffs, denomCoeffs = sl.coeffsTransfer(Lsym)
if len(numerCoeffs) > 1:
  sl.text2html('Zeros found, GB determination method not valid.')
else:
  sl.text2html('Found the nonzero DC loop gain.')
if denomCoeffs[0] == 0:
  sl.text2html('Found poles in the origin, GB determination method not valid.')
#
sl.text2html('The DC loop gain equals:')
sl.eqn2html('L_DC', gain)
#
if len(denomCoeffs) == 1:
  sl.text2html('No poles found, GB determination method not valid.')
LPproduct = -gain/denomCoeffs[-1]

sl.text2html('The loop gain-poles product is found as:')
sl.eqn2html('LP', LPproduct)
order = len(denomCoeffs) - 1
sl.text2html('The order of the LP product is: ' + str(order))

B_f = 500e3
R_o, C_d, C_c, G_B, GB_min, A_0 = sp.symbols('R_o, C_d, C_c, G_B, GB_min, A_0')

GB_minAll = sp.solve(LPproduct -(B_f*2*sp.pi)**order, G_B)[0]
sl.text2html('The required bandwidth  = ' + str(B_f/1000) + 'kHz')
sl.text2html('With this value, the show stopper value of the gain-bandwidth product $G_B$ is:')
GB_minNum = GB_minAll.subs([(R_o, 0), (C_d, 0), (C_c, 0)])
sl.eqn2html('GB_min', GB_minNum)
sl.htmlPage('Device selection and verification')
cir.defPar('A_0', '1M')
cir.defPar('C_d', '8p')
cir.defPar('C_c', '7p')
cir.defPar('R_o', 55)
cir.defPar('G_B', '16M')
cir.defPar('I_s', 1)
sl.params2html(cir)
Bf = 1/(2*sp.pi)*LPproduct**(1/order)
BfOPA627 = sp.N(Bf.subs([(R_o, 55), (C_d, 8e-12), (C_c, 7e-12), (G_B,16e6),  (A_0, 1e6)]), 4)
sl.text2html('The achievable low-pass cut-off frequency $f_h$ with the OPA627 in [MHz] is:')
sl.eqn2html('f_h', BfOPA627*1e-6)

sl.htmlPage('Bode plots')
A = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
S = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
D = sl.doLaplace(cir, transfer='direct', pardefs='circuit', numeric=True)
G = sl.doLaplace(cir, transfer='gain', pardefs='circuit', numeric=True)

figMag = sl.plotSweep('TrimpMag', 'Magnitude characteristics', [L, A, S, D, G], 10e3, 10e6, 200, funcType = 'mag', show = SHOW)
sl.fig2html(figMag, 600)
figPhase = sl.plotSweep('TrimpPhase', 'Phase characteristics', [L, A, S, D, G], 10e3, 10e6, 200, funcType = 'phase', show = SHOW)
sl.fig2html(figPhase, 600);