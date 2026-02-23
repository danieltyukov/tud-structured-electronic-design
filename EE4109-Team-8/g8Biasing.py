import SLiCAP as sl
import sympy as sp

sl.htmlPage('Biasing')
sl.head2html('Biasing')
sl.text2html('After finding the values for W, L and ID we can start to think about the biasing. The following values were found:')
sl.text2html('W = 18.45u')
sl.text2html('L = 0.18u')
sl.text2html('ID = 3.005uA')
sl.text2html('VDS = 636mV')
sl.text2html('From these values, $V_{GS}$ can be determined leading to the following circuit:')
sl.img2html('Biasing.png',600)

sl.head2html('Linearity')
sl.text2html('With a DC sweep on Vin, the linearity of the transistor can be checked. The output voltage is shown below when the input voltage is swept from -50mV to 50mV.')
sl.img2html('linearity.png',600)
sl.text2html('As can be seen in the plot, the curve goes through the origin. However, it is not linear across the input voltage range.')

sl.head2html('Adding extra stage')
sl.img2html('extra_stage.png', 600)
sl.img2html('extra_stage_circuit.png', 600)



