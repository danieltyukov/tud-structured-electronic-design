# Speaker notes: A1 Receive-Coil Amplifier review
**Daniel Tyukov (5714699) · 15 June 2026 · ~1 hour · 46 slides**

First-person notes to read from, one block per slide (matches the current deck order). Keep the
pace calm. The grade is in the reasoning, not the final numbers.

---

### 1 · Title
Good morning. I'm Daniel Tyukov, student number 5714699. This is my structured design of the A1
receive-coil amplifier for the hearing-loop receiver. I work top-down: I fix the specification
first, then justify every choice before I make it, and I build up to the circuit rather than
opening with it.

### 2 · Outline
Here's the route. Specification and environment first. Then the transfer function and the
feedback configuration. Then the first stage, designed from the noise budget. I check whether one
stage is enough, find it isn't, and move to a dual stage. Then the EKV model, the poles and
zeros, and frequency compensation. One idea runs through all of it: replace the how with the why.

### 3 · Part 1 (divider)
Let me start where every structured design has to start, with the specification.

### 4 · The hearing loop and where A1 lives
A hearing loop is a wire around a room that carries the audio as a magnetic field, and a hearing
aid picks it up with a coil. A1 is the first amplifier after that coil, and it feeds the ADC
driver and then the ADC. Before any transistor, I need to know the environment, because what
feeds A1 and what it drives sets the whole specification.

### 5 · A1 in the signal chain
Here is the chain. A1 amplifies the coil, then a switch selects between the microphone and the
loop, then the ADC driver, the ADC and the DSP. A1 runs from a single 0.9 volt supply, and the
whole amplifier shares a one milliwatt budget. So I ask three questions, in order: what is the
environment, how does it work, and what is the budget.

### 6 · Input of A1: the pick-up coil
The coil output is proportional to the rate of change of the magnetic flux, so the coil
differentiates. Its open-circuit sensitivity is about minus 59.4 dBV per amp-per-metre at one
kilohertz. The key consequence is simple: if the coil differentiates, A1 has to integrate, so the
two together stay flat across the audio band. That one fact drives the whole topology.

### 7 · Output of A1: switch and ADC
On the output side, the source-select switch needs the microphone and the loop to give the same
voltage at the one kilohertz reference, and that fixes my gain. The ADC input behaves like an
ideal voltage amplifier, it draws no current, so the only load A1 sees is a 10 picofarad
capacitor. So A1 is a voltage-to-voltage amplifier driving a capacitor, not a power stage.

### 8 · How should A1 work?
Four points. A1 is a voltage-to-voltage amplifier. Its transfer is an integrator that cancels the
coil's differentiation, about 62 thousand over s, with a time constant of 16 microseconds. The
gain is set so the microphone and the loop match at the reference. And the weighted output noise
has to stay below the microphone floor, 30 dB SPL. Notice the order: transfer first, then noise.

### 9 · Specification and budget
This table is the contract. The integrator transfer, the audio band of 600 hertz to 6 kilohertz,
the output-noise limit around 11 microvolts, the 10 picofarad load, the supply and power, and the
coil parameters. Every later decision traces back to one line here. And the design is graded on
this reasoning, not on whether the last digit is perfect.

### 10 · Circuit model: the complete picture
Now that the spec is set, here is the complete circuit model from SLiCAP. I've coloured it into
its functional blocks: the coil source, the termination, the amplifier as a nullor, the feedback
network, the ADC load, and the noise weighting. I'll take each coloured block in turn and justify
it.

### 11 · Representation 1: the pick-up coil
First block, the coil. The datasheet gives the resistance, the inductance and the sensitivity,
and a self-resonance at 150 kilohertz. From that resonance I back out the parasitic capacitance,
which comes to about 9.4 picofarad. So the coil is an inductance and resistance in series, with
that small parasitic capacitance across it.

### 12 · Representation 2: the termination resistor
Second block, the termination resistor. The inductance and capacitance resonate at 150
kilohertz, and undamped that peak rings, as the orange curve shows. I add a resistor across the
input and size it for critical damping, a quality factor of one over root two, which gives about
80 kilohm. The blue curve is the result, flat and then rolling off. The resistor exists only to
damp the resonance, and it then becomes a noise source I have to budget.

### 13 · Representation 3: the ideal amplifier (nullor)
Third block, the amplifier, modelled as an ideal nullor. From the coil sensitivity and the
microphone sensitivity, and using the fact that differentiation maps to s, I work out the
required gain, about 62 thousand over s. With a nullor, the transfer is set only by the passive
feedback, one over s R_f C_i. The real transistors come later.

### 14 · Representation 4: the output (ADC load)
Fourth block, the output. The ADC input draws no current, so the only thing loading A1 is its 10
picofarad parasitic capacitance. A capacitive load matters in two ways: the output stage has to
supply charging current at the full-power frequency, and that capacitor enters the stability
analysis later.

