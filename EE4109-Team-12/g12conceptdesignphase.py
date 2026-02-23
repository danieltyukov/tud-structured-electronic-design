import SLiCAP as sl
import sympy as sp

from SLiCAP import htmlPage, head2html, text2html
from g12specifications import global_specs

htmlPage('General Design - Concept Design Phase')

head2html('Amplifier Design A1')
text2html('We fully agree with the tranfer function given by the solutions')

head2html('Amplifier Design A1 - type')
text2html('A1 needs to be voltage to voltage, because the microphone is voltage and the induced electic field is a voltage from the coil.')
text2html('The amplifier needs to have an high input impedance, because its a voltage to voltage and you want all the voltage on the input (series input sensing) and dont want to load the coil.')
text2html('The output inpedance needs to be as low as possible so there is no voltage drop on the Zout and all the voltage is on the load.')
text2html('It needs common mode as the differential mode is more costly to design in terms of noise performance and noise. There is no need for differential mode so it is avoided. Only if there is enough interference in the wire between the pickup coil and the amplifier it might need to be reconsidered, but we assume this is not the case for now.')


head2html('Amplifier Design A1 - structure')
sl.img2html('A1 - Three port.jpeg', width=400)
text2html('We are looking at into the possibility to use a different topology for the amplifier then the solutions. The tought process is to see if it is possible to have a three port configuation which can perform similar or even better compared to Antons 4 port controller design.')
text2html('You have a voltage at the output of the coil. We nullify this difference to gound and provide the axis of freedom at the output with norrator. In opamp speak, current form the coil get into the cap, which gets integrated and inverted to the output as a voltage.')
text2html('We think this design might be better as it is three terminal, so it needs less transistors so less noise')


# TODO Check if R_i can be adjusted or if it is fixed and only can change C_i
text2html('')


text2html('Potential question: is there a problem with the resonant frequency which we have to keep in mind?')
text2html('theoretical awnser: no, because resonent frequency peak would increase thevenin equivalent impedance which would shift the voltage from the Ri to Rsource which will kill the gain.')
# TODO Skip: equivalent thevenin source voltage

text2html('potential question: Anton has put in a termination resistance which we dont yet know why')
text2html('potential awnser: we dont know if we need one in this design')

# -Vs/R * 1/(sC) = Vo
# 2x 1/(sRC) = Ax2

# TODO: Make LTSpice model so we can test the circuit in SLiCAP

# TODO: Phantom zero?

text2html('Q: Why did anton choose the 10k terminator resistor and not a 113k as this is the intersection to fix resonance?')
text2html('A: 10k is choosen as something with a pole or zero with source')


# optional TODO: add active feedback


head2html('Amplifier Design A2')
text2html('We agree with that as the amplifier needs an amplification of 1.4 we can just use a wire instead of designing an amplifier')
text2html('Q: The value is not 1 so why can you use a wire?')
# TODO: Add the answer here
text2html('A: ')

head2html('Amplifier Design A3')
head2html('Amplifier Design A3 - type')



text2html('We have a different number as we have a different specification for the amplifier, so we have a different conclusion to the awnser model. This is because they used the value at 1kHz, but the peak is at 2.5kHz which there the peak is 109 dBSPL (which is the max value instead of the typical). This is what we would like to discuss with the client, we would like to take the max to protect the ears')
# TODO: add equation with 109 dBSPL (10^((110-109)/20) * 0.18 = ...)
text2html('Since the desired max voltage level of loudspeaker is 1.21 volt, which is below is below the maximum battery voltage of 1.4. Compared to the awnser model, we dont have to do the trick with the doubling voltage of the battery as it is unncecessary.')
# Optional TODO: add what we would have done if the voltage was higher than 1.4 volt (full bridge amplifier for example)

text2html('This gives the different values which are')
text2html('1.21 at the output')
# TODO: make formula with our values


sl.img2html('A3fbType1.svg', width=800)
text2html('We would like to use A and it is theoraticly possible, but as the input signal is to close to a rail to rail voltage it is impractical to do it with a single transistor source follower, which leads us to also use B.')

text2html('Q: why do we take a crest factor of 3')
text2html('A: It is in the specs and its a usual value for audio signals.')

head2html('Circuit slicap simulations')
text2html('The pole of the resonance resistance is the least dominant.')

text2html('Our amplifier design needs a massive resistor')
text2html('What are the benifits of our design?')
text2html('Much lower power, since we can do it with a 3-terminal device which can be implemented with a single transistor, in stead of a differential stage')
text2html('Using a differential pair requires 4 times the current for the same noise.')

text2html('Where does the noise budget come from?')
text2html('The output noise specification is 30 dBSPL, which is approximately 10 uV. The gain of the total system is 2, since the maximum output voltage of the microphone is 636 mV.')
text2html('Therefore, the noise budget at the output of A1 is half of the total output noise budget: 5 uV.')

text2html('Since the input impedance of the amplifier in our configuration is not infinite, the impedance of the source/coil does influence the tranferfunction to the output. This effect has to be taken into account')
text2html('The impedance of the source/coil is flat until 4kHz and increases above. As a result, the desired gain drops. However, the maximum full power frequency is 5kHz.')

head2html('EUREKA')

text2html('After looking deeper it is easier than we initially thought. The noise budget of 30 dBSPL is calculated as the output of A1. This is because the 30dBSPL is the noise floor of the microphone and we are trying to match this with the microphone. The electrical noise of the microphone is the sensitivity times the noise floor of the system requirement which in the linear domain or plus in the dB domain. This gives the following equation:')
# V_noise         = 20E-6 * 10**((mic_dB_Pa + SPL_noise)/20)
vnoise = sp.Symbol('V_noise')
mic_dB_Pa = -35.5
SPL_noise = 30
eq = 20E-6 * 10**((mic_dB_Pa + SPL_noise)/20)
sl.eqn2html('V_noise', eq, 'V')

