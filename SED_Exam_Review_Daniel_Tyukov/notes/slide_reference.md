# Slide reference: A1 Receive-Coil Amplifier deck
**Daniel Tyukov (5714699) · 46 slides · footer page number = slide number**

This file describes the slides, focused on the circuits shown. If you name a slide by number or
title, this tells me exactly which circuit it is, every part in it, and how it looks on the slide.
Component values come from `../data/source/csv/dualStage.csv` via `gen_values.py`; netlists are in
`../data/source/cir/`.

Shared design values used across the circuits:

| Symbol | Value | Symbol | Value |
|---|---|---|---|
| L_s (coil inductance) | 120 mH | C_i (integrator cap) | 4.96 nF |
| R_s (coil resistance) | 875 Ω | R_b (bypass) | 53.5 kΩ |
| C_s (coil parasitic) | 9.382 pF | R_f (feedback) | 3.24 kΩ |
| R_t (termination) | 79.97 kΩ | R_phz (phantom zero) | ≈ 0.42 kΩ |
| C_L (ADC load) | 10 pF | DIN_A | weighting function E-source |

Transistors: **X1 = CMOS18PD (PMOS, 1st stage)** W = 19.1 µm, L = 0.72 µm, I_D = 8.07 µA ·
**X2 = CMOS18N (NMOS, 2nd stage)** W = 10 µm, L = 0.18 µm, I_D = 16.5 µA.
Behavioural transconductors: **g_m1 ≈ 73 µS** (1st stage, set by noise), **g_m2** (2nd stage, loop-gain),
**g_o1** (1st-stage output conductance, drawn as R = 1/g_o1).

---

## Quick slide index (number → title → what's on it)

| # | Title | Main visual |
|---|---|---|
| 1 | A1 Receive-Coil Amplifier (title) | title page |
| 2 | Outline | 8-part list |
| 3 | *Part 1: Specification & design environment* | divider |
| 4 | The hearing loop and where A1 lives | application photo/diagram |
| 5 | A1 in the signal chain | system block diagram |
| 6 | Input of A1: the pick-up coil | text + dΦ/dt |
| 7 | Output of A1: source-select switch + ADC | text |
| 8 | How should A1 work? | H(s) integrator |
| 9 | Specification & budget | spec table |
| 10 | **Circuit model: the complete picture** | **full SLiCAP concept circuit, 6 colour zones** |
| 11 | Representation 1: the pick-up coil | **coil mini-circuit** + datasheet table |
| 12 | Representation 2: the termination resistor | **R_t mini-circuit** + damping plot |
| 13 | Representation 3: the ideal amplifier (nullor) | **nullor symbol** + gain derivation |
| 14 | Representation 4: the output (ADC load) | **C_L mini-circuit** + ADC block |
| 15 | Representation 5: the noise sources | noise-spectrum plot |
| 16 | **Noise budgeting** | **same concept circuit, R_s/R_t/R_f circled red** |
| 17 | Noise is judged by ear: DIN-A weighting | DIN-A curve |
| 18 | *Part 2: Transfer function & feedback configuration* | divider |
| 19 | First generate the options, then choose | V-V vs I-V text |
| 20 | Why feedback? The asymptotic-gain model | **feedback block diagram** + formula |
| 21 | Sizing the feedback network | R_f / C_i / R_b values |
| 22 | *Part 3: First stage: noise design* | divider |
| 23 | The first stage sets the input-referred noise | **noisy-nullor SLiCAP schematic** |
| 24 | The knobs: gm, c_iss, inversion | 4kTγ/gm text |
| 25 | Which stage? CS vs CG vs CD | comparison table |
| 26 | From budget to device parameters | procedure + W/L/I_D |
| 27 | *Part 4: Single stage & loop-gain check* | divider |
| 28 | **Single stage: the circuit** | **behavioural single-stage SLiCAP circuit, 5 colour zones** |
| 29 | Is a single stage enough? | loop-gain plot + verdict |
| 30 | *Part 5: Dual stage (PMOS pair + NMOS CS)* | divider |
| 31 | Why a dual stage? | text |
| 32 | **Suggested topology** | **EKV dual-stage SLiCAP circuit, 5 zones (stages bold)** |
| 33 | First stage: differential pair vs single CS | comparison table |
| 34 | Second stage: NMOS common-source | W/L/I_D |
| 35 | **Dual-stage design parameters** | **behavioural dual-stage SLiCAP circuit + L_DC** |
| 36 | Asymptotic-gain model: every curve explained | 5-curve Bode plot |
| 37 | *Part 6: EKV model & pole-zero analysis* | divider |
| 38 | **EKV small-signal model** | **EKV dual-stage SLiCAP circuit, X1/X2 circled** |
| 39 | Pole-zero analysis | PZ map + pole/zero table |
| 40 | *Part 7: Frequency compensation (MFM)* | divider |
| 41 | Target: maximally-flat magnitude (MFM) | Q = 1/√2 text |
| 42 | The phantom-zero method | **actual SLiCAP compensated circuit, R_phz circled** |
| 43 | Compensation result | before/after plot + R_phz sweep plot |
| 44 | *Part 8: Conclusions* | divider |
| 45 | Conclusions | summary |
| 46 | Thank you | closing |

