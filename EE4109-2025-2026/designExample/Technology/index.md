# Technology Resources

## Overview
This directory contains MOS (Metal-Oxide-Semiconductor) device models, parameters, and design resources supporting the EE4109 (2025-2026) coursework at TU Delft. The materials focus on CMOS transistor modeling and common-source amplifier stage design.

## Available Resources

### Compressed Archives

1. **CSstage.zip** (2.1M)
   - Modified: 2025-11-19 20:06
   - Contents: Common-source amplifier stage design files

2. **MOS_EKV_BSIM.zip** (286K)
   - Modified: 2025-11-19 20:06
   - Contents: MOS models using both EKV and BSIM approaches

3. **MOSnoise.zip** (78K)
   - Modified: 2025-11-26 17:59
   - Contents: MOS noise modeling and analysis

4. **MOSparams.zip** (750K)
   - Modified: 2025-11-16 23:12
   - Contents: MOS device parameters and characterization

### Directories

- **CSstage/** - Common-source stage design resources
- **MOS_EKV_BSIM/** - EKV and BSIM model files and documentation
- **MOSnoise/** - Noise analysis tools and models
- **MOSparams/** - Device parameter libraries

## Key Modeling Approaches

### EKV Model
The EKV (Enz-Krummenacher-Vittoz) model provides:
- All-regions nonlinear dynamic modeling
- Strong connection to physical device operation
- Clear relationships between small-signal parameters and device geometry
- Inversion coefficient as a key design parameter

### BSIM Model
The BSIM (Berkeley Short-channel IGFET Model) offers:
- Optimized simulation speed
- Industry-standard accuracy
- Comprehensive short-channel effects modeling

## Related Course Materials

These technology files support lectures on:
- Lecture 3: MOS Modeling
- Lecture 4: CS Stage
- Lecture 5: CS Stage Noise Performance Optimization
- Lecture 9: Design of Noise Performance

## Usage

These resources are intended for:
- Understanding MOS transistor behavior across operating regions
- Comparing EKV and BSIM model predictions
- Designing and optimizing common-source amplifier stages
- Analyzing and minimizing noise in MOS circuits
- Parameter extraction and device characterization

## Tools Compatibility

Files are compatible with:
- SLiCAP (for EKV-based design)
- NGspice/LTspice (for SPICE simulation with BSIM models)
- Python/Jupyter Notebook (for parameter analysis)

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/designExample/Technology/
