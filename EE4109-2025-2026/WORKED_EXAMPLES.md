# EE4109-2025-2026 — worked code examples & PDFs

The existing [`README.md`](README.md) and [`DOWNLOAD_SUMMARY.md`](DOWNLOAD_SUMMARY.md) describe
the **text** content downloaded from the course site (`courseWebSite/` lectures and
`designExample/` specs). This file documents the parts they omit: the **runnable worked-example
notebook folders** and the **lecture/poster PDFs** — the executable reference material an agent
should consult when implementing or checking a design technique.

> These are **instructor reference examples** (author: "anton" in the module headers), not our
> team's design. The live design work is in the repo's [`Notebooks/`](../Notebooks/README.md).
> Several of these folders are the exact course downloads named in the repo root `SETUP.md` §1
> (`MOS_EKV_BSIM/`, `MOSparams/`).

## Worked-example notebook folders

Each follows the standard SLiCAP project layout (`cir/ csv/ html/ img/ kicad/ lib/ tex/
sphinx/ txt/ mathml/`); only the entry-point notebooks/scripts are listed here.

| Folder | Topic | Entry points | Related lecture(s) |
|---|---|---|---|
| `MOS_EKV_BSIM/` | EKV vs. BSIM MOS modeling & device lookup (the course "MOS_EKV_BSIM" download) | `NMOS_lookup.ipynb`, `PMOS_lookup.ipynb`, `MOS_EKV_BSIM.py`, `extras.py` | L3 (MOS modeling) |
| `MOSparams/` | MOS parameter characterization & EKV plots (the course "MOSparams" download) | `EKVplotsN.ipynb`, `EKVplotsN/P[_V].py`, `MOSparams.py` | L3, L4 |
| `SLiCAP_python_mosEKVplots/` | Pure-Python EKV plotting (no notebook) | `EKVplots.py` | L3 |
| `CSstage/` | Common-source stage design + resistor/noise analysis | `CSstageNMOS.ipynb`, `NMOS_lookup.ipynb`, `CSstage.py`, `CSresnoise.py`, `simFile.sp` | L4 (CS stage), L5 (CS noise) |
| `CDstages/` | Common-drain (CD) follower stage | `CDstage.ipynb` | L7 (feedback stages) |
| `SLiCAP_balancing/` | Balancing: differential-pair CS (anti-series) & push-pull CS | `diff_pair_cs.ipynb`, `push_pull-cs.ipynb`, `balancing/` | L6 (balancing) |
| `CH14/` | Book Ch.14 example: dual CS-stage controller amplifiers | `dualCS.ipynb` | L8 (multi-stage), L11 |
| `LTspiceComplementaryParallel/` | LTspice (not SLiCAP) complementary-parallel CS netlist | `complParlCS.cir`, `CMOS18-0.lib`, `CMOS18-1.lib` | L6, L8 |

**Mapping to the live design:** `MOS_EKV_BSIM/` + `MOSparams/` underpin the device modeling used
throughout `Notebooks/`; `CSstage/` is the reference for `firstStageDesign.ipynb`;
`SLiCAP_balancing/` (differential pair) backs the `singleStage`/`dualStage` topology choices;
`CH14/` is the closest analogue to the full `dualStage.ipynb`.

> ⚠️ Each worked example ships its **own** `lib/` (e.g. its own `SLiCAP_C18.lib`) and local
> `SLiCAP.ini`. Library values are fitted per-example and are **not** guaranteed identical to
> `Notebooks/lib/SLiCAP_C18.lib` — keep libraries with their own example.

## `course_pdfs/` — lecture slides & posters

~30 PDFs of lecture material and posters backing the `courseWebSite/lecture*.md` notes. Grouped:

- **Intro & method:** `CourseIntro.pdf`, `PrincipleOfAmplification.pdf`, `HearingLoopIntro.pdf`,
  `SED-CMOS.pdf`, `SED-CMOS-order.pdf`, `PreferredStages.pdf`, `StagesInterconnection.pdf`,
  `LPproductStages.pdf`.
- **MOS modeling:** `mosEKVmodel.pdf`, `mosEKVmodelApplication.pdf`,
  `MOStransistorModelingAndDesignPoster.pdf`.
- **CS stage / noise:** `CSstage-intro.pdf`, `CSstage-intrinsic.pdf`,
  `FeedbackAmpCSstageNoiseDesign.pdf`.
- **Balancing:** `Balancing-intro.pdf`, `Balancing-two-terminal.pdf`, `Balancing-two-ports.pdf`,
  `Balancing-differential-pair.pdf`, `Balancing-push-pull-stage.pdf`, `posterBalancing.pdf`.
- **Feedback stages:** `FeedbackStages-intro.pdf`, `FeedbackStages-CD-stage.pdf`,
  `FeedbackStages-CG-stage.pdf`, `FeedbackStages-other.pdf`, `CDstage.pdf`, `LDRamp.pdf`,
  `AmpStagesPoster.pdf`.
- **Controller / compensation:** `ControllerDesign.pdf`, `CMOScontrollerDesignPosterPalette.pdf`.
- **Biasing:** `Biasing.pdf`, `BiasingImplementation.pdf`, `quizBiasingTechniques.pdf`.

## See also

- Repo-root [`AGENTS.md`](../AGENTS.md) — overall repo map and what to use vs. ignore.
- [`courseWebSite/index.md`](courseWebSite/index.md) — 14-lecture schedule.
- [`designExample/HearingLoop/index.md`](designExample/HearingLoop/index.md) — A1/A2/A3 specs.
