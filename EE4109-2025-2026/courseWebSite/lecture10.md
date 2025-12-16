# Lecture 10: Design of Drive Capability (11-12-2025)

**Location:** Hall Ampere (36.HB.01.670)
**Time:** 08:45 - 15:30
**Instructor:** Anton Montagne

## Key Design Concepts

The lecture covers six fundamental design considerations:

1. **Output Stage Sizing**: Current and voltage drive demands determine transistor dimensions and quiescent operating conditions for output stage controllers.

2. **Budget Allocation**: A hierarchical approach distributes voltage and current drive specifications among system components.

3. **Minimum Supply Requirements**: Applications typically mandate lowest operating voltages; controllers must function reliably at these thresholds.

4. **Voltage Headroom Management**: The gap between peak supply and output voltage accommodates DC bias errors and saturation voltages, which must collectively stay within allocated margins.

5. **Current Drive Calculation**: Output capacity equals load current plus feedback network current plus bias errors in output devices.

6. **Biasing Strategy**: Proper biasing methodology must precede output stage design to maintain amplifier port errors within acceptable tolerances.

## Practical Exercise

Students continue working on the hearing loop receive amplifier project initiated in previous sessions, applying these drive capability design principles.

## Available Resources
- Downloadable .rst source file
- PDF version available
- Navigation to related lectures on noise performance and accuracy/bandwidth design

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/courseWebSite/lecture10/lecture10.html
