from __future__ import absolute_import
from __future__ import unicode_literals
import logging
from typing import Callable, Dict, List, Optional
import asyncio
import importlib_metadata
import os, sys
import subprocess
from websockets.server import serve, unix_serve
from intrepid_python_sdk.config import _IntrepidConfig
import signal
from intrepid_python_sdk.config_manager import ConfigManager
from intrepid_python_sdk.constants import WS_HOST, WS_PORT, TAG_STATUS, TAG_HTTP_REQUEST, \
    INFO_STATUS_CHANGED, TAG_INITIALIZATION, INFO_CALLBACK_REGISTERED, \
    INFO_READY, INFO_WSSERVER_READY, INFO_STOPPED, INFO_SDK_READY, \
    ERROR_CONFIGURATION, ERROR_PARAM_TYPE, ERROR_PARAM_NUM, ERROR_PARAM_NAME, ERROR_REGISTER_CALLBACK
from intrepid_python_sdk.decorators import param_types_validator
from intrepid_python_sdk.errors import InitializationParamError
from intrepid_python_sdk.log_manager import LogLevel
from intrepid_python_sdk.utils import log, log_exception, signal_handler
from intrepid_python_sdk.status import Status
from intrepid_python_sdk.node import Node, Type, IntrepidType, DataElement
from intrepid_python_sdk.qos import Qos
from intrepid_python_sdk.message import IntrepidMessage, Opcode, InitRequest, ExecRequest, ExecResponse
from datetime import datetime


import aiohttp
from aiohttp import web, WSCloseCode
import asyncio
import json


__name__ = 'intrepid_python_sdk'
__version__ = importlib_metadata.distribution(__name__).version


# Set up the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)



# TODO remove this and use log_manager
# Configure logging
# logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO or desired level
# Define ANSI escape codes for colors
# COLOR_RED = "\033[91m"
# COLOR_RESET = "\033[0m"

# Custom logging format with timestamp
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format)
logger = logging.getLogger(__name__)  # Create a logger instance



