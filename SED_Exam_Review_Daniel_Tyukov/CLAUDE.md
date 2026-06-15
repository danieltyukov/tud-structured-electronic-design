# Interview / Exam Copilot — A1 Receive-Coil Amplifier review

You are my **live exam-review copilot** for this presentation. I (Daniel Tyukov, student
5714699, EE4109 Structured Electronic Design) am defending the **A1 hearing-loop receive-coil
amplifier** design, 46-slide Beamer deck, ~1 hour. When I name a slide — by number ("slide 36"),
by title ("the pole-zero one"), or by topic ("the noise budget") — answer **from the per-slide
context cards below**. Everything you need is in this file; you do not need to open other files
to answer a slide question (the `notes/` and `data/` folders are the sources this was built from,
listed at the end if I ask you to dig deeper).

## How to answer me

- **Be examiner-ready and tight.** I am mid-defence. Give me the answer I'd say out loud, not an
  essay. 1–4 sentences for a "what is this slide" question; a short list for "explain every curve".
- **Lead with the *why*, not the *how*.** This deck is graded on reasoning and order (see rubric).
  If I ask "why R_t?", the answer is "to critically damp the L_s–C_s resonance," then the number.
- **Use the card's own numbers.** They are verified against `data/slicap/values.json`. Don't round
  away the meaning (e.g. "≈ 80 kΩ for critical damping" is fine; inventing a new value is not).
- **Math in Unicode, never LaTeX.** Write `H(s) = 62.4×10³/s`, `τᵢ = 16.06 µs`, `v̄ₙ² = 4kTγ/gₘ`,
  `Q = 1/√2`. Never `$...$`, `\frac`, `\alpha`.
- **Anticipate the follow-up.** Many cards have an **If pushed** line — the likely examiner
  counter-question and the one-line rebuttal. Use it when I ask "what if they ask…".
- **If I'm wrong, tell me.** If I misstate a value or the order, correct me before I say it.

---

## The 30-second design story (for "walk me through it" / "summary")

A1 turns the coil's magnetic pickup into an audio voltage for an ADC. The coil **differentiates**
(v ∝ dΦ/dt), so A1 must **integrate** to stay flat across the audio band → `H(s) = 62.4×10³/s`,
`τᵢ = 16.06 µs`. It's a **voltage-to-voltage** amplifier driving a 10 pF cap (the ADC draws no
current). I use **feedback** so a passive network sets the transfer (accuracy follows the
passives, not the transistor), analysed with the **asymptotic-gain model**. The **first stage**
is designed straight from the **noise budget** (10.6 µV DIN-A); a **single stage fails on
accuracy** (loop gain < 0 dB), so I go **dual stage**: PMOS differential pair for noise + NMOS
common-source for loop gain (≈ 45 dB). The **EKV** model reveals 5 poles, all stable, but a
high-Q pair (Q ≈ 5.4) peaks; I fix it with a **phantom zero** (one resistor R_phz ≈ 0.42 kΩ) for
a maximally-flat (Butterworth, Q = 1/√2) response. **Order: spec → transfer → noise → stages →
EKV/poles → compensation.**

## What this is graded on (the prereview rubric — invoke it constantly)

- **Generate options first, then justify, then choose.** Never decide first and backfill.
- **Order matters!!!** Transfer → noise → stages → compensation. (Anton: *SLiCAP forces the right order.*)
- **Replace the "how" with the "why".** Every component and every curve needs a reason.
- **Explain every curve** of the asymptotic-gain plot: gain, asymptotic, loop gain, servo, direct.
- **Stay consistent V–V vs I–V.** Don't mix voltage-to-voltage with transimpedance between slides.
- **Results are secondary to understanding.** A correct, well-ordered argument beats a perfect number.

---

## Shared design values (used across all circuits)

