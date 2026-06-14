  Here's a summary of all the fixes made to get Team 12's steps 7 and 8 working with SLiCAP v4.0.10:

  Fixes Applied

  Root Cause

  In old SLiCAP, F and H were 4-node CCCS and CCVS devices with implicit zero-impedance current sensing paths at their control
  nodes. SLiCAP v4 changed:
  - F → 2-node + 1 reference CCCS (current sensed through a reference element)
  - H → 2-node + 1 reference CCVS (current sensed through a reference element)
  - G → 4-node VCCS (voltage-controlled, no current path)
  - E → 4-node VCVS (voltage-controlled, no current path)

  Simply converting F→G and H→E removes the current paths, leaving nodes floating and making the MNA matrix singular.

  Files Changed

  1. cir/A1_controller_noise_ciss_gm.cir - Replaced G/E (VCCS/VCVS) with F/H (CCCS/CCVS) using voltage source current probes
  (V3, V4) to provide the zero-impedance sensing paths. Also added .lib C18.lib.
  2. lib/C18.lib (NM18_noise and PM18_noise subcircuits) - Same fix: replaced G/E with F/H + voltage source current probes
  (V_H1, V_F1).
  3. g12gmciss.py - Changed to load .cir instead of .kicad_sch. Added library parameter loading via helper circuit. Fixed
  c_iss_best selection to handle variable number of solutions.
  4. g12WLID.py - Changed to load .cir instead of .kicad_sch.
  5. cir/A1_controller_noiseWLI_n.cir and cir/A1_controller_noiseWLI_p.cir - Added .lib C18.lib directive.