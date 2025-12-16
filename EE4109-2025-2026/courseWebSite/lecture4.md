# Lecture 4: CS Stage (20-11-2025)

**Time:** 08:45-10:30
**Location:** Hall Ampere

## Overview
This lecture covers the Common-Source (CS) stage, a fundamental CMOS amplifier configuration.

## Key Resources

**SPICE Test Circuits**
Two simulation test circuits are available for analyzing the intrinsic CS stage and the stage with parallel RC network termination. These examine output/input drive capability, impedances, transfer parameters, and pole splitting.

**Presentations & Educational Materials**
- "CS stage introduction" - motivates CS stage usage and summarizes performance aspects
- "Intrinsic CS stage: Design of static and dynamic performance" - addresses instantaneous and transient behavior design

**Video Lectures** (6 videos available)
Topics include bias source determination, V-I drive capability, small-signal dynamics, impedance analysis, and geometry scaling.

**Demonstration Tools**
NGspice and SLiCAP simulations demonstrate static and dynamic CS stage behavior.

## Group Exercise
Students compare Bode plots of the small-signal transimpedance factor using:
- NGspice with BSIM model
- SLiCAP with EKV model

Conditions: minimum geometry, VDS = 0.9V, across weak/moderate/strong inversion regimes. Investigation includes geometry and inversion effects.

## Navigation
Linked lectures: MOS modeling (prior) and CS stage noise optimization (next).

## Source
https://analog-electronics.tudelft.nl/EE4109-2025-2026/courseWebSite/lecture4/lecture4.html