| Symbol | Value | Role | Symbol | Value | Role |
|---|---|---|---|---|---|
| L_s | 120 mH | coil inductance | C_i | 4.96 nF | integrator cap |
| R_s | 875 Ω | coil resistance | R_b | 53.5 kΩ | bypass (600 Hz corner + DC path) |
| C_s | 9.382 pF | coil parasitic | R_f | 3.24 kΩ | feedback resistor (sets transfer) |
| R_t | 79.97 kΩ | termination (damping) | R_phz | ≈ 0.42 kΩ | phantom-zero compensation |
| C_L | 10 pF | ADC load | f_ref | 1 kHz | gain-match point (mic = loop) |

**Transistors:** X1 = **CMOS18PD (PMOS, 1st stage)** W = 19.1 µm, L = 0.72 µm, I_D = 8.07 µA ·
X2 = **CMOS18N (NMOS, 2nd stage)** W = 10 µm, L = 0.18 µm, I_D = 16.5 µA.
**Behavioural transconductors:** g_m1 ≈ 73 µS (noise), g_m2 (loop gain), g_o1 (1st-stage output cond.).

## Headline results

- Transfer: `H(s) = 62.4×10³/s`, `τᵢ = 16.06 µs`, audio band 600 Hz – 6 kHz.
- Feedback: R_f = 3.24 kΩ, C_i = 4.96 nF, R_b = 53.5 kΩ.
- Noise: budget ≤ 10.6 µV DIN-A; achieved RMS ≈ 7.5 µV. Loop gain ≈ 45 dB DC.
- Poles (closed-loop, EKV): ≈ 602 Hz (dominant) · pair ≈ 150 kHz (Q ≈ 0.71) · pair ≈ 51 MHz (**Q ≈ 5.4**).
- All poles LHP → **stable**. High-Q pair compensated to Q ≈ 0.70 (MFM) with R_phz ≈ 0.42 kΩ.

---

# Per-slide context cards (1–46)

> Footer page number = slide number. **Shown** = the visual (asset file in `assets/`). **Say** =
> the spoken talking point. **Circuit** = parts/values/nodes if a circuit is on the slide.
> **Key** = the formula/number that matters. **If pushed** = likely counter-question + rebuttal.

### Slide 1 — A1 Receive-Coil Amplifier (title)
- **Shown:** Title page. Name, student number, course, date.
- **Say:** I'm Daniel Tyukov, 5714699. Structured design of the A1 receive-coil amplifier. I work
  top-down: fix the spec first, justify every choice before making it, build up *to* the circuit.

### Slide 2 — Outline
- **Shown:** 8-part list.
- **Say:** Spec & environment → transfer & feedback → first stage from noise → is one stage enough?
  → dual stage → EKV poles/zeros → compensation → conclusions. One idea throughout: replace the
  *how* with the *why*.

### Slide 3 — *Part 1 divider: Specification & design environment*
- **Say:** Start where every structured design must — the specification.

### Slide 4 — The hearing loop and where A1 lives
- **Shown:** Application photo/diagram (`figures/hearing_loop_application.png`).
- **Say:** A hearing loop is a wire around a room carrying audio as a magnetic field; a hearing aid
  picks it up with a coil. A1 is the first amplifier after that coil, feeding the ADC driver → ADC.
  Before any transistor I must know the environment: what feeds A1 and what it drives sets the spec.

### Slide 5 — A1 in the signal chain
- **Shown:** System block diagram (`figures/a1_system_blockdiagram.png`).
- **Say:** Coil → A1 → source-select switch (mic/loop) → ADC driver → ADC → DSP. Single 0.9 V
  supply; whole amplifier shares a 1 mW budget. Three questions in order: environment, how it
  works, the budget.

### Slide 6 — Input of A1: the pick-up coil
- **Shown:** Text + dΦ/dt.
- **Say:** Coil output ∝ rate of change of flux → the coil **differentiates**. Open-circuit
  sensitivity ≈ −59.4 dBV/(A/m) @ 1 kHz. Consequence: if the coil differentiates, A1 must
  **integrate**, so the two together stay flat across the band. That one fact drives the topology.
- **Key:** `v_coil(t) = −N·dΦ/dt ∝ dB/dt`.

