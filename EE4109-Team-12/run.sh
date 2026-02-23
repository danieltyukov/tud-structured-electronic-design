#!/usr/bin/env bash
#
# run.sh - Execute the full EE4109 Team 12 hearing loop design pipeline
#
# This script feeds all interactive design knob parameters automatically.
# Edit the values below to explore different design tradeoffs.
#
# Usage:
#   ./run.sh          # Run with default knobs
#   ./run.sh --dry    # Print the parameter values without running
#

set -euo pipefail
cd "$(dirname "$0")"

# ============================================================================
# DESIGN KNOBS - Edit these to change the design
# ============================================================================

# Step 5 (g12feedbacknetworknoise.py): Noise budget for integrator resistor
# Constraint: 0 < N_RI < 1 - n_SRC  (~0.980)
# Higher -> more noise allowed from R_i -> larger Ri_max -> less power
# Lower  -> tighter R_i constraint -> leaves more budget for MOS
N_RI="0.2"

# Step 5 (g12feedbacknetworknoise.py): Integrator resistance value [Ohm]
# Constraint: Ri_min <= R_I <= Ri_max
#   Ri_min = V_DD / I_max = 0.9 / (P_max/2/V_DD) = 1620 Ohm
#   Ri_max depends on n_Ri (with n_Ri=0.2: ~8972, with n_Ri=0.4: ~18420)
# Larger R_i -> less power, but larger C_i
R_I="5000"

# Step 7 (g12gmciss.py): MOS type for input stage
# N = NMOS (higher f_T peak ~50GHz, more noise)
# P = PMOS (lower f_T peak ~10GHz, less noise for this application)
MOS_TYPE_GMCISS="P"

# Step 7 (g12gmciss.py): Noise budget for controller MOS input stage
# Constraint: 0 < N_M < 1 - n_SRC - n_Ri
#   With n_Ri=0.2: max ~0.781
#   With n_Ri=0.4: max ~0.581
N_M="0.5"

# Step 8 (g12WLID.py): MOS type for W/L/ID sizing (must match step 7)
MOS_TYPE_WLID="P"

# Step 8 (g12WLID.py): Maximum finger width [um]
# Constraint: 0.18 <= W_FINGER <= 50
W_FINGER="10"

# Step 8 (g12WLID.py): Channel length [um]
# Constraint: >= 0.18  (minimum for C18 technology)
# Minimum length gives maximum f_T
CHANNEL_LENGTH="0.18"

# Step 9 (g12controller.py): MOS type for controller (must match step 7)
MOS_TYPE_CTRL="P"

# ============================================================================
# EXPECTED RESULTS (with default values above)
# ============================================================================
#
#   n_SRC (auto)           = 0.01951
#   Total noise budget     = n_SRC + n_Ri + n_M = 0.72 (72%)
#   Ri_min                 = 1620 Ohm
#   Ri_max                 = 8972 Ohm
#   C_i                    = 2.728 nF
#   c_iss (optimum)        = 4.750e-13 F
#   g_m (optimum)          = 6.450e-5 S
#   W                      = 0.270 mm
#   L                      = 0.180 um
#   M (fingers)            = 27
#   ID                     = 2.30 uA
#   IC                     = 0.00560 (deep weak inversion)
#   RMS DIN-A noise        = 8.82e-6 V
#   Power conflict         = None
#
# ============================================================================

# Detect Python
VENV_PYTHON="../.venv/bin/python3"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "Warning: virtual environment not found at ../.venv/"
    echo "Trying system python3..."
    VENV_PYTHON="python3"
fi

if [ "${1:-}" = "--dry" ]; then
    echo "=== Design Knob Parameters ==="
    echo ""
    echo "  Step 5: n_Ri           = $N_RI"
    echo "  Step 5: R_i            = $R_I Ohm"
    echo "  Step 7: mosType        = $MOS_TYPE_GMCISS"
    echo "  Step 7: n_M            = $N_M"
    echo "  Step 8: mosType        = $MOS_TYPE_WLID"
    echo "  Step 8: W_finger       = $W_FINGER um"
    echo "  Step 8: Channel length = $CHANNEL_LENGTH um"
    echo "  Step 9: mosType        = $MOS_TYPE_CTRL"
    echo ""
    echo "  Noise budget: n_SRC(~0.02) + $N_RI + $N_M = $(echo "$N_RI + $N_M + 0.02" | bc)"
    echo ""
    echo "Would run: printf '...' | $VENV_PYTHON g12main.py"
    exit 0
fi

echo "=== EE4109 Team 12 - Hearing Loop Design Pipeline ==="
echo ""
echo "Design knobs:"
echo "  n_Ri           = $N_RI"
echo "  R_i            = $R_I Ohm"
echo "  mosType        = $MOS_TYPE_GMCISS"
echo "  n_M            = $N_M"
echo "  W_finger       = $W_FINGER um"
echo "  Channel length = $CHANNEL_LENGTH um"
echo ""
echo "Running pipeline..."
echo ""

printf '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' \
    "$N_RI" \
    "$R_I" \
    "$MOS_TYPE_GMCISS" \
    "$N_M" \
    "$MOS_TYPE_WLID" \
    "$W_FINGER" \
    "$CHANNEL_LENGTH" \
    "$MOS_TYPE_CTRL" \
    | "$VENV_PYTHON" g12main.py

echo ""
echo "=== Pipeline complete ==="
echo "Open html/index.html to view results."
