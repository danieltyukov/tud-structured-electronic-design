import SLiCAP as sl
import sympy as sp

sl.htmlPage('Overall Design')
sl.head2html('Amplifier A1')
sl.head3html('Amplifier Specs')
sl.text2html('The receive coil converts the induced magnetic field into a voltage. The output of A1 must be matched to the microphone voltage, so the output of A1 must be voltage as well')
sl.text2html('Type: voltage to voltage')
sl.text2html('Grounded input, grounded output')
sl.text2html('$Z_{in} = \infty$ (Ideally)')
sl.text2html('$Z_{out} = 0$ (Ideally)')
sl.text2html('$V_{out,pp} = 636$ mV')

sl.head3html('Desired Transfer')
sl.text2html('The amplifier must have an integrating transfer since the induced voltage of the coil is proportional with the rate of change of the magnetic flux. Together with the specs of the microphone, the required transfer can be calculated:')
sl.text2html('$\\frac{V_{out}}{V_{in}} = \\frac{62.4\cdot 10^3}{s}$')

sl.head3html('Implementing desired transfer')
sl.text2html('Options:')
sl.img2html('transfer_impl.png',400)
sl.text2html('Option 1 allows for a design with 1 stage since it is a three-port, which can potentially perform better than a four-port in terms of noise, current and area. Furthermore, the terminiation resistance is maybe not needed since $R_i$ can be designed such that it acts like the terminiation resistance')
sl.text2html('Other option: active feedback')

sl.head2html('Amplifier A2')
sl.text2html('type: Voltage to voltage')
sl.text2html('$V_{in,pp} = 636$ mV')
sl.text2html('$V_{out,pp} = 900$ mV')
sl.text2html('Amplifier A2 is required to amplify the output of the previous stage to the maximum input of the ADC to maximize the resolution. However, the gain is only 1.41, so if the microphone is able to drive the ADC input, then the amplifier can be omitted at the cost of less dynamic range')
sl.text2html('The output impedance of the microphone is 5.5$k\Omega$ and forms a low-pass filter together with the input capacitance of 10pF of the ADC. However, the cut off frequency is 2.9MHz, so the drive capibility of the microphone is considered large enough in the required frequency range')

sl.head2html('Amplifier A3')
sl.head3html('Amplifier Specs')
sl.text2html('Voltage to voltage')
sl.text2html('Single ended to differential')
sl.text2html('DAC output impedance is 10k $\Omega$. Input impedance of A3 must be significantly higher')
sl.text2html('Common mode output voltage around 0V')
sl.text2html('$V_{in,pp} = 900$ mV')
sl.text2html('The output peak-to-peak voltage can be calculated. When driven with an RMS voltage of 0.18V, the loudspeaker generates maximally 109dBSPL (the provided answer uses 106dBSPL which is a typical value. For safety reasons we choose the maximum value). From this, the loudspeaker voltage, $V_{LSP}$ can be calculated')
sl.text2html('$V_{LSP} = 10^{\\frac{110-109}{20}}0.18=0.202$ V')
sl.text2html('When accounting for the crest factor, the loudspeaker peak to peak voltage becomes: $V_{LSP,pp} = 1.21 V$')
sl.text2html('Which is less than the value provided in the answers, and is less than the power supply. ')
sl.head3html('Possible Implementations')
sl.img2html('A3fbType1.svg', width=600)
sl.text2html('Option 1: higher input impedance, but requires rail to rail controller')
sl.text2html('Option 2: High input impedance must be selected. Controller does not have to be rail to rail')

#V_pp_out = sp.Symbol('V_pp')
#sl.eqn2html(V_pp_out,636,units='mV')


