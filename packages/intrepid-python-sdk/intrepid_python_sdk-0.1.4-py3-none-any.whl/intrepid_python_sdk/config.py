from __future__ import absolute_import

import json

from intrepid_python_sdk.cache_manager import CacheManager
# from intrepid.decision_mode import DecisionMode
from intrepid_python_sdk.log_manager import IntrepidLogManager, LogLevel, LogManager
# from intrepid.status_listener import StatusListener

__metaclass__ = type

# from intrepid.tracking_manager import TrackingManagerConfig
from intrepid_python_sdk.utils import pretty_dict


class _IntrepidConfig(object):
    """
     IntrepidConfig configuration.
    """

    __env_id = ''
    __api_key = ''

    # TODO