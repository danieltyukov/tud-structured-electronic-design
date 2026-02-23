import SLiCAP as sl
import sympy as sp
from g8specifications import *


sl.htmlPage('General Design - Bode plot comparions')
sl.text2html("When a MOS enters triode region, it's C_iss increases due to a 'larger channel'. In Saturation the C_iss is approximately 2/3 of C_ox")
sl.text2html("When a Mos enters triode region, it's gm decreases. In saturation the gm saturates, so dont put to much current because you dont gain gm")
sl.text2html("The Ft follows gm, because in saturation the C_iss is constant")
sl.eqn2html('f_T','g_m / (2 * pi * C_iss)')