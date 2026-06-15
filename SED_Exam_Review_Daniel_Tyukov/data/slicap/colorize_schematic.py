#!/usr/bin/env python3
"""
colorize_schematic.py -- Daniel Tyukov (5714699)
Overlays translucent TU-Delft-coloured zones behind the labelled blocks of a SLiCAP
schematic PNG, so the audience's eye is guided to each functional block (and Antoon/Chris
have fewer "what is this part?" questions). The schematics already carry the block labels,
so this only adds the colour bands.
"""
import os
from PIL import Image, ImageDraw

SCH = "/home/danieltyukov/workspace/tud/tud-structured-electronic-design/SED_Exam_Review_Daniel_Tyukov/assets/schematics"

# TU Delft palette (light tints used so the circuit stays readable)
CY=(0,166,214); PK=(239,96,163); OR=(236,104,66); YE=(255,184,28); GR=(108,194,74); GY=(150,150,165)

JOBS = {
  # circuit-model concept: colour every block (coil|termination|amp|feedback|load|noise)
  "feedbackConceptNoisyNullorN18.png": ("circuit_model_colored.png", 52, [
      (0.00,0.165, CY), (0.165,0.30, OR), (0.30,0.515, GR),
      (0.515,0.685, YE), (0.685,0.815, PK), (0.815,1.00, GY)]),
  # dual-stage EKV: all five blocks; the two stages (cyan/pink) kept prominent, the rest light.
  # per-zone alpha as optional 4th element.
  "dualStageEKV.png": ("dualstage_colored.png", 60, [
      (0.00,0.255, GY, 30), (0.255,0.485, CY, 64), (0.485,0.625, YE, 36),
      (0.625,0.815, PK, 64), (0.815,1.00, GR, 36)]),
  # single-stage behavioural: colour every block (matches the slide-10 roadmap scheme,
  # and the speaker note that walks coil -> termination -> amplifier -> feedback -> load)
  "singleStageSimple.png": ("singleStageSimple_colored.png", 48, [
      (0.00,0.255, CY), (0.255,0.385, OR), (0.385,0.605, GR),
      (0.605,0.795, YE), (0.795,1.00, PK)]),
  # dual-stage behavioural: all five blocks (note: feedback sits AFTER the 2nd stage here).
  # stages (cyan/pink) bold; coil/feedback/load light.
  "dualStageSimple.png": ("dualStageSimple_colored.png", 55, [
      (0.00,0.28, GY, 30), (0.28,0.55, CY, 60), (0.55,0.715, PK, 60),
      (0.715,0.845, YE, 38), (0.845,1.00, GR, 36)]),
}

def on_white(img):
    """Flatten a (possibly transparent) RGBA image onto a white background."""
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, img)

# flatten the plain schematics used directly in the deck onto white too
for f in ("dualStageEKV.png", "feedbackConceptNoisyNullorN18.png", "noisyNullorN.png",
          "singleStageSimple.png", "dualStageSimple.png"):
    p = os.path.join(SCH, f)
    if os.path.exists(p):
        on_white(Image.open(p).convert("RGBA")).convert("RGB").save(p)
        print("flattened", f)

for src, (dst, A, zones) in JOBS.items():
    im = on_white(Image.open(os.path.join(SCH, src)).convert("RGBA"))  # white first → no black
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    y0, y1 = int(h*0.10), int(h*0.99)
    for z in zones:
        x0f, x1f, col = z[0], z[1], z[2]
        a = z[3] if len(z) > 3 else A
        d.rectangle([int(w*x0f), y0, int(w*x1f), y1], fill=col + (a,))
    out = Image.alpha_composite(im, overlay).convert("RGB")
    out.save(os.path.join(SCH, dst))
    print("wrote", dst, out.size)
