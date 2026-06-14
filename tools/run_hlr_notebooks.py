#!/usr/bin/env python
"""Execute the 8 hearing-loop-receiver design notebooks in the course-specified
order, in-place, auto-answering the 3 interactive input() prompts from the
real bounds computed at runtime."""
import os, time, traceback
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

NB_DIR = "/home/danieltyukov/workspace/tud/tud-structured-electronic-design/Notebooks"
os.chdir(NB_DIR)
os.environ["MPLBACKEND"] = "Agg"

ORDER = [
    "specifications", "feedbackConfig", "feedbackConfigSimple",
    "firstStageDesign", "DIN_A", "singleStage", "dualStage",
    "dualStageFrequencyCompensation",
]
INTERACTIVE = {"feedbackConfig", "feedbackConfigSimple", "firstStageDesign"}

AUTO_INPUT_SRC = r'''# [auto-input shim injected by setup runner]
import builtins as _b, sympy as _sp
def _auto_input(prompt=""):
    sd = globals().get("spec_dict", {})
    def _f(x):
        try: return float(_sp.N(x.value))
        except Exception: return float(_sp.N(x))
    val = None
    if "R_f" in prompt and "R_f_min" in sd and "R_f_max" in sd:
        lo, hi = _f(sd["R_f_min"]), _f(sd["R_f_max"]); val = (lo * hi) ** 0.5
    elif "B_n2" in prompt and "B_n1" in sd:
        val = (_f(sd["B_n1"]) + 1.0) / 2.0
    if val is None:
        val = 0.5
    print(prompt, "->", val, "[auto-answered]")
    return str(val)
# Define `input` as a notebook-global so bare input() in later cells resolves
# here (LEGB: global beats builtins) regardless of ipykernel's stdin patching.
input = _auto_input
_b.input = _auto_input
'''

results = []
for name in ORDER:
    path = f"{name}.ipynb"
    nb = nbformat.read(path, as_version=4)
    injected = name in INTERACTIVE
    if injected:
        nb.cells.insert(0, nbformat.v4.new_code_cell(AUTO_INPUT_SRC))
    client = NotebookClient(
        nb, timeout=1800, kernel_name="python3", allow_errors=False,
        resources={"metadata": {"path": NB_DIR}},
    )
    t0 = time.time()
    status, err = "OK", ""
    try:
        client.execute()
    except CellExecutionError as e:
        status, err = "FAILED", str(e).strip().splitlines()[-1][:400]
    except Exception as e:
        status, err = "FAILED", f"{type(e).__name__}: {e}"[:400]
        traceback.print_exc()
    dt = time.time() - t0
    if injected:
        nb.cells.pop(0)  # keep the saved notebook clean
    nbformat.write(nb, path)
    results.append((name, status, dt, err))
    print(f"[{status}] {name}  ({dt:.1f}s)  {err}", flush=True)
    if status == "FAILED":
        print(f"  -> stopping pipeline; {name} is a dependency for later notebooks", flush=True)
        break

print("=" * 70)
for name, status, dt, err in results:
    print(f"{status:7} {name:34} {dt:7.1f}s {err}")
