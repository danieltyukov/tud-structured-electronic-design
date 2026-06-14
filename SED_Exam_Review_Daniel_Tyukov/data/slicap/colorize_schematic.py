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
  # dual-stage EKV: colour ONLY the two stages (like Group 2's topology slide)
  "dualStageEKV.png": ("dualstage_colored.png", 60, [
      (0.255,0.485, CY), (0.625,0.815, PK)]),
  # single-stage behavioural: highlight the one amplifier stage
  "singleStageSimple.png": ("singleStageSimple_colored.png", 55, [
      (0.40,0.60, CY)]),
  # dual-stage behavioural: highlight the two gm stages
  "dualStageSimple.png": ("dualStageSimple_colored.png", 55, [
      (0.335,0.545, CY), (0.545,0.745, PK)]),
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
    for x0f, x1f, col in zones:
        d.rectangle([int(w*x0f), y0, int(w*x1f), y1], fill=col + (A,))
    out = Image.alpha_composite(im, overlay).convert("RGB")
    out.save(os.path.join(SCH, dst))
    print("wrote", dst, out.size)
