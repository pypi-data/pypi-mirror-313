from typing import (
    TYPE_CHECKING,
    Union
)

import qcodes.validators as vals
from qcodes.validators import Enum, Ints, Numbers
from qcodes.instrument import VisaInstrument, VisaInstrumentKWArgs
from qcodes.parameters import Parameter

if TYPE_CHECKING:
    from typing_extensions import Unpack

class PPMSClassic(VisaInstrument):

    default_terminator = "\r\n"

    def __init__(
        self,
        name: str,
        address: str,
        max_temp: int = 320,
        **kwargs: "Unpack[VisaInstrumentKWArgs]",
    ):

        """initial
        """
        super().__init__(name, address, **kwargs)

        self.Trate: float = 20
        self.Brate: float = 200
        self.Bmode: int = 0
        self.Tmode: int = 0

        self.position: Parameter = self.add_parameter(
            "position",
            get_cmd = "MOVE?",
            set_cmd = "MOVE {} 0",
            vals=Numbers(min_value=0, max_value=360),
        )

        self.field: Parameter = self.add_parameter(
            "field",
            get_cmd = "FIELD?",
            set_cmd = self._set_field,
            vals=Numbers(min_value=-90000, max_value=90000),
            unit = "Oe"
        )

        self.temperature: Parameter = self.add_parameter(
            "temperature",
            get_cmd = "TEMP?",
            set_cmd = self._set_temp,
            vals=Numbers(min_value=1.9, max_value=max_temp),
            unit = "Oe"
        )

    def set_field_approach_mode(self, mode: Union[str, int]) -> None:
        modedict = {"linear":0, "no overshoot":1, "oscillate":2}
        self.Bmode = modedict[mode.lower()]

    def set_field_rate(self, rate: float) -> None:
        self.Brate = rate

    def set_temperature_approach_mode(self, mode: Union[str, int]) -> None:
        modedict = {"fast settle":0, "no overshoot":1}
        self.Tmode = modedict[mode.lower()]

    def set_temperature_rate(self, rate: float) -> None:
        self.Trate = rate

    def _set_field(self, field: float) -> str:
        ret = ["FIELD", str(field), str(self.Brate), str(self.Bmode), "0"]
        return ' '.join(ret)

    def _set_temp(self, temp: float) -> str:
        ret = ["TEMP", str(temp), str(self.Trate), str(self.Tmode)]
        return ' '.join(ret)

    def set_present_position_as(self, position: float) -> None:
        ret = ["MOVE" , str(position), "2"]
        self.write(' '.join(ret))

    def purge_and_seal(self) -> None:
        self.write("CHAMBER 1")