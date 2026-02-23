# Pre-Review Oral Exam Notes — EE4109 Hearing Loop Receiver

## Design Methodology

- **Structured Electronic Design (SED)**: top-down, specification-driven design
- Start from system specs, decompose into stages, derive sub-specs, then size components
- Use SLiCAP for symbolic + numeric analysis; verify with EKV model
- Noise budgeting is central: allocate noise fractions to each contributor, sum must be <= 1
- Technology: **CMOS18 (180 nm)**, EKV MOSFET model throughout

---

## Step 1 — Design Requirements (`hlr_specs.py`)

**What:** Define all top-level system specifications

**Key specs:**
- Battery: 1.4 V, 600 mAh, 100 h lifetime
- Regulated supply: V_DD = 0.9 V
- Max power: P_max = 1 mW
- Audio: hearing loop band 600–6000 Hz, max full-power freq 5 kHz
- Noise floor: 30 dBSPL, max SPL: 110 dBSPL, crest factor: 3
- Source: R_s = 875 Ohm, L_s = 0.12 H (receive coil)
- Termination: R_t = 10 kOhm (ADC input)

**Why these values:**
- Given by the assignment (hearing loop standard, battery constraints, CMOS18 process)
- V_DD = 0.9 V is the regulated output from the 1.4 V battery (LDO regulator)
- P_max = 1 mW sets the hard power budget for the entire analog front-end

---

## Step 2 — System Architecture (`hlr_system.py`)

**What:** Partition the system into three amplifier stages

**Three stages:**
- **A1** — Coil-to-ADC integrating voltage amplifier (main design focus)
  - Transfer: V_out/V_in = 62.4e3 / s (integrator)
  - Coil output ~ dB/dt, so integration recovers the audio signal
  - V_out,pp = 636 mV
- **A2** — Buffer amplifier (gain ~1.41 V/V)
  - Matches A1 output to ADC input range (636 mV -> 900 mV)
  - Z_in = 5.5 kOhm + 10 pF -> cutoff at 2.9 MHz (no issue)
  - Could potentially be a wire if gain margin allows
- **A3** — DAC-to-loudspeaker driver (conceptual only)
  - Single-ended to differential conversion
  - Two topology options discussed; not designed in detail

**Key choice — A1 topology:**
- **Considered:** Differential pair (4-terminal), single transistor (3-terminal)
- **Chosen:** Single transistor common-source in a **3-port nullor feedback topology**
- **Why:** 3-terminal device needs fewer transistors, requires **4x less current** for same noise performance (no current splitting), simpler biasing

---

## Step 3 — A1 Circuit Design (`hlr_a1_circuit.py`)

**What:** Define the A1 integrating amplifier circuit and derive noise specifications

**Schematic:** `A1_design.kicad_sch` — nullor-based integrating feedback amplifier
- Nullor (ideal amplifier) with feedback network: R_i in series with C_i
- Source: L_s + R_s (coil model)
- Load: R_t (ADC termination)

**Key equation:**
- C_i = 1 / ((R_i + R_s) * 62.4e3) — integrator capacitor from time constant

**Noise specs derived:**
- V_noise (DIN-A weighted allowed output noise) from 30 dBSPL requirement
- Vi_pp (max input swing) from 110 dBSPL + coil sensitivity
- C_s = source capacitance from coil self-resonance at 150 kHz

**Why this circuit:**
- The integrating feedback topology directly implements the required 1/s transfer
- Nullor analysis first proves the topology works ideally before adding real devices

---

## Step 4 — Source Noise Analysis (`hlr_source_noise.py`)

**What:** Compute baseline noise from the source (coil + termination) before adding any active components

**Schematic:** `A1_R_noise_without_Ri.kicad_sch` — noise model without R_i

**DIN-A weighting:**
- Standard A-weighting curve for acoustic noise measurement
- Normalized at 1 kHz, applied as multiplicative filter on noise spectral density
- Accounts for human hearing sensitivity vs frequency

**Analysis:**
- `doNoise()` -> output noise spectral density S_onoise
- Multiply by DIN_A^2, integrate from f_min to f_max using scipy.integrate.quad
- RMS noise = sqrt(integral)

**Result:**
- **n_SRC ~ 0.0195** (source consumes ~2% of total noise budget)
- This is fixed — cannot be changed by design choices
- Remaining budget: 1 - 0.0195 = 0.9805 available for R_i and MOS

**Why DIN-A weighting matters:**
- Unweighted noise would overestimate the perceived noise
- DIN-A weighting matches human ear sensitivity — required by the hearing aid standard

---

## Step 5 — Feedback Network Noise (`hlr_fb_noise.py`) [INTERACTIVE]

**What:** Budget noise for R_i, then select R_i value within valid range

**Schematic:** `A1_R_noise_with_Ri.kicad_sch` — noise model including R_i

