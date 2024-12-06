# most of the drivers only need a couple of these... moved all up here for clarity below
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import (
        Unpack,  # can be imported from typing if python >= 3.12
    )

from qcodes import validators as vals
from qcodes.instrument import (
    Instrument,
    VisaInstrument,
    VisaInstrumentKWArgs,
)
from qcodes.parameters import Parameter
from qcodes.validators import Enum, Ints, MultiType, Numbers

class Keithley6221(VisaInstrument):
    """Instrument Driver for Keithley6221"""

    default_terminator = "\r\n"

    def __init__(
        self,
        name: str,
        address: str,
        reset: bool = False,
        **kwargs: "Unpack[VisaInstrumentKWArgs]",
    ):

        """initial
        """
        super().__init__(name, address, **kwargs)


        self.output: Parameter = self.add_parameter(
            "output",
            get_cmd="OUTP:STAT?",
            set_cmd="OUTP:STAT {}",
            vals = Enum("ON", "OFF", "0", "1")
        )

        self.dc_amplitude: Parameter = self.add_parameter(
            "dc_amplitude",
            get_cmd="SOUR:CURR:AMPL?",
            set_cmd="SOUR:CURR:AMPL {}",
            vals=Numbers(min_value=-105e-3, max_value=105e-3),
            unit="A"
        )

        self.dc_compliance: Parameter = self.add_parameter(
            "dc_compliance",
            get_cmd="SOUR:CURR:COMP?",
            set_cmd="SOUR:CURR:COMP {}",
            vals=Numbers(min_value=0.1, max_value=105),
            unit="V"
        )

        self.auto_range: Parameter = self.add_parameter(
            "auto_range",
            get_cmd="SOUR:CURR:RANG:AUTO?",
            set_cmd="SOUR:CURR:RANG:AUTO {}",
            vals = Enum("ON", "OFF", "0", "1")
        )

        self.wave_func: Parameter = self.add_parameter(
            "wave_func",
            get_cmd="SOUR:WAVE:FUNC?",
            set_cmd="SOUR:WAVE:FUNC {}",
            val_mapping = {
                "sine": "SIN",
                "ramp": "RAMP",
                "square": "SQU",
                "arbitrary1": "ARB1",
                "arbitrary2": "ARB2",
                "arbitrary3": "ARB3",
                "arbitrary4": "ARB4",
            },
        )

        self.wave_amplitude: Parameter = self.add_parameter(
            "wave_amplitude",
            get_cmd="SOUR:WAVE:FUNC?",
            set_cmd="SOUR:WAVE:FUNC {}",
            vals=Numbers(min_value=2e-12, max_value=0.105),
            unit="A"
        )

        self.wave_frec: Parameter = self.add_parameter(
            "wave_frec",
            get_cmd="SOUR:WAVE:FUNC?",
            set_cmd="SOUR:WAVE:FUNC {}",
            vals=Numbers(min_value=1e-3, max_value=1e5),
            unit="Hz"
        )

        self.wave_offset: Parameter = self.add_parameter(
            "wave_offset",
            get_cmd="SOUR:WAVE:OFFS?",
            set_cmd="SOUR:WAVE:OFFS {}",
            vals=Numbers(min_value=-105e-3, max_value=105e-3),
            unit="A"
        )

    def waveform_arm(self):
        """ Arm the current waveform function. """
        self.write("SOUR:WAVE:ARM")

    def waveform_start(self):
        """ Start the waveform output. Must already be armed """
        self.write("SOUR:WAVE:INIT")

    def waveform_abort(self):
        """ Abort the waveform output and disarm the waveform function. """
        self.write("SOUR:WAVE:ABOR")

    def clear(self):
        self.write("SOUR:CLE:IMM")

    def on(self):
        self.write("OUTPUT ON")
    
    def off(self):
        self.write("OUTPUT OFF")