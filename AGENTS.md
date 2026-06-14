# AGENTS.md — orientation for `tud-structured-electronic-design`

Start here. This repo is the **TU Delft EE4109 "Structured Electronics Design"** course
project: the design of a **hearing-loop receiver**, focused on the **A1 receive-coil
amplifier**, using SLiCAP (symbolic) + ngspice/LTspice (numeric) + Jupyter.

## TL;DR — where to work

- **Doing / changing the design?** → [`Notebooks/`](Notebooks/README.md) — the live 8-notebook
  A1 pipeline. Run order & environment: [`SETUP.md`](SETUP.md).
- **Need theory or a worked technique?** → [`EE4109-2025-2026/`](EE4109-2025-2026/README.md)
  (course reference: 14 lectures, A1/A2/A3 specs, [worked examples](EE4109-2025-2026/WORKED_EXAMPLES.md)).
- **Cross-checking design reasoning?** → [`Review_g2.md`](Review_g2.md) — a peer group's review deck.
- **Never edit / don't trust** → `EE4109-Team-12-old-model-&-sylabus-dont-use/` (superseded).

## Repository map

| Path | What it is | Use it for |
|---|---|---|
| `Notebooks/` | **Current design work** — 8-step A1 pipeline (SLiCAP + Jupyter) | ✅ primary; read its [README](Notebooks/README.md) |
| `SETUP.md` | Software setup, notebook **run order**, last-verified run | ✅ run/setup reference |
| `tools/run_hlr_notebooks.py` | Batch runner for the 8 notebooks (auto-answers prompts) | ✅ non-interactive runs |
| `EE4109-2025-2026/` | **Course reference** — lectures, specs, worked examples, PDFs | ✅ theory & examples ([README](EE4109-2025-2026/README.md), [worked examples](EE4109-2025-2026/WORKED_EXAMPLES.md)) |
| `Review_g2.md` / `Review_g2.pdf` | Peer **Group 2** review presentation (A1 design) | ✅ reference / sanity-check |
| `Structured electronics prereview notes1 of group 12.md` / `.pdf` | Group 12's prereview notes (transcribed) | ✅ design-decision context |
| `SLiCAPexamples/` | Upstream SLiCAP examples (`myFirstRCnetwork`, etc.) | ✅ SLiCAP API reference |
| `SLiCAP_book/` | "Structured Electronics Design" book sources (per-chapter `CH*/`) | ✅ textbook reference |
| `nullors_serdijn.pdf` | Serdijn nullor paper | 📄 background reading |
| `SLiCAP.ini` | Repo-root SLiCAP config | ⚙️ config |
| `site.txt` | Course-site + Team-8 site URLs | 📄 links |
| `TU Delft - Powerpoint templates/` | Slide templates for the final presentation | 📄 deliverable templates |
| `attachments/` | Empty placeholder | — |
| `.venv/` | Repo venv (SLiCAP 4.0.10, **no Jupyter**); gitignored; backs the `slicap` MCP | ⚙️ MCP/SLiCAP-only |
| `EE4109-Team-12-old-model-&-sylabus-dont-use/` | **Superseded** old Team-12 script pipeline (`hlr_*.py`) | ⛔ ignore — do not edit or cite |

## Environment & tooling

- **Canonical venv (notebooks):** `/home/danieltyukov/workspace/tud/slicap_env/`
  (Python 3.12.3, SLiCAP **4.0.10**, Jupyter). The repo `.venv/` is SLiCAP-only (no Jupyter)
  and backs the `slicap` MCP. **Keep both pinned to 4.0.10** — see `SETUP.md` §2 before upgrading.
- **SPICE / analysis MCP servers** (see the parent `../CLAUDE.md` and
  `~/tools/slicap-mcp/OPERATING_RULES.md`):
  - `slicap` MCP → symbolic small-signal (transfer, poles/zeros, noise, DC). Slash: `/analyze-slicap`.
  - `spicelib` MCP → ngspice, native netlist design/sweeps. Slash: `/design-circuit`.
  - `ltspice` MCP → existing `.asc` coursework via Wine. Slash: `/analyze-circuit`.
  - **SLiCAP returns equations; ngspice/LTspice return numbers — always verify a design numerically.**
- **Math in prose/markdown:** use **Unicode** symbols (α β gₘ σ² → ≤ ∞ …), **never LaTeX**
  `$...$`/`\frac`. Full rule list in the parent `../CLAUDE.md`.

## The design problem (one paragraph)

A1 converts the magnetic field picked up by a coil into an audio voltage for an ADC. It is a
**voltage–voltage integrator** (transfer ≈ 62.4×10³/s), driving a 10 pF ADC input, with output
noise ≤ 30 dBSPL (≈ 11.9 µV RMS) after DIN-A weighting. The design proceeds top-down:
**specification → feedback configuration → first-stage (noise-driven CS) → single-stage →
dual-stage → frequency compensation**, which is exactly the order of the `Notebooks/` pipeline.
Full specs for A1/A2/A3: [`EE4109-2025-2026/designExample/HearingLoop/index.md`](EE4109-2025-2026/designExample/HearingLoop/index.md).

## Conventions

- SLiCAP projects use a fixed layout: `cir/ csv/ img/ html/ lib/ kicad/ tex/ sphinx/ txt/`.
  `csv/` carries **design hand-off data** between notebooks; `img/` holds paired `.svg`+`.pdf`.
- Each project/example keeps its **own** `lib/` and `SLiCAP.ini`; libraries are fitted per-context
  and are **not** interchangeable (notably the several `SLiCAP_C18.lib` copies).
- `.ipynb_checkpoints/` and `__pycache__/` are caches — ignore them.