**Design knobs:**
1. **n_Ri** = fraction of noise budget allocated to R_i
2. **R_i** = actual resistance value

**Constraints on R_i:**
- **Ri_min = V_DD / I_max** = 0.9 / (P_max/2/V_DD) = **1620 Ohm** (power constraint)
- **Ri_max** from noise budget: solve for R_i where DIN-A weighted noise = allowed noise
- If Ri_max < Ri_min -> **design conflict** (noise and power incompatible)

**Iterative DIN-A correction:**
- SLiCAP's `rmsNoise()` integrates unweighted
- Apply correction factor iteratively until DIN-A weighted result converges within 0.1%

**Our choices:**
- **n_Ri = 0.2** — conservative, leaves more budget for MOS (n_M can be up to 0.78)
- **R_i = 5000 Ohm** — mid-range within [1620, 8972] Ohm
- Resulting **C_i = tau_i / (R_i + R_s) = 2.728 nF**

**Tradeoff:**
- Larger R_i -> less power (less current through feedback) but larger C_i (more area)
- Smaller R_i -> more power, smaller C_i, tighter noise constraint on MOS
- n_Ri larger -> more Ri_max headroom, but less budget left for controller noise

---

## Step 6 — Ideal Controller Transfer (`hlr_ideal_ctrl.py`)

**What:** Verify that the circuit with an ideal controller (nullor) gives the correct transfer function

**Schematics:**
1. `A1_Ideal_Controller.kicad_sch` — simplified ideal controller
2. `A1_design copy.kicad_sch` — full A1 design with nullor

**Analyses:**
- Laplace transfer function (symbolic + numeric)
- Two cases: infinite R_i (pure integrator) vs finite R_i (with high-pass corner)
- Pole-zero analysis (symbolic + numeric)
- Step response

**Plots generated:** Magnitude, phase, polar, dB magnitude, group delay, pole-zero map, step response

**Key observations:**
- With infinite R_i: pure integrator (1/s), single pole at origin
- With finite R_i: high-pass zero appears, giving bandpass behavior
- Poles determine bandwidth and stability margins
- The nullor verification confirms the topology is correct before replacing with real transistor

**Why this step matters:**
- Validates the feedback topology independently of controller implementation
- Any issues here indicate topology problems, not device problems
- Sets the benchmark for what the real controller must approximate

---

## Step 7 — Transconductance Optimization (`hlr_gm_opt.py`) [INTERACTIVE]

**What:** Find optimal g_m and c_iss for the controller transistor under remaining noise budget

**Schematic:** `A1_controller_noise_ciss_gm.cir` — noise model with g_m, c_iss as parameters

**Design knobs:**
1. **MOS type:** N or P
2. **n_M** = noise budget fraction for controller

**MOS type choice:**
- **Considered:** NMOS (f_T peak ~50 GHz, higher noise) vs PMOS (f_T peak ~10 GHz, lower noise)
- **Chosen: PMOS**
- **Why:** For this application, the frequency range (600–6000 Hz) is far below f_T, so PMOS f_T (~10 GHz) is more than sufficient. PMOS has lower 1/f noise contribution in this process. Common-source PMOS naturally sources current from V_DD, simplifying biasing.

**Optimization approach:**
1. Express noise as function of f_T = g_m/(2*pi*c_iss) — shows noise improves with higher f_T
2. Solve noise equation for g_m as function of c_iss (given n_M budget)
3. Find **minimum c_iss** (lower bound from denominator constraint)
4. Find **minimum g_m** point (d(g_m)/d(c_iss) = 0) — lowest current solution
5. Find **minimum cost** point (d(g_m * c_iss)/d(c_iss) = 0) — optimal area-current tradeoff

**Our choices:**
- **n_M = 0.5** — uses most of remaining budget (max ~0.781)
- Total noise budget used: 0.0195 + 0.2 + 0.5 = **0.72 (72%)**

**Results:**
- c_iss (optimal) = 4.750e-13 F
- g_m (optimal) = 6.450e-5 S

**Why minimum cost, not minimum g_m:**
- Minimum g_m gives lowest current but very large c_iss (large area)
- Minimum cost (g_m * c_iss product) balances current and area
- More practical for CMOS layout

---
USES THE OLD TOPOLY LOOK AT NEW AB from the new NETLIST
## Step 8 — Transistor Sizing (`hlr_mos_sizing.py`) [INTERACTIVE]

**What:** Translate optimal g_m/c_iss into physical W, L, ID using EKV model

**Schematic:** `A1_controller_noiseWLI_p.cir` — PMOS noise model with W, L, ID

**Design knobs:**
1. **W_finger** = max finger width (layout constraint)
2. **Le** = channel length

