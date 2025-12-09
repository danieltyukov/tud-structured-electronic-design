#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 19:16:22 2021

@author: anton
"""

import SLiCAP as sl
SHOW = False
sl.initProject("CH13")

def doAnalysis(fileName):
    
    cirName = fileName.split('/')[-1].split('.')[0]

    # Define the circuit
    cir = sl.makeCircuit(fileName)
    #
    cir.defPar('W', '4u')
    cir.defPar('L', '500n')
    cir.defPar('ID', '500u')
    cir.defPar('R_s', '15k')
    cir.defPar('C_ell', '80f')
    cir.defPar('C_phz', 0)

    # Display the magnitude and phase plots of the transfers of the asymptotic-
    # gain model
    print("Calculation asymptotic gain")
    A  = sl.doLaplace(cir, transfer='asymptotic', pardefs='circuit', numeric=True)
    print("Calculation loop gain")
    L = sl.doLaplace(cir, transfer='loopgain', pardefs='circuit', numeric=True)
    print("Calculation servo")
    S = sl.doLaplace(cir, transfer='servo', pardefs='circuit', numeric=True)
    print("Calculation direct transfer")
    D = sl.doLaplace(cir, transfer='direct', pardefs='circuit', numeric=True)
    print("Calculation gain")
    G = sl.doLaplace(cir, pardefs='circuit', numeric=True)
    # Create the plots
    fig_as_gain_model_mag = sl.plotSweep(cirName + '_as_gain_model_mag', 
                                         'Magnitude plots', [A, L, S, D, G], 
                                         0.1, 100, 200, sweepScale='G', 
                                         funcType='mag', show=SHOW)
    fig_as_gain_model_phs = sl.plotSweep(cirName + '_as_gain_model_phs', 
                                         'Phase plots', [A, L, S, D, G], 
                                         0.1, 100, 200, sweepScale='G', 
                                         funcType='phase', show=SHOW)
    
    sl.htmlPage('Asymptotic-gain model ' + cirName)
    sl.fig2html(fig_as_gain_model_mag, 600)
    sl.fig2html(fig_as_gain_model_phs, 600)
    

    # Study the poles of the loop gain
    sl.htmlPage('Loop gain: ' + cirName)
    PZL = sl.doPZ(cir, transfer='loopgain', pardefs='circuit', numeric=True)
    sl.pz2html(PZL)

    # Study the expression for the DC loop gain
    DCloopgain = sl.doDC(cir, transfer='loopgain').laplace
    sl.eqn2html('L_DC', DCloopgain)

    # Study the poles of the gain
    sl.htmlPage('Gain: ' + cirName)
    PZG = sl.doPZ(cir, transfer='gain', pardefs='circuit', numeric=True)
    sl.pz2html(PZG)

    # Study the expression for the DC gain
    DCgain = sl.doDC(cir, transfer='gain').laplace
    sl.eqn2html('L_DC', DCgain)
    
    # Study the effect of a phantom zero on the pole positions
    stepDict = {}
    stepDict['params'] = 'C_phz'
    stepDict['method'] = 'lin'
    stepDict['start']  = 0
    stepDict['stop']   = '10f'
    stepDict['num']    = 50   
    RLgain_Cphz        = sl.doPoles(cir, pardefs='circuit', numeric=True, 
                                    stepdict=stepDict)
    figRL = sl.plotPZ(cirName + '_rootLocus', 'CD stage', RLgain_Cphz, 
                      xmin=-3e9, xmax=0, ymin=-1.5e9, ymax=1.5e9, show = SHOW)
    sl.fig2html(figRL, 600)

    # Study the effect of a phantom zero on the Bode plots
    stepDict['num']    = 5  
    gainLaplace        = sl.doLaplace(cir, pardefs='circuit', numeric=True, 
                                      stepdict=stepDict)
    figMag = sl.plotSweep(cirName + '_dBmag', 'CD stage', gainLaplace, 
                          0.1, 100, 200, sweepScale='G', funcType='dBmag', 
                          show=SHOW)
    sl.fig2html(figMag, 600)
    figPhase = sl.plotSweep(cirName + '_phase', 'CD stage', gainLaplace, 
                            0.1, 100, 200, sweepScale='G', funcType='phase', 
                            show=SHOW)
    sl.fig2html(figPhase, 600)

if __name__=='__main__':
    fileNames = ['kicad/CDcompM18/CDcompM18.kicad_sch', 
                 'kicad/CDcompM18bulk/CDcompM18bulk.kicad_sch']
    for fi in fileNames:
        doAnalysis(fi)