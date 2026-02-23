import SLiCAP as sl
import sympy as sp

sl.htmlPage('System Architecture')
sl.head2html('Stage A1: Coil-to-ADC Integrator')
sl.head3html('Design Targets')
sl.text2html('The receive coil transduces the induced magnetic field into a voltage signal. This signal must interface with the ADC input, maintaining voltage-to-voltage conversion characteristics.')
sl.text2html('Type: voltage to voltage')
sl.text2html('Grounded input, grounded output')
sl.text2html('$Z_{in} = \infty$ (Ideally)')
sl.text2html('$Z_{out} = 0$ (Ideally)')
sl.text2html('$V_{out,pp} = 636$ mV')

sl.head3html('Required Transfer Function')
sl.text2html('Since the coil output is proportional to the rate of change of magnetic flux, the design requires an integrating transfer characteristic. Using microphone specifications, the required transfer is:')
sl.text2html('$\\frac{V_{out}}{V_{in}} = \\frac{62.4\cdot 10^3}{s}$')

sl.head3html('Implementation Approach')
sl.text2html('Several topologies can achieve the required integration:')
sl.img2html('transfer_impl.png',400)
sl.text2html('The single-stage three-port configuration offers advantages including superior noise performance, reduced current consumption, and smaller die area compared to four-port alternatives. The input resistance can be designed to provide the required termination.')
sl.text2html('Alternative approach: active feedback topology')

sl.head2html('Stage A2: Buffer Amplifier')
sl.text2html('type: Voltage to voltage')
sl.text2html('$V_{in,pp} = 636$ mV')
sl.text2html('$V_{out,pp} = 900$ mV')
sl.text2html('This stage amplifies the integrated signal to the ADC full-scale input for optimal resolution utilization. The modest 1.41V/V gain allows omission of this stage if the source impedance permits, trading dynamic range for area savings.')
sl.text2html('The input impedance (5.5k$\\Omega$) creates a low-pass filter with the ADC input capacitance (10pF), yielding a cutoff frequency of 2.9MHz. This exceeds the signal bandwidth, ensuring the driving capability is sufficient.')

sl.head2html('Stage A3: DAC-to-Speaker Driver')
sl.head3html('Design Targets')
sl.text2html('Voltage to voltage')
sl.text2html('Single ended to differential')
sl.text2html('The DAC output impedance (10k$\\Omega$) requires an input impedance significantly higher to minimize loading effects.')
sl.text2html('Common mode output voltage around 0V')
sl.text2html('$V_{in,pp} = 900$ mV')
sl.text2html('The required output amplitude is determined by the acoustic performance target. For an RMS voltage of 0.18V driving the loudspeaker to 109dBSPL (conservative relative to the 110dBSPL specification), the speaker voltage is:')
sl.text2html('$V_{LSP} = 10^{\\frac{110-109}{20}}0.18=0.202$ V')
sl.text2html('Including the audio signal crest factor, the peak-to-peak speaker voltage becomes: $V_{LSP,pp} = 1.21$ V, which remains below both the supply voltage and typical component ratings.')
sl.head3html('Implementation Options')
sl.img2html('A3fbType1.svg', width=600)
sl.text2html('Option 1: Achieves higher input impedance at the cost of requiring a rail-to-rail output controller')
sl.text2html('Option 2: Implements high input impedance with a standard controller that does not require rail-to-rail operation')

#V_pp_out = sp.Symbol('V_pp')
#sl.eqn2html(V_pp_out,636,units='mV')


