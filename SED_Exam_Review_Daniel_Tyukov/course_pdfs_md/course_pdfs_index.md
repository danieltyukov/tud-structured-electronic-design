# EE4109 Course PDFs - Figure & Topic Index

## PDF Summary Table

| PDF File | Pages | Main Topics | Key Figures (Page #) | Relevance to Hearing Loop Amp Design |
|----------|-------|-------------|----------------------|--------------------------------------|
| **HearingLoopIntro.pdf** | 3 | Hearing loop system overview, application architecture, pick-up coil, electromagnetic induction concept, system block diagram, specifications (noise, frequency range, power) | Pages 1-3: System block diagram, signal flow, pick-up coil location in system | System context, pick-up coil as input transducer, induction loop concept |
| **FeedbackStages-intro.pdf** | 72 | Feedback fundamentals, feedback networks, T1 matrix parameters, feedback types (series/parallel, voltage/current), feedback configurations, asymptotic gain model, servo loop analysis | Pages 2-40+: Feedback diagrams, T1 matrix tables, feedback topologies; Pages 50+: Loop-gain/asymptotic models | V-V amplifier topology, feedback network design, servo loop for accurate gain |
| **PrincipleOfAmplification.pdf** | 40 | Amplification basics, biasing formalism, device equations, signal integrity, nullor concept, load transfer | Pages 2-10: Amplifier block diagram, signal correspondence principle; Pages 30+: Nullor representations | Foundational amplifier topology, understanding gain distribution |
| **FeedbackAmpCSstageNoiseDesign.pdf** | 14 | Noise model (MOS device), noise transformations, input-referred noise, noise budgeting, nullor representation in noise analysis, design equation | Pages 1-3: Feedback structure, noise transfer functions; Page 4-5: MOS noise model, thermal/1/f noise; Pages 7-14: Noise design equations | Input-stage noise budget, input capacitance/transconductance tradeoff, inversion coefficient impact |
| **mosEKVmodel.pdf** | 105 | MOS transistor physics, weak/strong inversion regions, EKV model parameters, inversion coefficient, transconductance gm, input capacitance c_iss, EKV drain current equation | Pages 1-50: MOS physics, inversion regions; Pages 50-80+: EKV equations, gm/c_iss behavior across inversion levels | Inversion coefficient choice, gm/ID ratio, weak-inversion operation for low-noise/low-power |
| **mosEKVmodelApplication.pdf** | 24 | EKV model application to design, gm vs current, transconductance scaling, design procedures | Pages 1-24: Design charts, gm/ID curves, area/current tradeoffs | Practical design: sizing W/L from gm and current specs |
| **CSstage-intro.pdf** | 38 | Common-source stage introduction, small-signal behavior, biasing, load-effect on gain | Pages 1-20+: CS stage schematic, bias point analysis; Pages 20+: Small-signal models | Input stage topology choice, CS gain behavior, load impedance effects |
| **CSstage-intrinsic.pdf** | 91 | CS stage intrinsic behavior, small-signal T1 matrix parameters, intrinsic gain, frequency response, nullor-like behavior, inversion coefficient effects, weak/strong inversion | Pages 1-30: CS stage ABCD/T1 matrices; Pages 40-60: Inversion coefficient impact; Pages 70+: Frequency response | CS stage chain matrices for cascading, understanding "nullor-like" behavior in feedback |
| **FeedbackStages-CG-stage.pdf** | 44 | Common-gate feedback stage, current follower, feedback effects on input impedance, current comparison feedback, series-shunt feedback | Pages 1-20: CG stage schematic, feedback topology; Pages 30+: Behavior modifications from feedback | Alternative feedback topology, input impedance shaping |
| **FeedbackStages-CD-stage.pdf** | 53 | Common-drain (source-follower) stage, voltage follower, feedback effects, series feedback, parallel output feedback, impedance transformation | Pages 1-20: CD stage schematic, follower behavior; Pages 30+: Feedback effects | Output buffering option, impedance matching |
| **Balancing-intro.pdf** | 27 | Balancing concept, differential pair as balanced circuit, common-mode rejection, symmetry | Pages 1-15: Differential pair basic structure, CMRR concept | Balanced input stage alternative to single CS |
| **Balancing-differential-pair.pdf** | 44 | Differential pair in detail, anti-series CS connection, matched transistors, common-mode behavior, PSRR, noise balancing | Pages 1-30: Diff-pair topology, matching; Pages 30+: CMRR/PSRR analysis | Noise-optimal differential input stage, pair balancing |
| **ControllerDesign.pdf** | 27 | Controller (amplifier) design methodology, input stage (CS/balanced), output stage (complementary parallel CS), nullor-like behavior, distortion minimization, number of stages | Pages 1-15: Input stage choice (CS vs balanced); Pages 15-20: Output stage (complementary parallel); Pages 20-27: 1-stage vs 2-stage vs multi-stage | Hearing-loop amp input/output stage selection, cascading strategy |
| **PreferredStages.pdf** | 12 | Preferred amplifier stages for low-noise, low-power design, stage rankings by performance metric | Pages 1-12: Stage comparison tables and rankings | Informed stage selection for noise budget |
| **FeedbackStages-other.pdf** | 41 | Other feedback topologies (transimpedance, transadmittance, etc.), load interface networks | Pages 1-41: Various feedback amplifier topologies | Transimpedance option for current input from pick-up coil |
| **Biasing.pdf** | 1 | Biasing overview poster | Page 1: Biasing techniques summary | Quick reference for DC operating point |
| **BiasingImplementation.pdf** | 40 | Biasing circuit design, current mirrors, cascode biasing, temperature stability | Pages 1-40: Bias circuit topologies, current sources | Implementing DC bias for amplifier stages |
| **Balancing-two-terminal.pdf** | 47 | Two-terminal balancing (impedance networks), impedance matching, source/load interaction | Pages 1-47: Balancing circuit topologies | Interface network design between stages |
| **Balancing-push-pull-stage.pdf** | 45 | Push-pull output stage, complementary pair, distortion analysis, output swing | Pages 1-45: Push-pull driver, output stage behavior | Output stage power delivery |
| **LDRamp.pdf** | 2 | Load-line diagram concept (brief) | Pages 1-2: Load-line analysis | DC operating point visualization |
| **LPproductStages.pdf** | 24 | LC-ladder, low-pass product stages, frequency response shaping | Pages 1-24: Low-pass filter/equalizer stages | Optional: if frequency shaping needed in hearing-loop path |
| **StagesInterconnection.pdf** | 7 | Connecting amplifier stages, inter-stage impedances, buffer stages | Pages 1-7: Stage cascading, interface networks | Impedance matching between CS/CD/CG stages |
| **Biasing.pdf** | 1 | Biasing overview | Page 1 | Biasing reference |
| **Balancing-two-ports.pdf** | 28 | Two-port balancing, differential port concepts | Pages 1-28 | Advanced balancing |
| **quizBiasingTechniques.pdf** | 52 | Biasing quiz/reference problems | Pages 1-52 | Biasing design examples |
| **AmpStagesPoster.pdf** | 1 | Amplifier stages poster summary | Page 1 | Quick stage reference |
| **MOStransistorModelingAndDesignPoster.pdf** | 1 | MOS transistor design poster | Page 1 | Quick MOS reference |
| **CMOScontrollerDesignPosterPalette.pdf** | 1 | CMOS controller design poster | Page 1 | Design method overview |
| **posterBalancing.pdf** | 1 | Balancing techniques poster | Page 1 | Balanced circuit summary |
| **CourseIntro.pdf** | 6 | Course overview, EE4109 structure, hearing-loop project introduction | Pages 1-6: Structured Electronics Design course context | Project context and methodology |

---

## Figure Shopping List for Hearing-Loop Amplifier Review Slides

**Target: One best (file, page) reference for each critical topic**

### Topic: Hearing Loop System Overview / Induction Loop Concept
- **Best source:** HearingLoopIntro.pdf, page 2
- **Content:** System block diagram showing pick-up coil input, electronic processing, induction loop output; signal flow from magnetic field to electrical; specification table (noise 30 dBSPL, 600Hz-6kHz)
- **Use case:** Title slide context, system spec summary

### Topic: Pick-Up Coil as Differentiator + LC Model + Termination Resistor
- **Best source:** HearingLoopIntro.pdf, page 1
- **Content:** Pick-up coil location in application diagram; electromagnetic signal (70dB SPL = 0.1 A/m), electrical output (−59.4 dBV/@1kHz)
- **Note:** Detailed coil model may require design document; this PDF shows system perspective
- **Use case:** Input transducer specifications and interface

### Topic: Feedback Configuration (V-V Amplifier), Asymptotic-Gain / Servo / Loop-Gain Model
- **Best source:** FeedbackStages-intro.pdf, pages 2–12
- **Content:** Feedback diagram (feedback network copies load signal to match source); T1 matrix (pages 8-12 show feedback type table: series/parallel, voltage/current); pages 50+ show asymptotic gain and loop-gain concepts
- **Use case:** Explain why feedback is used; voltage-follower vs transimpedance choice

### Topic: Noise Model (Noisy Nullor, Input-Referred Noise, Noise Budgeting)
- **Best source:** FeedbackAmpCSstageNoiseDesign.pdf, pages 4–6 (MOS noise model), pages 7–10 (noise design equations)
- **Content:** MOS transistor noise (thermal + flicker); input-referred voltage/current noise; nullor with noise sources; weighted output noise equation
- **Use case:** Justify input stage design (gm/c_iss choice), noise budget allocation

### Topic: gm / c_iss / Inversion Coefficient, EKV Model
- **Best source:** mosEKVmodel.pdf, pages 20–50 (inversion regions + EKV equations); mosEKVmodelApplication.pdf, pages 1–10 (design charts)
- **Content:** Weak/strong inversion operation; EKV transconductance equation; gm/ID ratio vs inversion coefficient; input capacitance scaling with current/geometry
- **Use case:** Design-point selection (gm for noise, c_iss for stability); W/L sizing justification

### Topic: CS vs CG vs CD Stage Choice (Chain/ABCD Matrices, "Nullor-Like" Behavior)
- **Best source:** CSstage-intrinsic.pdf, pages 1–30 (T1 matrices); ControllerDesign.pdf, pages 3–7 (stage selection rationale)
- **Content:** CS stage ABCD parameters (voltage gain A, input/output impedance B,C,D); explanation of "nullor-like" = high gain + low output impedance; CG/CD feedback modifications
- **Use case:** Justify CS input stage for low noise; understand gain per stage

### Topic: Differential Pair vs Single CS (Noise Balancing)
- **Best source:** Balancing-differential-pair.pdf, pages 1–20; ControllerDesign.pdf, page 5 ("CS or balanced — best nullor-like")
- **Content:** Anti-series CS structure; matched pair diagram; noise cancellation in differential mode
- **Use case:** Input stage architecture decision (single-ended vs differential for CMRR/noise)

### Topic: Dual-Stage Controller Topology (PMOS Diff-Pair + NMOS CS)
- **Best source:** ControllerDesign.pdf, pages 1–27 (two-stage design flow)
- **Content:** Input stage (noise-optimized); output stage (high-drive, complementary parallel CS); cascading, total gain distribution
- **Use case:** Amp architecture overview: why 2 stages vs 1 stage

### Topic: Frequency Compensation, Phantom Zero, Pole Splitting, MFM
- **Best source:** FeedbackStages-intro.pdf (50+ pages have frequency-compensation aspects in feedback loop-gain); ControllerDesign.pdf (stability discussion in multi-stage section)
- **Note:** Explicit compensation-circuit PDFs not found in current collection; refer to course textbooks or FeedbackStages series for loop-gain Bode
- **Content:** Feedback loop-gain magnitude/phase for stability margin; dominant pole placement; frequency-dependent feedback
- **Use case:** Stability argument for two-stage design; gain-bandwidth tradeoff

### Topic: Bode / Pole-Zero Plots, DIN-A Weighting (Audio Filtering)
- **Best source:** FeedbackStages-intro.pdf (frequency response in feedback context); LPproductStages.pdf, pages 1–10 (low-pass filter design)
- **Content:** Frequency response of feedback-configured stages; optional low-pass shaping for audio band limiting
- **Use case:** Loop-gain Bode for stability; optional anti-aliasing filter

---

## Top 10 Most Useful Figure Sources for Presentation

1. **HearingLoopIntro.pdf, page 2** — System block diagram + specs (context)
2. **FeedbackStages-intro.pdf, pages 8–12** — Feedback topology table & T1 matrices (V-V amplifier choice)
3. **FeedbackAmpCSstageNoiseDesign.pdf, page 4** — MOS noise model (noisy nullor, Vn/In sources)
4. **mosEKVmodel.pdf, pages 40–50** — Inversion coefficient vs gm/c_iss curves (design trade-off)
5. **CSstage-intrinsic.pdf, pages 1–10** — CS stage ABCD matrices & nullor equivalence (gain per stage)
6. **ControllerDesign.pdf, pages 1–15** — Input stage selection (CS vs balanced), noise-optimal choice
7. **Balancing-differential-pair.pdf, pages 1–15** — Differential pair structure (if using balanced input)
8. **FeedbackAmpCSstageNoiseDesign.pdf, pages 7–10** — Noise design equation & feasibility (spec-to-design link)
9. **FeedbackStages-intro.pdf, pages 50+** — Loop-gain/asymptotic gain model (stability/accuracy)
10. **ControllerDesign.pdf, pages 10–20** — Output stage (complementary parallel CS, VI-drive)

---

## Design Review Checklist

When reviewing hearing-loop amp noise/feedback design:
- [ ] Specification translation (30 dBSPL input noise) → input-referred noise requirement
- [ ] Feedback type justification (V-V: voltage feedback from output, compare to input source)
- [ ] Input stage topology: CS or differential pair? (check noise budget + gm/c_iss constraint)
- [ ] Inversion coefficient choice: weak, moderate, or strong? (noise vs current/area)
- [ ] CS stage gain A per stage: justify from chain-matrix B,C,D and output loading
- [ ] Output stage: complementary parallel for power efficiency + load drive
- [ ] Number of stages: 1 vs 2? (check DC gain, bandwidth, compensation feasibility)
- [ ] Stability: loop-gain phase margin > 45° (or set compensation strategy)
- [ ] DIN-A weighting: is low-frequency noise rejection needed? (optional LPproductStages)

