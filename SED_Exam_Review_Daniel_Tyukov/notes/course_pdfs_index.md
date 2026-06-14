# EE4109 Course PDF Reference Index — figure/diagram sourcing for the A1 hearing-loop receiver amplifier

Index of all 32 course PDFs in `EE4109-2025-2026/course_pdfs/`. For each PDF: topic, key concepts, and the specific pages that contain reusable diagrams/figures (schematics, Bode/pole-zero plots, block diagrams, transistor-stage drawings, noise models, EKV curves). These decks are incremental slide builds — for a topic that spans a run of pages, the **highest page number in the run** is the fully built-up figure to snap. All paths are under `/home/danieltyukov/workspace/tud/tud-structured-electronic-design/EE4109-2025-2026/course_pdfs/`.

---

# ⭐ Most relevant to A1 hearing-loop amplifier

> These are the decks/posters to mine first for A1 presentation figures: the system context (HearingLoopIntro, CourseIntro), the CS controller core (CSstage-*, PrincipleOfAmplification, ControllerDesign, CMOScontrollerDesignPosterPalette), the noise design (FeedbackAmpCSstageNoiseDesign), the EKV/inversion-coefficient sizing (mosEKVmodel*, MOStransistorModelingAndDesignPoster), the balanced input/output stages (Balancing-differential-pair, Balancing-push-pull-stage, posterBalancing), and the feedback/follower stages (FeedbackStages-*, CDstage).

## HearingLoopIntro.pdf
**Pages:** 3
**Topic:** Introduces Design Exercise 1: a complete hearing-loop / hearing-aid signal-processing system in CMOS18. Frames the full acoustic-to-acoustic chain (microphone and pick-up coil inputs, ADC/DSP/DAC, loudspeaker output) on a size-675 battery, and tasks the student with the gain distribution across A1, A2, A3. A1 is the pick-up-coil pre-amplifier — the focus of the exam presentation.
**Key concepts:**
- Full system block diagram: microphone path + magnetic pick-up-coil path → source-select → ADC driver (A2) → ADC → DSP → DAC → LSP driver (A3) → loudspeaker
- Noise sources annotated: mechanical, thermal, electro-magnetic
- Signal levels: 30–110 dBSPL; 20Hz–6kHz (mic), 600Hz–6kHz (hearing loop); 0 dBSPL = 20 μPa
- A1 pick-up-coil sensitivity: −59.4 dBV/(A/m) @ 1kHz; 70 dBSPL = 0.1 A/m
- Audio: crest factor = 3, max full-power frequency = 5kHz
- System reqs: noise 30 dBSPL, peak 110 dBSPL; ADC input max 0.9 Vpp, 10 pF; DAC output 10 kΩ
- Supplies: 0.9V (A1, A2, ADC); battery 1.4V 600mAh, 100hrs
**Figure pages to snap:**
- p2: Full end-to-end system block diagram (mic, pick-up coil, ADC/DSP/DAC, loudspeaker, battery, supply regulator) annotated with dBSPL levels and impedances — the canonical A1 system-context figure
- p3: Simplified "electronic information processing system" block diagram (A1/A2/ADC/DSP/DAC/A3) plus the gain-distribution table

## CourseIntro.pdf
**Pages:** 6
**Topic:** Course intro framing the systems-engineering approach to application-specific negative-feedback amplifiers in CMOS, anchored in the hearing-aid/hearing-loop application. Introduces A1 as the target design and the hierarchical feedback-amplifier breakdown (source, controller, feedback network, load, bias).
**Key concepts:**
- Hearing-aid chain: mic / pick-up coil → A1 → A2 (ADC driver) → ADC → DSP → DAC → A3 → loudspeaker
- A1 source: sensitivity −59.4 dBV/(A/m) @ 1kHz, band 600Hz–6kHz, 0.9V supply, size-675 battery
- Systems-engineering: divide product into less-complex parts, assign functions + performance/cost budgets, define interfaces, work hierarchically
- Feedback-amplifier model: signal source, controller (error amp minimizes transfer error), feedback network (defines source-load transfer), load; signal-path vs bias circuitry
- Performance/cost matrix axes: dissipation, bandwidth, frequency response, weak nonlinearity, accuracy, noise, drive capability, IO impedance, temperature stability, chip area
**Figure pages to snap:**
- p2: Full hearing-aid/hearing-loop system block diagram with signal levels and impedances — canonical A1 context figure
- p3: Simplified pick-up-coil pre-amplifier block diagram (magnetic signal → coil → A1 → battery)
- p5: Hierarchical breakdown block diagram of a feedback-amplifier application (source/controller/feedback/load; signal-path vs bias)
- p6: Group-exercise performance-vs-part matrix table (structured-design overview slide)

## PrincipleOfAmplification.pdf
**Pages:** 40
**Topic:** First-principles build-up of what amplification is and a formal approach to biasing a MOS amplifier stage. Develops why a single transistor cannot faithfully amplify and how adding output/input voltage sources plus bias currents produces a properly biased stage whose transfer characteristic passes through the origin. Ends with linearization and maximum available power gain of a linear two-port.
**Key concepts:**
- Amplifier between source and load: unique source-load correspondence; available output power must exceed source power
- MOS conduction: drain current only if V_DS ≠ 0 and V_GS > V_th
- Zero-signal operating (quiescent) point; the "no load signal" problem
- Progressive biasing: add output V source → add input V source → add bias currents so characteristics pass through the origin
- Linearization in the operating point → linear two-port model
- Maximum available power gain Gₐ of a unilateral linear resistive two-port
**Figure pages to snap:**
- p2–p5: Source–Amplifier–Load block diagram (p2 cleanest)
- p6–p14: Single-transistor stage schematic being built up; zero-signal operating-point graphic (p11–p14)
- p15–p19: Schematic with output V source added — characteristic curves (no unique correspondence)
- p20–p25: Schematic with input V source added — characteristic curves (unique correspondence)
- p26–p31: Schematic with bias currents added — characteristic curve through the origin (key biasing-result figure)
- p32–p34: Final "Biased amplifier stage" schematic (p32 clean)
- p35–p36: Biased amplifier stage, alternative arrangement
- p37–p40: Linearization → linear two-port box; maximum-available-power-gain figure

