# Speaker notes — A1 Receive-Coil Amplifier review
**Daniel Tyukov (5714699) · 15 June 2026 · ~1 hour**

First-person notes to read from, one block per slide. Keep the pace calm. The grade is in the
reasoning, not the final numbers.

---

### 1 · Title
Good morning. I'm Daniel Tyukov, student number 5714699. Today I'll take you through my design
of the A1 receive-coil amplifier for the hearing-loop receiver. I work top-down: I fix the
specification first, then I justify every choice before I make it.

### 2 · Outline
Here's the route. I start with the specification and the environment A1 lives in. Then the
transfer function and the feedback configuration. Then the first stage, which I design from the
noise budget. I check whether one stage is enough, find it isn't, and move to a dual stage.
Then I build the realistic EKV model, look at the poles and zeros, and finish with frequency
compensation. One idea runs through all of it: I replace the "how" with the "why".

### 3 · Part 1 — Specification & environment
Let me start where every structured design has to start, with the specification.

### 4 · The hearing loop and where A1 lives
A hearing loop is a wire around a room that carries the audio as a magnetic field. A hearing
aid picks that field up with a small coil. A1 is the first amplifier after that coil. Before I
touch a transistor I need to know the environment: what feeds A1, and what A1 drives. That is
what fixes the whole specification.

### 5 · A1 in the signal chain
Here is the chain. A1 amplifies the coil. Then a switch selects between the microphone and the
loop. Then the ADC driver, the ADC, and the DSP. A1 runs from a single 0.9-volt supply, and
the whole amplifier shares a one-milliwatt power budget. So I ask three questions, in order:
what is the environment, how does the block work, and what is the budget.

### 6 · The pick-up coil is a differentiator
The coil output is proportional to the rate of change of the magnetic flux, so the coil
differentiates the signal. Electrically I model it as a series inductance and resistance, about
120 millihenry and 875 ohm, with a small parasitic capacitance near 9 picofarad, plus a
termination resistor. The consequence is simple: if the coil differentiates, A1 has to
integrate, so the two together stay flat across the audio band.

### 7 · Coil resonance and the termination resistor
That inductance and capacitance resonate near 150 kilohertz. Left alone, the peak rings and can
overload the input. So I add a termination resistor across the input and size it for critical
damping, a quality factor of one over root two. This is exactly the kind of choice the review
wants justified. The resistor is there only to damp the resonance, and once it's there it
becomes a noise source I have to budget for.

### 8 · Output: source-select switch and ADC
The output side has two parts. The source-select switch needs the microphone and the loop to
give the same voltage at the one-kilohertz reference, and that fixes my gain. The ADC input
behaves like an ideal voltage amplifier, it draws no current, so the only load A1 actually sees
is a 10-picofarad capacitor. So A1 is a voltage-to-voltage amplifier driving a capacitor. It is
not a power stage.

### 9 · How should A1 work?
Four points. A1 is a voltage-to-voltage amplifier. Its transfer is an integrator, which cancels
the coil's differentiation, about 62 thousand over s, with a time constant of 16 microseconds.
The gain is set so the microphone and the loop match at the reference. And the weighted output
noise has to stay below the microphone floor, 30 dB SPL. Notice the order: transfer first, then
noise. And I keep it a voltage amplifier the whole way. I do not quietly switch to a
transimpedance amplifier.

### 10 · Specification & budget
This table is the contract. The integrator transfer, the audio band of 600 hertz to 6
kilohertz, the output-noise limit around 11 microvolts, the 10-picofarad load, the supply and
power, and the coil parameters. Every later decision traces back to one line here. And to be
clear, the amplifier is graded on this reasoning, not on whether the last digit is perfect.

### 11 · Noise is judged by ear: DIN-A weighting
Noise matters most where the ear is sensitive, so I weight the output noise with the standard
DIN-A curve before I integrate it to an RMS value. It is flat at one kilohertz and rolls off
hard below 600 hertz and above a few kilohertz. The weighting makes the budget perceptually
honest. It is tight exactly where it needs to be.

### 12 · Part 2 — Transfer & feedback configuration
Now the transfer function, and how I realise it with feedback.

