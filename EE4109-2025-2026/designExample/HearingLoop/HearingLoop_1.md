# Hearing Loop System in CMOS18 Technology - Part 1

## Overview
This TU Delft educational document describes the design of a hearing aid amplifier system implemented in CMOS18 technology, focusing on three key amplifier stages.

## Main Content Areas

### Application Components
The system comprises three amplifiers:

1. **A1 - Receive Coil Amplifier**: Converts magnetic field from a current-driven loop antenna into audio signals. The design requires matching the gain and frequency response to microphone outputs.

2. **A2 - ADC Driver**: Amplifies signals to drive a 10 pF ADC input capacitance, delivering 0.9 Vpp output at 110 dB SPL audio levels.

3. **A3 - Loudspeaker Driver**: Produces 110 dBSPL output using either single-ended or full-bridge voltage amplification configurations.

## Key Technical Specifications

**A1 Gain Calculation**: The receive coil sensitivity is approximately "-59.4 dBV/(A/m)" at 1 kHz. The required voltage transfer is calculated by comparing coil output to microphone sensitivity (-35.5 dBV/Pa).

**A2 Specifications**: Requires minimal gain (approximately 1.41x) to reach required ADC levels.

**A3 Configuration**: Needs full-bridge voltage amplification with gain of two to achieve target SPL, accounting for loudspeaker sensitivity variations across frequencies.

## Reference Materials
The page links to component datasheets (receive coil, microphone, loudspeaker), battery specifications, and historical patent documentation for hearing loop technology.

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/designExample/HearingLoop/HearingLoop_1.html
