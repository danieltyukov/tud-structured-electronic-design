# EE4109 — Software setup & notebook run order

Status as verified on **2026-06-14**. Everything on the course "Software installation
and group exercises" list is installed and meets (or exceeds) the required versions, and
the full hearing-loop-receiver notebook pipeline runs end-to-end.

## 1. Required software — verified

| Course requirement | Required | Installed | Status |
|---|---|---|---|
| ngspice | (latest) | `ngspice-42` at `/usr/bin/ngspice` (KLU solver) | ✅ |
| KiCad | (latest) | `9.0.8` (`kicad-cli 9.0.8`) | ✅ |
| Python 3.12+ + Jupyter | ≥ 3.12 | `3.12.3` + Jupyter (nbconvert 7.16.6, IPython 9.8, ipykernel 7.1) | ✅ |
| SLiCAP 4.0.7 | ≥ 4.0.7 | **4.0.10** | ✅ exceeds |
| SLiCAP examples | clone | `SLiCAPexamples/` (incl. `myFirstRCnetwork`) | ✅ |
| MOS_EKV_BSIM | download | `EE4109-2025-2026/MOS_EKV_BSIM/` (`NMOS_lookup.ipynb`, `PMOS_lookup.ipynb`, `MOS_EKV_BSIM.py`) | ✅ |
| MOSparams | download | `EE4109-2025-2026/MOSparams/` | ✅ |

## 2. Python / SLiCAP environment

The canonical environment for this coursework is **`slicap_env/`** (at the workspace root,
`/home/danieltyukov/workspace/tud/slicap_env`):

- Python **3.12.3**, **SLiCAP 4.0.10**, Jupyter (runs the `.ipynb` notebooks).
- Run notebooks with its interpreter: `slicap_env/bin/python`, `slicap_env/bin/jupyter`.

A second venv exists at `tud-structured-electronic-design/.venv` (also SLiCAP 4.0.10, **no
Jupyter**). It is what the home `~/SLiCAP.ini` `install` path and the `slicap` MCP server
point at. Both venvs are pinned to **4.0.10** so the shared `~/SLiCAP.ini`
(`install_version = 4.0.10`) stays consistent — do **not** upgrade either to the 5.x PyPI
latest without re-validating the course circuits (see the SLiCAP operating rules below).

### SLiCAP MCP & rules (this machine)
- `slicap` MCP server: `~/tools/slicap-mcp/`, pinned **SLiCAP 4.0.10** (matches the project).
- Operating rules: `~/tools/slicap-mcp/OPERATING_RULES.md`. Slash command: `/analyze-slicap`.
- SLiCAP returns **equations** (symbolic small-signal: transfer, poles/zeros, noise budgets);
  ngspice (`spicelib` MCP) / LTspice (`ltspice` MCP) return **numbers** — verify designs numerically.

## 3. Notebook run order (continuation design of the hearing-loop receiver)

Run these in `Notebooks/` **in this order** — they form a pipeline; later notebooks read
CSV/cache artifacts written by earlier ones. Some require user input (noted below).

| # | Notebook | Purpose | Input |
|---|---|---|---|
| 1 | `specifications.ipynb` | Functional model of the amplifier with specifications | — |
| 2 | `feedbackConfig.ipynb` | Design of feedback network (transfer, noise, power dissipation) | `R_f` (R_f_min < R_f < R_f_max) |
| 3 | `feedbackConfigSimple.ipynb` | As above, simplified design approach | `R_f` (R_f_min < R_f < R_f_max) |
| 4 | `firstStageDesign.ipynb` | Design and verification of CS input stage | `B_n2` (B_n1 < B_n2 < 1) |
| 5 | `DIN_A.ipynb` | Design of an ngspice DIN A weighting filter | — |
| 6 | `singleStage.ipynb` | Design of a single-stage receive-coil amplifier | — |
| 7 | `dualStage.ipynb` | Design of a dual-stage receive-coil amplifier | — |
| 8 | `dualStageFrequencyCompensation.ipynb` | Design of the frequency compensation | — |

Data flow: `specifications → A1specs.csv → {feedbackConfig, feedbackConfigSimple} →
fb_concept.csv → {firstStageDesign, singleStage, dualStage} → dualStage.csv →
dualStageFrequencyCompensation`.

## 4. How to run them

Interactively (recommended for studying):

```bash
cd tud-structured-electronic-design/Notebooks
/home/danieltyukov/workspace/tud/slicap_env/bin/jupyter notebook
# then Run-All each notebook in the order above; answer the input() prompts
```

Non-interactively (batch, all 8 in order): use `tools/run_hlr_notebooks.py`. It executes
each notebook in place with the `slicap_env` kernel and auto-answers the 3 `input()`
prompts from the bounds the notebook computes at runtime (geometric mean for `R_f`,
midpoint for `B_n2`):

```bash
/home/danieltyukov/workspace/tud/slicap_env/bin/python tools/run_hlr_notebooks.py
```

## 5. Last verified run (2026-06-14) — all pass

| # | Notebook | Result | Time |
|---|---|---|---|
| 1 | specifications | ✅ OK | 3.9 s |
| 2 | feedbackConfig | ✅ OK | 6.5 s |
| 3 | feedbackConfigSimple | ✅ OK | 6.1 s |
| 4 | firstStageDesign | ✅ OK | 22.4 s |
| 5 | DIN_A | ✅ OK | 5.0 s |
| 6 | singleStage | ✅ OK | 5.4 s |
| 7 | dualStage | ✅ OK | 11.8 s |
| 8 | dualStageFrequencyCompensation | ✅ OK | 4.6 s |

Artifacts produced under `Notebooks/`: CSV design data (`csv/`), schematic/plot SVGs
(`img/`), and HTML reports (`html/`).