## CSstage-intro.pdf
**Pages:** 38
**Topic:** Introduces the common-source (CS) stage as the fundamental MOS amplifier and central object of study, positioned as the best single-stage nullor approximation (ideal controller for negative-feedback amplifiers). Argues CG and CC stages are feedback stages built around a CS controller, and lays out the performance aspects and design parameters to study.
**Key concepts:**
- CS stage = basic MOS amplifier; equivalent to CE (BJT) and common-cathode (tube) stages
- Biased CS/CE/CC: no bias currents through source/load; characteristics through the origin
- Why CS is basic: smallest small-signal T1 (transmission-matrix) parameters → best single-stage nullor / ideal controller
- CG and CC modeled as feedback stages with a CS controller
- Performance aspects: voltage/current drive, noise, temperature, bandwidth; design params W, L, sections, operating point
- Cross-talk through C_gd → right-half-plane zero
**Figure pages to snap:**
- p2: Dense overview/roadmap — biased CS schematic, static drive-capability curves, small-signal model (g/d/s nodes), source–CS–load two-port, C_gd RHP-zero note
- p3–p6: CS schematics (single transistor, then biased CS); characteristic curves through the origin
- p7–p21: Two-port symbols labelled common-source/emitter/cathode; "Biased CS/CE/CC" comparison (p9 full set of stage symbols)

## CSstage-intrinsic.pdf
**Pages:** 91
**Topic:** Core analytical lecture on the intrinsic CS stage's static and dynamic performance. Walks through bias-source choice for output drive, the SPICE-practical biasing network, static V-I drive characteristics, large-signal dynamics (slewing / C_gd cross-talk), the full small-signal T1 (ABCD) two-port matrix derived parameter-by-parameter, input/output impedances under shorted/open terminations, and geometry/current scaling rules. Richest source of CS-stage schematics, transfer curves, and small-signal models for A1.
**Key concepts:**
- Bias-source determination for output drive: max negative output 0.9V, max positive output 10μA, weak inversion, minimum dimensions
- SPICE biasing network: R1 and V = 631.547μV (<0.1% inaccuracy); C_gs charging path; floating-node note; curves through origin
- Static: DIBL and triode region reduce output impedance and gₘ; I_o(Vᵢ) characteristic; strong-inversion quadratic vs short-channel effects
- Large-signal: C_gd cross-talk → RHP zero; ±100mV → 7μA source / 12μA sink; slew limitation
- Small-signal T1 matrix A, B, C parameters; pole counting; unity-gain frequency f_T; poles move higher with current
- Input impedance (shorted/open output); output impedance (shorted/open input)
- Geometry/current scaling: maintain inversion coefficient IC; maintain drain current I_D while scaling W/L
**Figure pages to snap:**
- p7–p9: CS bias-source schematics (M1 with "?" sources; then E1 added)
- p11–p16: "Apply bias sources" schematic (R1, V=631.547μV, C_gs charging path, floating-node note)
- p18–p26: Static behavior — CS schematic + I_o(Vᵢ) static drive curves (DIBL, triode, quadratic, short-channel annotations) — primary static V-I plots
- p27–p33: Large-signal dynamic — C_gd cross-talk / RHP-zero; ±100mV transient curves; slew poll
- p35–p43: Small-signal "A" parameter — two-port node diagrams; pole-count polls
- p44–p48: Small-signal "B" parameter — two-port node diagrams
- p49–p57: Small-signal "C" parameter — pole annotations, f_T, "higher freq with increasing current"
- p59–p72: Input/output impedance schematics (four shorted/open cases)
- p74–p91: Geometry/current-scaling figures (saturation approximation, maintain IC, maintain I_D)

## ControllerDesign.pdf
**Pages:** 27
**Topic:** Step-by-step build-up of the design procedure for a negative-feedback amplifier's active part (the controller/nullor implementation): choosing the input stage for noise, the output stage for VI-drive and power efficiency, and the number of cascaded stages. Core methodology underpinning the A1 controller.
**Key concepts:**
- Input stage chosen for noise: CS or balanced (best nullor-like); determine design limits W, L, W/L, I_D
- Output stage chosen for VI-drive + power efficiency: complementary-parallel CS (push-pull); determine W_P, W_N, I_DQ
- Number of stages: 1, 2, or n>2 (driveability of stage i by stage i−1)
- Three acceptance checks per topology: midband loop gain OK? loop-gain-poles product OK? differential-error-to-loop-gain ratio OK?
**Figure pages to snap:**
- p1 / p27: title slides
- p2–p13: progressively built bullet table of input/output-stage design criteria (text-heavy, low figure value)
- p14–p26: "Number of stages" decision table (1 / 2 / n>2 columns) filling in row by row — **p25/p26** is the fully-populated stage-count decision chart

## CMOScontrollerDesignPosterPalette.pdf
**Pages:** 1
**Topic:** Dense single-page A0 "poster palette" summarizing the whole methodology for deriving CMOS controller stages from a basic CS amplifier via error-reduction techniques. A visual map (schematic snippets, small-signal equivalents, noise models, pole-zero notes) in thematic columns. High-value figure source — compactly shows nearly every stage type and concept for A1.
**Key concepts:**
- Method: derive stages from the basic CS stage via error reduction; biased CS, intrinsic CS, CS between source and load
- Behaviors per stage: static nonlinear (drive), dynamic nonlinear, dynamic small-signal, noise
- Operating-point vs geometry (design params I, V and W, L); MOS scaling (W, L, k fingers, m devices)
- Balancing: differential pair (anti-series) + push-pull (complementary-parallel); even-order terms cancel; ABCD coefficient changes; noise spectrum ×2 or ÷2
- Local feedback: CD (source follower, non-energic unity-gain V amp), CG (non-energic unity-gain I amp); back-gate effect on loop gain
- Cascode (CS-CG): eliminates pole-splitting, near-unilateral, high output impedance, non-dominant pole at f_T; balanced cascode = best single-stage nullor
- Dynamic: RHP (positive) zero, pole-splitting/Miller for frequency compensation
- CS noise optimization for resistive source: IC near critical inversion, optimum width/best NF, lower 1/f corner by increasing W and L (f_T drops with L²); gate-induced noise i_dD at high freq
**Figure pages to snap:**
- p1: whole poster — snap full page, plus crops of: small-signal/transmission-matrix block, differential-pair and push-pull schematic clusters, equivalent noise-model block, cascode/balanced-cascode block, CS noise-optimization (inversion-coefficient) block

