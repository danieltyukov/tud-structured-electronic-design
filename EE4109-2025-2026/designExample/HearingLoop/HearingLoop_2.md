# Hearing Loop System in CMOS18 Technology - Part 2

## Overview
This TU Delft educational resource documents the design of a hearing aid system with three key amplifier stages implemented in CMOS18 technology.

## Core Components

**Three Main Amplifiers:**

1. **A1 - Receive Coil Amplifier**: Converts magnetic field signals from a loop antenna into audio, with transfer function of 62.4×10³/s and differential input resistance >4.524 kΩ

2. **A2 - ADC Driver**: Drives a 10 pF ADC input capacitance to 0.9 Vpp output at 110 dB SPL, though the document notes the microphone may directly interface with the ADC

3. **A3 - Loudspeaker Driver**: Produces differential output for the speaker with gain of 2, requiring rail-to-rail common-mode output voltage at half supply voltage

## Technical Specifications

- **Frequency range**: Upper limit approximately 10 kHz for A1
- **Input impedance requirement for A1**: Single-ended preferred over differential
- **Output characteristics**: A1 is single-ended; A3 is differential

## Design Resources
The document references presentation materials, DSP specifications, patent documentation, and battery datasheets from industry partners like Sonion and Rayovac.

## Educational Context
Part of EE4109 (2025-2026) coursework on structured electronics design at TU Delft, with design exercises requiring topology selection and impedance specification.

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/designExample/HearingLoop/HearingLoop_2.html
