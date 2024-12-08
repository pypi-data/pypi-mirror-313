from enum import Enum


class Status(Enum):
    """
    Intrepid Status enum
    """
    NOT_INITIALIZED = 0
    """
    Intrepid SDK has not been started or initialized successfully.
    """
    STARTING = 10
    """
    Intrepid SDK is starting.
    """
    POLLING = 20
    """
    Intrepid SDK has been started successfully but is still polling campaigns (Bucketing Mode).
    """
    PANIC = 30
    """
    Intrepid SDK is ready but is running in Panic mode: All features are disabled except 'fetchFlag' which refresh this
    status.
    """

    STOPPED = 40
    READY = 100
    """
    Intrepid SDK is ready to use.
    """

