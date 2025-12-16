# Lecture 11: Design of Accuracy, Weak Nonlinearity and Bandwidth (16-12-2025)

**Location:** Pulse-Hall 3 (33.A0.300)
**Time:** 15:45 - 17:30

## Key Design Principles

### Accuracy, Bandwidth, and Linearity
The lecture emphasizes that these three characteristics improve by increasing the loopgain:

1. **Midband accuracy** decreases inaccuracy through elevated DC loop gain
2. **Bandwidth** depends on the loop gain-poles product, with cascode stages offering optimal contributions
3. **Linearity** can be enhanced by reducing signal excursions and applying compensation techniques

### Optimal Stage Types
Cascode stages and balanced versions minimize T1 matrix parameters, making them "nullor-like" for accuracy, bandwidth, and linearity optimization.

### Stage Count Considerations
- **Accuracy:** No upper limit; additional stages or positive feedback can enhance DC loop gain
- **Bandwidth:** Limited by fT; stability and frequency compensation constrain stage count
- **Linearity:** Requires SPICE verification; improvement comes through bias adjustments and compensation

## Group Exercise Overview

The task involves designing a hearing loop receiver controller with adequate noise performance, drive capability, accuracy, bandwidth, and linearity. The workflow progresses from single-stage feasibility analysis through potential two-stage solutions.

## Available Resources
A design project archive containing multiple Jupyter notebooks:
- specifications.ipynb
- feedbackConfig.ipynb
- feedbackConfigSimple.ipynb
- firstStageDesign.ipynb
- DIN_A.ipynb

**Note:** SLiCAP version 4.0.9 includes bug fixes and library additions.

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/courseWebSite/lecture11/lecture11.html
