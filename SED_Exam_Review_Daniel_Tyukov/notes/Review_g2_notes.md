# Notes on `Review_g2.pdf` — Group 2's EE4109 Review (graded **8**)

> Reverse-engineering of the reference deck so my own solo review hits the same bar.
> Group 2: 32 slides, 16:9, official TU Delft template, dated 18-5-2026.
> This is the **same A1 hearing-loop receiver-amplifier** assignment I am presenting.

---

## 1. Why it scored an 8 (what the graders rewarded)

Cross-referencing the deck with Antoon's prereview feedback (`Structured electronics prereview notes1.md`):

1. **Strict top-down Structured-Electronic-Design (SED) order.** Specification → ideal
   behaviour (nullor) → noise budget → feedback network → first stage → staging →
   compensation. Never jumps to transistors before the ideal circuit is proven.
2. **"Generate options first, then justify and choose."** Every design fork is shown as a
   *set of options* with trade-offs before a choice is made (Z₁/Z₂ swap, CS vs CG vs CD,
   single vs dual stage, diff-pair vs single-ended). This is the single most-emphasised
   point in Antoon's notes.
3. **"Replace the *how* with the *why*."** Each component is justified by a reason
   (termination R damps the LC resonance; bypass R sets f_min; diff pair gives CMRR).
4. **Every curve in a plot is explained.** The Bode/loop-gain plots are walked through
   (peaking from Q of a pole pair, resonance bump from L₁–C₃).
5. **Real generated data, not hand-waving.** SLiCAP schematics, Bode plots, pole-zero
   tables and noise numbers all come straight from the tool. Key results are
   **highlighted in yellow**.
6. **Honest engineering.** Single stage is *tried*, shown to fail (|L_DC| < 1 → poor
   accuracy), and that failure motivates the dual stage. Antoon: "even if the amp doesn't
   work, they want the understanding."

---

## 2. Slide-by-slide structure (the spine I will mirror)

| # | Slide | Content & figures |
|---|-------|-------------------|
| 1 | **Title** | TU Delft template, campus photo, "Structured Electronics Design — Review", date |
| 2 | **Outline** | 6 blue rounded boxes: 1) Spec/concept 2) Feedback config 3) First stage/noise 4) Single stage 5) Dual stage 6) Frequency compensation |
| 3 | **Specification** | "What to do before constructing the spec": (1) environment, (2) how it works, (3) set spec & budget. System block: input = pickup coil; output = source-select switch + ADC (10 pF) |
| 4 | **Input of A1: Pick-up coil** | "How does it work? *Differentiator*." Flow: loop current → B-field → coil → induced current → V ∝ dΦ/dt. **Internet figure** (induction-loop diagram, majorcom.fr) |
| 5 | **Output of A1** | Source-select switch (mic/loop equal @ ref freq); ADC Z_in = ∞ + 10 pF parasitic only |
| 6 | **How would A1 work?** | (1) integrator, (2) V–V amplifier, (3) gain set at V_mic = V_coil @ ref freq, (4) noise ≤ mic noise floor (DIN-A) |
| 7 | **Circuit Model** | Section header / overview of the model build-up |
| 8 | **Pick-Up Coil Representation** | **Coil datasheet table** (L=120 mH, R=875 Ω, f_res=150 kHz) + C_s derivation → 9.382 pF. SLiCAP schematic (L1,C1,R1,V1) |
| 9 | **Termination Resistor** | "Damp LC resonance." 3 Bode pairs: without R_t / with R_t / critically damped. Q = 2π f_res C_s R_t, Q=1/√2 → **R_t = 79.97 kΩ** |
| 10 | **Ideal Amplifier (nullor)** | E1 = 1/(s·τ_i). Coil sensitivity −59.4 dBV/(A/m) → V_ind(s); mic −35.5 dBV/Pa → **A_v1 = 62.4·10³/s**, τ_i = 16.06 µs |
| 11 | **Output Representation** | ADC load C_L = 10 pF added |
| 12 | **Noise Representation** | Replace nullor with **noisy nullor**; add resistor noise sources |
| 13 | **Noise Budgeting** | Full chain schematic (coil → R_t → nullor → ADC → DIN-A weighting block). Source takes **0.1409** of output-noise power |
| 14 | **Feedback Design (intro)** | Generic **voltage-amplifier feedback model** (Z_s, V_eq/I_eq, Z₁, Z₂, Z_ℓ) — SED-book figure (yellow) |
| 15 | **Feedback Design (options)** | V-in/V-out, integrator τ_i. **Option 1**: Z₁=C, Z₂=R. **Option 2**: Z₂=L, Z₁=R. Trade-offs: inductor size, R noise, manufacturability |
| 16 | **Feedback Design (sizing)** | Noise budget caps R_f max; power budget sets R_f min; pick R then C for τ_i; bypass R sets DC path + f_min |
| 17 | **1st stage — Gm, Ciss, inversion, noise** | Input-referred noise set by 1st stage; 4kTγ/g_m; C_iss loading vs width; weak inversion for max g_m/I_D; nullor → noisy nullor |
| 18 | **1st-stage concept** | Schematic of the controller's first stage |
| 19 | **What stage? CS / CG / CD** | Choose **CS**: smallest T1 (ABCD) matrix → most nullor-like; CG/CD are followers (no gain). CS in saturation = max gain |
| 20 | **Budget → parameter flow** | 6-box flowchart: S_o(f) → integrate → σ₀² = (B_n²·V_onoise)² → g_m(C_iss) → lowest C_iss then g_m,Id,W,L via EKV |
| 21 | **Single Stage** | g_m,c_iss,W,L,I_DS from part 3. Single CS = 3 terminals → diff pair. ≈4× current/area. Drive ✓, headroom ✓, but |L_DC|<1 → poor accuracy → go dual |
| 22 | **Why Dual Stage?** | Hexagon trade-off: noise / power / accuracy / stability / area. "1st stage dominates noise, 2nd stage dominates loop gain" |
| 23 | **Suggested topology** | **1st: PMOS differential pair, 2nd: NMOS common-source** |
| 24 | **First Stage** | Diff pair (lower noise, high CMRR, matches 2-terminal coil, but more area/complexity) vs single-ended CS |
| 25 | **Second Stage** | NMOS CS: high loop gain/accuracy, high current drive, low power, small/simple |
| 26 | **Dual Stage Design** | Parameters: g_m1 (noise budget), g_m2 (extra loop-gain), R_f (transfer), g_o1 (1st-stage output R) |
| 27 | **EKV Small-Signal Model** | Realistic transistor-level; includes parasitic caps → accurate gain plots |
| 28 | **Pole-Zero Analysis** | PZ map + Bode; peaking ~40 MHz from Q of p₄,₅ > 1 (underdamped); stable Re(p)<0 |
| 29 | **Frequency Compensation** | Maximally-flat magnitude; **phantom-zero** method (benefits, implementation). z = −(1−L_DC)p₁p₂/√… ; R_phz = −1/(z·C_L). Full compensated dual-stage transistor schematic |
| 30 | **Frequency Compensation (result)** | Compensated-gain Bode + final pole table |
| 31 | **Thank you** | Closure slide |

