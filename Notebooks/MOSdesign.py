#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 13:02:51 2025

@author: anton
"""
import SLiCAP as sl
from SLiCAPmosNoise import process, specObject, doMOSnoiseDesign

sl.initProject("MOSdesign")

# Circuit specification

baseName  = "kicad/Trimp/Trimp"
kicad_sch = baseName + ".kicad_sch"

# NGspice circuit files N and P-type noisy nullor circuits must have the following names:
    # N-type: baseName + "NoisyNullorN.kicad_sch"
    # P-type: baseName + "NoisyNullorP.kicad_sch"

# The KiCAD NGspice symbol for the noisy nullor is found in the "kicad/Libs/"
# subfolder: "spiceNoisyNullor.kicad_sym"
# The sub circuits for this symbol also reside in this folder:
    # N-type: "noisyNullorN.kicad_sch"
    # P-Type: "noisyNullorP.kicad_sch"

# Noise specifications
specs = specObject()
specs.noiseRMS = 500e-6  # Total RMS output noise budget over frequency range
specs.f_min    = 1e6     # Lower limit of frequency range
specs.f_max    = 250e6   # Upper limit of frequency range
specs.ID_spec  = 0.5e-3  # Current budget: always positive; also for P-channel
specs.IC       = None    # IC for noise design according to specs
specs.IC_max   = 15      # IC for minimum noise (maximum fT)
specs.gmID     = 12      # gmID for noise design according to specs
                         # will be overruled by specs.IC
specs.gmID_min = None    # gmID for minimum noise (maximum fT)
                         # will be overruled by specs.IC_max
specs.VDS      = 0.9     # V_DS: always positive; also for P-channel

# Technology specifications, file locations are relative to the project folder
models = []

model          = process()
model.name     = "MN18_noisyNullor"                   # SLiCAP built-in EKV-based noisy nullor sub circuit
model.bias     = "kicad/Libs/biasN.kicad_sch"         # NMOS bias circuit
model.subckt   = "kicad/Libs/noisyNullorN.kicad_sch"  # NMOS NGspice noisy nullor sub circuit
model.channel  = "N"
model.IG       = 0
model.L_min    = 0.18e-6
model.L_max    = 50e-6
model.W_min    = 0.18e-6
model.W_max    = 10e-3
model.W_finger = 50e-6

models.append(model)

model          = process()
model.name     = "MP18_noisyNullor"                    # SLiCAP built-in EKV-based noisy nullor sub circuit
model.bias     = "kicad/Libs/biasP.kicad_sch"          # PMOS bias circuit
model.subckt   = "kicad/Libs/noisyNullorP.kicad_sch"   # PMOS NGspice noisy nullor sub circuit
model.channel  = "P"
model.IG       = 0
model.L_min    = 0.18e-6
model.L_max    = 50e-6
model.W_min    = 0.18e-6
model.W_max    = 10e-3
model.W_finger = 50e-6

models.append(model)

# Noise design without iteration
all_results = doMOSnoiseDesign(kicad_sch, specs, models, printAll=True)