## FeedbackAmpCSstageNoiseDesign.pdf
**Pages:** 14
**Topic:** Concentrated, high-value 2025 deck on noise design of the MOS input (CS) stage in feedback amplifiers — directly central to A1. Defines the feedback-amplifier structure, equivalent input noise sources V_n and I_n, the MOS noise model and transformations, the MOS noise design equation, feasibility, the gm/capacitance → current/geometry mapping, and the SLiCAP design-automation flow with a transimpedance-integrator example.
**Key concepts:**
- Feedback-amplifier structure: source impedance + source-interface, load impedance + load-interface, feedback network(s), output-noise weighting function
- Equivalent input noise: series V_n + parallel I_n; weighted output noise = sum of V_n, I_n, source, feedback, interface contributions
- MOS noise model + transformations: input capacitance ∝ oxide capacitance C_ox (overlap ignored)
- MOS noise design equation: total squared weighted output noise = MOS + source/feedback/interface; coefficients depend on inversion coefficient
- One minimum gₘ for the noise requirement; relation between gₘ and input capacitance C_iss; minimum may fall below technological min (W·L)
- Feasibility limits from area/current budgets; "NOT FEASIBLE" region; lowest-noise condition
- gₘ and C → I_DS and W,L (ignoring velocity saturation; EKV/IC mapping)
- SLiCAP automation: fit EKV to BSIM, nullor controller in KiCad, evaluate W, L, I_DS for six scenarios
**Figure pages to snap:**
- p2: "Structure Feedback Amplifier" block diagram (source / source-interface / amplifier+feedback / load-interface / load) — high reuse value
- p3: "Noise Transfer Functions" block diagram (V_n series, I_n parallel injected, contribution labels)
- p4: "MOS Noise Model" figure-only page — transistor small-signal noise model schematic
- p5: MOS Noise Transformations-1 (noise-source transformation, − / + directions)
- p6: MOS Noise Transformations-2 (input-capacitance / C_ox annotation)
- p7: "Feedback amplifier MOS Noise" full block diagram (source/feedback/load + MOS noise sources)
- p9: noise design equation slide (boxed equation/derivation)
- p13: Example — transimpedance integrator with capacitive source (schematic + SLiCAP coefficient annotations)

## mosEKVmodel.pdf
**Pages:** 105
**Topic:** Detailed build-up of MOS device physics and the EKV (Enz-Krummenacher-Vittoz) compact model in five sub-decks: (1) MOS operation/physics, (2) design question & methods, (3) small-signal model elements, (4) EKV equations, (5) SLiCAP small-signal implementation. Explains how small-signal parameters depend on geometry and operating point via the inversion coefficient. Primary source for EKV curves and the small-signal model schematic.
**Key concepts:**
- Regions: weak inversion (I_D ∝ exp V_GS) → strong inversion (I_D ∝ V_GS²); cross-sections (n-well, p-substrate)
- V_DS dependency: channel length modulation (CLM), breakdown
- Short-channel: VFMR (vertical-field mobility reduction), velocity saturation, DIBL
- Small-signal elements: gate-channel capacitance, drain-gate overlap capacitance, gₘ, output conductance (CLM), source-bulk capacitance, channel-noise source
- EKV (1995): all regions weak→strong; charge-controlled; technology current I_0; slope factor n; μ₀; t_ox
- Forward/reverse inversion coefficient IC_f, IC_r; total drain current = forward − reverse
- Critical inversion coefficient IC_crit: where short-channel sets in; CLM as early voltage (bipolar analogy)
- SLiCAP MOS model: CMOS18 parameters + device-equation subcircuits in SLiCAP.lib
**Figure pages to snap:**
- p3–p13: EKV small-signal model schematic (G-D-S,B) built element by element — **p13** complete annotated model (capacitances, gₘ, output conductance, noise source)
- p20–p31: MOS physics cross-sections (PMOS/NMOS, n-well/p-substrate, channel formation) + weak/strong-inversion band/capacitive-coupling diagrams (p30–p31 full summary)
- p50–p52: "MOS design" W/L/cross-section sketch with design-question/parameters/methods layout
- p60–p62: small-signal model schematic again (clean)
- p72–p92: EKV figures — transistor symbol with equation callouts; p82–p83 full equation set; p89–p92 critical-inversion / short-channel (VFMR/VS)
- p100–p103: likely figure-heavy — EKV small-signal trade-off plots (Binkley-style gₘ/I_D vs IC) — strong IC-vs-parameter curve candidates
- p104–p105: SLiCAP MOS small-signal model schematic (G-D-S-B with technology + circuit params)

## mosEKVmodelApplication.pdf
**Pages:** 24
**Topic:** Applies the EKV model to practical MOS small-signal design, centered on the inversion coefficient (IC) as the master design variable. Shows how transconductance efficiency, f_T, channel thermal noise, and 1/f corner scale with IC, with the design trade-off chart across weak/moderate/strong inversion. Key source for the IC-axis design trade-off figure justifying A1 input-stage sizing/biasing.
**Key concepts:**
- MOS largest available power gain in forward saturation; "Keep it simple!" simplified small-signal two-port model
- Up to critical inversion, gₘ (and gₘ/I_D efficiency) increase with IC
- Cut-off frequency f_T ∝ gₘ; channel-current noise PSD ∝ gₘ; 1/f corner ∝ f_T
- Trade-off: increasing L (maintaining IC) → low 1/f noise, low f_T, high output resistance; high IC (strong inversion) → low channel noise, high f_T, low area, possible velocity saturation
- IC axis: weak (0.1) / moderate (1) / strong (10–100) / velocity-saturation (1000)
**Figure pages to snap:**
- p1 / p14: title slides
- p10–p13: simplified MOS small-signal two-port model schematic (cascaded +/− boxes) for largest available power gain
- p24: **the key IC design trade-off chart** — inversion-coefficient axis (0.1 → 1000, weak/moderate/strong/velocity-sat) annotated with low-1/f / low-f_T / high-output-resistance / low-channel-noise / high-f_T-low-area / increase-length arrows — highest-value figure in this PDF
- p19–p23: figure pages building the IC-dependent property list (gₘ, f_T, channel noise, 1/f corner) — may include gₘ-vs-IC efficiency graphics