### 13 · Generate the options, then choose
The prereview lesson was clear: list the options first, justify, then pick. Don't decide and
backfill. So, two options. Option A is a voltage-to-voltage amplifier with the integrator in
the feedback, and the coil resistance only shows up in the noise. Option B is a transimpedance
amplifier where the inductor integrates, but then the coil resistance enters the transfer and
the inductor gets large. I choose Option A, and I stay consistent with it for the rest of the
design. That last part is what tripped up the previous review.

### 14 · Why feedback? The asymptotic-gain model
I use feedback so a passive network sets the transfer. That means accuracy follows the passive
components, not the transistor. I analyse it with the asymptotic-gain model: the gain is the
asymptotic gain times the servo function, plus a small direct term. The asymptotic gain is the
ideal nullor transfer. The loop gain, L, is how hard the feedback works. When the loop gain is
large the servo goes to one, and the gain becomes the ideal transfer. The review wants me to
explain every one of these curves, so keep the names in mind.

### 15 · Sizing the feedback network
I bound the feedback resistor from two budgets. The noise budget caps it from above, around 7.5
kilohm. The power budget caps it from below, around 1.4 kilohm. I pick 3.2 kilohm in between.
The integrator capacitor then follows from the time constant, about 5 nanofarad, and I add a
bypass resistor of about 53 kilohm in parallel. That bypass does two justified jobs: it sets
the low corner at 600 hertz, and it gives the DC bias a path.

### 16 · Part 3 — First stage: noise design
Now the first stage, which I design straight from the noise budget.

### 17 · The first stage sets the input-referred noise
I model the controller as a noisy nullor: an ideal nullor plus the input transistor's own
voltage and current noise. The trick is that later stages add almost nothing, because their
noise is divided by the first-stage gain. So the entire noise budget is effectively spent on
stage one. That is why I design stage one first.

### 18 · The knobs: gm, c-iss, inversion
The input-referred thermal noise goes as 4kT-gamma over gm. So more transconductance means less
noise: more current for less voltage. But a wider device adds input capacitance, which loads
the coil. Weak inversion gives me the most transconductance per amp of current. So I minimise
the product of gm and input capacitance: enough gm for the noise, the lowest capacitance for
the source. The reason I pick weak inversion is that it gives the best transconductance
efficiency for the budget I have.

### 19 · Which stage? CS, CG or CD
Between common-source, common-gate and common-drain, I pick common-source. Its chain matrix has
the smallest entries, which means it behaves most like a nullor, so the stages after it barely
add noise. Common-gate and common-drain are followers. They give no voltage gain to suppress
later noise. So the first stage is a common-source stage in saturation.

### 20 · From budget to device parameters
Four steps. Find the output noise spectrum. Integrate it, DIN-A weighted, to a variance. Write
the transconductance as a function of input capacitance. Then take the lowest feasible
capacitance and convert to gm, current, width and length with the EKV model. That gives me a
PMOS input around 73 microsiemens, 19 micron wide, 0.7 micron long, at about 8 microamp. SLiCAP
gives me the symbolic spectrum, the EKV model turns the budget into geometry, and ngspice checks
the numbers.

### 21 · Part 4 — Single stage & loop-gain check
Before I add complexity, I check whether one stage is enough.

### 22 · Is a single stage enough?
A single common-source has only three usable terminals, so I'd use a differential pair, which
costs about four times the current and area. The current drive into the load is fine. The
voltage headroom on 0.9 volt is fine. But the loop gain stays below one across the band. If the
loop gain is below one, the feedback can't enforce the transfer, so the accuracy is poor. So one
stage fails the accuracy test, and I move to a dual stage.

### 23 · Part 5 — Dual stage
So, the dual stage.

### 24 · Why a dual stage?
There are five competing costs: noise, power, accuracy, stability and area. The key insight is
that the first stage dominates the noise and the second stage dominates the loop gain. So I
split the job, and optimise each stage for one thing. The first stage is a low-noise PMOS
differential pair, the second is a high-loop-gain NMOS common-source. One stage couldn't give me
both low noise and enough loop gain. Two stages can.

