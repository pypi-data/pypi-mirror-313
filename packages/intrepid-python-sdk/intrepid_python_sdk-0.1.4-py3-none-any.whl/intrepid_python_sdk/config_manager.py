# from intrepid.api_manager import ApiManager
# from intrepid.bucketing_manager import BucketingManager
from intrepid_python_sdk.cache_manager import CacheManager
# from intrepid.config import DecisionApi
from intrepid_python_sdk.constants import WARNING_DEFAULT_CONFIG, TAG_INITIALIZATION
# from intrepid.decision_mode import DecisionMode
from intrepid_python_sdk.log_manager import LogLevel
# from intrepid.tracking_manager import TrackingManager
from intrepid_python_sdk.status import Status

class ConfigManager:

    def __init__(self):
        self.intrepid_config = None
        self.decision_manager = None
        self.tracking_manager = None
        self.cache_manager = None

        # TODO