Slides in **bold** show a circuit, detailed below.

---

## Circuit details

### Slide 10: "Circuit model: the complete picture"
Figure: `assets/schematics/circuit_model_colored.png` (netlist `feedbackConceptNoisyNullorN18.cir`).
The full conceptual model, left to right, with the colour band of each block. The amplifier is an
ideal **noisy nullor**, not yet a transistor.

| Block (colour) | Part | Value | Nodes | Role |
|---|---|---|---|---|
| coil source (**cyan**) | V1 | 0 (AC source) | 2→0 | the coil EMF, the signal source |
| | L1 | L_s = 120 mH | 4→1 | coil inductance |
| | R1 | R_s = 875 Ω | 1→2 | coil series resistance |
| | C1 | C_s = 9.382 pF | 4→0 | coil parasitic capacitance |
| termination (**orange**) | R2 | R_t = 79.97 kΩ | 4→0 | damps the L_s–C_s resonance |
| amplifier (**green**) | X1 | MN18_noisyNullor | out,0,4,3 | ideal nullor + the input device's noise (v_n, i_n) |
| feedback (**yellow**) | C3 | C_i = 4.96 nF | out→3 | integrator capacitor |
| | R3 | R_f = 3.24 kΩ | 3→0 | feedback resistor (sets the transfer) |
| | R4 | R_b = 53.5 kΩ | out→3 | bypass, sets the 600 Hz low corner + DC path |
| ADC load (**pink**) | C2 | C_L = 10 pF | out→0 | ADC input capacitance |
| noise weighting (**grey**) | E2 | DIN_A | noise,0 ← out,0 | applies the DIN-A weighting to the output noise |

Directives: `.source V1`, `.detector V_out`, `.lib SLiCAP_C18.lib`, `.param IG=0`. The input node
is `4` (where the coil, C_s and R_t meet); the output node is `out`.

### Slide 16: "Noise budgeting"
Figure: `assets/schematics/circuit_model_noise.png`. **Exactly the slide-10 circuit**, but the three
budgeted noise resistors are **circled in red**: R1 (R_s, source), R2 (R_t, termination), R3 (R_f,
feedback). Together they take B_n1 = 0.4 of the noise budget; the rest goes to the input transistor.

### Slide 23: "The first stage sets the input-referred noise"
Figure: `assets/schematics/noisyNullorN.png` (the `noisyNullorN` subcircuit). This is the **inside of
the amplifier block** (X1 above): an ideal nullor (nullator input, norator output) with the input
MOS device's noise added as a series gate-referred voltage-noise source and a parallel current-noise
source. It is what "noisy nullor" means.

### Slide 28: "Single stage: the circuit"
Figure: `assets/schematics/singleStageSimple_colored.png` (netlist `singleStageSimple.cir`).
Behavioural model with **one** transconductor; coloured by block (coil cyan, termination orange, amplifier **green**, feedback yellow, load pink), matching the slide-10 roadmap.

| Block | Part | Value | Nodes | Role |
|---|---|---|---|---|
| coil source | V1 | AC source | 4→0 | coil EMF |
| | L1 | L_s = 120 mH | 2→3 | coil inductance |
| | R1 | R_s = 875 Ω | 3→4 | coil resistance |
| | C4 | C_s = 9.382 pF | 2→0 | coil parasitic |
| termination | R2 | R_t = 79.97 kΩ | 2→0 | resonance damping |
| amplifier (**green**) | G1 | −g_m (VCCS) | out→0, sense 2→1 | the single CS transconductor |
| | C1 | c_iss | 2→1 | input capacitance of the stage |
| feedback | C3 | C_i = 4.96 nF | out→1 | integrator capacitor |
| | R3 | R_f = 3.24 kΩ | 1→0 | feedback resistor |
| | R4 | R_b = 53.5 kΩ | out→1 | bypass |
| load | C2 | C_L = 10 pF | out→0 | ADC load |

Directives: `.source V1`, `.detector V_out`, `.lgref G1` (loop-gain reference is the transconductor).
Point of the slide: this is the simplest realisation; its loop gain falls below 0 dB (slide 29), so it
fails on accuracy.

### Slide 32: "Suggested topology"
Figure: `assets/schematics/dualstage_colored.png` (netlist `dualStageEKV.cir`). The **EKV
transistor** dual stage, coloured by block: coil (grey), **1st stage cyan**, feedback (yellow),
**2nd stage pink**, load (green). The two stages are the bold colours; coil/feedback/load sit lighter.

