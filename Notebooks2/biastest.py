#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 10:31:13 2025

@author: anton
"""

import SLiCAP as sl 

sl.initProject("bias")

# Enter positive values for N and for P channel devices
IDS = 5e-6
VDS = 0.9 
W   = 220e-9
L   = 180e-9
M   = 1
CH  = "N"

# Update library subcircuit definitions
fileName = "kicad/Libs/bias{}.kicad_sch".format(CH.upper())
sl.makeCircuit(fileName, language="SPICE")
fileName = "kicad/Libs/noisyNullor{}.kicad_sch".format(CH.upper())
sl.makeCircuit(fileName, language="SPICE")

# Obtain MOS operating point information
simCmd = "OP"
names  = {"V_D"  : "V(d1)",
          "V_G"  : "V(g1)",
          "I_DS" : "@M1[id]",
          "g_m"  : "@M1[gm]",
          "c_iss": "@M1[cgg]"}
params = [("ID", IDS), ("VDS", VDS), ("W", W), ("L", L), ("M", M)]

bias   = sl.ngspice2traces(sl.ini.cir_path + "bias{}".format(CH.upper()), 
                           simCmd, names, parList=params)
VGS    = bias["V_G"]
VDS    = bias["V_D"]
IDS    = bias["I_DS"]

# Obtain operating point information of the circuit with the noisy nullor
fileName = "kicad/Trimp/TrimpNoisyNullor{}.kicad_sch".format(CH.upper())
sl.makeCircuit(fileName, language="SPICE")
simCmd = "OP"
names  = {"V_in" : "V(in)",
          "V_out": "V(out)"}
params = [("VGS", VGS), ("ID", IDS), ("VDS", VDS), ("W", W), ("L", L), ("M", M)]
opinfo = sl.ngspice2traces(sl.ini.cir_path + "TrimpNoisyNullor{}".format(CH.upper()), 
                           simCmd, names, parList=params)

print("\n-------------------------")
for key in opinfo.keys():
    print(key, "\t:", opinfo[key])
for key in bias.keys():
    print(key, "\t:", bias[key])