## Balancing-differential-pair.pdf
**Pages:** 44
**Topic:** Core A1-relevant deck: synthesis/analysis of the differential pair as the balanced input stage. Builds the diff pair from anti-series CS stages, then anti-series biased CS stages, then a four-terminal stage with improved port isolation. Covers V-I transfer (odd differential current, even common-mode source voltage), small-signal transfer, stationary noise, and the SLiCAP/LTspice differential-pair MOSFET model. This is the A1 input differential pair.
**Key concepts:**
- Differential pair = anti-series connection of two CS stages; then anti-series biasing
- Four-terminal stage with improved port isolation; CM voltages defined by application / CM bias sources
- V-I transfer: relative differential output current = odd characteristic; CM source voltage = even; linearity increases with IC
- Small-signal transfer from anti-series of linear two-ports; equivalent small-signal diagram in the quiescent point
- Stationary noise: equivalent input noise of a diff pair = a single CS stage if each transistor has 2× W and 2× I_D → "same performance: 4× area, 4× current"
- SLiCAP diff-pair model (MD): params gm, go, cgg, cdg, cdd; netlist "Mx D1 D2 G1 G2 myMOS"; subcircuits CMOS18ND/CMOS18PD; nMOS M1/M2 W=220n L=180n biased by tail I_ss
**Figure pages to snap:**
- p3–p5: anti-series-connected CS stages (+/− build-up)
- p7: anti-series connected + anti-series biased CS stages
- p8–p12: four-terminal stage with improved port isolation, CM-voltage annotations (p10–p12 most complete)
- p14–p21: differential-pair V-I transfer schematic (M1/M2 W=220n L=180n, tail I_ss, V1/V2/V3/E1) — **p21** fully annotated (odd diff current, even CM source voltage, IC linearity)
- p24–p30: small-signal diagram + equivalent small-signal in quiescent point (p27–p30 most complete)
- p33–p43: stationary-noise diagrams (anti-series two-port noise sources) — p41–p43 fully annotated (2×W, 2×I_D; 4× area/current)
- p44: differential-pair SLiCAP model — LTspice symbol SLXMD + internal small-signal schematic (Cgg, Gm, Go, Cdd, Cdg, ports D1/D2/G1/G2)

## Balancing-push-pull-stage.pdf
**Pages:** 45
**Topic:** Synthesis/analysis of the push-pull (complementary) output/driver stage as a balanced structure. Builds it from complementary-parallel CS stages, then complementary-parallel biased CS stages. Covers V-I transfer with the operating-class taxonomy (A/B/AB/C), small-signal transfer, stationary noise, and the SLiCAP push-pull model. The parallel-output dual of the series-input differential pair — the A1 output stage.
**Key concepts:**
- Push-pull = complementary-parallel connection of CS stages (PMOS + NMOS); then complementary-parallel biasing
- Operating classes: A (both conduct), B (one per phase), AB (overlap), C (dead zone)
- Small-signal transfer from anti-parallel of linear two-ports; equivalent small-signal in quiescent point
- Stationary noise: equivalent input noise = single CS stage if transistors have ½ W and ½ I_D → "same performance: equal area, equal current"; caveat: PMOS mobility ≈ 4× lower
- SLiCAP push-pull model: LTspice symbol SLXMPN; params W_N, L_N, ID_N, W_P, L_P, ID_P; subcircuit CMOS18PN
**Figure pages to snap:**
- p3–p5: complementary-parallel CS stage schematics (+/− with complementary "C" block)
- p7–p10: complementary-parallel biased CS stages, CM-current annotations (p9–p10 complete)
- p12–p13: push-pull V-I transfer schematic (PMOS W=770n + NMOS W=220n, E1/E2, V1/V2 {VP}/{VN}, I1/I2 {IQ})
- p14–p21: full push-pull V-I test schematic with operating-class annotations A→B→AB→C — **p21** fully annotated (figure-heavy)
- p24–p30: small-signal + equivalent small-signal in quiescent point (g/s/d; p28–p30 complete)
- p33–p44: stationary-noise two-port diagrams (Result/Conclusion build-up) — p42–p44 fully annotated (½W, ½I_D; PMOS-mobility caveat)
- p45: push-pull SLiCAP model — LTspice symbol SLXMPN with W_N/L_N/ID_N/W_P/L_P/ID_P

## posterBalancing.pdf
**Pages:** 1
**Topic:** Single dense summary poster ("Balanced Stages / Small-signal models," © 2021 Anton Montagne) condensing the entire balancing module onto one page — two-terminal, two-port, differential-pair, and push-pull material (schematics, small-signal equivalents, noise results). Ideal one-glance overview/title slide for the A1 presentation.
**Key concepts:**
- Two-terminal balancing: odd-function synthesis via anti-series + complementary-series and anti-parallel + complementary-parallel (DM = odd transfer, CM = even)
- Small-signal equivalents for series and parallel balanced two-terminals
- Noise: series anti-series → voltage-noise spectrum 2× single element; parallel anti-parallel → current-noise spectrum 2×
- Two-port balancing: two-ports and complementary two-ports, eight interconnections with odd transfer
- Balanced stages: anti-series of equal devices (diff pair), parallel of complementary devices (push-pull); small-signal models + noise (anti-series: 2× V-noise / ½ I-noise; complementary-parallel: 2× I-noise / ½ V-noise)
**Figure pages to snap:**
- p1: whole poster — full page plus crops of: top-left "Balancing of two-terminal devices" (anti-series synthesis, DM/CM odd/even), center "Balancing of two-ports" (eight-interconnection grid), right "Balanced Stages" (anti-series diff pair + complementary-parallel push-pull schematics, small-signal models, noise summaries)

## FeedbackStages-CD-stage.pdf
**Pages:** 53
**Topic:** Detailed treatment of the Common-Drain (CD) stage as a non-energic negative-feedback voltage follower. Analyzed with the asymptotic-gain model: ideal/asymptotic gain, loop gain, bandwidth/stability, closing with a SLiCAP phantom-zero compensation example for a capacitively loaded stage. Relevant to the A1 output/buffer reasoning.
**Key concepts:**
- CD stage = non-energic feedback voltage follower: A = +1; B, C, D as CS stage (non-inverting)
- Input series feedback (voltage comparison) + output parallel/shunt feedback (voltage sensing)
- Equivalent input noise, drive capability, energy storage, power efficiency = CS stage
- Loop gain drops if: load R decreases, load C increases, source R increases
- Two poles → bandwidth from loop-gain-poles (LP) product; two dominant poles → peaking/instability
- Phantom-zero compensation: external capacitor establishes a phantom zero to stabilize
**Figure pages to snap:**
- p3–p10: CD-stage intro schematic (non-energic voltage-follower drawing; p8–p10 add Poll boxes)
- p11–p19: CD-stage schematic vs CS comparison (p11 minimal text)
- p21: ideal-gain/asymptotic-gain diagram with "controller" block
- p24–p28: side-by-side ideal-gain vs asymptotic-gain nullor diagrams
- p30: CD-stage loop-gain "controller" block diagram
- p34–p41: loop-gain simplified block diagram (1)(2) with ± ports (p40–p41 add poles/zeros polls)
- p43–p52: bandwidth-and-stability sub-deck — almost certainly Bode/pole-zero plots (figure-only frames)
- p53: SLiCAP example — phantom-zero compensation of a capacitively loaded CS stage (schematic + plot)

