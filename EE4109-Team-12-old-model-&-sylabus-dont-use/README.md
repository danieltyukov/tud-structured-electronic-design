# EE4109 Team 12 - Hearing Loop Receiver Amplifier

Structured Electronic Design project for EE4109 at TU Delft.
Design of a hearing loop receiver amplifier in CMOS18 technology using SLiCAP.

## How to run

Requires Python 3 with SLiCAP v4, SymPy, NumPy, SciPy installed.
The virtual environment is at `../.venv/`.

```bash
# Quick run with default design knobs
./run.sh

# Or manually
../.venv/bin/python3 hlr_main.py
```

The pipeline is interactive and prompts for 8 design parameters (see Design Knobs below).
`run.sh` feeds these automatically via stdin.

After running, open `html/index.html` in a browser to view all generated documentation.

## Design overview

Three-stage hearing loop receiver amplifier:
- **A1**: Receive coil to ADC integrating voltage amplifier (main design focus)
- **A2**: Buffer amplifier (gain ~1.4, implemented as wire)
- **A3**: DAC to loudspeaker driver (conceptual only)

The A1 design uses a single PMOS common-source stage as the controller in a
three-port nullor-based integrating feedback topology. This is chosen over a
differential pair because a 3-terminal device needs fewer transistors and
requires 4x less current for the same noise performance.

## Pipeline steps

`hlr_main.py` imports 10 modules sequentially. Each step generates HTML documentation.

| Step | Module | Description |
|------|--------|-------------|
| 1 | `hlr_specs.py` | Design requirements (battery, audio, frequency, noise specs) |
| 2 | `hlr_system.py` | System architecture (A1/A2/A3 stage structure) |
| 3 | `hlr_a1_circuit.py` | A1 circuit design, integration capacitor equation |
| 4 | `hlr_source_noise.py` | Source noise analysis with DIN-A weighting |
| 5 | `hlr_fb_noise.py` | Feedback network noise budget, R_i/C_i sizing |
| 6 | `hlr_ideal_ctrl.py` | Ideal controller transfer function analysis |
| 7 | `hlr_gm_opt.py` | gm/c_iss transconductance optimization |
| 8 | `hlr_mos_sizing.py` | Transistor W, L, ID sizing |
| 9 | `hlr_controller.py` | Single MOS + cascode controller analysis |
| 10 | `hlr_biasing.py` | Operating point and linearity verification |

## Design knobs

The pipeline prompts for 8 interactive parameters. These are design tradeoff choices:

