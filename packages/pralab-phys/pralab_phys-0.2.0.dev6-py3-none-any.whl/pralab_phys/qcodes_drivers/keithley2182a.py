# most of the drivers only need a couple of these... moved all up here for clarity below
import sys
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import (
        Unpack,  # can be imported from typing if python >= 3.12
    )

from qcodes import validators as vals
from qcodes.instrument import (
    InstrumentChannel,
    VisaInstrument,
    VisaInstrumentKWArgs,
)
from qcodes.parameters import Parameter
from qcodes.validators import Enum, Numbers


class Keithley2182Achannel(InstrumentChannel):

    """A single channel of the Keithley2182A"""
    def __init__(
        self,
        parent: Instrument,
        name: str,
        channel: str,
        **kwargs: "Unpack[InstrumentBaseKWArgs]",
    ) -> None:

        """
        Args:
            parent: The Instrument instance to which the channel is
                to be attached.
            name: The 'colloquial' name of the channel
            channel: The name used by the Keithley, i.e. either
                'smua' or 'smub'
            **kwargs: Forwarded to base class.
        """

        super().__init__(parent, name, **kwargs)
        self.model = self._parent.model






class Keithley2182A(VisaInstrument):
    """Instrument Driver for Keithley2182A (1 channel, Voltage only)

    Attributes:
        nplc (Parameter): Set or get the number of power line cycles (min=0.01, max=50)
        auto_range (Parameter): Set or get the measurement range automatically (1: ON, 0: OFF)
        rel (Parameter): Enables or disables the application of
                         a relative offset value to the measurement. (1: ON, 0: OFF)
        active (Parameter): Set or get the active function. (VOLT or TEMP)
        filter (Parameter): Enables or disables the digital filter for measurements.
        amplitude (Parameter): Get the voltage (unit: V)
    """
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

        self._trigger_sent = False

        self.nplc: Parameter = self.add_parameter(
            "nplc",
            get_cmd="SENS:VOLT:NPLC?",
            set_cmd="SENS:VOLT:NPLC {}",
            vals=Numbers(min_value=0.01, max_value=50),
            get_parser=float
        )

        # 将来的にチャンネルを変更できるようにする
        self.auto_range: Parameter = self.add_parameter(
            "auto_range",
            get_cmd="SENS:VOLT:CHAN1:RANG:AUTO?",
            set_cmd="SENS:VOLT:CHAN1:RANG:AUTO {}"
        )

        # 将来的に「チャンネルの変更」「Bool値の入力方法」「温度かボルテージか」など変更できるようにしたい
        self.rel: Parameter = self.add_parameter(
            "rel",
            get_cmd="SENS:VOLT:REFerence:STATe?",
            set_cmd="SENS:VOLT:REFerence:STATe {}"
        )

        self.active: Parameter = self.add_parameter(
            "active",
            get_cmd=":SENS:FUNC?",
            set_cmd="SENS:FUNC {}",
            vals=Enum("VOLT", "TEMP")
        )

        self.filter: Parameter = self.add_parameter(
            "filter",
            get_cmd=":SENS:VOLT:DFILter:STAT?",
            set_cmd=":SENS:VOLT:DFILter:STAT {}"
        )

        self.amplitude: Parameter = self.add_parameter(
            "amplitude",
            get_cmd="SENS:DATA:FRES?",
            get_parser=float,
            unit="V"
        )

        self.get = self.amplitude

        