## CDstage.pdf
**Pages:** 1
**Topic:** A single dense reference poster on the common-drain (CD) stage as a non-energic negative-feedback voltage follower. Contrasts an ideal-controller voltage follower with a CS-stage-controller realization, and works through behavioral modifications under feedback (drive, efficiency, noise, offset/drift, gain accuracy, nonlinearity, bandwidth) plus dynamic analysis via the asymptotic-gain model, loop gain, pole/zero placement, and frequency compensation. The most directly A1-relevant single poster for the output voltage-follower stage.
**Key concepts:**
- CD stage = non-energic feedback voltage follower: ideal gain unity; feedback adds no noise/offset/drift, does not degrade drive/efficiency (all equal the biased CS controller)
- Output voltage sensing + input voltage comparison → higher Z_in, lower Z_out than bare CS (significant only when driven low-Z / terminated high-Z)
- Negative feedback reduces gain inaccuracy and weak nonlinearity, enlarges bandwidth; if shorted/current-driven, loop gain very low → feedback ineffective
- Asymptotic-gain dynamic analysis; C_dg outside controller changes ideal gain; gₘ as loop-gain reference makes asymptotic gain = modified ideal gain; substrate (back-gate) effect strongly reduces loop gain
- Two-pole analysis: both dominant if (sum)² < 4·(product); MFM at (sum)² = 2·(product); C_dg left-half-plane phantom-zero for compensation
- Combine techniques: complementary-parallel CD (high current drive at low quiescent current); anti-series CS controller (low-offset follower); isolated-bulk transistors
**Figure pages to snap:**
- p1: whole-page CD poster — ideal-controller voltage-follower schematic, CS-controller version, signal-path + small-signal equivalent, asymptotic-gain feedback model, simplified loop-gain (1)/(2), pole-zero / DC-loop-gain plots, complementary-parallel CD-stage schematic, anti-series CS follower schematic (richest single CD/voltage-follower source for A1)

## MOStransistorModelingAndDesignPoster.pdf
**Pages:** 1
**Topic:** Dense single-page poster on MOS transistor modeling and design for CMOS18. Lays out the CMOS IC design flow, NMOS operation/regions, small-geometry effects, the level-1/BSIM/EKV models, simulated I-V and gₘ/f_T characteristics for CMOS18 NMOS, the simple small-signal and noise models, and transconductance-efficiency / inversion-level sizing guidance. Highly relevant for A1 MOS-sizing and operating-point figures.
**Key concepts:**
- CMOS IC design flow + structured-analog-design philosophy (top-down vs bottom-up)
- NMOS regions: cut-off, weak (exp), strong (quadratic), linear (VCR), saturation; V_T weak→strong transition; CLM; back-gate effect
- Small-geometry: VFMR, velocity saturation, DIBL
- Models: level-1 (hand calcs), BSIM3+ (numeric, Ward-Dutton), EKV (single expression all regions, IC as design parameter, in SLiCAP)
- Noise: channel thermal + 1/f; low f_L via large device at low current
- gₘ, f_T (current gain = 1); f_T dominated by gₘ; c_iss weakly depends on I_DS
- gₘ/I_DS as inversion measure: weak >20, moderate 10–20, strong <10; increase W (more drive, higher gₘ/f_T), increase L (less CLM, better matching/flicker)
- EKV: oxide capacitance, substrate factor, transconductance factor, technology current, IC (weak <0.1, strong >10); obtain SLiCAP EKV params from BSIM
**Figure pages to snap:**
- p1: whole poster — CMOS18 NMOS I-V family curves (L=18µm vs 180nm short-channel), gₘ(I_DS) and f_T(I_DS) log-log plots (L=180nm/W=220nm), top-down/bottom-up design-flow diagram, CMOS cross-section, MOS symbols, simple small-signal model (C_gs/C_gd), Ward-Dutton hybrid-pi, inversion-coefficient region diagrams — key source for A1 gₘ, f_T, operating-point/sizing figures

## PreferredStages.pdf
**Pages:** 12
**Topic:** Short deck presenting the preferred uni-lateral controller stages giving maximum LP-product contribution. Shows two canonical cascode topologies — the inverting CS-CG cascode and the non-inverting CD-CG cascode — and notes anti-series / complementary-parallel variants, with book-chapter pointers.
**Key concepts:**
- Uni-lateral stages with maximum LP-product contribution
- Inverting CS-CG cascode and non-inverting CD-CG cascode
- Anti-series and complementary-parallel versions also available
- Chapter map: CS (Ch5), balanced (Ch6), local feedback (Ch13), cascode + multi-stage controllers (Ch14)
**Figure pages to snap:**
- p3: inverting CS-CG cascode schematic (in/out labelled)
- p4: side-by-side inverting CS-CG and non-inverting CD-CG cascode schematics — key preferred-stages comparison figure
- p5–p11: same two cascode schematics with progressively added chapter-reference captions (p11 fully captioned; schematics identical to p4)

## StagesInterconnection.pdf
**Pages:** 7
**Topic:** Deck on interconnecting controller stages: chaining preferred stages (input of stage i+1 to output of stage i) while keeping internal nodes at infinite impedance to the signal reference to maximize CMRR and loop gain. Shows preferred two-stage solutions (anti-series output/input stages, fully balanced), flags not-preferred connections, and covers balanced-to-unbalanced conversion via an inverting current follower.
**Key concepts:**
- Input of stage i+1 to output of stage i; controllers have 3–4 terminals (internal nodes infinite impedance to signal reference) → maximize CMRR and loop gain
- Preferred two-stage solutions: anti-series output stage; anti-series input stage (push-pull as 2nd stage); fully balanced two-stage controller
- Not-preferred: internal nodes tied to signal reference violate natural-two-port assumption; no port isolation; simple two-transistor controller
- Balanced-to-unbalanced conversion via inverting current follower
**Figure pages to snap:**
- p2: generic n-stage interconnection block diagram (stage 1…n with ± ports over a common reference/supply)
- p3: three preferred two-stage controller schematics (anti-series output, anti-series input/push-pull, fully balanced) — key figure
- p4: not-preferred interconnection (internal node tied to signal reference)
- p5: other not-preferred schematics (no port isolation; popular 2-stage BJT controller)
- p6–p7: balanced-to-unbalanced conversion; p7 adds the inverting-current-follower schematic