| Block | Part | Value | Nodes (D,G,S,B) | Role |
|---|---|---|---|---|
| coil source | V1 / L1 / R1 / C4 | as above | in-side | coil EMF + L_s + R_s + C_s |
| termination | R2 | R_t = 79.97 kΩ | in→0 | resonance damping |
| 1st stage (**cyan**) | X1 | CMOS18PD (PMOS) | 3,0,in,4 | input pair: W=19.1 µm, L=0.72 µm, I_D=8.07 µA |
| feedback | C3 / R3 / R5 | C_i / R_f / R_b | around node 4 | integrator + feedback + bypass |
| 2nd stage (**pink**) | X2 | CMOS18N (NMOS) | out,3,0,0 | CS output: W=10 µm, L=0.18 µm, I_D=16.5 µA |
| load | C2 | C_L = 10 pF | out→0 | ADC load |

Nodes: `in` = amplifier input (coil side), `3` = inter-stage node (X1 drain → X2 gate), `4` =
feedback summing node, `out` = output. Directives: `.source V1`, `.detector V_out`,
`.lgref Gm_M1_X2` (loop-gain reference is the X2 transconductance).

### Slide 35: "Dual-stage design parameters"
Figure: `assets/schematics/dualStageSimple_colored.png` (netlist `dualStageSimple.cir`). The
**behavioural** dual stage (transconductors, not transistors); **1st stage cyan, 2nd stage pink**.
This is where the four design knobs live.

| Block | Part | Value | Nodes | Role |
|---|---|---|---|---|
| coil source | V1 / L1 / R1 / C4 | as above | in-side | coil EMF + L_s + R_s + C_s |
| termination | R2 | R_t = 79.97 kΩ | in→0 | resonance damping |
| 1st stage (**cyan**) | G1 | g_m1 ≈ 73 µS (VCCS) | int→0, sense in→fb | first-stage transconductance (noise) |
| | C1 | c_iss | in→fb | first-stage input cap |
| | R5 | 1/g_o1 | int→0 | first-stage output resistance |
| 2nd stage (**pink**) | G2 | g_m2 (VCCS) | out→0, sense int→0 | second-stage transconductance (loop gain) |
| | C5 | c_iss2 | int→0 | second-stage input cap |
| feedback | C3 / R3 / R4 | C_i / R_f / R_b | around node fb | integrator + feedback + bypass |
| load | C2 | C_L = 10 pF | out→0 | ADC load |

Nodes: `in` = input, `fb` = feedback summing node, `int` = inter-stage node, `out` = output.
The four parameters on the slide: **g_m1** (noise budget), **g_m2** (extra loop-gain factor),
**R_f** (transfer), **g_o1** (first-stage output conductance). They give |L_DC| ≈ 45 dB, where

  L_DC = −R_f · g_m1 · g_m2 / g_o1.

### Slide 38: "EKV small-signal model"
Figure: `assets/schematics/dualStageEKV_hl.png`. The **same topology as slide 32** (netlist
`dualStageEKV.cir`) with **X1 and X2 circled in red**: each transistor now carries the full EKV
small-signal model (finite g_o + parasitic caps C_gs, C_gd, C_gb, C_db, C_sb) that the ideal nullor
and the behavioural model omitted. These parasitics create the HF poles/zeros. Realistic transistor-level model
with all parasitic capacitances. This is the circuit the pole-zero analysis (slide 39) runs on.

### Slide 42: "The phantom-zero method"
Figure: `assets/schematics/dualStageEKVcompensated_hl.png` (netlist `dualStageEKVcompensated.cir`),
the **actual SLiCAP compensated circuit** with the one added component **R4 = R_phz ≈ 0.42 kΩ
circled in red**. It sits in series between the 2nd-stage output node (`5`) and the load node (`out`). The load C2 (C_L) sits at
`out`; the feedback (C3 = C_i, R5 = R_b) is tapped at node `5`, i.e. **before** R_phz. Because the
feedback is taken before R_phz, the resistor adds a zero to the **loop gain** without putting a real
pole in the signal path. The zero is at z = −1/(R_phz·C_L).

---

## Mini / conceptual circuits (not full SLiCAP schematics)

- **Slide 11** coil mini (circuitikz): v_emf source, L_s, R_s in series, C_s and R_t to ground. The
  coil-source block on its own.
- **Slide 12** termination mini (circuitikz): just R_t from the input node to ground, beside the
  damping plot (undamped / light / critical).
- **Slide 13** nullor symbol (tikz): a triangle marked ∞ with + and − inputs, the ideal amplifier.
- **Slide 14** output (tikz): the A2→ADC block (Z_in = ∞, C = 10 pF) and a C_L-to-ground mini-circuit.
- **Slide 20** feedback block diagram (tikz): Σ → nullor → V_o with the Z1,Z2 feedback network, for
  the asymptotic-gain model A_f = A_∞·L/(1−L) + 1/(1−L).