### 25 · The dual-stage topology
Here's the full circuit, straight from SLiCAP. On the left, the coil source with its
termination. Then the PMOS first stage. Then the feedback network: the integrator capacitor, the
feedback resistor and the bypass. Then the NMOS common-source second stage. And the 10-picofarad
ADC load. At the bottom you can see the SLiCAP directives, the source, the detector and the
loop-gain reference.

### 26 · First stage: differential pair vs single CS
Why the differential pair for stage one? It has lower noise, high common-mode rejection, and it
naturally matches the coil, which is a floating two-terminal source. The single-ended
common-source is smaller, lower power and simpler, but it lets common-mode interference through
and it's noisier. The coil is floating and noise is my priority here, so the differential pair
wins.

### 27 · Second stage: NMOS common-source
The second stage is chosen for what the first one isn't optimised for: high loop gain for
accuracy, strong current drive into the load, low power and small area. I use minimum length,
0.18 micron, for speed, and I trade width for transconductance efficiency. The current, about 16
microamp, is set so it can charge the load at the full-power frequency.

### 28 · Asymptotic-gain model — every curve explained
This is the plot the review really cares about, so let me read it carefully. Dark blue is the
closed-loop gain, what I actually deliver. Cyan is the asymptotic gain, the ideal target. Orange
is the loop gain, about 45 dB at DC, which is my budget for accuracy. Green is the servo
function: it stays at one while the loop gain is large, which is why the gain sits on the
asymptotic line. Pink is the direct term, the feed-through, negligible here. So the gain follows
the ideal target precisely where the servo is one, and it departs only once the loop gain falls.

### 29 · Part 6 — EKV model & pole-zero
Now I make the model realistic.

### 30 · From behavioural to the EKV model
I swap the ideal devices for the EKV small-signal model, which includes the real
transconductance, the output conductance, and all the parasitic capacitances. The passband still
sits on the asymptotic gain, but now the high-frequency behaviour is trustworthy, so I can look
at the real poles and zeros.

### 31 · Pole-zero analysis
There are five poles, and they all have negative real parts, so the amplifier is stable. The
dominant pole is around 600 hertz. There's a well-damped pair near 150 kilohertz. And there's a
pair near 50 megahertz with a quality factor around five, which is severely underdamped, and
it's the peaking I can see in the gain. The gain plot follows the poles and zeros, exactly as
expected. So that high-Q pair is the thing I now have to fix.

### 32 · Part 7 — Frequency compensation
So I compensate.

### 33 · Target: maximally-flat magnitude
A pole pair with a quality factor above one over root two peaks and rings. The maximally-flat,
or Butterworth, target sets that pair to a Q around 0.7. No peaking, the fastest flat response,
and a comfortable phase margin. To move a pole pair I add a zero to the loop gain near it, which
injects phase lead and lowers the effective Q. I'm shaping stability here, not only the gain.

### 34 · The phantom-zero method
The method I use is the phantom zero: a resistor in series with the load capacitor, which makes
a zero in the loop gain without putting a real pole in the signal path. I choose it because it
costs almost nothing. No extra noise source in the signal path, negligible power and area, and
no compensation capacitor to store energy. It's the cheapest way to buy stability.

### 35 · Compensation result
And here's the result. A phantom-zero resistor of about 0.7 kilohm pulls the quality factor of
that high-frequency pair from five down to 0.7, which is maximally flat. The peak is gone, the
passband is untouched, and all the poles stay in the left half-plane, so it's still stable. The
whole fix is one resistor.

### 36 · Part 8 — Conclusions
Let me wrap up.

### 37 · Conclusions
So, the structured path from end to end. I set the specification from the environment. I chose a
voltage-to-voltage integrator after listing the options. I designed the first stage from the
noise budget. I found a single stage fails on accuracy and moved to a dual stage. I used a PMOS
pair for noise and an NMOS common-source for loop gain. The EKV pole-zero analysis showed it's
stable, with one high-Q pair. And a phantom zero gave me a maximally-flat response. The point of
all of it is the reasoning: the right order, options before choices, and every curve and
component justified.

### 38 · Thank you
That's the design. Thank you. I'm happy to take questions.