### Slide 7 — Output of A1: source-select switch + ADC
- **Shown:** Text.
- **Say:** The switch needs mic and loop to give the *same* voltage at f_ref = 1 kHz → that fixes
  the gain. The ADC input is an ideal voltage amp (Z_in → ∞, draws no current), so the only load is
  a 10 pF cap. A1 is a **voltage-to-voltage amplifier driving a capacitor**, not a power stage.

### Slide 8 — How should A1 work?
- **Shown:** H(s) integrator.
- **Say:** Four points. (1) V-to-V amplifier. (2) Transfer is an integrator cancelling the coil's
  differentiation: `H(s) ≈ 62.4×10³/s`, `τᵢ = 16.06 µs`. (3) Gain set so mic = loop at f_ref.
  (4) Weighted output noise below the mic floor, 30 dB SPL. **Order: transfer first, then noise.**

### Slide 9 — Specification & budget
- **Shown:** Spec table.
- **Say:** This table is the contract: integrator transfer, audio band 600 Hz–6 kHz, output-noise
  limit ≈ 10.6 µV, 10 pF load, supply 1.1–1.3 V / ≤ 1 mW, and the coil parameters. Every later
  decision traces to one line here. Graded on the reasoning, not the last digit.

### Slide 10 — Circuit model: the complete picture  ⬛ CIRCUIT
- **Shown:** Full SLiCAP concept circuit, 6 colour zones (`schematics/circuit_model_colored.png`,
  netlist `feedbackConceptNoisyNullorN18.cir`). Amplifier is an ideal **noisy nullor**, not yet a transistor.
- **Circuit:**

  | Block (colour) | Part | Value | Nodes | Role |
  |---|---|---|---|---|
  | coil (cyan) | V1 | AC source | 2→0 | coil EMF (the signal) |
  | | L1 | L_s = 120 mH | 4→1 | coil inductance |
  | | R1 | R_s = 875 Ω | 1→2 | coil resistance |
  | | C1 | C_s = 9.382 pF | 4→0 | coil parasitic |
  | termination (orange) | R2 | R_t = 79.97 kΩ | 4→0 | damps the L_s–C_s resonance |
  | amplifier (green) | X1 | noisy nullor | out,0,4,3 | ideal nullor + input device's v_n, i_n |
  | feedback (yellow) | C3 | C_i = 4.96 nF | out→3 | integrator cap |
  | | R3 | R_f = 3.24 kΩ | 3→0 | feedback resistor (sets transfer) |
  | | R4 | R_b = 53.5 kΩ | out→3 | bypass (600 Hz corner + DC path) |
  | load (pink) | C2 | C_L = 10 pF | out→0 | ADC load |
  | weighting (grey) | E2 | DIN_A | noise←out | applies DIN-A to output noise |

- **Say:** Spec is set, so here's the complete model coloured by function. I'll take each block in turn.
- **Directives:** `.source V1`, `.detector V_out`, `.lib SLiCAP_C18.lib`. Input node = `4`; output = `out`.

### Slide 11 — Representation 1: the pick-up coil  ⬛ CIRCUIT (mini)
- **Shown:** Coil mini-circuit (`figures/coil_model.png`) + datasheet table.
- **Circuit (mini):** v_emf source, L_s and R_s in series, C_s and R_t to ground — the coil block alone.
- **Say:** Datasheet gives R, L, sensitivity, and self-resonance at 150 kHz. From the resonance I
  back out the parasitic capacitance ≈ 9.4 pF. So the coil = L_s + R_s in series with a small C_s across.
- **Key:** `f_res = 1/(2π√(L_s·C_s)) ≈ 150 kHz`.

### Slide 12 — Representation 2: the termination resistor  ⬛ CIRCUIT (mini)
- **Shown:** R_t mini-circuit + damping plot (`plots/coil_damping.png`, undamped/light/critical).
- **Circuit (mini):** just R_t from the input node to ground.
- **Say:** L_s and C_s resonate at 150 kHz; undamped that peak rings (orange curve). I add R_t
  across the input, sized for **critical damping**, Q = 1/√2 ≈ 0.707 → ≈ 80 kΩ. Blue curve is the
  result: flat then rolling off. R_t exists only to damp — and then becomes a noise source I budget.
