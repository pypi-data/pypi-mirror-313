import sys
import clr
from qcodes.instrument.parameter import Parameter
from qcodes.instrument.base import Instrument

sys.path.append(r"C:\qd")

# add .net reference and import so python can see .net
clr.AddReference(r"QDInstrument")

from QuantumDesign.QDInstrument import QDInstrumentBase, QDInstrumentFactory

DEFAULT_PORT = 11000

class PPMSdotNET(Instrument):
    """
    QD PPMS Multivu (dotNET)
    """
    def __init__(
        self,
        name: str,
        ip_address: str,
        remote: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)

        self.device = QDInstrumentFactory.GetQDInstrument(
            QDInstrumentBase.QDInstrumentType.PPMS, remote, ip_address, DEFAULT_PORT)

        self.Trate: float = 1.0
        self.Brate: float = 20.0
        self.Tmode: int = 0
        self.Bmode: int = 0

        # Create Position parameter
        self.position: Parameter = self.add_parameter(
            name="position",
            parameter_class=Position,
            label="Motor position",
            unit="deg",
        )

        self.temperature: Parameter = self.add_parameter(
            name="temperature",
            parameter_class=Temperature,
            label="Temperature",
            unit="K",
        )

        self.field: Parameter = self.add_parameter(
            name="field",
            parameter_class=Field,
            label="Field",
            unit="Oe",
        )

    def get_position(self):
        return float(str(self.device.GetPosition("Horizontal Rotator", 0, 0)))
    
    def set_position(self, position):
        return self.device.SetPosition("Horizontal Rotator", position, 0, 0)

    def set_temperature(self, temp):
        if 1.9 <= temp <= 320:
            return self.device.SetTemperature(temp, self.Trate, self.Tmode)
        else:
            raise RuntimeError("Temperature is out of bounds. Should be between 0 and 320 K")

    def get_temperature(self) -> float:
        return float(set(self.device.GetTemperature(0, 0)))

    def set_field(self, field):
        if -85000 <= field <= 85000:
            return self.device.SetField(field, self.Brate, self.Bmode, 0)
        else:
            raise RuntimeError("Field is out of bounds. Should be between -85000 and 85000 Oe")

    def get_field(self) -> float:
        return float(set(self.device.GetField(0, 0)))
        
    def set_t_rate(self, rate: float):
        self.Trate = rate
    
    def set_b_rate(self, rate: float):
        self.rate = rate

    def get_idn(self):
        return {
            "vendor": "Qauntum Design",
            "model": "PPMS3",
            "serial": self.serial,
            "firmware": None,
        }


class Position(Parameter):
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
        self.instrument.set_position(position)

    def get_raw(self) -> float:
        """Returns the motor position"""
        return self.instrument.get_position()


class Temperature(Parameter):
    """
    Parameter class for the temperature
    """
    def __init__(
        self,
        name: str,
        instrument: PPMSdotNET,
        **kwargs,
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)

    def set_raw(self, temperature: float) -> None:
        """Sets the temperature"""
        self.instrument.set_temperature(temperature)

    def get_raw(self) -> float:
        """Returns the temperature"""
        return self.instrument.get_temperature()


class Field(Parameter):
    """
    Parameter class for the temperature
    """
    def __init__(
        self,
        name: str,
        instrument: PPMSdotNET,
        **kwargs,
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)

    def set_raw(self, mag: float) -> None:
        """Sets the magnetic field"""
        self.instrument.set_field(mag)

    def get_raw(self) -> float:
        """Returns the magnetic field"""
        return self.instrument.get_field()