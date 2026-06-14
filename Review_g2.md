# Review — Group 2 (transcription of `Review_g2.pdf`)

> Markdown transcription of `Review_g2.pdf` — a **peer group's** mid-project review
> presentation for the EE4109 hearing-loop-receiver design.
>
> | | |
> |---|---|
> | **Author (PDF metadata)** | Silvana Salamur |
> | **Group** | Group 2 |
> | **Date on slides** | 18-5-2026 |
> | **Slides** | 32 |
> | **Scope** | The A1 receive-coil amplifier — same design problem as our `Notebooks/` pipeline |
>
> This is **not our team's work** — it is another group's review deck, kept as a reference
> for how the same A1 design problem was approached and motivated. The slide structure maps
> one-to-one onto our notebook pipeline (specification → feedback → first-stage/noise →
> single-stage → dual-stage → frequency compensation), so it is useful for cross-checking
> design reasoning. Figure-only slides (schematics, plots) are noted as **[figure]** because
> the PDF carries no extractable text for them — open the PDF for those visuals.

---

## Outline (slide 2)

1. Specification / concept design
2. Feedback configurations
3. First stage / noise design
4. Single stage
5. Dual stage
6. Frequency compensation

---

## 1. Specification

### What to do before constructing the specification? (slide 3–4)

1. In what environment does our circuit work? What components does our circuit interact with?
2. Understand how our circuit works.
3. Set the specification and budget.

- **Input:** pick-up coil.
- **Output:**
  1. Source-select switch (microphone / hearing loop).
  2. ADC with input impedance of 10 pF.

### Input of A1: pick-up coil — how does it work? (slide 5)

It is a **differentiator**:

- Current passes through the induction loop →
- a magnetic field is generated around it →
- the pick-up coil is brought within this magnetic field →
- a corresponding current is created →
- a voltage is generated proportional to the **rate of change of magnetic flux over time**.

(Reference: majorcom.fr induction-loop-systems.)

### Output of A1 (slide 6)

- **Source-select switch (microphone / hearing loop)**
  - Allows switching between the microphone output and the hearing loop (pick-up coil).
  - Requires V_microphone = V_hearing-loop at the reference frequency.
- **ADC with input impedance = 10 pF**
  - The ADC (A2) works as a voltage-amplifier input: Zᵢ = ∞, draws no current from A1's output.
  - The only loading effect left is the parasitic capacitance of the ADC input (10 pF).

### How would A1 work? (slide 7)

1. A1 will work as an **integrator**.
2. A1 is a **voltage–voltage amplifier**.
3. A1 has a specific gain magnitude, applied when V_microphone = V_pick-up-coil at the reference frequency.
4. **Noise requirement:** the output noise V_o,noise (after DIN-A weighting) does not exceed the microphone's noise floor.

### Circuit modeling (slides 8–14) — [figures]

- **Circuit Model** [figure]
- **Pick-Up Coil Representation** [figure]
- **Termination Resistor Representation** — purpose: damp the LC resonance (a property of the
  pick-up coil). Three cases shown: without termination resistor, with termination resistor,
  and the critically-damped condition (R_t optimal). [figure]
- **Ideal Amplifier Representation** [figure]
- **Output Representation** [figure]
- **Noise Representation** [figure]

### Noise budgeting (slide 15)

For initiation, deciding on the noise budgeting of the **signal source** is crucial.

---

## 2. Feedback design (slides 18–20)

- Selected configuration: **voltage as input, voltage as output**.
- Overall transfer is an **integrator** with time constant τᵢ.
- Two choices for the components of Z₁ and Z₂:
  - **Option 1:** Z₁ = capacitor, Z₂ = resistor.
  - **Option 2:** Z₂ = inductor, Z₁ = resistor.
- Trade-offs in feasible inductor size and the corresponding resistor size (i.e. more noise),
  and in manufacturability.

Sizing the feedback network:

- The **noise budget** of the feedback network limits the **maximum** value of the feedback resistor.
- The **power budget** of the feedback network limits the **minimum** value of the feedback resistor.
- A suitable resistor value is chosen, then the capacitor value is selected to match the
  integrator time constant defined by the specifications.