### 15 · Representation 5: the noise sources
Fifth block, the noise. I convert the 30 dB SPL floor to a voltage through the microphone
sensitivity, which gives about 10.6 microvolts as the weighted output-noise budget. Each resistor
adds thermal noise, four k T R, and the input device adds its own voltage and current noise,
which is the noisy nullor. The plot shows the output noise spectrum, raw and DIN-A weighted.

### 16 · Noise budgeting
I decide the budget of the signal source first. The source, termination and feedback resistors,
circled here, together take 40 percent of the noise budget, and the rest goes to the input
transistor, which is what sets its transconductance. The source resistor alone takes about 14
percent. The total output-noise RMS comes to about 7.5 microvolts, inside the 10.6 microvolt
budget.

### 17 · Noise is judged by ear: DIN-A weighting
One more point on noise: it's judged by ear. I weight the output noise with the standard DIN-A
curve before integrating it to an RMS value. It's flat at one kilohertz and rolls off outside the
audio band. That makes the budget perceptually meaningful, tight where hearing is sensitive.

### 18 · Part 2 (divider)
Now the transfer function, and how I realise it with feedback.

### 19 · Generate the options, then choose
The prereview lesson was to list the options first, justify, then pick. So, two options. Option A
is a voltage-to-voltage amplifier with the integrator in the feedback, where the coil resistance
only shows up in the noise. Option B is a transimpedance amplifier where the inductor integrates,
but then the coil resistance enters the transfer and the inductor gets large. I choose Option A,
and I stay consistent with it for the rest of the design.

### 20 · Why feedback? The asymptotic-gain model
I use feedback so a passive network sets the transfer, which means accuracy follows the passive
components, not the transistor. I analyse it with the asymptotic-gain model: the gain is the
asymptotic gain times the servo function, plus a small direct term. The asymptotic gain is the
ideal nullor transfer, the loop gain is how hard the feedback works, and when the loop gain is
large the servo goes to one and the gain becomes the ideal transfer. I'll read every one of these
curves later.

### 21 · Sizing the feedback network
I bound the feedback resistor from two budgets. The noise budget caps it from above at about 7.5
kilohm, and the power budget caps it from below at about 1.4 kilohm. I pick 3.2 kilohm. The
integrator capacitor follows from the time constant, about 5 nanofarad, and I add a bypass
resistor of about 53 kilohm. That bypass does two justified jobs: it sets the low corner at 600
hertz and gives the DC bias a path.

### 22 · Part 3 (divider)
Now the first stage, designed straight from the noise budget.

### 23 · The first stage sets the input-referred noise
I model the controller as a noisy nullor, an ideal nullor plus the input transistor's own voltage
and current noise. The trick is that later stages add almost nothing, because their noise is
divided by the first-stage gain. So the entire noise budget is effectively spent on stage one,
which is why I design stage one first.

### 24 · The knobs: gm, c-iss, inversion
The input-referred thermal noise goes as four k T gamma over gm. So more transconductance means
less noise. But a wider device adds input capacitance, which loads the coil, and weak inversion
gives the most transconductance per amp. So I minimise the product of gm and input capacitance:
enough gm for the noise budget, the lowest capacitance for the source.

### 25 · Which stage? CS, CG or CD
Between common-source, common-gate and common-drain, I pick common-source. Its chain matrix has
the smallest entries, which means it behaves most like a nullor, so the stages after it barely add
noise. Common-gate and common-drain are followers, they give no voltage gain to suppress later
noise. So the first stage is a common-source stage in saturation.

### 26 · From budget to device parameters
The procedure is four steps. Find the output noise spectrum, integrate it DIN-A weighted to a
variance, write the transconductance as a function of input capacitance, then take the lowest
feasible capacitance and convert to gm, current, width and length with the EKV model. That gives a
PMOS input around 73 microsiemens, 19 micron wide, 0.7 micron long, at about 8 microamp.

### 27 · Part 4 (divider)
Before I add complexity, I check whether one stage is enough.

### 28 · Single stage: the circuit
Here is the single-stage realisation, modelled behaviourally with one transconductor. Coil,
termination, a single common-source controller, the feedback network, and the load. This is the
simplest thing that could work, so I test it.

### 29 · Is a single stage enough?
The plot is the asymptotic-gain model for the single stage, so let me read the five curves. The
red curve is the asymptotic gain, the ideal target the feedback should deliver. The black curve
is the loop gain, and that is the problem here: it stays below 0 dB, magnitude one, across the
whole band. The magenta curve is the servo function, and because the loop gain never reaches 0 dB
the servo can't reach one, so the blue closed-loop gain is not locked onto the red asymptotic
target. The green curve is the direct feed-through, which is negligible.

Now the checks. A single common-source has only three usable terminals, so I'd use a differential
pair, about four times the current and area. The current drive into the load is fine, and the
voltage headroom on 0.9 volt is fine. But with the loop gain below one, the feedback can't enforce
the transfer, so the accuracy is poor. So one stage fails the accuracy test, and I move to a dual
stage.

### 30 · Part 5 (divider)
So, the dual stage.