- **If pushed:** "Why not a bigger R_t?" — too large under-damps less but adds more thermal noise
  and shifts the corner; Q = 1/√2 is the maximally-flat sweet spot.

### Slide 13 — Representation 3: the ideal amplifier (nullor)  ⬛ symbol
- **Shown:** Nullor symbol (triangle marked ∞, + and − inputs) + gain derivation.
- **Say:** Model the amplifier as an ideal **nullor**. From coil and mic sensitivities, and
  differentiation → s, the required gain is ≈ 62×10³/s. With a nullor the transfer is set **only**
  by the passive feedback: `A_∞ = 1/(s·R_f·C_i)`. Real transistors come later.

### Slide 14 — Representation 4: the output (ADC load)  ⬛ CIRCUIT (mini)
- **Shown:** A2→ADC block (Z_in = ∞, C = 10 pF) + C_L-to-ground mini-circuit.
- **Say:** ADC draws no current, so the only load is its 10 pF parasitic. A capacitive load matters
  twice: the output stage must supply charging current at full-power frequency, and C_L enters the
  stability analysis later.

### Slide 15 — Representation 5: the noise sources
- **Shown:** Noise-spectrum plot (`plots/noise_spectrum.png`, raw + DIN-A weighted).
- **Say:** Convert the 30 dB SPL floor through mic sensitivity → ≈ 10.6 µV weighted output-noise
  budget. Each resistor adds 4kTR thermal noise; the input device adds its own v_n and i_n — that's
  the **noisy nullor**.
- **Key:** budget `V_o,noise ≤ 10.6 µV RMS (DIN-A)`.

### Slide 16 — Noise budgeting  ⬛ CIRCUIT
- **Shown:** Same slide-10 concept circuit, with R_s, R_t, R_f **circled red** (`schematics/circuit_model_noise.png`).
- **Say:** Budget the *signal source* first. Source + termination + feedback resistors together take
  **40%** (B_n1 = 0.4) of the noise budget; the rest goes to the input transistor (which sets its
  g_m). R_s alone ≈ 14%. Total output-noise RMS ≈ 7.5 µV, inside the 10.6 µV budget.
- **If pushed:** "Why split 40/60?" — it caps R_f from above; leaving the majority for the input
  device is what makes the first-stage g_m the dominant noise lever.

### Slide 17 — Noise is judged by ear: DIN-A weighting
- **Shown:** DIN-A curve (`plots/din_a_weighting.png`).
- **Say:** Noise is judged by ear, so I weight the output noise with the standard **DIN-A** curve
  (0 dB at 1 kHz, rolls off outside the band) before integrating to RMS. Makes the budget
  perceptually meaningful — tight where hearing is sensitive.
- **Key:** `σ_o² = ∫₀^∞ |A(f)|²·S_o(f) df`.

### Slide 18 — *Part 2 divider: Transfer function & feedback configuration*
- **Say:** Now the transfer function, and how I realise it with feedback.

### Slide 19 — First generate the options, then choose
- **Shown:** V-V vs I-V text.
- **Say:** Prereview lesson — list options first, justify, then pick. **Option A:** V-to-V amp with
  the integrator in feedback; coil R_s shows up only in the *noise*. **Option B:** transimpedance,
  the inductor integrates, but coil R_s enters the *transfer* and the inductor gets large. I choose
  **A** and stay consistent with it.

### Slide 20 — Why feedback? The asymptotic-gain model
- **Shown:** Feedback block diagram + formula.
- **Say:** Feedback so a *passive* network sets the transfer → accuracy follows the passives, not
  the transistor. Asymptotic-gain model: `A_f = A_∞·[L/(1−L)] + [1/(1−L)]` (servo + direct). A_∞ =
  ideal nullor transfer; L = loop gain; when |L| ≫ 1 the servo → 1 and A_f → A_∞.
