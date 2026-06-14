#!/usr/bin/env python3
"""
gen_plots.py -- Daniel Tyukov (5714699)
Generates clean, large-font, TU-Delft-coloured presentation figures for the A1
hearing-loop amplifier review, driven by authentic SLiCAP data (doLaplace/doPZ) on
the EKV dual-stage netlist, plus two analytic figures (coil damping, DIN-A weighting).

Run with the canonical venv:
  /home/danieltyukov/workspace/tud/slicap_env/bin/python gen_plots.py
Outputs -> SED_Exam_Review_Daniel_Tyukov/assets/plots/*.png  (+ a results_summary.json)
"""
import os, shutil, json, traceback
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp
import SLiCAP as sl

REPO = "/home/danieltyukov/workspace/tud/tud-structured-electronic-design"
ROOT = os.path.join(REPO, "SED_Exam_Review_Daniel_Tyukov")
OUT  = os.path.join(ROOT, "assets", "plots")
DATA = os.path.join(ROOT, "data", "slicap")
WORK = os.path.join(DATA, "_work")
NBLIB = os.path.join(REPO, "Notebooks", "lib", "SLiCAP_C18.lib")
os.makedirs(OUT, exist_ok=True)

# ----- TU Delft palette -----
BLUE="#0C2340"; CYAN="#00A6D6"; ORANGE="#EC6842"; GREEN="#6CC24A"; PINK="#EF60A3"; YELLOW="#FFB81C"; GREY="#8A8A8A"
plt.rcParams.update({
    "font.size": 15, "axes.titlesize": 16, "axes.labelsize": 15,
    "xtick.labelsize": 13, "ytick.labelsize": 13, "legend.fontsize": 12.5,
    "axes.edgecolor": "#444444", "axes.linewidth": 1.0, "figure.dpi": 130,
    "axes.grid": True, "grid.color": "#cccccc", "grid.linewidth": 0.7,
    "lines.linewidth": 2.4, "savefig.bbox": "tight", "savefig.facecolor": "white",
})
FIG = (7.6, 4.5)

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=200); plt.close(fig); print("  saved", name)

# ===== build work project =====
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(os.path.join(WORK, "cir")); os.makedirs(os.path.join(WORK, "lib"))
shutil.copy2(NBLIB, os.path.join(WORK, "lib", "SLiCAP_C18.lib"))
# uncompensated netlist with a bare .lib reference (so the project lib/ resolves it)
with open(os.path.join(DATA, "dualStageEKV_numeric.cir")) as fh:
    netu = fh.read()
import re
netu = re.sub(r'\.lib ".*?SLiCAP_C18\.lib"', ".lib SLiCAP_C18.lib", netu)
with open(os.path.join(WORK, "cir", "dual.cir"), "w") as fh:
    fh.write(netu)
# compensated netlist: same params + R_phz, phantom-zero R4 in series with load
paramblock = "\n".join(l for l in netu.splitlines() if l.startswith(".param") or l.startswith(".lib"))
with open(os.path.join(REPO, "Notebooks", "cir", "dualStageEKVcompensated.cir")) as fh:
    comp_body = fh.read()
comp_lines = [l for l in comp_body.splitlines() if not l.startswith("dualStageEKVcompensated") and l.strip() and not l.startswith(".end")]
netc = "dualc\n" + paramblock + "\n.param R_phz=1e3\n" + "\n".join(comp_lines) + "\n.end\n"
with open(os.path.join(WORK, "cir", "dualc.cir"), "w") as fh:
    fh.write(netc)

os.chdir(WORK)
sl.initProject("a1review")
s = sl.ini.laplace  # sympy symbol for s
summary = {}

def mag_db(expr, f):
    e = sp.sympify(str(expr))
    if s in e.free_symbols:
        fn = sp.lambdify(s, e, "numpy")
        H = fn(2j*np.pi*f)
    else:
        H = np.full_like(f, complex(e))
    return 20*np.log10(np.abs(H) + 1e-30), H

