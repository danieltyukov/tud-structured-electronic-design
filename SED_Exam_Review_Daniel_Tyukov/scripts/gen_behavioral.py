#!/usr/bin/env python3
"""
Generate the BEHAVIOURAL-flow SLiCAP data + plots for the A1 hearing-loop review:
  1. Coil self-resonance, with / without termination resistor R_t  (Bode magnitude)
  2. Ideal integrator (nullor V-V amplifier) transfer + pole-zero
  3. Source + termination noise spectrum and DIN-A weighted RMS / source fraction

All plots are saved as SVG (SLiCAP native) and converted to PNG for the slides.
Numeric results are dumped to data/slicap_results_behavioral.json.
"""
import os, shutil, json, math, sys

HERE   = os.path.abspath(os.path.dirname(__file__))
ROOT   = os.path.abspath(HERE + "/..")
WORK   = os.path.join(ROOT, "data", "slicap_work")
CIRSRC = os.path.join(ROOT, "data", "cir")
PLOTS  = os.path.join(ROOT, "assets", "plots")
LIBSRC = "/home/danieltyukov/workspace/tud/tud-structured-electronic-design/EE4109-Team-12-old-model-&-sylabus/lib/C18.lib"

os.makedirs(WORK, exist_ok=True)
os.makedirs(CIRSRC, exist_ok=True)
os.makedirs(PLOTS, exist_ok=True)
os.chdir(WORK)

import SLiCAP as sl
sl.initProject("A1_review")
# make the technology library available to the project
for d in ("cir", "lib"):
    os.makedirs(d, exist_ok=True)
shutil.copy(LIBSRC, os.path.join("cir", "C18.lib"))
try:
    shutil.copy(LIBSRC, os.path.join("lib", "C18.lib"))
except Exception:
    pass

results = {}

def write_cir(name, text):
    """Write a .cir both to the working cir/ dir and to the deliverable data/cir/."""
    p = os.path.join("cir", name)
    with open(p, "w") as f:
        f.write(text)
    with open(os.path.join(CIRSRC, name), "w") as f:
        f.write(text)
    return p

def svg2png(stem, width=1100):
    """Convert SLiCAP's img/<stem>.svg to assets/plots/<stem>.png via the MCP venv cairosvg."""
    src = os.path.join("img", stem + ".svg")
    dst = os.path.join(PLOTS, stem + ".png")
    if os.path.exists(src):
        import subprocess
        subprocess.run(["/home/danieltyukov/tools/slicap-mcp/.venv/bin/python", "-c",
                        f"import cairosvg; cairosvg.svg2png(url={src!r}, write_to={dst!r}, output_width={width}, background_color='white')"],
                       check=False)
        return os.path.exists(dst)
    return False

# ----------------------------------------------------------------------------
# 1. COIL + TERMINATION  -----------------------------------------------------
# ----------------------------------------------------------------------------
coil = """"Coil and termination"
.source V1
.detector V_in
.param L_s=120m R_s=875 f_res=150k C_s={1/(L_s*4*pi^2*f_res^2)} R_t=79.97k
V1 1 0 V value=1 dc=0 noise=0 dcvar=0
L1 1 2 L value={L_s} iinit=0
R1 2 in R value={R_s} noisetemp=0 noiseflow=0 dcvar=0 dcvarlot=0
C1 in 0 C value={C_s} vinit=0
R2 in 0 R value={R_t} noisetemp=0 noiseflow=0 dcvar=0 dcvarlot=0
.end
"""
p = write_cir("01_coil.cir", coil)
cir = sl.makeCircuit(p)
Cs = float(sl.fullSubs(sl.sp.sympify("1/(L_s*4*pi**2*f_res**2)"), {sl.sp.Symbol('L_s'):0.12, sl.sp.Symbol('f_res'):150e3}))
results["C_s_F"] = Cs
results["f_res_Hz"] = 150e3
# damped (R_t = 79.97k)
g_damped = sl.doLaplace(cir, pardefs="circuit", numeric=True)
# undamped (R_t huge)
cir.defPar("R_t", 1e12)
g_open = sl.doLaplace(cir, pardefs="circuit", numeric=True)
g_open.label = "no termination (R_t=inf)"
g_damped.label = "with R_t = 79.97 k (Q=1/sqrt2)"
fig = sl.plotSweep("coil_termination", "Coil self-resonance: effect of termination R_t",
                   [g_open, g_damped], 1e3, 1e6, 300, funcType="dBmag", show=False)
svg2png("coil_termination")
print("[1] coil termination done; C_s =", Cs)