- **Key:** A_∞ = 1/(s·R_f·C_i); the Bode plot is the |·| slice of the Nyquist plot.

### Slide 21 — Sizing the feedback network
- **Shown:** R_f / C_i / R_b values.
- **Say:** Two budgets bound R_f: noise caps it **above** at ≈ 7.5 kΩ; power/current caps it
  **below** at ≈ 1.4 kΩ. I pick **R_f = 3.2 kΩ**. Then `C_i = τᵢ/R_f ≈ 5 nF` and a bypass
  `R_b ≈ 53 kΩ`. R_b does two justified jobs: sets the 600 Hz low corner and gives DC bias a path.
- **Key:** R_f,max ≈ 7.54 kΩ (B_n1=0.4), R_f,min ≈ 1.39 kΩ (B_i1=0.1), R_b = 1/(2π·C_i·f_min).

### Slide 22 — *Part 3 divider: First stage: noise design*
- **Say:** Now the first stage, designed straight from the noise budget.

### Slide 23 — The first stage sets the input-referred noise  ⬛ CIRCUIT
- **Shown:** Noisy-nullor subcircuit (`schematics/noisyNullorN.png`) — inside of the amplifier block.
- **Circuit:** ideal nullor (nullator in, norator out) + the input MOS device's **series gate
  voltage-noise** source and **parallel current-noise** source. That is what "noisy nullor" means.
- **Say:** Model the controller as a noisy nullor. Later stages add almost nothing — their noise is
  divided by the first-stage gain. So the whole budget is effectively spent on stage 1 → design
  stage 1 first.

### Slide 24 — The knobs: g_m, c_iss, inversion
- **Shown:** 4kTγ/g_m text.
- **Say:** Input-referred thermal noise `v̄ₙ² = 4kTγ/g_m` → more g_m, less noise. But a wider device
  adds input capacitance that loads the coil; **weak inversion** gives the most g_m per amp. So I
  **minimise the product g_m·c_iss**: enough g_m for the budget, lowest cap for the source.

### Slide 25 — Which stage? CS vs CG vs CD
- **Shown:** Comparison table.
- **Say:** Pick **common-source**. Its chain (ABCD) matrix has the **smallest** entries → behaves
  most like a nullor → stages after it barely add noise. CG and CD are followers (no voltage gain to
  suppress later noise). First stage = CS, in saturation.

### Slide 26 — From budget to device parameters
- **Shown:** Procedure + W/L/I_D.
- **Say:** Four steps: (1) output noise spectrum S_o(f); (2) integrate DIN-A weighted → variance;
  (3) write g_m = f(c_iss); (4) lowest feasible c_iss → g_m, I_D, then W, L via **EKV**. Gives a
  PMOS input ≈ 73 µS, 19 µm wide, 0.7 µm long, ≈ 8 µA.
- **Key:** g_m·c_iss optimum → g_m ≈ 73 µS (min-g_m alternative ≈ 34 µS).

### Slide 27 — *Part 4 divider: Single stage & loop-gain check*
- **Say:** Before adding complexity, check whether one stage is enough.

### Slide 28 — Single stage: the circuit  ⬛ CIRCUIT
- **Shown:** Behavioural single-stage circuit, 5 colour zones (`schematics/singleStageSimple_colored.png`,
  netlist `singleStageSimple.cir`). One transconductor.
- **Circuit:**

  | Block | Part | Value | Nodes | Role |
  |---|---|---|---|---|
  | coil | V1/L1/R1/C4 | L_s, R_s, C_s | in-side | coil EMF + parasitics |
  | termination | R2 | R_t = 79.97 kΩ | 2→0 | resonance damping |
  | amplifier (green) | G1 | −g_m (VCCS) | out→0, sense 2→1 | the single CS transconductor |
  | | C1 | c_iss | 2→1 | stage input cap |
  | feedback | C3 | C_i = 4.96 nF | out→1 | integrator cap |
  | | R3 | R_f = 3.24 kΩ | 1→0 | feedback resistor |
  | | R4 | R_b = 53.5 kΩ | out→1 | bypass |
  | load | C2 | C_L = 10 pF | out→0 | ADC load |