## AmpStagesPoster.pdf
**Pages:** 1
**Topic:** Very dense single-page reference poster covering amplifier stages from basic devices to feedback stages — basic CE/CS stages and two-port notation, biasing implementation, small-signal and noise models, BJT-vs-MOS parameters and figure of merit, balanced stages, local-feedback stages (CC/CD voltage follower, CB/CG current follower), and indirect-feedback stages (voltage/current mirrors). High value for A1 (CD/CC voltage-follower and complementary-parallel CD output-stage schematics).
**Key concepts:**
- Basic CE (BJT) and CS (MOS) stages; two-port notation of nonlinear/complementary two-ports; small-signal and noise models
- Biased transistor = simplest nullor; select operating point for drive/noise/dynamics; redirect current sources over supply; AC coupling
- Temperature/tolerance: negative-feedback biasing, auto-zero, compensation
- BJT vs MOS small-signal params; figure of merit = f_T; Miller effect; T1 matrix params
- Balanced stages: anti-series (odd transfer, offset comp, even-nonlinearity reduction) + complementary-parallel
- Local feedback: CC/CD = non-energic non-inverting unity-gain V follower; CB/CG = unity-gain I follower; asymptotic-gain model
- Complementary-parallel CD output stage: easy to bias, unity gain, no rail-to-rail (low efficiency at rail-to-rail)
- Indirect-feedback: voltage mirror, current mirror (inverting indirect-feedback unity-gain amps)
**Figure pages to snap:**
- p1: entire poster — NPN-BJT and N-MOS symbols, nonlinear/complementary two-port boxes, biasing schematics, BJT/MOS small-signal + noise models, balanced-stage (anti-series, complementary-parallel) schematics, CD/CC and CG/CB follower schematics with asymptotic-gain models, complementary-parallel CD output stage, voltage/current-mirror schematics — densest single-page amplifier-stage figure source for A1

---

# Supporting / background PDFs

## FeedbackStages-intro.pdf
**Pages:** 72
**Topic:** Foundational lecture on the structured feedback-amplifier methodology (Montagne). Introduces feedback as establishing an accurate transfer via a copy of the source signal generated from the load signal. Defines the four port-quantity combinations (voltage/current sensing and comparison) and the asymptotic-gain model, ideal gain, loop gain, and servo function. Organized into named sub-decks separated by near-blank section-title pages.
**Key concepts:**
- Feedback establishes an accurate transfer; feedback-network input = load quantity, output = accurate copy of source quantity
- Asymptotic-gain model: Aₜ = A_∞·(−Aβ)/(1−Aβ) + Aₜ₀/(1−Aβ); −Aβ = loop gain, A_∞ = asymptotic gain (controller → nullor)
- Ideal gain A_∞ vs asymptotic gain; servo function; loop-gain reference variable
- Four feedback topologies: series/shunt at input (V/I comparison), series/shunt at output (I/V sensing)
- Nullor as ideal controller (A, B, C, D parameters); loop gain sets accuracy; error ∝ 1/(1−Aβ)
**Figure pages to snap:**
- p2: section-title "Feedback" (likely clean conceptual block diagram)
- p19: section-title (low text) — feedback-configuration block diagram start
- p28–p29: text-dense slide (~1530 chars) — fully built-up block diagram with annotated source/load/feedback ports
- p30: section-title — asymptotic-gain-model block diagram intro
- p43–p44: built-up asymptotic-gain / loop-gain block diagram
- p45–p47: section-title pages — error/transfer-accuracy diagrams start
- p55–p59: progressively built annotated transfer/error diagram
- p60: section-title — final sub-deck conceptual diagram
- p70–p72: final built-up block/transfer diagram

## FeedbackStages-CG-stage.pdf
**Pages:** 44
**Topic:** Detailed treatment of the Common-Gate (CG) stage as a non-energic negative-feedback current follower — the dual of the CD stage. Covered with the asymptotic-gain model: ideal/asymptotic gain, loop gain, bandwidth/stability. Useful for A1 input-stage / cascode reasoning.
**Key concepts:**
- CG stage = non-energic feedback current follower: D = +1; A, B, C as CS stage (non-inverting)
- Input parallel/shunt feedback (current comparison) + output series feedback (current sensing) — dual of CD
- Equivalent input noise, drive, energy storage, efficiency = CS stage
- Loop gain drops if: load R increases, load C decreases, source R decreases, source C decreases
- Two poles + one zero; zero coincides with a pole (direct transfer); bandwidth best when driven high-Z and terminated low-Z
**Figure pages to snap:**
- p2–p3: CG-stage intro schematic (figure-only)
- p4–p8: non-energic current-follower schematic with annotations (p7–p8 plateau)
- p9: CG-stage schematic, figure-only
- p19: ideal/asymptotic-gain diagram with "controller" block
- p27: CG loop-gain "controller" block diagram (figure-heavy)
- p28–p36: loop-gain + simplified (1)(2) block diagram with ± ports ("establishes a direct transfer")
- p37–p44: bandwidth-and-stability sub-deck — (1)(2) loop-gain diagram + Bode/pole-zero plots ("Two poles / One zero")

## FeedbackStages-other.pdf
**Pages:** 41
**Topic:** Survey of additional feedback-stage architectures beyond CS/CD/CG: indirect-feedback current amplifiers, indirect-feedback voltage amplifiers, balanced (anti-series / complementary-parallel) stages, and multiple-loop feedback stages. Closes with a taxonomy of feedback and balancing techniques.
**Key concepts:**
- Indirect feedback current amplifier: inverting, indirect current sensing via a current mirror; feedback no influence on output impedance
- Indirect feedback voltage amplifier: inverting, indirect voltage comparison via a voltage mirror; feedback no influence on input impedance
- Balanced stages: anti-series transadmittance; complementary-parallel CD; behavior modified by feedback + balancing
- Multiple-loop feedback: nested A/B/C/D blocks (B,C; A=1,D; A,D=1)
- Taxonomy — feedback: direct, indirect, non-energic, passive, active; balancing: anti-series/complementary-series, anti-parallel/complementary-parallel
**Figure pages to snap:**
- p3–p8: indirect-feedback current-amplifier schematic — stacked A,B,C,D boxes + current-mirror drawing (p7–p8 plateau)
- p10–p15: indirect-feedback voltage-amplifier schematic — A,B,C,D boxes + voltage-mirror (p14–p15 fully built)
- p17–p22: balanced feedback stages — anti-series transadmittance + complementary-parallel CD schematics (p21–p22 plateau)
- p24–p27: multiple-loop feedback-stage schematics — nested B,C / A=1,D / A,D=1 drawings
- p23, p28: section-title pages (clean diagram intros)

