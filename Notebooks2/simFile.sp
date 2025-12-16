feedbackConceptNoisyNullorPspice
.inc lib/DIN_A.lib
.lib lib/log018.l TT
.inc lib/noisyNullorP.lib
C1 in 0 {C_s}
C2 out fb {C_i}
C3 out 0 {C_L}
L1 in 1 {L_s}
R1 1 2 {R_s} noisy=1
R2 in 0 {R_t} noisy=1
R3 fb 0 {R_f} noisy=1
R4 out fb {R_b} noisy=1
V1 2 0 DC 0 AC 1 0
X1 out 0 in fb noisyNullorP VGS={VGS} VDS={VDS} ID={ID} W={W} L={L} M={M}
X2 noise 0 out 0 DIN_A
** Python input section **
.param ID=1.35455409e-05
.param VDS=-0.45
.param W=3.87576707256127e-05
.param L=2.17426535566897e-7
.param M=1
.param VGS=-0.458347984
.param R_s=875.000000000000
.param C_s=9.38159107799424e-12
.param L_s=0.120000000000000
.param R_t=79971.8928868506
.param R_f=7500.00000000000
.param R_b=123862.547701198
.param C_i=2.14155322500223e-9
.param C_L=1.00000000000000e-11
.control
set wr_vecnames
set wr_singlescale
NOISE V(noise) V1 dec 20 600 6k

setplot noise1

setplot noise2
let v_no = onoise_total
wrdata cir/feedbackConceptNoisyNullorPspice.csv v_no
.endc
.end