# Lecture 13: Design of Biasing (06-01-2026)

**Location:** Hall Ampere (36.HB.01.670)
**Time:** 15:45 - 17:30
**Instructor:** Anton Montagne

## Main Topics

### Biasing Design Considerations

The lecture outlines a two-step biasing procedure:

**Step 1: Ideal Source Design**
- Add biasing sources to transistors (four per transistor)
- Integrate the power supply into the circuit
- Connect amplifier ports to power supply reference points
- Redirect bias currents through the power supply for passive implementation
- Minimize voltage sources in the signal path through device selection or topology changes

**Step 2: Bias Source Implementation**
Starting from a stable voltage or current reference, designers must:
- Define architectural requirements (floating vs. connected sources)
- Establish static voltage-current characteristics
- Assess noise performance
- Evaluate small-signal and parasitic impedances
- Identify operating principles
- Apply optimization techniques including negative feedback, compensation, and filtering

## Practical Exercise

The guided group exercise examines biasing implementations for the hearing loop receive amplifier, both single-stage and dual-stage configurations.

**Resource:** A zip archive containing SLiCAP notebooks is available for download.

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/courseWebSite/lecture13/lecture13.html