**Iterative sizing algorithm:**
1. Start with IC (inversion coefficient) = 1
2. Compute c_iss(W, L, IC) from EKV model, solve for W at target c_iss
3. Round W to integer multiple of W_finger -> M fingers
4. Compute g_m(ID) from EKV, solve for ID at target g_m
5. Recompute IC from actual W, L, ID
6. Repeat until IC converges (< 0.1% change)

**Our choices:**
- **W_finger = 10 um** — standard finger width for 180 nm
- **Le = 0.18 um** — minimum length for maximum f_T

**Results:**
- W = 0.270 mm (total width)
- L = 0.180 um
- M = 27 fingers
- ID = 2.30 uA
- IC = 0.00560 — **deep weak inversion** (subthreshold operation)

**Why minimum length:**
- Minimum L gives maximum f_T (transit frequency)
- Audio application doesn't need long-channel accuracy
- Deep weak inversion -> very low power (uA-level current)

**Noise verification:**
- Recompute DIN-A weighted noise with actual W, L, ID
- Confirm it meets the allocated budget

---

## Step 9 — Controller Analysis (`hlr_controller.py`) [INTERACTIVE]

**What:** Full feedback model analysis with real transistor replacing the nullor

**Schematics:**
1. `single_PMOS.kicad_sch` — single PMOS common-source controller
2. `cascode_PMOS.kicad_sch` — PMOS CS-CG cascode controller

**Biasing:**
- ID_P = -0.6 * I_fb (60% of max feedback current allocated to operating point)
- Width scaled proportionally: W_P = -0.6 * I_fb / ID_P * W_P

**Asymptotic gain model — 5 transfers analyzed:**
1. **Gain** — actual closed-loop transfer function
2. **Asymptotic gain** — gain with infinite loop gain (ideal limit)
3. **Loop gain** — measure of feedback strength (determines accuracy)
4. **Servo** — 1/(1+1/L), bandwidth of the feedback system
5. **Direct transfer** — signal leakage bypassing the controller

**Additional analyses:**
- Pole-zero analysis for all 5 transfers
- Servo bandwidth computation
- Maximum mid-band loop gain: L_MB_max = -g_m * R_i (with parasitic caps removed)

**Cascode comparison (PMOS only):**
- Same analyses repeated for CS-CG cascode topology
- **Purpose:** Cascode improves output impedance -> higher loop gain -> better accuracy
- Comparison of magnitude plots between single and cascode

**Key results to discuss:**
- Loop gain magnitude and phase margin
- How close the gain is to the asymptotic gain (accuracy metric)
- Servo bandwidth vs required signal bandwidth
- Whether the single transistor provides sufficient loop gain or cascode is needed

---

## Step 10 — Operating Point & Biasing (`hlr_biasing.py`)

**What:** Document the final operating point and verify linearity

**No new schematics** — documentation and verification step

**Operating point:**
- W = 18.45 um, L = 0.18 um
- ID = 3.005 uA
- VDS = 636 mV
- V_GS determined from EKV model at this operating point

**Linearity verification:**
- DC sweep: V_in from -50 mV to +50 mV
- Output passes through origin (correct DC bias)
- Noted: not perfectly linear across full input range (weak inversion characteristic)

**Additional output stage:**
- Images show a buffer/level-shifter stage may be needed
- This connects to the A2 buffer discussion from Step 2

---

## Summary of All Design Choices

| Decision | Considered | Chosen | Rationale |
|----------|-----------|--------|-----------|
| A1 topology | Differential pair vs single transistor | Single transistor 3-port | 4x less current for same noise, fewer devices |
| Controller type | NMOS vs PMOS | PMOS | Lower 1/f noise, natural V_DD biasing, f_T sufficient |
| n_Ri | Range (0, 0.98) | 0.2 | Conservative, leaves budget for MOS |
| R_i | [1620, 8972] Ohm | 5000 Ohm | Mid-range: balances power and C_i area |
| n_M | Range (0, 0.78) | 0.5 | Uses most remaining budget for good noise |
| Optimization target | Min g_m vs min cost | Min cost (g_m * c_iss) | Balances current and die area |
| Channel length | >= 0.18 um | 0.18 um (minimum) | Maximum f_T |
| W_finger | 0.18–50 um | 10 um | Standard for C18 process |
| Controller variant | Single CS vs CS-CG cascode | Both analyzed | Cascode gives higher loop gain |

---

## Noise Budget Summary

| Contributor | Budget fraction | Source |
|-------------|----------------|--------|
| Source (coil + R_t) | n_SRC = 0.0195 | Fixed (computed in Step 4) |
| Integrator resistor R_i | n_Ri = 0.200 | Design choice (Step 5) |
| Controller MOS | n_M = 0.500 | Design choice (Step 7) |
| **Total used** | **0.720 (72%)** | |
| Margin remaining | 0.280 (28%) | Safety margin |

