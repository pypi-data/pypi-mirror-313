"""
Temperature status
:author: Zilvinas Binisevicius <zilvinas@binis.me>
"""
import json
import domipy

TEM_COMMAND_CODE = "TEM"
TE1_COMMAND_CODE = "TE1"
TE2_COMMAND_CODE = "TE2"
COOLING_MESSAGE_DATA_TYPE = 'U'
HEATING_MESSAGE_DATA_TYPE = 'T'


class GenericTemperaturetatusMessage(domipy.Message):
    """
    Generic Temperature input module status
    """

    def __init__(self, address=None):
        domipy.Message.__init__(self)
        self.moduleType = TEM_COMMAND_CODE
        self.serialNumber = None
        self.dataType = None
        self._current = None
        self._mode = None
        self._regulation_mode = None
        self._cooling_set_point = None
        self._heating_set_point = None
        self._range = None

    def get_temperature(self):
        return self._current
    
    def get_mode(self):
        return self._mode

    def get_regulation_mode(self):
        return self._regulation_mode

    def get_cooling_set_point(self):
        return self._cooling_set_point
   
    def get_heating_set_point(self):
        return self._heating_set_point
     
    def get_range(self):
        return self._range
    
    def get_dataType(self):
        return self.dataType

    def populate(self, serialNumber, dataType, dataString):
        """
        :return: None
        """
        # assert isinstance(dataString, str)

        self.serialNumber = serialNumber
        self.dataType = dataType
        # [T20.2 21.0 AUTO 21.0]
        # [U20.2 21.0 HEATING 21.0]
        data = dataString.split()
        
        self._current = float(data[0])

        if dataType == COOLING_MESSAGE_DATA_TYPE :
            self._cooling_set_point = float(data[1])
            self._mode = data[2]
        else :
            self._heating_set_point = float(data[1])
            self._regulation_mode = data[2]

        self._range = float(data[3])

    def to_json(self):
        """
        :return: str
        """

        json_dict = self.to_json_basic()
        json_dict['current'] = self._current
        json_dict['mode'] = self._mode
        json_dict['regulation_mode'] = self._regulation_mode
        json_dict['cooling_set_point'] = self._cooling_set_point
        json_dict['heating_set_point'] = self._heating_set_point
        json_dict['range'] = self._range
        return json.dumps(json_dict)


class TE1TemperaturetatusMessage(GenericTemperaturetatusMessage):
    def __init__(self, address=None):
        GenericTemperaturetatusMessage.__init__(self)
        self.moduleType = TE1_COMMAND_CODE

class TE2TemperaturetatusMessage(GenericTemperaturetatusMessage):
    def __init__(self, address=None):
        GenericTemperaturetatusMessage.__init__(self)
        self.moduleType = TE2_COMMAND_CODE


domipy.register_command(TE1_COMMAND_CODE, TE1TemperaturetatusMessage)
domipy.register_command(TE2_COMMAND_CODE, TE2TemperaturetatusMessage)
