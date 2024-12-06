
class FunctionalError(Exception):
    
    def __init__(self, code, message, details=""):
        super(FunctionalError, self).__init__(message)
        self._code = code
        self._message = message
        self._details = details

    def get_code(self):
        return self._code

    def get_message(self):
        return self._message

    def get_details(self):
        return self._details