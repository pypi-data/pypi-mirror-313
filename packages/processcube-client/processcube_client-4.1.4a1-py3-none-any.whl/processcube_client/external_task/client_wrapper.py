import asyncio
import warnings

from .external_task_client import ExternalTaskClient
from ..core.loop_helper import get_or_create_loop


class ClientWrapper:

    def __init__(self, atlas_engine_url):
        self._atlas_engine_url = atlas_engine_url

    def subscribe_to_external_task_for_topic(self, topic, handler, **task_options):

        loop = task_options.get('loop', get_or_create_loop())

        warnings.warn("Please use 'subscribe_to_external_task_topic' instead of 'subscribe_to_external_task_for_topic'.", DeprecationWarning)
        return self.subscribe_to_external_task_topic(topic, handler, loop=loop)

    def subscribe_to_external_task_topic(self, topic, handler, **task_options):
        loop = task_options.get('loop', get_or_create_loop())

        external_task_client = ExternalTaskClient(self._atlas_engine_url, loop=loop)

        external_task_client.subscribe_to_external_task_for_topic(topic, handler)

        return external_task_client
        
