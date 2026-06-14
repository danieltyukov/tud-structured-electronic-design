# Prereview — Structured Electronics

> Transcription of the handwritten notes in *Structured electronics prereview notes1.pdf* (5 pages).
> The original is color-coded; the colors are preserved here as inline tags:
> **🖤 (black)** = running notes · **❤️ (red)** = warnings / corrections / "attention" · **💚 (green)** = supervisor (Anton) remarks & reasoning.
> Spots marked *[?]* were ambiguous in the handwriting; *[cut off]* marks text running past a page edge.

---

## Page 1

🖤 Why directly feedback — we can first put voltage-controlled voltage [source].

🖤 First, transfer func: we can sense current **or** have a voltage integrator — only 2 options.

❤️ **First generate options, then justify and choose.**

💚 We could say we want a voltage–voltage amp, cuz the impedance of [the] integrator will get into our transfer — but also current-to-voltage, [where] the inductor would do the integration.

🖤 \* Look at specs and generate all possible ideas progressively, and choose and justify.

🖤 So:
- **1 — transfer**
  - 💚 feedback, for example — why feedback?
  - ❤️ cuz they want to follow our design decisions
- **2 — noise**
  - noise of feedback

❤️ **Attention to order !!!**

💚 Bro stopped sensing the voltage, he went on and switched to current.

❤️ So we had a voltage–voltage amp [in the] first slide, then we went on [to] current→voltage. We should have a **current-controlled voltage source, not a voltage-controlled voltage source ???**

---

## Page 2

🖤 First we analyze after each step: for transfer, for example, we look at [the] transfer function.

❤️ We don't have to ground the coil. We have 3 elements in series — coil, feedback elements, and nullor — so we can place the ground in 3 positions, always leading to one element floating (this is in the book).

💚 Why do we need R₁: our transfer function should be [an] integrator (second-order integrator, second pole at 7 kHz as he calculated).

❤️ Our topology now is an inverting amp for integration, which is not really a voltage–voltage amp — it's more a transimpedance amp.

💚 Basically our plots are wrong — this is not the behaviour of the simulator.

🖤 We have a funny topology between a transimpedance amp and a voltage amp, so the circuit doesn't work.

💚 *(current–voltage)*

🖤 Either we choose [a] transimpedance amp and the inductor is integrating, but now R_inductor plays a role in [the] transfer function — or [a] V–V amp, and the R_inductor [cut off →]

---

## Page 3

🖤 [cut off ←] …the design ? — only intervenes in noise.

🖤 First we choose V–V or I–V, then come up with feedback configurations. We get some impractical values for components, so make a choice.

🖤 \* ideal → Controller → TF — sheet should be in the beginning.

🖤 \* Controller → noise → CISS → g_m·C_in — is using an old notebook.

💚 The results are not important — even if the amp doesn't work, they want the understanding.

🖤 Chain (ABCD) matrix:

```
⎛ V_in ⎞   ⎛ A  B ⎞ ⎛ V_o ⎞
⎜      ⎟ = ⎜      ⎟ ⎜     ⎟
⎝ I_in ⎠   ⎝ C  D ⎠ ⎝ I_o ⎠
```
*(B and D circled in ❤️ red)*

❤️ anticausal

🖤 B and D produce current noise at [the] output.

❤️ The book could really be useful — if not now, even later.

---

## Page 4

💚 Anton quote: *"replace the how with the why."*

🖤 SLiCAP kinda forces us to think in the right order.

🖤 If we make R_integrator lower, then it damps the resistor more.

🖤 If you add a resistor you need, [have] a good reason for it.

🖤 Asymptotic-gain model:

```
                  ⎛   L   ⎞   ⎛   1   ⎞
gain = A_∞ (gain) ⎜ ───── ⎟ + ⎜ ───── ⎟
                  ⎝  1−L  ⎠   ⎝  1−L  ⎠
```
- 💚 L/(1−L) = **servo function**
- ❤️ 1/(1−L) = **direct gain** → ❤️ *IDK where that came from*

💚 We had to explain the plot with loop gain.

❤️ **We should explain everything in this plot.**

🖤 *[Embedded photo: a Bode magnitude plot titled "Magnitude plots feedback model parameters", with a transfer-function expression along the top. Curves are labelled in the legend: gain, asymptotic, loopgain, servo, direct.]*

- ❤️ L₁ and C₃ resonance !!! *(circled on the bump in the curve)*
- 🖤 blue line is the red + purple
- 🖤 purple is servo

---

## Page 5

🖤 *(continuation of the Bode plot photo — frequency axis 10¹…10⁶ Hz)*

🖤 Servo function behaviour:

```
   L
 ─────   for small L,  servo ≈ L
 1−L     for big L,    servo ≈ 1
```

💚 Bode plot is only the vertical axis at 0 of [the] Nyquist plot.

❤️ ⚠️ **We can have another prereview.**

💚 Everyone should speak during [the] review.

💚 Have [a] secretary to reserve [the] room.