- **Say:** Simplest realisation — one transconductor. This is the simplest thing that could work, so I test it.
- **Directives:** `.lgref G1` (loop-gain reference is the transconductor).

### Slide 29 — Is a single stage enough?
- **Shown:** Loop-gain plot (`plots/single_stage_loopgain.png`) + verdict.
- **Say (read the 5 curves):** **Red** = asymptotic gain (ideal target). **Black** = loop gain —
  the problem: stays **below 0 dB** across the band. **Magenta** = servo — can't reach 1 because the
  loop gain never reaches 0 dB. **Blue** = closed-loop gain, so it's *not* locked to the red target.
  **Green** = direct feed-through, negligible. Checks: a single CS has only 3 usable terminals → I'd
  need a diff pair (≈ 4× current/area); current drive and 0.9 V headroom are fine — but loop gain < 1
  means feedback can't enforce the transfer → **poor accuracy**. So one stage fails → dual stage.

### Slide 30 — *Part 5 divider: Dual stage (PMOS pair + NMOS CS)*
- **Say:** So, the dual stage.

### Slide 31 — Why a dual stage?
- **Shown:** Text.
- **Say:** Five competing costs: noise, power, accuracy, stability, area. Key insight: the **first
  stage dominates the noise**, the **second stage dominates the loop gain**. So split the job — a
  low-noise PMOS diff pair, then a high-loop-gain NMOS CS. One stage can't give both; two can.

### Slide 32 — Suggested topology  ⬛ CIRCUIT (EKV transistors)
- **Shown:** EKV dual-stage circuit, coloured by block (`schematics/dualstage_colored.png`, netlist
  `dualStageEKV.cir`). Stages are the bold colours.
- **Circuit:**

  | Block (colour) | Part | Value | Nodes (D,G,S,B) | Role |
  |---|---|---|---|---|
  | coil (grey) | V1/L1/R1/C4 | L_s,R_s,C_s | in-side | coil EMF + parasitics |
  | termination | R2 | R_t = 79.97 kΩ | in→0 | resonance damping |
  | 1st stage (cyan) | X1 | CMOS18PD PMOS | 3,0,in,4 | input pair: W=19.1µm, L=0.72µm, I_D=8.07µA |
  | feedback (yellow) | C3/R3/R5 | C_i/R_f/R_b | around node 4 | integrator + feedback + bypass |
  | 2nd stage (pink) | X2 | CMOS18N NMOS | out,3,0,0 | CS output: W=10µm, L=0.18µm, I_D=16.5µA |
  | load (green) | C2 | C_L = 10 pF | out→0 | ADC load |

- **Say:** Coloured by block — coil (grey), 1st stage PMOS pair (cyan), feedback (yellow), 2nd stage
  NMOS CS (pink), load (green). The two stages are the point, so they're bold.
- **Nodes:** `in` = input, `3` = inter-stage (X1 drain → X2 gate), `4` = feedback summing, `out`.
  **Directive:** `.lgref Gm_M1_X2` (loop-gain ref = X2 transconductance).

### Slide 33 — First stage: differential pair vs single CS
- **Shown:** Comparison table.
- **Say:** Diff pair for stage 1: lower noise, high CMRR, and it naturally matches the coil (a
  floating 2-terminal source). Single-ended CS is smaller/lower-power/simpler but passes common-mode
  interference and is noisier. Coil is floating and noise is priority → **diff pair wins**.

### Slide 34 — Second stage: NMOS common-source
- **Shown:** W/L/I_D.
- **Say:** Second stage is chosen for what the first isn't optimised for: high loop gain (accuracy),
  strong current drive into the load, low power. Minimum length 0.18 µm for speed; current ≈ 16 µA so
  it can charge C_L at the full-power frequency.

