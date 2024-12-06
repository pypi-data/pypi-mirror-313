# most of the drivers only need a couple of these... moved all up here for clarity below
import sys
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import (
        Unpack,  # can be imported from typing if python >= 3.12
    )

from qcodes.instrument import Instrument
from qcodes.parameters import Parameter
from qcodes.validators import Enum, Ints, MultiType, Numbers

class Timer(Instrument):
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
        
        self.initialtime = 0

    def initialize():
        self.initialtime = time.time()

    def get_time:
        return 



class time_now(Parameter):
    """
    Parameter class for the motor position
    """
    def __init__(
        self,
        name: str,
        instrument: PPMSdotNET,
        **kwargs,
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)

    def set_raw(self, position: float) -> None:
        """Sets the motor position"""
        self.instrument.move_position(position)

    def get_raw(self) -> float:
        """Returns time"""
        return self.instrument.get_position()