# try:
#     from abc import ABC, abstractmethod
# except ImportError:
import json
import sqlite3 as sl
import time
import traceback
from abc import abstractmethod, ABC

# from intrepid.constants import TAG_CACHE_MANAGER
from intrepid_python_sdk.utils import log_exception


class HitCacheImplementation:

    def __init__(self):
        """
        HitCacheImplementation is an abstract class which helps to connect the Flagship SDK and an existing database
        in order to provide a custom cache implementation for visitors hits.

        Caching visitors hits will prevent any data loss in case of errors or network failures.
        """
        pass

    @abstractmethod
    def cache_hits(self, hits):
        """
        This method is called when the Flagship SDK needs to save visitors hits into cache.
        @param hits: dictionary of hits that need to be saved into cache.
        """
        pass

    @abstractmethod
    async def lookup_hits(self):
        """
        This method is called when the Flagship SDK needs to load visitors hits from the cache.
        @return dictionary of previously cached visitors hits. Please check the documentation for the expected format.
        """
        pass

    @abstractmethod
    def flush_hits(self, hits_ids):
        """
        This method is called when the Flagship SDK needs to flush specific hits.
        @param hits_ids: hits ids that need to be flushed from cache.
        """
        pass

    @abstractmethod
    def flush_all_hits(self):
        """
        This method is called when the Flagship SDK needs to flush all the hits from cache.
        """
        pass


class CacheManager(ABC):

    def __init__(self, **kwargs):
        """
        Abstract class to extend in order to provide a custom CacheManager and link the Flagship SDK to an existing
        database. Your custom class must implement VisitorCacheImplementation class to manage Visitor cache and/or
        HitCacheImplementation class to manager visitor hits.
        @param kwargs: <br><br>
        'timeout' (int) : timeout for database operation in milliseconds. Default is 100.
        """
        self.timeout = (kwargs['timeout'] if 'timeout' in kwargs and isinstance(kwargs['timeout'],
                                                                                int) else 100.0) / 1000.0

    def init(self, flagship_config):
        self.env_id = flagship_config.env_id if flagship_config is not None else None
        self.open_database(self.env_id)

    @abstractmethod
    def open_database(self, env_id):
        pass

    @abstractmethod
    def close_database(self):
        pass

