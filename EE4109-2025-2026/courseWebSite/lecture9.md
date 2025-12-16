# Lecture 9: Design of Noise Performance (09-12-2025)

**Location:** Pulse-Hall 5 (33.A1.200)
**Time:** 15:45 - 17:30
**Instructor:** Anton Montagne

## Main Topics

### Design Considerations for Noise Performance
The lecture employs a systems engineering methodology using top-down error budget distribution across subcircuit components.

### Three Primary Noise Contributors

1. **Signal Source**
   - Noise characteristics must be established before design begins
   - Not a design variable

2. **Feedback Network**
   - Passive elements (resistors, capacitors, inductors) introduce noise
   - Sub-budget assignment limits feedback element values
   - Potential conflict between noise and power dissipation specifications

3. **Controller Noise Sources**
   - Input stage noise (CS stages, differential pairs dominate)
   - Subsequent stage contributions (minor budget)
   - Biasing circuit noise including PSRR and bias source noise

## Learning Activities

### Presentation Component
Students analyze a hearing loop receiver coil amplifier design covering:
- Specifications and functional modeling
- Transfer characteristics validation
- Signal source noise contribution assessment

**Resource:** Design project archive available for download (specifications.ipynb notebook)

### Group Exercise Tasks

**Part 1:** Develop feedback amplifier schematic replacing voltage-controlled voltage source, ensuring:
- Desired frequency response
- Noise-free nullor controller with passive feedback elements
- Output noise ≤25% of total noise budget
- Peak current ≤25% of supply budget

**Part 2:** Design input stage transistor (NMOS18/PMOS18 CS-stage and differential-pair configurations) using gm/ID methodology

**Tool:** SLiCAP software for equation derivation and optimization

## Resources
- Design archive: Notebooks.zip (includes MOSdesign.py script)
- Navigation links to previous (Lecture 8) and subsequent (Lecture 10) lectures

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/courseWebSite/lecture9/lecture9.html