Constraint: n_SRC + n_Ri + n_M <= 1

---

## Key Equations to Know

1. **Integration capacitor:** C_i = 1 / ((R_i + R_s) * omega_i) where omega_i = 62.4e3 rad/s
2. **Ri_min (power):** R_i >= V_DD / (P_max / (2 * V_DD)) = 1620 Ohm
3. **Ri_max (noise):** Solve integral of DIN_A^2 * S_noise(R_i) df = V_noise^2 * (n_SRC + n_Ri)
4. **Optimal g_m/c_iss:** Minimize g_m * c_iss subject to noise constraint
5. **f_T = g_m / (2*pi*c_iss)** — figure of merit for speed
6. **EKV model:** IC = ID / (I_0 * W/L), g_m = f(IC, W, L, ID)
7. **Max loop gain:** L_max = g_m * R_i (at DC, ignoring parasitics)
8. **DIN-A weighting:** Standard A-weighting for acoustic noise measurement

---

## Schematic Types Used and Why

| Schematic | Type | Purpose |
|-----------|------|---------|
| A1_design.kicad_sch | Nullor circuit | Prove topology works with ideal controller |
| A1_R_noise_without_Ri.kicad_sch | Noise model | Compute source noise baseline (n_SRC) |
| A1_R_noise_with_Ri.kicad_sch | Noise model | Compute R_i noise contribution, find Ri_max |
| A1_Ideal_Controller.kicad_sch | Ideal controller | Verify transfer function before real devices |
| A1_design copy.kicad_sch | Full design | Pole-zero and step response analysis |
| A1_controller_noise_ciss_gm.cir | Abstract noise model | Optimize g_m vs c_iss (device-independent) |
| A1_controller_noiseWLI_p.cir | EKV noise model | Size W, L, ID with technology parameters |
| single_PMOS.kicad_sch | Real controller | Full feedback analysis with single PMOS |
| cascode_PMOS.kicad_sch | Real controller | Compare cascode vs single for performance |

---

## Potential Oral Exam Questions & Answers

**Q: Why an integrator for A1?**
The receive coil output is proportional to dB/dt (time derivative of magnetic field). Integration recovers the original audio signal. The transfer V_out/V_in = omega_i/s implements this.

**Q: Why PMOS over NMOS?**
At audio frequencies, both have f_T far above the signal band. PMOS has lower 1/f noise in C18 process. Single PMOS common-source naturally sources current from V_DD rail, simplifying the bias network. Also, with a 3-terminal device approach, PMOS avoids needing a current mirror.

**Q: Why single transistor instead of differential pair?**
A 3-terminal single transistor in a 3-port feedback topology uses 4x less current than a differential pair for the same noise performance (no current splitting loss). Fewer transistors means less parasitics and simpler layout.

**Q: How does the noise budget work?**
Total noise is the sum of squared contributions: S_total = S_source + S_Ri + S_MOS. We define fractions n_SRC, n_Ri, n_M such that each contributor's integrated DIN-A weighted noise is n_x * V_noise^2. The sum must be <= 1. Source noise is fixed; we choose how to split the remainder between R_i and MOS.

**Q: Why 72% budget instead of 100%?**
Leaves 28% safety margin. In practice, there are additional noise sources (biasing circuits, supply noise) not captured in the simplified model. The margin accounts for modeling inaccuracies.

**Q: What is the minimum-cost optimization?**
The product g_m * c_iss represents the cost (proportional to current times area). Minimizing this product gives the most efficient design point. It differs from minimizing g_m alone (which gives lowest current but very large c_iss/area).

**Q: Why deep weak inversion (IC = 0.0056)?**
The optimization naturally lands in weak inversion because the required g_m is small (audio frequencies, sufficient noise budget). Weak inversion gives the highest g_m/I_D ratio, so it's the most power-efficient regime. This is a feature, not a limitation.

**Q: What does the asymptotic gain model tell you?**
It decomposes the closed-loop transfer into five components. The gain approaches the asymptotic gain as loop gain increases. The servo function shows the bandwidth. The direct transfer reveals signal leakage. Together they characterize accuracy, bandwidth, and stability.

**Q: Why consider a cascode?**
The single PMOS common-source has limited output impedance (g_o = ID/VAL/L). Adding a common-gate cascode dramatically increases output impedance, which increases loop gain, improving accuracy. The tradeoff is additional complexity and a slightly higher minimum supply voltage.

**Q: What sets Ri_min and Ri_max?**
Ri_min comes from the power constraint: max current I_max = P_max/(2*V_DD), so Ri_min = V_DD/I_max. Ri_max comes from the noise constraint: thermal noise of R_i must stay within the allocated budget fraction n_Ri. If Ri_max < Ri_min, there is a fundamental conflict between power and noise.
