"""
:author: Zilvinas Binisevicius <zilvinas@binis.me>
"""
import domipy
import domipy.messages
from domipy.messages.temperature_status import COOLING_MESSAGE_DATA_TYPE, HEATING_MESSAGE_DATA_TYPE

DOM_ABSENSE = 1
DOM_AUTO = 2
DOM_COMFORT = 5
DOM_FROST = 6

DOM_REG_MODE_OFF = 0
DOM_REG_MODE_HEATING = 1
DOM_REG_MODE_COOLING = 2
DOM_REG_MODE_MIXED = 3

class DTEM01Module(domipy.Module):
    """
    DTEM01 - temperature controll module (1 channels)
    """
    COMMAND_CODE = 'TE1'

    def __init__(self, serial_number, controller):
        domipy.Module.__init__(self, serial_number, controller)
        self._temperature = None
        self._mode = None
        self._heating_set_point = None
        self._cooling_set_point = None
        self._set_point = None
        self._range = None
        self._regulation_mode = None

    def get_range(self):
        return self._range

    def get_temperature(self):
        return self._temperature
    
    def get_mode(self):
        return self._mode
    
    def get_set_point(self):
        if self._mode == DOM_REG_MODE_HEATING:
            return self._heating_set_point
        else:
            return self._cooling_set_point
        
    def get_heating_set_point(self):
        return self._heating_set_point
    
    def get_cooling_set_point(self):
        return self._cooling_set_point

    def get_regulation_mode(self):
        return self._regulation_mode
        
    def set_temperature(self, temperature):
        if self._mode == DOM_REG_MODE_HEATING:
            message = domipy.SetHeatingTemperatureMessage(self.get_module_code(), self.get_serial_number(), temperature)
        else:
            message = domipy.SetCoolingTemperatureMessage(self.get_module_code(), self.get_serial_number(), temperature)
            
        self._controller.send(message)
    
    def set_mode(self, mode):
        """ Set temperature controll mode, modes:
        0 - off
        1 - heating
        2 - cooling
        3 - mixed
        """
        message = domipy.SetTemperatureModeMessage(self.get_module_code(), self.get_serial_number(), mode)
        self._controller.send(message)

    def set_regulation_mode(self, mode):
        message = domipy.SetRegulationModeMessage(self.get_module_code(), self.get_serial_number(), mode)
        self._controller.send(message)
    
    def set_automatic(self):
        message = domipy.SetTemperatureAutomaticMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)

    def set_absence(self):
        message = domipy.SetTemperatureAbsenceMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)
 
    def set_comfort(self):
        message = domipy.SetTemperatureComfortMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)

    def set_frost(self):
        message = domipy.SetTemperatureFrostMessage(self.get_module_code(), self.get_serial_number())
        self._controller.send(message)

    def number_of_channels(self):
        return 1

    def _on_message(self, message):
        if isinstance(message, domipy.TE1TemperaturetatusMessage):
            self._temperature = message.get_temperature()
            if(message.get_dataType() == HEATING_MESSAGE_DATA_TYPE): 
                self._heating_set_point = message.get_heating_set_point()
            else:
                self._cooling_set_point = message.get_cooling_set_point()
                
            self._mode = self._mode_text_to_number(message.get_mode())
            self._regulation_mode = self._regulation_mode_text_to_number(message.get_regulation_mode())
            print("mode", self._mode)
            self._range = message.get_range()

            for ch in range(0, self.number_of_channels()):
                if ch in self._callbacks:
                    for callback in self._callbacks[ch]:
                        callback(self._temperature, self._mode, self._set_point, self._range)

    def _mode_text_to_number(self, mode):
        if mode == 'AUTO':
            return DOM_AUTO 
        elif mode == 'ABSENCE':
            return DOM_ABSENSE
        elif mode == 'COMFORT':
            return DOM_COMFORT
        elif mode == 'FROST':
            return DOM_FROST
        return DOM_AUTO

    def _regulation_mode_text_to_number(self, regulation_mode):
        if regulation_mode == 'COOLING':
            return DOM_REG_MODE_COOLING
        elif regulation_mode == 'HEATING':
            return DOM_REG_MODE_HEATING
        elif regulation_mode == 'MIXED':
            return DOM_REG_MODE_MIXED
        elif regulation_mode == 'OFF':
            return DOM_REG_MODE_OFF
        
class DTEM02Module(domipy.Module):
    """
    DTEM02 -  controll module (1 channels)    
    """
    COMMAND_CODE = 'TE2'
    def _on_message(self, message):
        if isinstance(message, domipy.TE2TemperaturetatusMessage):
            self._temperature = message.get_temperature()
            if(message.get_dataType() == HEATING_MESSAGE_DATA_TYPE): 
                self._set_point = message.get_heating_set_point()
            else:
                self._set_point = message.get_cooling_set_point()
            self._mode = message.get_mode()
            self._range = message.get_range()

            for ch in range(0, self.number_of_channels()):
                if ch in self._callbacks:
                    for callback in self._callbacks[ch]:
                        callback(self._temperature, self._mode, self._set_point, self._range)

domipy.register_module_class(DTEM01Module)
domipy.register_module_class(DTEM02Module)