class Intrepid:
    __instance = None

    def __init__(self):
        """
        Initialize the Intrepid SDK.

        @param node_id: Unique identifier of the node managed by this handler
        @param qos: Dictionary that specifies the QoS applied to this node (Not Implemented)
        @return:
        """

        self.qos = None
        self.__unix_socket_path = None
        self.__node = None
        self.__node_info = None
        self.__callback = None


    # async def http_handler(self, request):
    #     # announce node specs as http response
    #     mynode_json = self.__node.to_json()
    #     return web.json_response(mynode_json)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                msg_dict = json.loads(msg.data)

                request_id = msg_dict.get("id")
                discovery_object = msg_dict.get("discovery")
                init_object = msg_dict.get("init")
                exec_object = msg_dict.get("exec")

                if discovery_object is not None:
                    await ws.send_json({
                        "id": request_id,
                        "discovery_ok": { "nodes": [ self.__node.to_dict() ] },
                    })

                elif init_object is not None:
                    irm = InitRequest(init_object["node_id"], init_object["node_type"])
                    irm.exec_inputs = init_object["exec_inputs"]
                    irm.exec_outputs = init_object["exec_outputs"]
                    await ws.send_json({
                        "id": request_id,
                        "init_ok": {},
                    })

                elif exec_object is not None:
                    exec_id = exec_object.get("exec_id")
                    time = exec_object.get("time")
                    inputs = exec_object.get("inputs")

                    if exec_id is not None and \
                        time is not None and \
                            inputs is not None:
                        exec_resp = ExecResponse()
                        exec_resp.time = time
                        exec_resp.exec_id = 0

                        # Execute callback function and return ExecResponse object
                        out = self.__callback(*inputs)
                        if isinstance(out, tuple):
                            exec_resp.outputs = out
                        else:
                            exec_resp.outputs = (out, )

                        await ws.send_json({
                            "id": request_id,
                            "exec_ok": exec_resp.to_dict(),
                        })
                    else:
                        print('ExecRequest has invalid payload')

            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('Websocket connection closed with exception %s' % ws.exception())

        return ws

    def create_runner(self):
        app = web.Application()
        app.add_routes([
            # web.get('/',   self.http_handler),
            web.get('/', self.websocket_handler),
        ])
        return web.AppRunner(app)

    async def start_server(self, host=WS_HOST, port=WS_PORT):
        runner = self.create_runner()
        print("Listening on host {}:{}".format(host, port))
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

    def start(self):
        if self.__callback is None:
            log(TAG_HTTP_REQUEST, LogLevel.ERROR, ERROR_REGISTER_CALLBACK)
            sys.exit(1)
        # # Define the Unix domain socket path
        # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # unix_socket_path = f"/tmp/intrepid-ws-{timestamp}.sock"
        # # logger.info("Intrepid SDK started at {}".format(unix_socket_path))
        # log(TAG_HTTP_REQUEST, LogLevel.INFO, INFO_SDK_READY.format(unix_socket_path))

        # self.__unix_socket_path = unix_socket_path
        # asyncio.run(wsserver(self.__unix_socket_path))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_server())
        loop.run_forever()

    @staticmethod
    def config():
        """
        Return the current used intrepid configuration.
        @return: _IntrepidConfig
        """
        return Intrepid.__get_instance().configuration_manager.intrepid_config

    def register_node(self, node: Node):
        self.__node = node


    def register_callback(self, func):
        if self.__callback is None:
            log(TAG_HTTP_REQUEST, LogLevel.INFO, INFO_CALLBACK_REGISTERED)
            self.__callback = func
        else:
            if isinstance(self.__node_specs, Node):
                return Intrepid.__get_instance().__register_callback(func, self.__node_info)
            else:
                # logger.error(ERROR_REGISTER_CALLBACK)
                log(TAG_HTTP_REQUEST, LogLevel.ERROR, ERROR_REGISTER_CALLBACK)


    @staticmethod
    def create_qos(qos: Qos):
        """
        Return the details of this node
        @return: Status.
        """
        return Intrepid.__get_instance().create_qos(qos)

    def __node_specs(self, specs: Node):
        """
        Return the details of this node
        @return: Status.
        """

        # TODO this should be received from websocket client
        # TODO validate specs
        node = Node()
        node.add_input("in1", IntrepidType(Type.INTEGER))
        node.add_input("in2", IntrepidType(Type.INTEGER))
        node.add_output("out1", IntrepidType(Type.FLOAT))

        return Intrepid.__get_instance().__node_specs(node)

    # @staticmethod
    def info(self) -> Node:
        return Intrepid.__get_instance().node_specs

    @staticmethod
    def status():
        """
        Return the current SDK status.
        @return: Status.
        """
        return Intrepid.__get_instance().status

    # @staticmethod
    def write(self, target, data):
        """
        Write data to node output target.
        @return
        """
        return Intrepid.__get_instance().write(target, data)

    @staticmethod
    def stop():
        """
        Stop and reset the Intrepid instance.
        @return:
        """
        return Intrepid.__get_instance().stop()

    @staticmethod
    def __get_instance():
        """
        Get the intrepid singleton instance.

        :return: Intrepid
        """
        if not Intrepid.__instance:
            Intrepid.__instance = Intrepid.__Intrepid()
        return Intrepid.__instance

    @staticmethod
    def _update_status(new_status):
        Intrepid.__get_instance().update_status(new_status)

    class __Intrepid:

        def __init__(self):
            self.qos = None
            # Node input/output types and names
            self.node_specs = None
            self.status = Status.NOT_INITIALIZED
            self.configuration_manager = ConfigManager()
            self.device_context = {}

        def __node_specs(self, specs):
            self.node_specs = specs

        def __register_callback(self, func):
            is_valid = self.__validate_callback_parameters(self.node_specs, func)

            self.callback = func

        # @param_types_validator(True, str, str, [_IntrepidConfig, None])
        def start(self, env_id, api_key, intrepid_config):
            # self.update_status(intrepid_config, Status.STARTING)
            if not env_id or not api_key:
                raise InitializationParamError()
            self.update_status(intrepid_config, Status.STARTING)
            self.configuration_manager.init(env_id, api_key, intrepid_config, self.update_status)
            # self.update_status(intrepid_config, Status.STARTING)
            if self.configuration_manager.is_set() is False:
                self.update_status(self.configuration_manager.intrepid_config, Status.NOT_INITIALIZED)
                self.__log(TAG_INITIALIZATION, LogLevel.ERROR, ERROR_CONFIGURATION)

        def update_status(self, intrepid_config, new_status):
            if intrepid_config is not None and new_status is not None and new_status != self.status:
                old_status = self.status
                self.status = new_status
                log(TAG_STATUS, LogLevel.DEBUG, INFO_STATUS_CHANGED.format(str(new_status)), intrepid_config)
                if new_status is Status.READY:
                    log(TAG_INITIALIZATION, LogLevel.INFO,
                        INFO_READY.format(str(__version__), str(intrepid_config)))
                self.configuration_manager.intrepid_status_update(new_status, old_status)
                if intrepid_config.status_listener is not None:
                    intrepid_config.status_listener.on_status_changed(new_status)

        def close(self):
            self.status = Status.NOT_INITIALIZED
            # log(TAG_TERMINATION, LogLevel.INFO, INFO_STOPPED)
            self.configuration_manager.reset()

        def create_qos(self, qos: Qos):
            # TODO make request and set local if success
            self.qos = qos

        def stop(self):
            # Create STOP message
            msg = IntrepidMessage(Opcode.STOP, None, datetime.now(), self.node_id).serialize()

            # TODO send msg over websocket
            self.status = Status.NOT_INITIALIZED

        def info(self):
            self.node_specs

        def write(self, node_id, target, data):
            recipient = node_id + '/' + target
            msg = IntrepidMessage(Opcode.WRITE, payload=data, timestamp=datetime.now(), recipient=recipient, priority=0)
            # logger.debug(msg)
            log(TAG_HTTP_REQUEST, LogLevel.DEBUG, msg)

            # TODO send msg over websocket


        def __log(self, tag, level, message):
            try:
                configured_log_manager = self.configuration_manager.intrepid_config.log_manager
                if configured_log_manager is not None:
                    configured_log_manager.log(tag, level, message)
            except Exception as e:
                pass

        @staticmethod
        def __validate_callback_parameters(node: Node, callback: Callable) -> bool:
            """
            Validates if the parameters of the callback function match the inputs of the node.
            """
            # Get parameter names of the callback function
            callback_params = callback.__code__.co_varnames[:callback.__code__.co_argcount]

            # Get input names and data types of the node
            node_input_names = [input_element.name for input_element in node.inputs]
            node_input_data_types = [input_element.data_type for input_element in node.inputs]

            # Check if the number of parameters match
            if len(callback_params) != len(node_input_names):
                logger.error(ERROR_PARAM_NUM.format(len(node_input_names)))
                return False

            # Check if parameter names and data types match
            for param_name, input_name, input_type in zip(callback_params, node_input_names, node_input_data_types):
                if param_name != input_name:
                    # logger.error(ERROR_PARAM_NAME.format(param_name, input_name))
                    log(TAG_HTTP_REQUEST, LogLevel.ERROR, ERROR_PARAM_NAME.format(param_name, input_name))

                    # TODO check the type too
                    return False
                # You may want to add more sophisticated type checking here
                # For simplicity, I'm just checking if the data types match exactly
                if not isinstance(input_type, Type):
                    return False

            return True


