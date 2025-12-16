# Design of a Hearing Loop System in CMOS18 Technology - Part 3

## Overview
This TU Delft educational resource documents the design of a hearing loop amplifier system implemented in CMOS 18nm technology. The project encompasses three primary amplifier stages for a hearing aid application.

## Key Components

**Three Amplifier Stages:**
1. **A1 - Receive Coil Amplifier**: Converts magnetic field signals from a loop antenna into audio signals with characteristics matching microphone output
2. **A2 - ADC Driver**: Drives a 10 pF ADC input capacitance to 0.9 Vpp at 110 dB SPL
3. **A3 - Loudspeaker Driver**: Produces 110 dB SPL output from peak-peak battery voltage

## Design Specifications

The integrated noise at amplifier A1's output must not exceed "30 dBSPL," which corresponds to approximately 11.9 µV RMS. The hearing loop receiver employs an integrating characteristic with idealized gain of 62.8×10³/s.

## Design Exercise Focus

The exercise involves determining optimal transistor parameters:
- Transconductance (g_m) and input capacitance (c_iss)
- Device geometry (W, L) and operating current (I_DS)
- Minimizing costs while meeting DIN A-weighted noise specifications

## Available Resources

- SLiCAP design scripts for noise optimization
- SPICE verification models
- HTML design reports documenting calculated parameters
- Referenced technical documents from Sonion and OnSemi

## Source Materials
Presentation and supporting documents address hearing aid DSP functionality, battery specifications, and patent background on hearing loop technology.

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/designExample/HearingLoop/HearingLoop_3.html
