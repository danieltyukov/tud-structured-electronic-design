#!/usr/bin/env python3
"""
gen_values.py  -- Daniel Tyukov (5714699)
Reads the SLiCAP design hand-off CSVs from the A1 notebook pipeline, evaluates the
exact (sympy) expressions to clean engineering numbers, and emits:
  - values.json                 : machine-readable {symbol: value, eng, units, desc}
  - a printed verification table
  - dualStageEKV_numeric.cir     : self-contained EKV netlist (.param + absolute .lib)
                                   ready for the slicap MCP (numeric=True, pardefs='circuit')
Run with the canonical venv:
  /home/danieltyukov/workspace/tud/slicap_env/bin/python gen_values.py
"""
import json, re, os
import sympy as sp

REPO = "/home/danieltyukov/workspace/tud/tud-structured-electronic-design"
NB   = os.path.join(REPO, "Notebooks")
OUT  = os.path.join(REPO, "SED_Exam_Review_Daniel_Tyukov", "data", "slicap")
CSV  = os.path.join(NB, "csv", "dualStage.csv")
LIB  = os.path.join(NB, "lib", "SLiCAP_C18.lib")

# ---- parse CSV -> {symbol: expr_string} ----
rows = {}
meta = {}
with open(CSV) as fh:
    next(fh)  # header
    for line in fh:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) < 5:
            continue
        sym  = parts[0].strip()
        desc = parts[1].strip().replace("&#44;", ",")
        val  = parts[2].strip()
        unit = parts[3].strip()
        typ  = parts[4].strip()
        rows[sym] = val
        meta[sym] = dict(description=desc, units=unit, type=typ)

# ---- symbolic evaluation (iterative substitution) ----
names = {n: sp.Symbol(n) for n in rows}
loc = dict(names); loc["pi"] = sp.pi; loc["f"] = sp.Symbol("f")
parsed = {}
for n, v in rows.items():
    try:
        parsed[n] = sp.sympify(v, locals=loc)
    except Exception:
        parsed[n] = None

numeric = {}
for _ in range(30):
    for n, e in parsed.items():
        if e is None or n in numeric:
            continue
        sub = e.subs({sp.Symbol(k): val for k, val in numeric.items()})
        free = sub.free_symbols
        if not free:
            try:
                numeric[n] = float(sub)
            except Exception:
                pass

def eng(x, unit=""):
    """Engineering-notation string with SI prefix."""
    if x == 0:
        return f"0 {unit}".strip()
    import math
    pref = {-15:'f',-12:'p',-9:'n',-6:'u',-3:'m',0:'',3:'k',6:'M',9:'G',12:'T'}
    sgn = "-" if x < 0 else ""
    a = abs(x)
    e3 = int(math.floor(math.log10(a)/3)*3)
    e3 = max(-15, min(12, e3))
    m = a/10**e3
    return f"{sgn}{m:.4g} {pref.get(e3,'e%d'%e3)}{unit}".strip()

# ---- emit values.json ----
data = {}
for n in rows:
    entry = dict(meta[n])
    if n in numeric:
        entry["value"] = numeric[n]
        entry["eng"]   = eng(numeric[n], "")
    else:
        entry["value"] = None
        entry["expr"]  = rows[n]
    data[n] = entry
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "values.json"), "w") as fh:
    json.dump(data, fh, indent=2)

# ---- printed verification table (curated key values) ----
key = ["tau_i","f_min","f_max","R_s","L_s","C_s","R_t","C_L","V_onoise","Vi_pp",
       "B_i1","B_n1","R_f_min","R_f_max","R_f","C_i","R_b",
       "g_mP1","g_mP2","ID1","W1","L1","ID2","W2","L2","P_max"]
print(f"{'symbol':10} {'value (eng)':>16}   description")
print("-"*78)
for n in key:
    if n in numeric:
        u = meta[n]['units'].replace('Omega','ohm')
        print(f"{n:10} {eng(numeric[n], u):>16}   {meta[n]['description'][:42]}")
print(f"\n1/tau_i = {1/numeric['tau_i']:.4g} /s  (integrator transfer constant)")

# ---- build self-contained numeric netlist for the slicap MCP ----
with open(os.path.join(NB, "cir", "dualStageEKV.cir")) as fh:
    base = fh.read()
needed = sorted(set(re.findall(r"\{(\w+)\}", base)))
param_lines = []
extra = {"T": 300.0}     # noise temperature [K] (irrelevant for transfer/PZ)
for p in needed:
    if p in numeric:
        param_lines.append(f".param {p}={numeric[p]:.6e}")
    elif p in extra:
        param_lines.append(f".param {p}={extra[p]:.6e}")
    else:
        param_lines.append(f"* MISSING PARAM {p}")
# strip the bare title line, re-add directives
body = "\n".join(l for l in base.splitlines() if l.strip() and not l.startswith(".end"))
net = ["dualStageEKV_numeric",
       f'.lib "{LIB}"',
       *param_lines,
       *[l for l in body.splitlines() if not l.startswith("dualStageEKV")],
       ".end", ""]
with open(os.path.join(OUT, "dualStageEKV_numeric.cir"), "w") as fh:
    fh.write("\n".join(net))
print(f"\nwrote values.json + dualStageEKV_numeric.cir to {OUT}")
print("params:", ", ".join(needed))
