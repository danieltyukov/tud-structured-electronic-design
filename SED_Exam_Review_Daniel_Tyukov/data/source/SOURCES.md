# Source data behind the presentation

These are the **actual SLiCAP / KiCad sources** the deck is built from — copied verbatim from
the current `Notebooks/` A1 pipeline (the *new* notebooks, not the old Team-12 model) so the
presentation is self-contained and auditable.

## What's here

| Folder | Contents |
|---|---|
| `cir/` | SLiCAP netlists: `dualStageEKV` (EKV transistor model), `dualStageEKVcompensated` (with the phantom-zero $R_{phz}$), `dualStageSimple` / `singleStageSimple` (behavioural $g_m$ models), `feedbackConcept` + `feedbackConceptNoisyNullorN18` (the concept / noisy-nullor model) |
| `csv/` | Design hand-off data: `A1specs`, `fb_concept(_simple)`, `dualStage` — the exact (sympy) values every number in the deck is derived from |
| `lib/` | SLiCAP libraries: `SLiCAP_C18.lib` (CMOS18 EKV models), `noisyNullorN/P.lib`, `DIN_A.lib`, `log018.l` |
| `kicad/` | KiCad schematics for the circuits exported as images (`A1/`, shared symbols in `Libs/`) — openable in KiCad |

## How every figure was produced (plot provenance)

All circuit plots are computed by **SLiCAP 4.0.10** running on the **actual netlists above** —
not by hand. Scripts live one level up in `../`:

| Figure | Source | SLiCAP routine |
|---|---|---|
| `fb_decomposition` | `dualStageEKV` | `doLaplace` × {gain, asymptotic, loopgain, servo, direct} |
| `gain_uncompensated` | `dualStageEKV` | `doLaplace` (gain) |
| `pole_zero_map` + tables | `dualStageEKV` | `doPZ` (gain & loopgain) |
| `compensation_mfm` + table | `dualStageEKVcompensated` | `doLaplace`/`doPZ`, $R_{phz}$ swept to MFM ($Q\to1/\sqrt2$) |
| `noise_spectrum` | `dualStageEKV` | `doNoise` + `rmsNoise` |
| `coil_damping` | coil RLC netlist (built in `gen_plots.py`) | `doLaplace` (gain), $R_t$ swept |
| `single_stage_loopgain` | course `singleStage` notebook | SLiCAP feedback-magnitude plot |
| `din_a_weighting` | SLiCAP `DIN_A()` weighting function (from `A1specs.csv`) | analytic course function |

Schematics in `../assets/schematics/` were exported from the `kicad/` files via the `slicap`
MCP (`slicap_schematic_export`); the colour-coded versions add translucent zones on top
(`../slicap/colorize_schematic.py`).

## Regenerate everything

```bash
cd ..                     # SED_Exam_Review_Daniel_Tyukov/data/slicap
PY=/home/danieltyukov/workspace/tud/slicap_env/bin/python
$PY gen_values.py         # CSV -> values.json + numeric netlist
$PY gen_plots.py          # SLiCAP -> all plots + pz_table.json
$PY colorize_schematic.py # colour-coded circuit overlays
```