### 31 · Why a dual stage?
There are five competing costs: noise, power, accuracy, stability and area. The key insight is
that the first stage dominates the noise and the second stage dominates the loop gain. So I split
the job, a low-noise PMOS differential pair first, then a high-loop-gain NMOS common-source. One
stage couldn't give both; two stages can.

### 32 · Suggested topology
Here's the suggested topology, coloured by block. On the left, in grey, the coil source. Then in
cyan the first stage, the PMOS differential pair. In yellow the feedback network. In pink the
second stage, the NMOS common-source. And in green the ADC load. The two stages are the point, so
they're the bold colours, coil, feedback and load sit lighter around them. At the bottom are the
SLiCAP directives: the source, the detector, and the loop-gain reference.

### 33 · First stage: differential pair vs single CS
Why the differential pair for stage one? It has lower noise, high common-mode rejection, and it
naturally matches the coil, which is a floating two-terminal source. The single-ended
common-source is smaller, lower power and simpler, but it lets common-mode interference through
and it's noisier. The coil is floating and noise is my priority, so the differential pair wins.

### 34 · Second stage: NMOS common-source
The second stage is chosen for what the first one isn't optimised for: high loop gain for
accuracy, strong current drive into the load, and low power. I use minimum length, 0.18 micron,
for speed, and the current, about 16 microamp, is set so it can charge the load at the full-power
frequency.

### 35 · Dual-stage design parameters
Here is the behavioural dual stage and the loop-gain expression. Four parameters define it. The
first-stage transconductance is set by the noise budget. The second-stage transconductance is the
extra loop-gain factor. The feedback resistor is set by the transfer. And the first-stage output
conductance sets its output resistance. Together they give a DC loop gain of about 45 dB, which is
enough for accuracy.

### 36 · Asymptotic-gain model: every curve explained
This is the plot the review really cares about, so let me read every curve. Dark blue is the
closed-loop gain, what I deliver. Cyan is the asymptotic gain, the ideal target. Orange is the
loop gain, about 45 dB at DC. Green is the servo function, which stays at one while the loop gain
is large, and that's why the gain sits on the asymptotic line. Pink is the direct term, the
feed-through, which is negligible. So the gain follows the ideal target exactly where the servo is
one, and departs once the loop gain falls.

### 37 · Part 6 (divider)
Now I make the model realistic.

### 38 · EKV small-signal model
It's the same topology as the suggested-topology slide, but I've circled the two transistors,
because that's where the change is. Each transistor is now the full EKV small-signal model: it
adds finite output conductance and all the parasitic capacitances, C_gs, C_gd, C_gb, C_db, C_sb,
that the ideal nullor and the behavioural model left out. Those parasitics are exactly what create
the high-frequency poles and zeros, so now the stability check is trustworthy.

### 39 · Pole-zero analysis
There are five poles and they all have negative real parts, so the amplifier is stable. The
dominant pole is around 600 hertz, there's a well-damped pair near 150 kilohertz, and there's a
pair near 51 megahertz with a quality factor around 5.4, which is severely underdamped and shows
up as peaking. The gain plot follows the poles and zeros exactly as the table says, so that
high-Q pair is the thing I fix next.

### 40 · Part 7 (divider)
So I compensate.

### 41 · Target: maximally-flat magnitude
A pole pair with a quality factor above one over root two peaks and rings. The maximally flat, or
Butterworth, target sets that pair to a Q of about 0.7. No peaking, the fastest flat response, and
a comfortable phase margin. To move the pair I add a zero to the loop gain near it, which injects
phase lead and lowers the effective Q. I'm shaping stability, not just the gain.

### 42 · The phantom-zero method
This is the actual SLiCAP compensated circuit, and I've circled the one component I added: R_phz,
in series with the load. It makes a zero in the loop gain without putting a real pole in the
signal path, because the feedback is tapped before it. I choose it because it costs almost
nothing: no extra noise source in the signal path, negligible power and area, and no compensation
capacitor. The cheapest way to buy stability.

### 43 · Compensation result
Here's the result, with two plots. On the left, the full-band gain before and after: the peak is
gone and the passband is untouched. On the right, a sweep of R_phz showing how it tunes the peak:
too small under-damps and the bump stays, the MFM value flattens it, too large over-damps and
costs bandwidth. The MFM value, about 0.42 kilohm, pulls the 51 megahertz pair's Q from 5.4 down
to 0.7. All poles stay in the left half-plane, so it is still stable. The whole fix is one resistor.

### 44 · Part 8 (divider)
Let me wrap up.

### 45 · Conclusions
So, the structured path from end to end. I set the specification from the environment, chose a
voltage-to-voltage integrator after listing the options, built the model up block by block,
designed the first stage from the noise budget, found a single stage fails on accuracy and moved
to a dual stage, used a PMOS pair for noise and an NMOS common-source for loop gain, checked the
poles and zeros and found it stable with one high-Q pair, and fixed that with a phantom zero for a
maximally flat response. The point of all of it is the reasoning: the right order, options before
choices, and every curve and component justified.

### 46 · Thank you
That's the design. Thank you, and I'm happy to take questions.
