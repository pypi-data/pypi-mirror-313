# URLS

URL_DECISION_API = "https://api.intrepid.ai/v1/"
URL_GRAPHS = "/graphs"
URL_TRACKING = "https://events.intrepid.ai/"
URL_ACTIVATE = URL_DECISION_API + "activate"
WS_HOST = "127.0.0.1"
WS_PORT = 9999


# TAGS
TAG_MAIN = "Intrepid"
TAG_INITIALIZATION = "Initialization"
TAG_STATUS = "Status"
TAG_UPDATE_CONTEXT = "Update Context"
TAG_TRACKING = "Tracking"
TAG_HTTP_REQUEST = "Http Request"

# INFO
INFO_STATUS_CHANGED = "SDK status has changed ({})"
INFO_READY = "Intrepid version {} has started successfully.\nConfiguration: {}"
INFO_SDK_READY = "Intrepid SDK started at {}"
INFO_CALLBACK_REGISTERED = "Function callback registered and waiting for node specs."
INFO_WSSERVER_READY = "Listening on port {}"
INFO_BUCKETING_POLLING = "Polling event."
INFO_TRACKING_MANAGER = "Polling event."
INFO_STOPPED = 'Intrepid has been stopped.'

# DEBUG
DEBUG_CONTEXT = "Context have been updated with success.\n{}"
DEBUG_REQUEST = "{} {} {} {}ms\n"
DEBUG_FETCH_FLAGS = "Flags have been updated.\n{}"
DEBUG_TRACKING_MANAGER_STARTED = "Started."
DEBUG_TRACKING_MANAGER_STOPPED = "Stopped."
DEBUG_TRACKING_MANAGER_LOOKUP_HITS = "Lookup hits \n"
DEBUG_TRACKING_MANAGER_ADDED_HITS = "Add hits into the pool\n"
DEBUG_TRACKING_MANAGER_CACHE_HITS = "Cache hits \n"


# WARNING
WARNING_PANIC = "Panic mode is enabled : all features are disabled except 'fetchFlags()'."
WARNING_DEFAULT_CONFIG = "No Intrepid configuration is passed. Default configuration will be used."
WARNING_CONFIGURATION_PARAM_TYPE = "'{}' parameter type is not valid. Please check the documentation. Default value " \
                                   "will be used."
WARNING_CONFIGURATION_PARAM_MIN_MAX = "'{}' parameter type is not valid. Please check the documentation. Default " \
                                      "value {} will be used."

# ERRORS
ERROR_INITIALIZATION_PARAM = "Params 'envId' and 'apiKey' must not be None or emtpy."
ERROR_CONFIGURATION = "Configuration has failed, the SDK has not been initialized successfully."
ERROR_PARAM_TYPE = "Parameter '{}' for function '{}' is not valid. Expecting {} type."
ERROR_PARAM_NUMBER = "Number of parameters incompatible with node info. Expecting {} parameters."
ERROR_PARAM_NAME = "Parameter name '{}' is not valid. Expecting parameter '{}'."
ERROR_PARAM_NUM = "Number of parameters do not match. Expecting {} parameters."
ERROR_PARSING_CAMPAIGN = "An error occurred while parsing campaign json object."
ERROR_PARSING_VARIATION_GROUP = "An error occurred while parsing variation group json object."
ERROR_PARSING_VARIATION = "An error occurred while parsing variation json object."
ERROR_PARSING_MODIFICATION = "An error occurred while parsing modification json object."
ERROR_REGISTER_CALLBACK = "Cannot register callback, or callback not yet registered."
ERROR_UPDATE_CONTEXT_RESERVED = "Context key '{}' is reserved by flagship and can't be overridden."
ERROR_UPDATE_CONTEXT_TYPE = "Context key '{}' value must be of type: '{}'."
ERROR_UPDATE_CONTEXT_EMPTY = "Context key '{}' will be ignored as its value is empty'."
ERROR_UPDATE_CONTEXT_EMPTY_KEY = "Context key must be a non null or empty 'str'."

ERROR_METHOD_DEACTIVATED = "Method '{}' have been deactivated: {}"
ERROR_METHOD_DEACTIVATED_PANIC = "SDK is running in panic mode."
ERROR_METHOD_DEACTIVATED_NOT_READY = "SDK is not started yet."

ERROR_TRACKING_HIT_SUBCLASS = "send_hit() param must be a subclass of Hit."
ERROR_INVALID_HIT = "Hit {} {} has invalid data and wont be sent."

ERROR_CACHE_HIT_TIMEOUT = "'HitCacheImplementation.{}' has timed out."
ERROR_CACHE_HIT_LOOKUP_FORMAT = "'HitCacheImplementation.{}' for hit id '{}' has returned a " \
                                    "wrong format. Please check the documentation."
