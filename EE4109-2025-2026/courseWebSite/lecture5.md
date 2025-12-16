# Lecture 5: CS Stage Noise Performance Optimization (25-11-2025)

**Time:** 15:45 - 17:30
**Location:** Hall Ampere (36.HB.01.670)

## Main Content

### Design of CS Stage Noise Behavior

The lecture focuses on input stage design principles for feedback amplifiers. Key concepts include:

- Input-referred noise sources in feedback amplifiers ideally match those of the controller alone
- "Passive feedback elements increase the controller's input-referred noise sources' contribution to the amplifier noise"
- The Common-Source (CS) stage provides the best nullor approximation, making it the preferred controller input stage

### Educational Resources

**Primary Learning Material:**
- Presentation: "Noise Design of the Input Stage MOS in Feedback Amplifiers"
  - Available in full and parts versions
  - Source: analog-electronics.tudelft.nl

**Technical Tools:**
- SLiCAP MOS noise design automation script (downloadable)

## Group Exercise Assignment

Students must design a feedback amplifier for a hearing loop receiver using these eight steps:

1. Develop source network model
2. Create load network model
3. Design feedback configuration for accurate transfer across frequency range
4. Budget feedback element noise contribution
5. Budget controller current-drive requirements
6. Set feedback element values within budget constraints
7. Assign controller input stage noise budget
8. Design NMOS or PMOS input stage with finalized feedback values

**Deadline:** Lecture 9 (09-12-2025)

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/courseWebSite/lecture5/lecture5.html
