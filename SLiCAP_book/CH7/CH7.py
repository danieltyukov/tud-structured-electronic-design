#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 20:31:51 2021

@author: anton
"""
import SLiCAP as sl
import sympy as sp

sl.initProject('VampNoise')

cir = sl.makeCircuit('kicad/VampNoise/VampNoise.kicad_sch', imgWidth = 600)
#
sl.htmlPage('Symbolic noise analysis')

noiseResultSym = sl.doNoise(cir)
sl.noise2html(noiseResultSym)
#
sl.htmlPage('Numeric noise analysis')
noiseResultNum = sl.doNoise(cir, pardefs='circuit', numeric=True)
sl.noise2html(noiseResultNum)
#
# Let us find show-stopper values for R_a, S_v, and S_i for the case in
# which the noise factor NF=2 (3dB).
#
# Determine the noise factor NF: (this procedure works with
# frequency-independent noise spectra only)
#
R_a, S_v, S_i, NF, R_a_max, S_i_max, S_v_max = sp.symbols('R_a, S_v, S_i, NF, R_a_max, S_i_max, S_v_max')
sl.htmlPage('Show-stopper values')
#
sl.text2html('Let us find show-stopper values for $R_a$, $S_v$, and $S_i$ ' +
             'for the case in which the noise factor $NF$ equals 2 (3dB).')
sl.head2html('Noise factor NF')
sl.text2html('The noise factor NF [-] is obtained as:')
NFact = sp.simplify(noiseResultNum.inoise/noiseResultNum.inoiseTerms['I_noise_R3'])
sl.eqn2html(NF, NFact)
#
# Show stopper (= maximum) value $R_{amax}$ for R_a with S_i=0 and S_v=0
Ra_max = sp.N(sp.solve(NFact.subs({S_v: 0, S_i: 0}) - 2, R_a)[0])
sl.head2html('Show-stopper value $R_a$')
sl.text2html('The show stopper value $R_{amax}$ for $R_a$ with $NF=2$, ' +
             '$S_v=0$ and $S_i=0$ is obained as:')
sl.eqn2html(R_a_max, Ra_max)
#
# Show stopper (= maximum) $S_{v,max}$ for S_v as a function of R_a and S_i=0
Sv_max = sp.N(sp.solve(NFact.subs(S_i, 0) - 2, S_v)[0])
sl.head2html('Show-stopper value $S_v$')
sl.text2html('The show stopper value for $S_v$ with $NF=2$ and $S_i=0$ can ' +
             'be obained as a function of $R_a$ (setting $R_a$ to zero ' +
             'would be meaningless):')
sl.eqn2html(S_v_max, Sv_max)
#
# Show stopper (= maximum) $S_{i,max}$ for S_i as a function of R_a and S_i=0
Si_max = sp.N(sp.solve(NFact.subs(S_v, 0) - 2, S_i)[0])
sl.head2html('Show-stopper value $S_i$')
sl.text2html('The show stopper value for $S_i$ with $NF=2$ and $S_v=0$ can ' +
             'be obained as a function of $R_a$: (setting $R_a$ to zero ' +
             'would be meaningless):')
sl.eqn2html(S_i_max, Si_max)