## Balancing-intro.pdf
**Pages:** 27
**Topic:** Introductory deck on the balancing design principle as a form of additive compensation (reproduce the error, then subtract it). Distinguishes balancing with identical vs complementary elements, showing how even-order error/distortion terms cancel while error reduction is limited by element matching. Conceptual foundation for differential pairs and push-pull stages used in A1.
**Key concepts:**
- Additive compensation: reproduce the error → subtract it
- Balancing with identical elements: even-order terms cancel; error reduction limited by matching
- Balancing with complementary elements: same cancellation, matching-limited
- Odd-order behavior preserved; even-order (e.g. 2nd harmonic) cancels
**Figure pages to snap:**
- p6: additive-compensation block diagram (signal path with +/− summing node)
- p8–p12: "Balancing with Identical Elements" build-up (p12 most complete)
- p16: identical-element balancing diagram fully annotated
- p18–p23: "Balancing with Complementary Elements" build-up (p23 most complete)
- p27: complementary-element balancing diagram fully annotated

## Balancing-two-terminal.pdf
**Pages:** 47
**Topic:** Balancing applied to two-terminal (one-port) elements. Two synthesis routes for an odd transfer characteristic: anti-series of equal vs series of complementary elements; anti-parallel of equal vs parallel of complementary elements. Develops small-signal models, impedance/admittance, and noise. Underpins how series/parallel device stacking changes impedance and noise in A1.
**Key concepts:**
- Odd-function synthesis via anti-series/complementary-series and anti-parallel/complementary-parallel
- DM → odd transfer; CM → even transfer
- Anti-series biased with CM current sources; anti-parallel biased with CM voltage sources
- Series small-signal: Z_total = Z₁ + Z₂; in quiescent point Z = 2× single; voltage-noise PSD adds (S_v,tot = S_v1 + S_v2)
- Parallel small-signal: Y_total = Y₁ + Y₂; Y = 2× single; current-noise PSD adds (S_i,tot = S_i1 + S_i2)
**Figure pages to snap:**
- p3–p8: anti-series vs complementary-series two-terminal schematics (p8 most complete)
- p10–p14: biased anti-series schematic with CM current-source annotations (p13–p14)
- p17–p24: small-signal model of series; impedance summation + "twice the impedance" + voltage-noise PSD (p21–p24)
- p26–p31: anti-parallel vs complementary-parallel schematics (p31 most complete)
- p33–p37: biased anti-parallel schematic with CM voltage-source annotations (p35–p37)
- p40–p47: small-signal model of parallel; admittance summation + current-noise PSD (p44–p47)

## Balancing-two-ports.pdf
**Pages:** 28
**Topic:** Balancing generalized to two-ports (the abstraction behind differential and push-pull stages). Introduces nonlinear and complementary two-ports with the anti-causal (T1) notation, then enumerates the eight two-port interconnection topologies. Unifying theory connecting the differential pair and push-pull decks.
**Key concepts:**
- Six possible two-port notations; anti-causal (T1) notation used
- Complementary two-ports ("C")
- Eight interconnection topologies (anti-series/complementary-series in × anti-parallel/complementary-parallel out)
- Input connection sets common-mode handling; output connection sets how port quantities combine; series-in/parallel-out map onto diff-pair vs push-pull
**Figure pages to snap:**
- p4–p9: anti-causal (T1) two-port notation diagrams (port boxes with ± terminals)
- p10–p13: complementary two-ports definition diagrams ("C" block)
- p14–p18: complementary two-ports with ± source/load port representation (p18 complete)
- p20: anti-series interconnection schematic (clean)
- p21: anti-series vs complementary-series side-by-side
- p22–p23: 4-up grid adding anti-series-in/anti-parallel-out etc.
- p24–p27: full grid of all eight interconnection topologies (**p27** = complete 8-topology matrix)

## Biasing.pdf
**Pages:** 1
**Topic:** Dense single-page poster "Principle of Amplification and Biasing." Explains amplification as modulation of power transfer from a power source to the load, then develops the biasing principle: adding power sources so transfer characteristics pass through the origin, building a biased CS stage, AC coupling, biasing with a supply + passive elements, biasing errors and their reduction, and the small-signal model.
**Key concepts:**
- Amplification = modulation of power transfer (input port, output port, power port)
- Biasing principle: add power sources so input and output v-i characteristics pass through the origin → all A/B/C/D characteristics through origin
- Biased CS stage: four arrangements; two of the four bias sources independent, two follow from device equations
- Output-port bias sources set drive: V_DS = max negative output excursion, I_DS = max positive output current
- No current through bias-voltage sources / no voltage across bias-current sources; AC coupling when DC not of interest
- Supply + passive-element biasing: redirect current sources so only the supply delivers power
- Biasing errors → equivalent-input offset current/voltage (+ noise); reduce via compensation, negative feedback, auto-zero
- Small-signal: three-terminal active two-port; T1 matrix (anti-causal); max low-frequency available power gain
**Figure pages to snap:**
- p1: whole poster — power-transfer modulation diagram, four biased-CS arrangements, no-current/no-voltage source arrangements, AC-coupling schematics, supply-biasing with passive elements, equivalent-input offset-source models, small-signal biased-stage two-port model

## BiasingImplementation.pdf
**Pages:** 40
**Topic:** Build-up slide deck on implementing biasing for an amplifier stage: from the biased-stage arrangement, through defining output then input bias-source values, applying bias sources, AC coupling, adding the supply and redirecting current sources, finishing with bias-error reduction and a worked-examples quiz. Most slides are near-identical schematics growing one annotation per page.
**Key concepts:**
- Biased-stage arrangements; bias power by source vs by current source
- Output bias sources: negative output-voltage and positive output-current excursions limited by operating current
- Input bias-source values: nullify output V/I, control input V/I; implement with a high-gain VCVS
- AC coupling at source/load: required if no DC current allowed; only if zero frequency not of interest
- Supply: add supply voltage, redirect current sources → passive (V·I positive); supply = only power-delivering bias source
- Bias-error reduction: compensation, model-based, brute-force, negative-feedback biasing, electronic self-inductance
**Figure pages to snap:**
- p2–p8: biased-stage schematics (bias power by source / current source, alternative) — p3, p5, p7 most-annotated
- p9–p13: output-bias-source-definition schematics with excursion annotations (p13)
- p14–p21: input bias-source determination; p21 shows the high-gain VCVS
- p22–p24: applying / adding input bias sources (p24)
- p25–p29: AC-coupling schematics
- p30–p33: supply + redirected-current-source schematics (p32/p33) — key "redirect over supply" figure
- p34–p39: bias-error-reduction schematic (p38/p39)
- p40: five worked biasing examples A–E