# ===== 1. feedback / asymptotic-gain decomposition =====
try:
    cir = sl.makeCircuit("cir/dual.cir")
    f = np.logspace(1, 8, 1000)
    curves = {}
    for t in ["gain", "asymptotic", "loopgain", "servo", "direct"]:
        r = sl.doLaplace(cir, transfer=t, lgref="Gm_M1_X2", pardefs="circuit", numeric=True)
        curves[t] = str(r.laplace)
    style = {
        "loopgain":  (ORANGE, "loop gain  $L$",          2.6, "-"),
        "asymptotic":(CYAN,   "asymptotic  $A_\\infty$", 2.4, "--"),
        "servo":     (GREEN,  "servo  $L/(1-L)$",        2.2, "-"),
        "direct":    (PINK,   "direct  $1/(1-L)$",       2.0, ":"),
        "gain":      (BLUE,   "gain (closed loop)",      3.2, "-"),
    }
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for t in ["loopgain", "asymptotic", "servo", "direct", "gain"]:
        db, _ = mag_db(curves[t], f)
        c, lab, lw, ls = style[t]
        ax.semilogx(f, db, color=c, label=lab, lw=lw, ls=ls)
    ax.axhline(0, color=GREY, lw=1.0, ls="-")
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("magnitude [dB]")
    ax.set_title("Asymptotic-gain model — every curve explained")
    ax.legend(loc="lower left", ncol=2, framealpha=0.95)
    ax.set_ylim(-60, 90)
    save(fig, "fb_decomposition.png")
except Exception:
    traceback.print_exc()

# ===== 2. closed-loop gain, wideband =====
try:
    f = np.logspace(1, 9, 1600)
    db, H = mag_db(curves["gain"], f)
    pass_db = np.median(db[(f > 1e3) & (f < 3e3)])
    fig, ax = plt.subplots(figsize=FIG)
    ax.semilogx(f, db, color=BLUE, lw=2.8)
    ax.axhline(pass_db - 3, color=GREY, ls=":", lw=1.3)
    ax.text(15, pass_db - 3 + 2, "$-3$ dB", color=GREY, fontsize=11)
    ax.axvspan(600, 6000, color=YELLOW, alpha=0.16)
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("magnitude [dB]")
    ax.set_title("EKV dual-stage closed-loop gain")
    save(fig, "gain_uncompensated.png")
    summary["passband_dB"] = float(pass_db)
except Exception:
    traceback.print_exc()

# ===== 3. pole-zero map (loop gain + closed loop), axes in Hz (symlog) =====
def _cl(roots):
    return [complex(sp.N(r)) for r in roots]
def _hz(c):
    return complex(c.real/2/np.pi, c.imag/2/np.pi)
try:
    rlg = sl.doPZ(cir, transfer="loopgain", lgref="Gm_M1_X2", pardefs="circuit", numeric=True)
    rg  = sl.doPZ(cir, transfer="gain",     lgref="Gm_M1_X2", pardefs="circuit", numeric=True)
    lp, lz = _cl(rlg.poles), _cl(rlg.zeros)
    gp, gz = _cl(rg.poles),  _cl(rg.zeros)
    ph = [_hz(p) for p in gp]; zh = [_hz(z) for z in gz]
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.scatter([p.real for p in ph], [p.imag for p in ph], marker="x", s=180,
               color=BLUE, lw=3, label="poles", zorder=3)
    if zh:
        ax.scatter([z.real for z in zh], [z.imag for z in zh], marker="o", s=140,
                   facecolors="none", edgecolors=ORANGE, lw=2.6, label="zeros", zorder=3)
    ax.set_xscale("symlog", linthresh=1e3); ax.set_yscale("symlog", linthresh=1e3)
    ax.axvline(0, color=GREY, lw=1.4); ax.axhline(0, color=GREY, lw=1.0)
    ax.axvspan(ax.get_xlim()[0], 0, color=GREEN, alpha=0.06)
    ax.set_xlabel("Re  [Hz]"); ax.set_ylabel("Im  [Hz]")
    ax.set_title("Closed-loop poles ($\\times$) & zeros ($\\circ$) — all in LHP → stable")
    ax.legend(loc="upper left")
    save(fig, "pole_zero_map.png")
    summary["n_poles"] = len(gp); summary["n_zeros"] = len(gz)
    summary["closedloop_poles_fn_hz"] = sorted(abs(p)/2/np.pi for p in gp)
    summary["closedloop_Q"] = sorted(abs(p)/(2*abs(p.real)) for p in gp if p.imag > 1 and p.real != 0)
    cpx = sorted([p for p in lp if abs(p.imag) > 1], key=lambda p: abs(p.imag))
    if cpx:
        pp = cpx[-1]; summary["hf_pair_fn_MHz"] = abs(pp)/2/np.pi/1e6
        summary["hf_pair_Q"] = abs(pp)/(2*abs(pp.real)) if pp.real else None
    summary["loopgain_poles_fn_hz"] = sorted(abs(p)/2/np.pi for p in lp)
