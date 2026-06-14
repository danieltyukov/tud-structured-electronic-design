# SED Exam Review — A1 Receive-Coil Amplifier
**Daniel Tyukov (5714699) · EE4109 Structured Electronics Design · 15 June 2026**

A self-contained, ~1-hour design-review presentation of the A1 hearing-loop receive-coil
amplifier, modelled on the structure of the Group-2 review and built around the supervisor's
prereview expectations (right order, options before choices, every curve and component
justified). Solo work — my name and student number only.

## Layout

```
SED_Exam_Review_Daniel_Tyukov/
├─ presentation/
│  ├─ main.tex                 # the Beamer deck (38 slides, LaTeX equations)
│  ├─ beamerthemeTUDelft.sty   # TU Delft theme (palette + logo from the official template)
│  └─ main.pdf                 # ← compiled deck (the deliverable)
├─ assets/
│  ├─ logos/                   # TU Delft logo (svg/pdf/png + white variant)
│  ├─ plots/                   # SLiCAP-driven figures (TU Delft colours, large fonts)
│  ├─ schematics/              # KiCad schematics exported via the slicap MCP
│  └─ figures/                 # system figures cropped from course PDFs
├─ data/slicap/
│  ├─ gen_values.py            # CSV → clean engineering values + numeric netlist
│  ├─ gen_plots.py             # SLiCAP doLaplace/doPZ/doNoise → the plots
│  ├─ colorize_schematic.py    # colour-coded circuit overlays
│  ├─ dualStageEKV_numeric.cir # self-contained EKV netlist (.param + .lib)
│  ├─ values.json / results_summary.json / pz_table.json  # computed data
├─ data/source/                # SLiCAP/KiCad SOURCES the deck is built from
│  ├─ cir/  csv/  lib/  kicad/  # netlists, design CSVs, libraries, schematics
│  └─ SOURCES.md               # provenance: which SLiCAP routine made each figure
├─ notes/
│  ├─ theory_notes.md          # formulas, derivations, what the review wants
│  └─ speaker_notes.md         # first-person notes to read from (humanised)
└─ course_pdfs_md/
   └─ course_pdfs_index.md     # which course PDF/page holds which figure
```

## Build the deck

```bash
cd presentation
latexmk -pdf main.tex        # → main.pdf
```
Requires a TeX Live with beamer, sourcesanspro, circuitikz, pifont, tcolorbox, pgfplots, siunitx.

## Regenerate data & figures (optional)

```bash
cd data/slicap
/home/danieltyukov/workspace/tud/slicap_env/bin/python gen_values.py   # values + netlist
/home/danieltyukov/workspace/tud/slicap_env/bin/python gen_plots.py    # figures
```
All numbers trace back to `Notebooks/csv/dualStage.csv` (the current/new pipeline — not the old
Team-12 model).

## Deck outline (8 parts, 38 slides)

1. Specification & design environment
2. Transfer function & feedback configuration
3. First stage: noise design (gₘ, c_iss, EKV)
4. Single stage & loop-gain check
5. Dual stage (PMOS pair + NMOS CS)
6. EKV model & pole-zero analysis
7. Frequency compensation (MFM phantom zero)
8. Conclusions
