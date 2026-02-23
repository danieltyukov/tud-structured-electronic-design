# Requirement specifications of the Hearing Loop EE4109
import SLiCAP as sl
from pprint import pprint

# Battery properties
batteryvoltage      = 1.4   #V
batterycurrenth     = 600   #mAh
batteryduration     = 100   #hours
# Audio signal properties
crestfactor         = 3
maxfullpowerfreq    = 5e3   #Hz
zerodBSPLvalue      = 20e-6 #Pa
# System Requirements
noiselevel          = 30    #dBSPL
peakpowerlevel      = 110   #dBSPL
flowmicrophoneinput = 20    #Hz   
fhighmicrophoneinput= 6e3   #Hz
flowhearingloop     = 600   #Hz
fhighhearingloop    = 6e3   #Hz
#Electrical Requirements
regulatedvoltage     = 0.9   #Vpp
#A1outputsignal ~= microphoneoutput
#DACoutput ~= batteryvoltage


# Add all this data to a table with specifications
# Primary Specification Categories: Interface, Power Supply, Performance (part of functional) 
# Secondary Specification Categories:  Environment, Reliability, Safety, Cost 

# create a global object to store the specifications

class specsObject:
    def __init__(self):
        self.specs = []
    def append(self, name, description, value, units, specType):
        self.specs.append(
            sl.specItem(
                name,
                description = description,
                value    = value,
                units       = units,
                specType    = specType,
            )
        )
    def getSpecs(self):
        return self.specs
    def getSpec(self, name):
        for spec in self.specs:
            pprint(vars(spec))
            if spec.description == name:
                return spec
        return None
    def getSpecValue(self, name):
        for spec in self.specs:
            if spec.SpecItem.name == name:
                return spec.value
        return None
    def getSpecUnit(self, name):
        for spec in self.specs:
            if spec.name == name:
                return spec.units
        return None

global_specs = specsObject()

global_specs.append("V_battery", "Battery voltage", batteryvoltage, "V", "Power Supply")

# Power Supply specifications
global_specs.append("I_battery", "Battery current", batterycurrenth, "mAh", "Power Supply")
global_specs.append("T_battery", "Battery duration", batteryduration, "hours", "Power Supply")
global_specs.append("V_regulated", "Battery voltage regulated", regulatedvoltage, "V", "Power Supply")

# Performance specifications
global_specs.append("Crest_factor", "Audio signal crest factor", crestfactor, "", "Performance")
global_specs.append("f_max_full_power", "Maximum full power frequency", maxfullpowerfreq, "Hz", "Performance")
global_specs.append("0dB_SPL", "Zero dB SPL value", zerodBSPLvalue, "Pa", "Performance")
global_specs.append("Noise_level", "Noise level", noiselevel, "dBSPL", "Performance")
global_specs.append("Peak_power_level", "Peak power level", peakpowerlevel, "dBSPL", "Performance")
global_specs.append("f_low_microphone_input", "Low frequency microphone input", flowmicrophoneinput, "Hz", "Performance")
global_specs.append("f_high_microphone_input", "High frequency microphone input", fhighmicrophoneinput, "Hz", "Performance")
global_specs.append("f_low_hearing_loop", "Low frequency hearing loop", flowhearingloop, "Hz", "Performance")
global_specs.append("f_high_hearing_loop", "High frequency hearing loop", fhighhearingloop, "Hz", "Performance")



sl.htmlPage("Design Requirements")
sl.specs2html(global_specs.getSpecs())

A1specs = specsObject()