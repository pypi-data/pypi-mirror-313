from intrepid_python_sdk.constants import ERROR_INITIALIZATION_PARAM, ERROR_CACHE_HIT_TIMEOUT, ERROR_CACHE_HIT_LOOKUP_FORMAT

class IntrepidException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class InitializationParamError(IntrepidException):
    def __init__(self):
        super(IntrepidException, self).__init__('[Initialization Param Error] ' + ERROR_INITIALIZATION_PARAM)


class ParamTypeError(IntrepidException):
    def __init__(self, message):
        super(IntrepidException, self).__init__(message)


class IntrepidParsingError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__('[ParsingError] ' + message)