## quizBiasingTechniques.pdf
**Pages:** 52
**Topic:** Incremental-reveal quiz/lecture deck classifying biasing techniques (brute force, compensation, negative feedback, electronic self-inductance), then diving into each: brute-force drawbacks, model-based biasing (V_GS temperature compensation), feedback biasing with a loop filter, and electronic self-inductance with its impedance-vs-frequency behavior. Closes with an A–E examples page.
**Key concepts:**
- Brute force: insert a two-terminal element with the desired v-i relation
- Compensation: reproduce error at a location and subtract it
- Negative feedback: measure response, compare with desired, nullify difference
- Brute-force drawbacks: degraded noise, increased dissipation/energy storage, degraded overdrive recovery
- Model-based biasing = compensation; limited by matching error; generates temperature-dependent V_GS to keep I_DS temperature-independent
- Feedback biasing: needs a loop filter so DC transfer is ~zero; works only when bias-error and signal bands don't overlap
- Electronic self-inductance: low Z at low frequency, high Z at high frequency → inductive |Z|(|f|)
**Figure pages to snap:**
- p33–p34: model-based/compensation biasing schematic generating temperature-dependent V_GS
- p39–p41: feedback-biasing block/loop-filter schematics (p41 most complete, multi-stage loop)
- p45–p49: electronic-self-inductance circuit schematics (p46/p48 add "Output impedance?")
- p50–p51: electronic-self-inductance impedance Bode plot |Z| vs |f| (inductive region)
- p52: five biasing examples A–E (same set as BiasingImplementation p40)

## LDRamp.pdf
**Pages:** 2
**Topic:** Short two-page deck ("Principle of Amplification — LDR demo") motivating amplification via an LDR + light-bulb thought experiment. Asks whether a passive LDR + bulb can give available power gain > 1, concludes a power source is needed, and shows how biasing the passive device turns it into an active device with controllable current/voltage transfer.
**Key concepts:**
- LDR is passive: V-I characteristic controllable but cannot deliver power → power source needed for gain > 1
- Current/voltage/combined transfer from power source to output can be controlled
- Output/input operating points shifted so positive/negative V and I possible; curves pass through origin
- A biased passive device is modeled as an active device; available power gain (Ch2)
**Figure pages to snap:**
- p2: LDR-to-amplifier figure array — LDR V-I characteristic, current/voltage/combined-transfer circuits, operating-point-shift / origin diagrams (conceptual "what is amplification/biasing" visuals)

## LPproductStages.pdf
**Pages:** 24
**Topic:** Incremental deck on how much each stage contributes to the loop-gain-poles (LP) product and estimating the required number of controller stages. Explains how negative feedback and resistive broadbanding push poles out of the dominant group, identifies the current-driven shorted CS stage as the maximum contributor (= f_T), and derives a design equation for the number of stages.
**Key concepts:**
- LP product = product of loop gain and dominant poles
- Negative feedback and resistive broadbanding increase bandwidth but may move a pole out of the dominant group, reducing a stage's LP contribution
- Current-driven shorted CS stage (or balanced) has the largest LP contribution; maximum = f_T
- Number-of-stages parameters: LP₁ (single-stage LP), f_H (min low-pass cut-off of servo), m (dominant poles of single-stage), n (stages to add for f_H)
- Design equation relating LP₁, f_H, m, n and its solution for n
**Figure pages to snap:**
- p11–p12: current-driven shorted CS stage contributing max LP = f_T (small CS schematic / annotation)
- p19–p23: "Design equation" and "Solution" slides — LP-product / number-of-stages formulas (snap p21 or p23 for the complete equation+solution)
- (Most pages are bulleted text; this deck is more equation/figure-light than the schematic decks)

## SED-CMOS.pdf
**Pages:** 1
**Topic:** Single-page reference matrix poster, "Structured Amplifier Design in CMOS technology," cross-tabulating design techniques (rows) against performance aspects, cost factors, environment, reliability, and safety (columns). The course's master overview/end-terms poster.
**Key concepts:**
- Columns — performance: drive (static V-I, slew), noise (SNR, PSRR, CMRR), port isolation, transfer quality (gain & impedances, bandwidth, weak nonlinearity, accuracy, offset, frequency response/stability); costs (quiescent dissipation, temperature stability, power efficiency, dimensions, mass, chip resources); environment; reliability (MTTF/MTBF/MTTR); safety
- Rows — techniques: device (geometry, operating current/voltage); feedback (direct/indirect ±, increase loop gain / LP product, decrease error-gain ratio); error feedforward; balancing (anti-series, complementary-parallel); frequency compensation (phantom-zero, pole-splitting, PZ-canceling, resistive broadbanding, bandwidth reduction); impedance correction/transformation; modulation; auto-zero; filtering
- End terms: identify strong positive/negative interactions between techniques and aspects/costs
**Figure pages to snap:**
- p1: entire poster — design-techniques-vs-performance/cost interaction matrix (canonical structured-design overview table; orientation/method slide, not a circuit schematic)

## SED-CMOS-order.pdf
**Pages:** 1
**Topic:** Single-page poster diagramming the hierarchically structured circuit-design process flow for amplifiers and bias sources: a top-to-bottom design-sequence flowchart (specification → concept design → signal-path design → biasing-concept design → performance verification → performance optimization) with deliverables per step and recursion into child hierarchical levels.
**Key concepts:**
- Specification → Object Performance/Test Spec, figure of merit
- Concept design: type (port impedances, DM/CM), structure (cascade / parallel-series), feedback configuration + overall biasing concept
- Signal-path design: output stage (drive → type, W/L), input stage (noise, DC reproducibility → type, W/L, operating point), number of stages (mid-band loop gain, LP product, diff-error/gain ratio), interconnection, frequency compensation → "most promising signal path"
- Biasing-concept design: minimize floating voltage sources, combine current sources, DM/CM feedback loops → "most promising amplifier circuit"
- Performance verification → FOM, performance/cost parameters; performance optimization → optimized circuit; recursion into child levels
**Figure pages to snap:**
- p1: entire poster — full top-down design-process flowchart (specification → concept → signal-path → biasing → verification → optimization, with deliverables and child-level recursion) — ideal "design methodology / our process" slide for the A1 presentation