except Exception:
    traceback.print_exc()

# ===== 4. frequency compensation: phantom zero tuned to MFM (Q -> 1/sqrt2) =====
def _hfQ(poles):
    cpx = [complex(sp.N(p)) for p in poles if abs(complex(sp.N(p)).imag) > 1]
    if not cpx:
        return None, None
    pp = max(cpx, key=lambda p: abs(p))            # highest-frequency complex pair
    Q = abs(pp)/(2*abs(pp.real)) if pp.real else None
    return Q, abs(pp)/2/np.pi
try:
    circ = sl.makeCircuit("cir/dualc.cir")
    target = 1/np.sqrt(2)
    sweep = []
    for rphz in np.logspace(2, 5, 40):
        circ.defPar("R_phz", float(rphz))
        rp = sl.doPZ(circ, transfer="gain", lgref="Gm_M1_X2", pardefs="circuit", numeric=True)
        Q, fn = _hfQ(rp.poles)
        if Q is not None:
            sweep.append((float(rphz), float(Q), float(fn)))
    rphz, Qc, fnc = min(sweep, key=lambda t: abs(t[1]-target))
    circ.defPar("R_phz", float(rphz))
    rr = sl.doLaplace(circ, transfer="gain", lgref="Gm_M1_X2", pardefs="circuit", numeric=True)
    f = np.logspace(3, 8.7, 1600)                 # 1 kHz .. 500 MHz (shows the HF peak)
    db_u, _ = mag_db(curves["gain"], f)
    db_c, _ = mag_db(str(rr.laplace), f)
    Qu = summary.get("closedloop_Q", [None])[-1]
    summary["R_phz_ohm"] = float(rphz); summary["compensated_Q"] = float(Qc)
    fig, ax = plt.subplots(figsize=FIG)
    ax.semilogx(f, db_u, color=ORANGE, lw=2.4, ls="--",
                label=f"uncompensated  (Q$\\approx${Qu:.1f})" if Qu else "uncompensated")
    ax.semilogx(f, db_c, color=BLUE, lw=3.0,
                label=f"compensated MFM  (Q$\\approx${Qc:.2f}, $R_{{phz}}\\approx${rphz/1e3:.1f}k$\\Omega$)")
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("magnitude [dB]")
    ax.set_title("Phantom-zero compensation → maximally-flat magnitude")
    ax.legend(loc="lower left")
    save(fig, "compensation_mfm.png")
except Exception:
    traceback.print_exc()

