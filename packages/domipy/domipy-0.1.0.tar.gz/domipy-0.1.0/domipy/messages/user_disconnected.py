"""
Session opened  Message
:author: Zilvinas Binisevicius <zilvinas@binis.me>
"""
import json
import domipy

class UserDisconnected(domipy.Message):
    """
    Session opened message
    """

    def __init__(self):

        domipy.Message.__init__(self)
        self.moduleType = 'User database empty. Connect first with GoldenGate'
    
    def populate(self, serialNumber, dataType, dataString):
        pass

    def to_json(self):
        """
        :return: str
        """
        json_dict = self.to_json_basic()
        return json.dumps(json_dict)
