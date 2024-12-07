from __future__ import absolute_import

import json
import traceback
from enum import Enum

from websockets.sync.client import connect

from intrepid.constants import TAG_HTTP_REQUEST, DEBUG_REQUEST, URL_TRACKING, URL_ACTIVATE, URL_DECISION_API
from intrepid.decorators import param_types_validator
from intrepid.log_manager import LogLevel
from intrepid.utils import pretty_dict, log, log_exception
from intrepid.message import IntrepidMessage


class WebSocketHelper:
    def __init__(self, address, port):
        self.ws_address = f"ws://{address}:{port}"

    class RequestType(Enum):
        PUB = "PUB",
        SUB = "SUB"


    @staticmethod
    @param_types_validator(False, RequestType, str, dict, dict, int)
    def send_to_ws(url, node_id, content, timeout=5000):
        # TODO create message to send

        # TODO serialize via CDR

        with connect(WebSocketHelper.ws_address) as  websocket:
            websocket.send("Hello world!")

    @staticmethod
    @param_types_validator(False, RequestType, str, dict, dict, int)
    def recv_from_ws(url, node_id, output_id, timeout=5000):

        with connect(WebSocketHelper.ws_address) as websocket:
            message = websocket.recv()
            # TODO deserialize and return

            return message


    @staticmethod
    def log_request(method, url, node_id, content, response):
        body_str = "Request body =>\n" \
                 "{}\n" \
                 "Response body =>\n" \
                 "{}\n"
        if response is None:
            message = DEBUG_REQUEST.format(method.name, url, 'FAIL', int(0))
            pretty_request = pretty_dict(content, 2)
            pretty_response = ''
        else:
            message = DEBUG_REQUEST.format(method.name, url, response.status_code,
                                           int(response.elapsed.total_seconds() * 1000))
            try:
                response_dict = json.loads(response.content.decode("utf-8"))
            except Exception as e:
                response_dict = {}
            pretty_request = pretty_dict(content, 2)
            pretty_response = pretty_dict(response_dict, 2)
        message += body_str.format(pretty_request, pretty_response)
        log(TAG_HTTP_REQUEST,
            LogLevel.DEBUG if response is not None and response.status_code in range(200, 305) else LogLevel.ERROR,
            message)