- A **bypass resistor** is added in parallel with the capacitor. It specifies the DC path of
  the circuit and sets the lower corner frequency of the amplifier to f_min.

---

## 3. First stage — gₘ, c_iss, inversion and noise (slides 21–24)

- Why is noise so important? — The input-referred noise is set by the **1st stage**.
- **gₘ** — defines how "strongly" the input stage is driven; also helps with thermal noise
  (4kTγ/gₘ). More current for less voltage is desirable.
- **c_iss** — more c_iss means more loading. Increasing device width for more gₘ increases c_iss. :(
- **Inversion** — weak inversion (large gₘ/I_D) is preferred for maximum transconductance gain.
- To implement the 1st stage we need to model noise, so we replace the nullor by a **noisy nullor**.

### First-stage concept (slide 22) — [figure]

### What stage to implement the 1st stage as? (slide 23)

- Between CS, CG and CD we choose to design the first stage as a **CS stage** because of its T1 matrix.
- The T1 matrix of a CS stage has the smallest values — showing the most nullor-like properties
  (so the noise performance of subsequent stages can be removed).
- Even if CS, CG and CD could be modeled with the same noise, CD and CG are voltage and current
  **followers**, so we wouldn't get any gain.
- So we model the 1st stage as a **CS-stage amplifier** (in saturation → max gain).

### Budget-to-parameter calculations (slide 24)

1. Find S_o(f).
2. Integrate it over the design frequency band to get the output variance σ₀².
   - σ₀² = (B_n2 · V_o,noise)²
3. Calculate gₘ as a function of c_iss.
4. Find the lowest possible c_iss, then gₘ and I_D, W, L using the **EKV model**.

---

## 4. Single stage (slides 25–26)

- From Part 3: gₘ, c_iss, W, L, I_DS.
- Check if one stage is enough.
- A single CS = only 3 usable terminals → use a **differential pair** (≈ 4× current, 4× area
  vs. a single CS).
- Current-drive check: ✓
- Voltage-headroom check: ✓
- Loop-gain analysis: |L_DC| is below unity across all frequencies → **poor accuracy**.
- → move to a **dual-stage** design.

---

## 5. Dual stage (slides 27–31)

### Why dual stage? (slide 27)

Trade-off across: noise, power, accuracy, stability, area.

- The **first stage dominates noise**.
- The **second stage dominates loop gain**.

### Suggested topology (slide 28)

- **1st stage:** PMOS differential pair.
- **2nd stage:** NMOS CS.

### First stage: differential pair vs. single-ended CS (slide 29)

| Differential pair | Single-ended CS |
|---|---|
| Lower noise | Less area |
| High CMRR | Lower power consumption |
| Matches the coil's 2-terminal input | Simple design |
| (−) More area | (−) Allows CM interference |
| (−) Higher complexity | (−) Higher noise |

### Second stage: NMOS common source (slide 30)

Characteristics: high loop gain / accuracy, high current-drive capability, low power
dissipation, simple / small area.

### Dual-stage design parameters (slide 31)

- **gₘ₁** — first-stage transconductance, mainly set by the noise budget.
- **gₘ₂** — second-stage transconductance, an extra loop-gain factor.
- **R_f** — feedback resistor, set by the desired transfer function.
- **g_o1** — first-stage output conductance, defines the first-stage output resistance.

---

## EKV small-signal model (slide 32)

- Realistic transistor-level design.
- Includes most parasitic capacitances.
- Results in more accurate gain plots.

### Pole-zero analysis (slide 33) — [figure + notes]

- The gain plot follows the results of the poles and zeros as expected.
- At around 40 MHz there is **peaking** caused by the quality factor (Q) of poles P₄,₅, which
  is quite larger than 1 — meaning the pole pair is severely **underdamped**, leading to
  visible peaking in the plot.
- The circuit is **stable**: Re(p) < 0.

---

## 6. Frequency compensation (slides 34–35)

- **Maximally Flat Magnitude (MFM)** target.
- **Phantom-zero method**
  - Benefits
  - Implementation

(Slide 35: Maximally Flat Magnitude — [figure].)

---

## Closing (slide 36)

> Thank you — Review | Group 2 — 18-5-2026
