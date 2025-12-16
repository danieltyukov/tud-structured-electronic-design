# HearingLoop Design Example

## Overview
This directory contains comprehensive resources for the design of a hearing aid amplifier system implemented in CMOS18 technology. The project is part of the EE4109 (2025-2026) coursework on structured electronics design at TU Delft.

## Main Design Documents

### 1. HearingLoop_1.md
Introduction to the hearing loop system with overview of the three main amplifier stages:
- A1 - Receive Coil Amplifier
- A2 - ADC Driver
- A3 - Loudspeaker Driver

Includes gain calculations and basic specifications.

### 2. HearingLoop_2.md
Detailed technical specifications including:
- Transfer functions and impedance requirements
- Frequency range specifications (up to 10 kHz for A1)
- Input/output characteristics for each stage
- Design exercises on topology selection

### 3. HearingLoop_3.md
Advanced design considerations:
- Noise specifications (30 dBSPL max at A1 output)
- Transistor parameter optimization (g_m, c_iss, W, L, I_DS)
- Cost minimization while meeting DIN A-weighted noise specs
- SLiCAP design scripts and SPICE verification

## Available Resources in Directory

### Subdirectories

- **2600_Sonion_2600_pspice/** - PSpice simulation files (2023-08-29)
- **Components/** - Component datasheets and specifications (2023-11-11)
- **NGspice/** - NGspice simulation tools and models (2023-11-11)
- **Notebooks/** - Jupyter notebooks for design and analysis (2025-12-16)
- **Presentations/** - Course presentation materials (2025-11-11)
- **Sonion/** - Sonion manufacturer documentation (2023-11-15)

### Archives

- **Notebooks.zip** (1.7M, 2025-12-16) - Complete collection of design notebooks

### Image Files

- **A1fbType.svg** - A1 amplifier feedback topology diagram
- **A3fbType.svg** - A3 amplifier feedback topology diagram
- **noise_1.svg** - Noise analysis visualization

## Design Specifications Summary

### A1 - Receive Coil Amplifier
- Transfer function: 62.4×10³/s (integrating characteristic)
- Differential input resistance: >4.524 kΩ
- Frequency range: Up to ~10 kHz
- Output noise: ≤30 dBSPL (11.9 µV RMS)
- Coil sensitivity: -59.4 dBV/(A/m) at 1 kHz

### A2 - ADC Driver
- Output: 0.9 Vpp at 110 dB SPL
- Load: 10 pF ADC input capacitance
- Gain: ~1.41x

### A3 - Loudspeaker Driver
- Output: 110 dBSPL
- Configuration: Full-bridge differential voltage amplification
- Gain: 2
- Common-mode output: Rail-to-rail at half supply voltage

## Educational Context

Part of the EE4109 course on Structured Electronics Design, this project serves as a practical application of:
- Systems engineering methodology
- Top-down design approach
- Noise budgeting and optimization
- CMOS amplifier design techniques
- Feedback amplifier theory

## Tools Required

- SLiCAP (circuit analysis and design automation)
- NGspice/LTspice (SPICE simulation)
- Python with Jupyter Notebook
- KiCAD (schematic capture)

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/designExample/HearingLoop/