| # | Parameter | Module (step) | Constraint | Description |
|---|-----------|--------------|------------|-------------|
| 1 | `n_Ri` | hlr_fb_noise (5) | 0 < n_Ri < 1 - n_SRC (~0.980) | Noise budget fraction for integrator resistor R_i |
| 2 | `R_i` | hlr_fb_noise (5) | Ri_min <= R_i <= Ri_max | Integrator resistance value in Ohm |
| 3 | `mosType` | hlr_gm_opt (7) | N or P | NMOS or PMOS input stage |
| 4 | `n_M` | hlr_gm_opt (7) | 0 < n_M < 1 - n_SRC - n_Ri | Noise budget fraction for controller MOS |
| 5 | `mosType` | hlr_mos_sizing (8) | N or P (match #3) | MOS type for W/L/ID sizing |
| 6 | `W_finger` | hlr_mos_sizing (8) | 0.18 to 50 um | Maximum finger width |
| 7 | `Le` | hlr_mos_sizing (8) | >= 0.18 um | Channel length |
| 8 | `mosType` | hlr_controller (9) | N or P (match #3) | MOS type for controller analysis |

The noise budgets must satisfy: `n_SRC + n_Ri + n_M <= 1` (total noise budget).
`n_SRC` is computed automatically (~0.0195) from source and termination noise.

### Knob tradeoffs

- **n_Ri** controls how much noise the integrator resistor is allowed to contribute.
  Higher n_Ri -> larger Ri_max -> less current -> less power, but leaves less
  budget for the MOS stage. Lower n_Ri -> tighter R_i constraint -> more current.
- **R_i** is chosen within [Ri_min, Ri_max]. Ri_min comes from max power constraint.
  Ri_max comes from the noise budget. Larger R_i means less power but larger C_i.
- **n_M** controls MOS noise budget. Must fit in remaining budget after n_SRC + n_Ri.
- **W_finger / Le** are layout parameters. Minimum Le (0.18um) gives highest f_T.

### Our chosen values

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| n_Ri | 0.2 | Conservative noise budget for R_i, leaves more room for MOS |
| R_i | 5000 Ohm | Mid-range within [1620, 8972] Ohm |
| mosType | P | PMOS common-source stage |
| n_M | 0.5 | Uses most of remaining budget (max ~0.781) |
| W_finger | 10 um | Standard finger width |
| Le | 0.18 um | Minimum length for maximum f_T |

Total noise budget used: n_SRC + n_Ri + n_M = 0.0195 + 0.2 + 0.5 = 0.72 (72%)

### Results with our values

| Result | Value |
|--------|-------|
| Ri_max | 8972 Ohm |
| Ri_min | 1620 Ohm |
| C_i | 2.728 nF |
| c_iss (optimum) | 4.750e-13 F |
| g_m (optimum) | 6.450e-5 S |
| W | 0.270 mm |
| L | 0.180 um |
| M (fingers) | 27 |
| ID | 2.30 uA |
| IC (inversion coefficient) | 0.00560 (deep weak inversion) |
| RMS DIN-A weighted noise | 8.82e-6 V |
| Power conflict | None |

## Fixed specifications (from requirements)

| Parameter | Value | Unit |
|-----------|-------|------|
| Battery voltage | 1.4 | V |
| Regulated voltage | 0.9 | V |
| Max power dissipation | 1 mW | W |
| Source resistance R_s | 875 | Ohm |
| Source inductance L_s | 0.12 | H |
| Termination resistance R_t | 10k | Ohm |
| Integration time constant tau_i | 1/62.4k | s |
| Frequency range (hearing loop) | 600 - 6000 | Hz |
| Max full-power frequency | 5000 | Hz |
| Noise floor | 30 | dBSPL |
| Max SPL | 110 | dBSPL |
| Crest factor | 3 | - |
| CMOS technology | C18 (180nm) | - |

## Project structure

```
EE4109-Team-12/
|
|-- hlr_main.py                      # Entry point: imports all steps sequentially
|-- hlr_specs.py                     # Step 1: design requirements
|-- hlr_system.py                    # Step 2: system architecture
|-- hlr_a1_circuit.py                # Step 3: A1 circuit design
|-- hlr_source_noise.py              # Step 4: source noise + DIN-A weighting
|-- hlr_fb_noise.py                  # Step 5: feedback network noise (interactive)
|-- hlr_ideal_ctrl.py                # Step 6: ideal controller transfer function
|-- hlr_gm_opt.py                    # Step 7: gm/c_iss optimization (interactive)
|-- hlr_mos_sizing.py                # Step 8: W/L/ID transistor sizing (interactive)
|-- hlr_controller.py                # Step 9: controller analysis + cascode (interactive)
|-- hlr_biasing.py                   # Step 10: operating point and linearity
|-- run.sh                           # Shell script to run full pipeline
|-- SLiCAP.ini                       # SLiCAP project configuration
|-- README.md                        # This file
|
|-- lib/
|   `-- C18.lib                      # CMOS18 device library (EKV model params)
|
|-- kicad/                           # KiCAD schematics (source for netlists)
|   |-- nullorcir/
|   |   |-- A1_design.kicad_sch
|   |   `-- A1_design copy.kicad_sch
|   |-- controller/
|   |   |-- single_NMOS.kicad_sch
|   |   |-- single_PMOS.kicad_sch
|   |   `-- cascode_PMOS.kicad_sch
|   |-- A1_Ideal_Controller.kicad_sch
|   |-- A1_R_noise_without_Ri.kicad_sch
|   `-- A1_R_noise_with_Ri.kicad_sch
|
|-- cir/                             # Generated SPICE netlists
|-- html/                            # Generated HTML documentation (output)
|-- img/                             # Generated circuit diagrams (SVG + PDF)
|-- csv/                             # Specification data files
|-- tex/                             # LaTeX output
`-- notes/                           # Design notes
```

### Key relationships

- `hlr_main.py` imports steps 1-10 in order. Each step builds on results from previous steps.
- KiCAD schematics (`kicad/`) are converted to SPICE netlists (`cir/`) by SLiCAP's `makeCircuit()`.
- `lib/C18.lib` defines CMOS18 EKV model parameters used by all circuits with MOS devices.
- Each step generates HTML pages in `html/` with equations, plots, and tables.
- The `specsObject` class (defined in `hlr_specs.py`) passes design parameters between steps.
- Steps 5, 7, 8, 9 are interactive (require design knob inputs).