---

## 3. Figure inventory (what kinds of images the deck uses)

- **SLiCAP/KiCad schematics** (the coloured ones: `L1 {L_s}`, `CMOS18PD`, `.source/.detector/.lgref` directives). ~9 slides. *I reuse the team's authentic renders for the nullor flow and author a fresh dual-stage transistor schematic.*
- **SLiCAP Bode plots** (magnitude + phase, log-log, blue curves). ~5 slides.
- **SLiCAP pole-zero tables / maps**. ~2 slides.
- **Coil datasheet table** (real product electrical data). 1 slide.
- **One internet figure** (induction-loop concept). 1 slide.
- **Generic feedback model** (Z_s/Z₁/Z₂ voltage-amp, yellow background — from the SED book). 1 slide.
- **LaTeX-rendered formula images** with **yellow highlight** on the key result. Most slides.
- **Block/flow diagrams** (TU Delft blue rounded rectangles; 6-box budget flow; hexagon trade-off).

---

## 4. Numerical anchors (match the same standardized coil, so my numbers agree)

| Quantity | Value |
|---|---|
| Coil inductance L_s | 120 mH |
| Coil series resistance R_s | 875 Ω |
| Coil self-resonance f_res | 150 kHz |
| Source capacitance C_s = 1/((2π f_res)² L_s) | **9.382 pF** |
| Integrator time constant τ_i | **16.06 µs** |
| Ideal gain A_v1 | **62.4·10³ / s** |
| Critical-damping termination R_t (Q=1/√2) | **79.97 kΩ** |
| DIN-A output-noise source fraction | 0.1409 |
| ADC load C_L | 10 pF |
| Supply V_DD / P_max | 0.9–1.3 V / 1 mW |

*(My Team-12 spec CSV confirms identical L_s, R_s, C_s, τ_i — same assignment, so I regenerate these with SLiCAP under my own name and they should reproduce.)*

---

## 5. How my deck improves on G2 (addressing Antoon's exact critiques)

- **Add an explicit "Transfer-function options" slide** — V–V amplifier *vs* transimpedance
  (I–V) with the inductor integrating — and *justify rejecting I–V*. Antoon's notes show G2's
  prereview flip-flopped between these; making the choice explicit is worth marks.
- **Dedicated asymptotic-gain slide** that explains **every** curve (gain, asymptotic,
  loop gain, servo, direct) and the L₁–C₃ resonance bump — the #1 thing Antoon said "we
  should explain everything in this plot."
- **Keep the options-first framing** on every fork, with a one-line *why* under each choice.
- Present **current-reuse (complementary)** and **chopper** as *considered-then-rejected*
  alternatives on the first-stage slide, to show breadth.
