# `Notebooks/` — current hearing-loop-receiver (A1) design pipeline

This folder is the **live design work**: the continuation design of the A1 receive-coil
amplifier for the EE4109 hearing-loop project, as a chain of 8 SLiCAP/Jupyter notebooks.
This is the code an agent should read and run when asked about "the design."

> **Run order, environment, and last-verified run live in the repo root [`SETUP.md`](../SETUP.md).**
> This README documents what each notebook *consumes and produces*, the folder conventions,
> and the helper modules — the things you need to modify the pipeline safely.

## Environment (quick reference)

- Run with the canonical venv: `/home/danieltyukov/workspace/tud/slicap_env/bin/jupyter`
  (Python 3.12.3, SLiCAP 4.0.10, Jupyter). See `SETUP.md` §2.
- Batch-run all 8 in order: `../tools/run_hlr_notebooks.py` (auto-answers the `input()` prompts).
- Local [`SLiCAP.ini`](SLiCAP.ini) pins math/plot/display settings (Laplace var `s`, SVG plots,
  4 significant digits, engineering notation). SLiCAP reads it from the project working dir.

## Pipeline & data flow

Notebooks form a chain — later notebooks read CSV artifacts written by earlier ones. **Do not
run a later notebook before its inputs exist.**

```
specifications ──▶ csv/A1specs.csv
                       │
        ┌──────────────┴───────────────┐
        ▼                               ▼
feedbackConfig                  feedbackConfigSimple
        └──────────────┬───────────────┘
                       ▼
                csv/fb_concept.csv  (+ csv/fb_concept_simple.csv)
                       │
     ┌─────────────────┼─────────────────┐
     ▼                 ▼                 ▼
firstStageDesign   singleStage        dualStage ──▶ csv/dualStage.csv
                                                        │
                                                        ▼
                                       dualStageFrequencyCompensation
```

| # | Notebook | Title in notebook | Reads | Writes |
|---|---|---|---|---|
| 1 | `specifications.ipynb` | Specifications | — | `csv/A1specs.csv` |
| 2 | `feedbackConfig.ipynb` | Feedback network design (full) | `csv/A1specs.csv` | `csv/fb_concept.csv` |
| 3 | `feedbackConfigSimple.ipynb` | Feedback network design (simplified) | `csv/A1specs.csv` | `csv/fb_concept_simple.csv` |
| 4 | `firstStageDesign.ipynb` | Controller input CS stage gₘ & c_iss (noise design) | `csv/fb_concept*.csv` | noisy-nullor `cir/`, `csv/` |
| 5 | `DIN_A.ipynb` | NGspice DIN-A weighting-filter subcircuit | — | `lib/DIN_A.lib`, `img/DIN_A_*` |
| 6 | `singleStage.ipynb` | Single-stage receive-coil amplifier | `csv/fb_concept*.csv` | `cir/singleStageSimple.cir`, `img/` |
| 7 | `dualStage.ipynb` | Dual-stage receive-coil amplifier | `csv/fb_concept*.csv` | `csv/dualStage.csv`, `cir/dualStageEKV*.cir` |
| 8 | `dualStageFrequencyCompensation.ipynb` | Frequency compensation (MFM low-pass servo) | `csv/dualStage.csv` | `cir/dualStageEKVcompensated.cir`, `img/` |

Notebooks 2 and 3 require an `R_f` input (R_f_min < R_f < R_f_max); notebook 4 requires a
`B_n2` input (B_n1 < B_n2 < 1). The batch runner fills these from the bounds each notebook
computes at runtime.

`CSstageDesignExample.ipynb` is a **standalone tutorial** ("CS stage noise design automation"),
not part of the 8-step chain — keep it but don't wire it into the pipeline.

## Folder conventions

These mirror the SLiCAP project layout (the same `cir/ csv/ img/ html/ tex/ sphinx/` set
appears in every `EE4109-2025-2026/` worked example):

| Dir | Contents |
|---|---|
| `cir/` | SLiCAP/SPICE netlists + their per-circuit `.csv` outputs (noisy-nullor, bias, feedback-concept, dual-stage, DIN-A test) |
| `csv/` | **Design hand-off data** between notebooks (`A1specs`, `fb_concept*`, `dualStage`) + bias/noisy-nullor SPICE results |
| `img/` | Generated plots & schematics as paired `.svg` + `.pdf` (gain/feedback magnitude, noisy nullors, bias, dual-stage) |
| `html/` | SLiCAP HTML reports (`*_index.html`, `*_Circuit-data.html`) + `css/`, `img/` |
| `kicad/` | KiCad sources — `A1/` (the amplifier), `Trimp/` (transimpedance test), `Libs/` (shared symbols incl. `biasN/P` schematics used by `biastest.py`) |
| `lib/` | SLiCAP/SPICE libraries — see below |
| `tex/`, `sphinx/` | LaTeX/Sphinx export scaffolding (`SLiCAPdata/`, preamble) for report generation |
| `.ipynb_checkpoints/`, `__pycache__/` | Jupyter/Python caches — ignore |

### `lib/` libraries

- `SLiCAP_C18.lib` — CMOS18 device models (EKV) for the C18 process used in this design.
  **Note:** different fitting/values than Team-12's old `C18.lib` and from
  `EE4109-2025-2026/.../SLiCAP_C18.lib` — do not assume they are interchangeable.
- `log018.l` — log/level-0.18 µm model includes.
- `noisyNullorN.lib`, `noisyNullorP.lib` — "noisy nullor" subcircuits (nullor + MOS input
  noise sources) generated for the first-stage noise design.
- `DIN_A.lib` — the DIN-A weighting-filter subcircuit produced by `DIN_A.ipynb`.

## Helper modules (`.py`)

| Module | Role |
|---|---|
| `SLiCAPmosNoise.py` | MOS noise-design automation. Defines a `process()` class (channel type, W/L bounds, finger width, gate current, noisy-nullor subcircuit name) and the symbolic noise variables used to build the noisy-nullor models. |
| `WLI.py` | Solves device geometry from targets: given `gₘ`/`c_iss` it back-solves W, L and inversion coefficient (IC) via the EKV model (`updateModel`, `WLI`). |
| `biastest.py` | **Standalone** script (not imported by the pipeline) that regenerates the `biasN/biasP` library subcircuits from `kicad/Libs/bias{N,P}.kicad_sch`. Run on its own when bias library definitions change. |

## Gotchas

- The `C_i` parameter warning during runs is **pre-existing and benign**.
- Keep both venvs pinned to SLiCAP **4.0.10** — see `SETUP.md` §2 before upgrading.
- SLiCAP returns **symbolic equations**; verify numbers with ngspice (`spicelib` MCP) or
  LTspice (`ltspice` MCP). See the root [`AGENTS.md`](../AGENTS.md) and `~/tools/slicap-mcp/OPERATING_RULES.md`.
