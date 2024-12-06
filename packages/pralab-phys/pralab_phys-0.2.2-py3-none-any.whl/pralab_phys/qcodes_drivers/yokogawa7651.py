# Reference: https://github.com/QCoherence/QCodes-drivers/blob/master/Yokogawa_7651.py

# Last updated on 30 Oct 2020
#                     -- Arpit
from functools import partial
from qcodes import (VisaInstrument,
					validators as vals)
from qcodes.parameters import Parameter

import logging

log = logging.getLogger(__name__)


class Yokogawa7651(VisaInstrument):
	"""  
    QCoDeS driver for the Yokogawa 7651 I/V source.  

    Args:  
        VisaInstrument (_type_): _description_  

    Attributes:  
        voltage_range (Parameter): Set output voltage range in mV.  
        current_range (Parameter): Set output current range in mA.  
        voltage_limit (Parameter): Set output voltage limit in mV.  
        current_limit (Parameter): Set output current limit in mA.  
        voltage (Parameter): Set output voltage in mV.  
        current (Parameter): Set output current in mA.  
        status (Parameter): Output on/off. ("on", "off")
    """  
	def __init__(self, name, address, **kwargs):
		# supplying the terminator means you don't need to remove it from every response
		super().__init__(name, address, terminator='\n', **kwargs)

		# init: crashes the I/O, clear from visa test panel fixes the issue
		# self.write('RC')

		self.voltage_range: Parameter = self.add_parameter(
			name = 'voltage_range',  
			label = 'Set the output voltage range in mV',
			vals = vals.Enum(10, 100, 1000, 10000, 30000),
			unit   = 'mV',
			set_cmd = partial(self._set_range(), mode = "VOLT")
			)

		self.current_range: Parameter = self.add_parameter(
			name = 'current_range',  
			label = 'Set output current range in mA',
			vals = vals.Enum(1,10,100),
			unit   = 'mA',
			set_cmd = partial(self._set_range(), mode = "CURR")
			)

		self.voltage_limit: Parameter = self.add_parameter(
			name = 'voltage_limit',  
			label = 'Set output voltage limit in mV',
			vals = vals.Numbers(1000,30_000),
			unit   = 'mV',
			set_parser = self._div_1000_int,
			set_cmd = 'LV'+'{}'
			)

		self.current_limit: Parameter = self.add_parameter(
			name = 'current_limit',
			label = 'Set output current limit in mA',
			vals = vals.Numbers(5,120),
			unit   = 'mA',
			set_parser = int,
			set_cmd = 'LA'+'{}')

		self.add_parameter( name = 'voltage',  
							label = 'Set output voltage in mV',
							vals = vals.Numbers(-30_000,30_000),
							unit   = 'mV',
							set_cmd = self._set_V)

		self.add_parameter( name = 'current',  
							label = 'Set output current in mA',
							vals = vals.Numbers(-120,120),
							unit   = 'mA',
							set_cmd = self._set_A)

		self.add_parameter( name = 'status',  
							label = 'Output on/off',
							vals = vals.Enum('on','off'),
							set_cmd='O' + '{}' + 'E',
							set_parser =self._easy_read_status
							)
	
	def _set_range(self, range:int, mode:str) -> None:
		if mode == "CURR":
			range_options = {1:"R4", 10:"R5", 100:"R6" }
			self.write('F5'+range_options[int(range)]+'E')
		elif mode == "VOLT":
			range_options = {10:"R2", 100:"R3", 1000:"R4", 10000:"R5", 30000:"R6" }
			self.write('F1'+range_options[int(range)]+'E')

	def _get_mode(self, status:str) -> str:
		if "F1R" in status:
			return "VOLT"
		elif "F5R" in status:
			return "CURR"
	def _get_range(self, status:str) -> int:
		if "F1R" in status:
			if "R2" in status:
				return 10
			elif "R3" in status:
				return 100
			elif "R4" in status:
				return 1000
			elif "R5" in status:
				return 10000
			elif "R6" in status:
				return 30000
		elif "F5R" in status:
			if "R4" in status:
				return 1
			elif "R5" in status:
				return 10
			elif "R6" in status:
				return 100

	def _volt_limit(self, status:str) -> int:
		if "LV" in status:
			return int(status[2:])

	def _curr_limit(self, status:str) -> int:
		if "LA" in status:
			return int(status[status.index("LA")+2:])

	def _get_status(self) -> None:
		status = self.ask('OS')
		slist = status.split()
		self.statusmap = {
			'mode': self._get_mode(slist[1]),
			'range': self._get_range(slist[1]),
			'voltage_limit': self._volt_limit(slist[3]),
			'current_limit': self._curr_limit(slist[3]),
			}

	def _div_1000_int(self,val):
		return int(val/1000)

	def _set_V(self,voltage):

		if voltage>0:
			polarity = '+'
		else:
			polarity = '-'
		self.write('S'+polarity+str(round(abs(voltage)/1000.,6))+'E')

	def _set_A(self,current):

		if current>0:
			polarity = '+'
		else:
			polarity = '-'
		self.write('S'+polarity+str(round(abs(current)/1000.,6))+'E')

	def _easy_read_status(self,state):

		if state == 'on':
			ret = '1'
		else:
			ret = '0'
		return ret

	def initialize(self):

		self.write('RC')

	# To avoid identity query error
	def get_idn(self):
		return self.ask('OS')