# ===== 5. analytic: pick-up coil damping (no R_t / under / critical) =====
try:
    Ls, Rs, Cs = 0.12, 875.0, 9.381591e-12
    Rt_crit = 79971.89
    f = np.logspace(3, 7, 1400); w = 2*np.pi*f
    def coil_mag(Rt):
        # transfer V_node/I_in into the parallel R_t || C_s, fed through series L_s+R_s
        ZC = 1/(1j*w*Cs); ZL = 1j*w*Ls
        Zpar = 1/(1/Rt + 1/ZC) if Rt != np.inf else ZC
        H = Zpar/(ZL + Rs + Zpar)
        return 20*np.log10(np.abs(H))
    fig, ax = plt.subplots(figsize=FIG)
    ax.semilogx(f, coil_mag(np.inf),      color=ORANGE, lw=2.6, label="no $R_t$ (undamped)")
    ax.semilogx(f, coil_mag(Rt_crit*6),   color=GREEN,  lw=2.2, ls="--", label="light damping")
    ax.semilogx(f, coil_mag(Rt_crit),     color=BLUE,   lw=3.0, label="critical ($R_t\\approx$80 k$\\Omega$)")
    ax.axvline(150e3, color=GREY, lw=1.2, ls=":")
    ax.text(150e3*1.1, ax.get_ylim()[1]-6, "$f_{res}\\approx$150 kHz", color=GREY, fontsize=12)
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("magnitude [dB]")
    ax.set_title("Pick-up coil resonance & termination damping")
    ax.legend(loc="lower left")
    save(fig, "coil_damping.png")
except Exception:
    traceback.print_exc()

# ===== 6. analytic: DIN-A weighting curve =====
try:
    f = np.logspace(1, 5, 1400)
    DINA = (18719114681919*f**4 /
            (100000*np.sqrt((f**2 + 1159929/100)*(f**2 + 54449641/100))*(f**2 + 10609/25)*(f**2 + 148693636)))
    fig, ax = plt.subplots(figsize=FIG)
    ax.semilogx(f, 20*np.log10(DINA), color=CYAN, lw=3.0)
    ax.axvline(1000, color=GREY, lw=1.2, ls=":")
    ax.text(1100, -3, "0 dB @ 1 kHz", color=GREY, fontsize=12)
    ax.axvspan(600, 6000, color=YELLOW, alpha=0.18, label="audio band 0.6–6 kHz")
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("weighting [dB]")
    ax.set_title("DIN-A perceptual noise weighting")
    ax.legend(loc="lower center"); ax.set_ylim(-50, 5)
    save(fig, "din_a_weighting.png")
except Exception:
    traceback.print_exc()

# ===== 7. output noise spectrum (raw + DIN-A weighted) =====
try:
    rn = sl.doNoise(cir, pardefs="circuit", numeric=True)
    onoise = sp.sympify(str(rn.onoise)).evalf()   # float coeffs (avoid huge-int overflow)
    fsyms = list(onoise.free_symbols)
    fvar = fsyms[0] if fsyms else sp.Symbol("f")
    f = np.logspace(1, 7, 1400)
    So = np.asarray([float(onoise.subs(fvar, x)) for x in f], dtype=float)   # V^2/Hz
    Sv = np.sqrt(np.abs(So)) * 1e9                                        # nV/sqrtHz
    DINA = (18719114681919*f**4 /
            (100000*np.sqrt((f**2 + 1159929/100)*(f**2 + 54449641/100))*(f**2 + 10609/25)*(f**2 + 148693636)))
    fig, ax = plt.subplots(figsize=FIG)
    ax.loglog(f, Sv, color=ORANGE, lw=2.2, ls="--", label=r"output noise $\sqrt{S_o}$")
    ax.loglog(f, Sv*DINA, color=BLUE, lw=2.8, label="DIN-A weighted")
    ax.axvspan(600, 6000, color=YELLOW, alpha=0.18, label="audio band")
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel(r"noise density [nV/$\sqrt{\mathrm{Hz}}$]")
    ax.set_title("Output noise spectrum")
    ax.legend(loc="best")
    save(fig, "noise_spectrum.png")
    try:
        summary["rms_onoise_V"] = float(sp.N(sl.rmsNoise(rn, "onoise", 1, 1e5)))
    except Exception:
        pass
except Exception:
    traceback.print_exc()

with open(os.path.join(DATA, "results_summary.json"), "w") as fh:
    json.dump(summary, fh, indent=2, default=str)
print("\nSUMMARY:", json.dumps(summary, indent=2, default=str))
