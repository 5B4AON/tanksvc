import inspect

class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

class UnauthorizedRequestError(Exception):
    """Used for unauthorized request errors when deserializing"""

class TankCommand():
    """
    left and right represent a target speed level for the two tank tracks.
    The tank will try to reach the target based on its own algorithm.
    Drive instructions should not be sent in intervals less than 200ms so as not
    to overwelm the tank api rest listeners. This suggests that the most current
    instruction as well as the last one is stored in a buffer and is only sent if
    it is different from the last and if at least 200ms have passed since the last one
    was sent. A scheduler should be checking for new instructions to send every
    100ms. 
    """
    # Tank track relative speeds 0-100. Negative speeds means reverse.
    passphrase = None
    left = 0
    right = 0
    status = None

    def serialize(self):
        """Serializes a Tank Command into a dictionary"""
        json = {}
        if self.passphrase:
            json["passphrase"] = self.passphrase
        if self.left:
            json["left"] = self.left
        if self.right:
            json["right"] = self.right
        if self.status:
            json["status"] = self.status 
        return json

    def deserialize(self, data):
        """
        Deserializes a Tank Command from a dictionary
        Args:
            data (dict): A dictionary containing the command data
        """
        try:
            self.passphrase = data["passphrase"]
            if self.passphrase != "1234":
                raise UnauthorizedRequestError("Wrong passphrase")
            self.setAttribute("left", data)
            self.setAttribute("right", data)
            self.setAttribute("status", data)
        except KeyError as error:
            raise DataValidationError("Invalid Command: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Tank Command: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self
    
    def clear(self):
        for i in inspect.getmembers(self):
            # to remove private and protected functions
            if not i[0].startswith('_'):
                # To remove methods
                if not inspect.ismethod(i[1]):
                    setattr(self, i[0], None)

    def setAttribute(self, name, data):
        attr = data.get(name)
        if attr:
            setattr(self, name, attr)
        else:
            setattr(self, name, None)
        