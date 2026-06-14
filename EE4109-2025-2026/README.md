# EE4109 2025-2026: Structured Electronics Design

**Institution:** TU Delft
**Instructors:** Chris Verhoeven and Anton Montagne
**Last Updated:** 16/12/2025

## Overview

This repository contains all downloaded content from the EE4109 (2025-2026) course website on Structured Electronics Design. The course teaches a systematic approach to designing application-specific negative feedback amplifiers using CMOS technology.

## Educational Approach

The course uses a practical, project-based methodology centered on designing a hearing loop receiver. Students progress through design aspects step-by-step, alternating between:
- **Odd lectures:** Introduce new design concepts with homework assignments
- **Even lectures:** Review and discuss completed work

## Repository Structure

> **Note:** the tree below covers the downloaded *text* content. The folder also contains
> **runnable worked-example notebook folders** (`MOS_EKV_BSIM/`, `MOSparams/`, `CSstage/`,
> `CDstages/`, `SLiCAP_balancing/`, `CH14/`, `LTspiceComplementaryParallel/`,
> `SLiCAP_python_mosEKVplots/`) and `course_pdfs/` (lecture slides & posters). These are
> documented in **[`WORKED_EXAMPLES.md`](WORKED_EXAMPLES.md)**.

```
EE4109-2025-2026/
├── courseWebSite/          # Main course lectures and materials
│   ├── index.md            # Course overview and lecture schedule
│   ├── lecture1.md         # Introduction (11-11-2025)
│   ├── lecture2.md         # Amplification and Biasing (13-11-2025)
│   ├── lecture3.md         # MOS Modeling (18-11-2025)
│   ├── lecture4.md         # CS Stage (20-11-2025)
│   ├── lecture5.md         # CS Stage Noise Optimization (25-11-2025)
│   ├── lecture6.md         # Balancing Techniques (27-11-2025)
│   ├── lecture7.md         # Feedback Stages (02-12-2025)
│   ├── lecture8.md         # Multi-Stage Amplifiers (04-12-2025)
│   ├── lecture9.md         # Noise Performance (09-12-2025)
│   ├── lecture10.md        # Drive Capability (11-12-2025)
│   ├── lecture11.md        # Accuracy, Bandwidth, Linearity (16-12-2025)
│   ├── lecture12.md        # Frequency Compensation (18-12-2025)
│   ├── lecture13.md        # Biasing Design (06-01-2026)
│   └── lecture14.md        # Wrap Up (08-01-2026)
│
└── designExample/          # Design project resources
    ├── HearingLoop/        # Hearing aid amplifier design
    │   ├── index.md        # HearingLoop resources overview
    │   ├── HearingLoop_1.md
    │   ├── HearingLoop_2.md
    │   └── HearingLoop_3.md
    │
    └── Technology/         # MOS models and parameters
        └── index.md        # Technology resources overview
```

## Course Content Summary

### Lecture Series (14 Sessions)

1. **Introduction** - Course overview, hearing loop project introduction, SLiCAP setup
2. **Amplification & Biasing** - Transresistance amplification, biasing techniques
3. **MOS Modeling** - EKV model, device characterization, inversion coefficient
4. **CS Stage** - Common-source stage design, static/dynamic performance
5. **Noise Optimization** - Input stage noise design for feedback amplifiers
6. **Balancing** - Error reduction through differential and push-pull techniques
7. **Feedback Stages** - CD and CG stages, single-stage negative feedback
8. **Multi-Stage Design** - Controller architectures, cascode stages, stage interconnection
9. **Noise Performance** - Top-down noise budgeting, source/feedback/controller contributions
10. **Drive Capability** - Output stage sizing, voltage/current budgets, headroom management
11. **Accuracy & Bandwidth** - Loop gain optimization, linearity, cascode benefits
12. **Frequency Compensation** - Dual-stage solution, stability analysis
13. **Biasing Design** - Ideal sources, passive implementation, bias circuit optimization
14. **Wrap Up** - Design methodology recap, exam preparation

### Design Project: Hearing Loop Receiver

The capstone project involves designing three amplifier stages:

- **A1 - Receive Coil Amplifier:** Converts magnetic field to audio (62.4×10³/s transfer, ≤30 dBSPL noise)
- **A2 - ADC Driver:** Drives 10 pF capacitance to 0.9 Vpp at 110 dB SPL
- **A3 - Loudspeaker Driver:** Produces 110 dBSPL output with full-bridge differential configuration

## Prerequisites

- EE3C11 or homologation program completion
- Proficiency with:
  - KiCAD (schematic capture)
  - LTspice/NGspice (SPICE simulation)
  - SLiCAP (circuit analysis)
  - Python/Jupyter Notebook

## Assessment

Oral group examination (3-7 students) focusing on:
- Complete and correct design motivation
- Signal path verification using SLiCAP and SPICE
- Biasing considerations (mandatory)
- Bias circuit design (optional, rewarded)

## Key Topics Covered

- **Device Modeling:** EKV vs. BSIM models, small-signal parameters, noise modeling
- **Amplifier Stages:** CS, CD, CG, differential pairs, push-pull, cascode
- **Design Techniques:** Negative feedback, balancing, frequency compensation
- **Performance Optimization:** Noise, bandwidth, accuracy, linearity, drive capability
- **Systems Engineering:** Top-down budgeting, hierarchical design, verification

## Additional Resources

- **Book:** Structured Electronics Design 3rd edition (PDF and HTML)
- **SLiCAP:** Circuit analysis and design automation tool
- **Posters:** Noise, poles/zeros, frequency compensation, CMOS design techniques
- **Videos:** YouTube lecture series from 2020 course

## Related Courses

- **Homologation:** 10 supplementary modules for prerequisite knowledge
- **EE3C11 2024-2025:** Foundational course (17 lectures)
- **ET8011 2024-2025:** Related graduate-level course
- **Seminar series Honolulu:** 10 specialized sessions

## Source Information

All content downloaded from:
https://analog-electronics.tudelft.nl/EE4109-2025-2026/

**Download Date:** December 2025

## Notes

- Content saved in Markdown format for readability and version control
- Original HTML pages available on course website
- Supplementary materials (PDFs, ZIP archives, videos) referenced but not downloaded
- Images and diagrams noted but not included in text-based downloads

## Usage

This repository serves as an offline reference for course materials. For the most current content, interactive demos, and downloadable resources, visit the original course website.