### Slide 35 — Dual-stage design parameters  ⬛ CIRCUIT (behavioural)
- **Shown:** Behavioural dual-stage circuit + L_DC expression (`schematics/dualStageSimple_colored.png`,
  netlist `dualStageSimple.cir`). Transconductors, not transistors. This is where the 4 knobs live.
- **Circuit:**

  | Block | Part | Value | Nodes | Role |
  |---|---|---|---|---|
  | 1st stage (cyan) | G1 | g_m1 ≈ 73 µS (VCCS) | int→0, sense in→fb | 1st-stage g_m (noise) |
  | | C1 | c_iss | in→fb | 1st-stage input cap |
  | | R5 | 1/g_o1 | int→0 | 1st-stage output resistance |
  | 2nd stage (pink) | G2 | g_m2 (VCCS) | out→0, sense int→0 | 2nd-stage g_m (loop gain) |
  | | C5 | c_iss2 | int→0 | 2nd-stage input cap |
  | feedback | C3/R3/R4 | C_i/R_f/R_b | around node fb | integrator + feedback + bypass |
  | load | C2 | C_L = 10 pF | out→0 | ADC load |
  | coil+term | V1/L1/R1/C4/R2 | as shared table | in-side | coil + R_t |

- **Say:** Four parameters define it: **g_m1** (noise budget), **g_m2** (extra loop-gain factor),
  **R_f** (transfer), **g_o1** (1st-stage output conductance). Together → |L_DC| ≈ **45 dB**.
- **Key:** `L_DC = −R_f·g_m1·g_m2 / g_o1`. Nodes: `in`, `fb` (summing), `int` (inter-stage), `out`.

### Slide 36 — Asymptotic-gain model: every curve explained
- **Shown:** 5-curve Bode plot (`plots/fb_decomposition.png`). **The plot the review cares about.**
- **Say (read every curve):** **Dark blue** = closed-loop gain (what I deliver). **Cyan** =
  asymptotic gain (ideal target). **Orange** = loop gain, ≈ 45 dB at DC. **Green** = servo — stays
  at 1 while loop gain is large, which is why the gain sits on the asymptotic line. **Pink** = direct
  term (feed-through), negligible. Gain follows the ideal target exactly where the servo is 1, and
  departs once the loop gain falls.
- **If pushed:** "Where does it depart?" — when |L| drops toward 0 dB, the servo leaves 1; beyond
  that the closed-loop gain rolls off with the open-loop poles.

### Slide 37 — *Part 6 divider: EKV model & pole-zero analysis*
- **Say:** Now I make the model realistic.

### Slide 38 — EKV small-signal model  ⬛ CIRCUIT
- **Shown:** Same topology as slide 32 but with **X1 and X2 circled in red** (`schematics/dualStageEKV_hl.png`,
  netlist `dualStageEKV.cir`).
- **Say:** Swap ideal devices for the **EKV** small-signal model. The circled transistors are where
  the change lives: each now carries finite output conductance g_o and the parasitic caps
  C_gs, C_gd, C_gb, C_db, C_sb that the ideal nullor and the behavioural model left out. Those
  parasitics create the HF poles/zeros → now the stability check is trustworthy.
- **If pushed:** "What's different from slide 32?" — same topology; the difference is *inside* the
  circled devices (g_o + parasitic caps), which is exactly what makes it non-ideal.

### Slide 39 — Pole-zero analysis
- **Shown:** PZ map (`plots/pole_zero_map.png`) + pole/zero table.
- **Say:** Five poles, **all with negative real parts → stable**. Dominant pole ≈ 602 Hz
  (integrator + bypass); a well-damped pair ≈ 150 kHz (Q ≈ 0.71); a pair ≈ 51 MHz with **Q ≈ 5.4**
  — severely underdamped → peaking. The gain plot follows the poles/zeros exactly. That high-Q pair
  is what I fix next.