# critical damping R_t
Rt_crit = 1/(math.sqrt(2) * 2*math.pi*150e3*Cs)
results["R_t_crit_ohm"] = Rt_crit
print("    R_t critical =", Rt_crit)

# ----------------------------------------------------------------------------
# 2. IDEAL INTEGRATOR (nullor V-V) -------------------------------------------
# ----------------------------------------------------------------------------
integ = """"Ideal integrator A1 (nullor)"
.source V1
.detector V_out
.param L_s=120m R_s=875 f_res=150k C_s={1/(L_s*4*pi^2*f_res^2)} R_t=79.97k
.param A_v1=62.4e3 tau_i={1/A_v1} R_i=1.6k C_i={tau_i/R_i}
V1 1 0 V value=1 dc=0 noise=0 dcvar=0
L1 1 2 L value={L_s} iinit=0
R1 2 in R value={R_s} noisetemp=0 noiseflow=0 dcvar=0 dcvarlot=0
C1 in 0 C value={C_s} vinit=0
R2 in 0 R value={R_t} noisetemp=0 noiseflow=0 dcvar=0 dcvarlot=0
R3 in 3 R value={R_i} noisetemp=0 noiseflow=0 dcvar=0 dcvarlot=0
C2 3 out C value={C_i} vinit=0
N1 out 0 3 0 N
.end
"""
p = write_cir("02_integrator.cir", integ)
cir = sl.makeCircuit(p)
gain = sl.doLaplace(cir, pardefs="circuit", numeric=True)
results["integrator_laplace"] = str(gain.laplace)
fig = sl.plotSweep("integrator_mag", "Ideal A1 integrator: magnitude",
                   gain, 1e2, 1e6, 300, funcType="dBmag", show=False)
svg2png("integrator_mag")
figp = sl.plotSweep("integrator_phase", "Ideal A1 integrator: phase",
                    gain, 1e2, 1e6, 300, funcType="phase", show=False)
svg2png("integrator_phase")
pz = sl.doPZ(cir, pardefs="circuit", numeric=True)
try:
    results["integrator_poles"] = [str(x) for x in pz.poles]
    results["integrator_zeros"] = [str(x) for x in pz.zeros]
    results["integrator_dcgain"] = str(pz.DCvalue)
except Exception as e:
    results["integrator_pz_err"] = str(e)
print("[2] integrator done; H(s) =", gain.laplace)

# ----------------------------------------------------------------------------
# 3. SOURCE + TERMINATION NOISE ----------------------------------------------
# ----------------------------------------------------------------------------
noise = """"Source and termination noise"
.source V1
.detector V_out
.param L_s=120m R_s=875 f_res=150k C_s={1/(L_s*4*pi^2*f_res^2)} R_t=79.97k
.param A_v1=62.4e3 tau_i={1/A_v1} R_i=1.6k C_i={tau_i/R_i}
V1 1 0 V value=1 dc=0 noise=0 dcvar=0
L1 1 2 L value={L_s} iinit=0
R1 2 in R value={R_s} noisetemp={T} noiseflow=0 dcvar=0 dcvarlot=0
C1 in 0 C value={C_s} vinit=0
R2 in 0 R value={R_t} noisetemp={T} noiseflow=0 dcvar=0 dcvarlot=0
R3 in 3 R value={R_i} noisetemp={T} noiseflow=0 dcvar=0 dcvarlot=0
C2 3 out C value={C_i} vinit=0
N1 out 0 3 0 N
.param T=300
.end
"""
p = write_cir("03_noise.cir", noise)
cir = sl.makeCircuit(p)
noiseres = sl.doNoise(cir, pardefs="circuit", numeric=True)
try:
    onoise = noiseres.onoise
    fig = sl.plotSweep("noise_onoise", "Output-referred noise spectral density",
                       noiseres, 20, 6e3, 300, funcType="onoise", show=False)
    svg2png("noise_onoise")
    rms = sl.rmsNoise(noiseres, "onoise", 20, 6e3)
    results["rms_onoise_20_6k"] = str(rms)
    print("[3] noise done; RMS onoise (20Hz-6kHz) =", rms)
except Exception as e:
    results["noise_err"] = str(e)
    print("[3] noise error:", e)

with open(os.path.join(ROOT, "data", "slicap_results_behavioral.json"), "w") as f:
    json.dump(results, f, indent=2, default=str)
print("\nDONE. results ->", os.path.join(ROOT, "data", "slicap_results_behavioral.json"))
print("plots ->", PLOTS)
print(json.dumps(results, indent=2, default=str)[:1500])
