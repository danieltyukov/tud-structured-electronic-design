biasN
.lib lib/log018.l TT
B1 g1 0 V=0.9*(1+tanh(I(V1)))
F1 0 d1 V1 1
I2 0 d1 {ID}
M1 d1 g1 0 0 nch m={M} w={W} l={L}
V1 d1 0 {VDS}
** Python input section **
.param ID=2143038610475213/300000000000000000000
.param VDS=0.45
.param W=1e-05
.param L=1.8e-07
.param M=1
.control
set wr_vecnames
set wr_singlescale
OP
let V_D = V(d1)
let V_G = V(g1)
let I_DS = @M1[id]
let g_m2 = @M1[gm]
let c_iss2 = @M1[cgg]
wrdata cir/biasN.csv V_D V_G I_DS g_m2 c_iss2
.endc
.end