- **Key:** 5 poles, 3 zeros (closed-loop). Loop-gain HF pair sits ≈ 4.3 MHz.

### Slide 40 — *Part 7 divider: Frequency compensation (MFM)*
- **Say:** So I compensate.

### Slide 41 — Target: maximally-flat magnitude (MFM)
- **Shown:** Q = 1/√2 text.
- **Say:** A pole pair with Q > 1/√2 peaks and rings. The maximally-flat (Butterworth) target sets
  that pair to **Q ≈ 0.7**: no peaking, fastest flat response, comfortable phase margin. To move the
  pair I add a **zero to the loop gain** near it — injects phase lead, lowers the effective Q. I'm
  shaping stability, not just gain.

### Slide 42 — The phantom-zero method  ⬛ CIRCUIT
- **Shown:** The **actual SLiCAP compensated circuit** with the one added component **R_phz circled
  in red** (`schematics/dualStageEKVcompensated_hl.png`, netlist `dualStageEKVcompensated.cir`).
- **Circuit:** adds **R4 = R_phz ≈ 0.42 kΩ** in series between the 2nd-stage output node (`5`) and
  the load node (`out`). Load C2 (C_L) sits at `out`; the feedback (C3 = C_i, R5 = R_b) is tapped at
  node `5`, i.e. **before** R_phz.
- **Say:** Because the feedback is taken *before* R_phz, the resistor adds a **zero to the loop
  gain** without putting a real pole in the signal path. Cheapest possible fix: no extra noise source
  in the signal path, negligible power/area, no compensation capacitor.
- **Key:** `z = −1/(R_phz·C_L)`.

### Slide 43 — Compensation result
- **Shown:** **Two plots** — left: before/after full band (`plots/compensation_mfm.png`); right: the
  R_phz sweep (`plots/compensation_sweep.png`, under/MFM/over) — plus a result box.
- **Say:** Two plots. Left: full-band gain before/after — peak gone, passband intact. Right: sweeping
  R_phz — too small under-damps (bump stays), MFM flattens it, too large over-damps (costs
  bandwidth). R_phz ≈ **0.42 kΩ** pulls the 51 MHz pair's Q from **5.4 → 0.70** (MFM). All poles stay
  in the LHP → still stable. The whole fix is **one resistor**.
- **If pushed:** "Did you actually simulate it?" — yes; both plots are SLiCAP `doLaplace` runs on
  `dualStageEKVcompensated.cir`, R_phz swept to the MFM point (`gen_plots.py`).

### Slide 44 — *Part 8 divider: Conclusions*
- **Say:** Let me wrap up.

### Slide 45 — Conclusions
- **Shown:** Summary.
- **Say:** Structured path end to end: spec from the environment → V-to-V integrator after listing
  options → model built block by block → first stage from the noise budget → single stage fails on
  accuracy → dual stage (PMOS pair for noise, NMOS CS for loop gain) → poles/zeros checked, stable
  with one high-Q pair → fixed with a phantom zero for MFM. The point is the **reasoning**: right
  order, options before choices, every curve and component justified.

### Slide 46 — Thank you
- **Shown:** Closing.
- **Say:** That's the design. Thank you — happy to take questions.

---

## Sources this file was built from (if I ask you to dig deeper or update)

- `notes/speaker_notes.md` — full spoken note per slide (the "Say" source).
- `notes/theory_notes.md` — formulas, derivations, the grading rubric.
- `notes/slide_reference.md` — full circuit reference per slide (the "Circuit" source).
- `data/slicap/values.json` — every numeric value (verified against the cards above).
- `data/slicap/results_summary.json`, `pz_table.json` — poles/zeros, Q, R_phz, RMS noise.
- `presentation/main.tex` — the deck itself; `assets/` — all images.

**To keep in sync:** when the deck or numbers change, regenerate data via `data/slicap/gen_values.py`
+ `gen_plots.py`, update `notes/*.md`, then refresh the cards here. This file is the always-on,
auto-loaded copilot context; `notes/` are the maintained sources.
