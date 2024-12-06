#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

import os
import time
import json
import select
import struct
import socket
import asyncio
import inspect
import threading
import itertools
from typing import Union, Callable, Dict, Tuple, Set, Any, Optional, List

from ._exceptions import logger, SocketInitException, SocketTimeoutException, SocketConnectionException


async def default_async_response_callback(json_resp: Dict[str, Any], binary_data: bytes) -> None:
    """Default callback function that logs the received response.

    Args:
        json_resp (Dict[str, Any]): The JSON response received.
        binary_data (bytes): The binary data received.
    """
    logger.info(f"Received response and doing nothing by default callback: {json_resp}")


def default_dispatch_completion(
    async_sock: AsyncSocket, dispatch: DispatchCallback, json_resp: dict, binary_data: bytes
):
    logger.info(f"Finished response handling and doing nothing by default completion.")


def dafault_empty_completion(_self: AsyncSocket):
    pass


class DispatchCallback:
    """Class for storing callback functions and their identifiers."""

    callback_function: Callable[[Dict, bytes], None]
    identifier: int
    use_coroutine: bool
    completion: Callable[[AsyncSocket, DispatchCallback, dict, bytes], None]

    def __init__(
        self,
        callback: Callable[[Dict, bytes], None] = default_async_response_callback,
        identifier: int = 0,
        use_coroutine: bool = True,
        completion: Callable[[AsyncSocket, DispatchCallback, dict, bytes], None] = default_dispatch_completion,
        *args,
        **kwargs,
    ) -> None:
        """Initialize the DispatchCallback with a callback function and an identifier.

        Args:
            callback (Callable[[Dict, bytes], None], optional):
                The callback function to be called. Defaults to default_callback.
            identifier (int, optional): The identifier for the callback function. Defaults to 0.
        """
        self.callback_function = callback
        self.identifier = identifier
        self.use_coroutine = use_coroutine
        self.completion = completion


class AsyncSocket:
    """Main thread and watch thread model
    ╔═════════════╗
    ║ Main thread ║
    ╚═════════════╝
     │ ┏━━━━━━━━━━━━━━━━━━━━┓
     ├─┫ Async Request Pool ┃        ┌─────────────┐      ┌────────────────┐
     │ ┗━━━━▲━━━━━━━━━━━━━━━┛        │             ◀──────┤   Async Send   ◀══(Request, Callback)═══
     │      └───{ReqId: Callback}────┤ Call Send() │      └────────────────┘
     │                               │             │
     │      ┌────{ReqId: Null}───────┤             ◀───────────────┐
     │      │                        └─────────────┘               │
     │ ┏━━━━▼━━━━━━━━━━━━━━━┓                             ┌────────┴───────┐
     ├─┫ Sync Response Pool ┣──────────Wait for────────┬──▶   Sync Send    ◀═══════(Request)════════
     │ ┗━━━━━━━━━━━━━━━━━━━━┛      {ReqId: Response}      └────────────────┘
     │                                                 │
     │ ┏━━━━━━━━━━━━━━━━━━━━┓                             ┌────────────────┐
     └─┫   Handlers Pool    ◀──────(Response)->bool────┼──│Register Handler│
       ┗━━━━━━━━━━━━━━━━━━━━┛                             └────────────────┘
                                                       │
                                                        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
    ╔════════════════╗
    ║  Watch thread  ║                                                              │
    ╚════════════════╝
          ┌─────────────┐       ┏━━━━━━━━━━━━━━━━━━┓            ┌────────────────┐  │
          │             │   ┌───▶  in Async Pool?  ┣───ReqId────▶  Run Callback  │
    ══════▶ Loop Recv() ├───┤   ┗━━━━━━━━━━━━━━━━━━┛            └────────────────┘  │
          │             │   │   ┏━━━━━━━━━━━━━━━━━━┓            ┌────────────────┐
          └─────────────┘   ├───▶  in Sync Pool?   ┣──Response──▶ Fill Sync Pool │─ ┘
                            │   ┗━━━━━━━━━━━━━━━━━━┛            └────────────────┘
                            │   ┏━━━━━━━━━━━━━━━━━━┓
                            │   ┃   Accepted by    ┃            ┌────────────────┐
                            └───▶     handlers     ┣──Response──▶  Run Handler   │
                                ┃ in Handler Pool? ┃            └────────────────┘
                                ┗━━━━━━━━━━━━━━━━━━┛
    """
    
    refresh_rate: float

    _sock: socket.socket
    _running: bool
    _thread_pool: Set[threading.Thread]
    _coroutine_loop: asyncio.AbstractEventLoop
    _coroutine_task_pool: Set[asyncio.Task]
    _thread_stop_completion: Callable[[AsyncSocket], None]
    _lock: threading.Lock

    """Request Pool
    This class is used to store the unfinished async request and response.

    Key:    
        Request ID (str)
    Val:
        Callback function:
        def callback(json_resp: Dict, binary_data: bytes)
    """
    _async_request_pool: Dict[str, DispatchCallback]

    """Sync Request Pool
    This class is used to store the unfinished sync request and response that block the main thread.

    Key: 
        Request ID (str)
    Val:
        Response, None or (json_resp, binary_data)
    """
    _sync_response_pool: Dict[str, Optional[Tuple[Dict, bytes]]]

    """Event Pool
    This class is used to store the subscibed event.

    Key: 
        Event name (str)
    Val:
        Callback function:
        def callback(json_resp: Dict, binary_data: bytes)
    """
    _response_handler_list: List[Callable[[Dict, bytes], bool]]

    def __init__(self, 
                 addr: Union[str, Tuple[str, int], socket.socket],
                 start_watch: bool = True,
                 refresh_rate: float = 100):
        """Initialize the socket connection based on the given address.

        Args:
            addr (Union[str, Tuple[str, int], socket.socket]):
                The address to connect to.
                Can be a string (host:port or unix socket path), a tuple (host, port), or a socket object.
            start_watch (bool): Start the watch thread immediately if True.
            refresh_rate (float): 
                The refresh rate of socket watch thread. Defaults to 100Hz.
                The time interval between each refresh = (1 / refresh_rate).
                The higher the rate is, the more accurate and frequent the socket receiving behaviors will be.
        """
        self.refresh_rate = refresh_rate
        
        self._id_iter = itertools.count()
        self._async_request_pool = {}
        self._sync_response_pool = {}
        self._response_handler_list = []
        self._thread_stop_completion = dafault_empty_completion
        self._running = False

        self._thread_pool = set()
        self._coroutine_task_pool = set()
        self._coroutine_loop = asyncio.new_event_loop()
        self._lock = threading.Lock()

        self.__init_socket_connection(addr)
        self.set_sock_timeout(1)

        threading.Thread(target=self._start_event_loop, daemon=True).start()

        if start_watch:
            self.watch()

    def __init_socket_connection(self, addr: Union[str, Tuple[str, int], socket.socket]):
        if isinstance(addr, socket.socket):
            self._sock = addr
        else:
            if isinstance(addr, str):
                if ":" in addr:
                    host, port = addr.split(":", 1)
                    addr = (host, int(port))
                    family = socket.AF_INET
                elif os.path.exists(addr):
                    family = socket.AF_UNIX
                else:
                    raise SocketInitException(f"socket unix:{addr} unable to connect")
            else:
                family = socket.AF_INET
            self._sock = socket.socket(family, socket.SOCK_STREAM)
            self._sock.connect(addr)

    @property
    def logger(self):
        return logger

    def set_sock_timeout(self, timeout: float):
        self._sock.settimeout(timeout)

    """
    PUBLIC:
    """

    def send(self, request: Dict, callback: Callable[[Dict, bytes], None] = default_async_response_callback) -> None:
        """Send an asynchronous request and register a callback function.

        Args:
            request (Dict): The request dictionary to send.
            callback (
                Callable[[Dict, bytes], None], optional
                async Callable[[Dict, bytes], None], optional
                ):
                The callback function to be called when the response is received.
                It could be a COROUTINE function or a normal one as you wish.
                The sender will automatically decide whether to run the callback in coroutines.
        """

        def async_send_completion(
            _async_sock: AsyncSocket, _dispatch: DispatchCallback, _json_resp: dict, _binary_data: bytes
        ):
            # Remove the request from the pool
            del _async_sock._async_request_pool[_json_resp.get("requestId")]

        request_id = self.__get_request_id_and_iter()
        request = self.__insert_request_id(request, request_id)
        self.__write(request)
        self._async_request_pool[request_id] = DispatchCallback(
            callback=callback,
            identifier=request_id,
            use_coroutine=inspect.iscoroutinefunction(callback),
            completion=async_send_completion,
        )
        logger.debug(f"Send: {self.__pretty_json(request)}, callback = {callback.__name__}")

    def sync_send(
        self, request: Dict, timeout: float = 10.0, raise_timeout_error: bool = True
    ) -> Tuple[Dict, Optional[bytes]]:
        """Send a synchronous request and wait for the response while blocking the calling thread.

        Args:
            request (Dict): The request dictionary to send.
            timeout (float, optional): The maximum time to wait for the response in seconds. Defaults to 10.0.

        # Returns:
            Tuple[Dict, Optional[bytes]]: A tuple containing the JSON response and any binary data received.
        """
        request_id = self.__get_request_id_and_iter()
        self._sync_response_pool[request_id] = None
        self.__write(self.__insert_request_id(request, request_id))
        logger.debug(f"Sync send: {self.__pretty_json(request)}")

        deadline = time.time() + timeout
        while True and time.time() < deadline:
            if self._sync_response_pool[request_id]:
                break

        ret: Optional[Tuple[Dict, Optional[bytes]]] = self._sync_response_pool[request_id]
        if not ret:  # Timeout
            logger.error(f"Failed to receive sync request. Blocked for {timeout} second. Request = {request}")
            if raise_timeout_error:
                raise SocketTimeoutException(f"Request timeout. Request = {request}")
            return {}, None  # FIXME: Should return a empty dict with valid keys to prevent KeyError
        logger.debug(f"Successfully received sync response. Json response = {ret[0]}")

        # Remove the response from the pool
        del self._sync_response_pool[request_id]
        return ret

    def close(self):
        def close_socket_completion(_self: AsyncSocket):
            _self._sock.close()
            _self._thread_stop_completion = dafault_empty_completion

        self._thread_stop_completion = close_socket_completion
        self.stop_watch()
        self.stop_event_loop()

    def restart(self, socket: socket.socket, start_watch: bool = True):
        self._sock = socket
        if start_watch:
            self.watch()

    def watch(self):
        """Start the watcher thread to receive messages from the server."""
        if self._running:
            return
        self._running = True
        watcher_thread = threading.Thread(target=self._thread_watch)
        watcher_thread.daemon = True
        watcher_thread.start()
        return self

    def stop_watch(self):
        self._running = False

    def add_to_async_request_pool(self, request_id: str, dispatch_callback: DispatchCallback):
        self._async_request_pool[request_id] = dispatch_callback

    def remove_from_async_request_pool(self, request_id: str):
        del self._async_request_pool[request_id]

    def register_response_handler(self, handler: Callable[[Dict, bytes], bool]):
        self._response_handler_list.append(handler)

    def unregister_response_handler(self, index: int):
        self._response_handler_list.pop(index)

    def get_registered_handler(self) -> Callable[[Dict, bytes], bool]:
        return self._response_handler_list

    def _start_event_loop(self):
        asyncio.set_event_loop(self._coroutine_loop)
        self._coroutine_loop.run_forever()

    def stop_event_loop(self):
        """Stop the asyncio event loop running in a separate thread."""
        if self._coroutine_loop.is_running():
            self._coroutine_loop.call_soon_threadsafe(self._coroutine_loop.stop)

    """
    PROTECTED:
    """

    def _thread_watch(self):
        """The thread inner func to call _get() infinitely"""
        while self._running or len(self._async_request_pool) > 0 or len(self._sync_response_pool) > 0:
            try:
                ready_to_read, _, _ = select.select([self._sock], [], [], 1 / self.refresh_rate)
                if ready_to_read:
                    self._receive()
            except Exception as e:
                logger.error(e)
                raise e from None
        logger.info("Watch thread stopped.")
        self._thread_stop_completion(self)

    def _coroutine_processor(self, dispatch: DispatchCallback, json_resp: dict, binary_body: bytes):
        coro = dispatch.callback_function(json_resp, binary_body)
        future = asyncio.run_coroutine_threadsafe(coro, self._coroutine_loop)
        future.add_done_callback(lambda fut: self._coroutine_task_pool.discard(fut))
        self._coroutine_task_pool.add(future)

    def _thread_processor(self, dispatch: DispatchCallback, json_resp: dict, binary_body: bytes):
        def thread_target():
            dispatch.callback_function(json_resp, binary_body)
            self._thread_pool.discard(thread)

        thread = threading.Thread(target=thread_target)
        self._thread_pool.add(thread)
        thread.start()

    def _receive(self):
        """Read the response from the server and process it based on the request ID."""
        json_resp, binary_body = self.__read()
        request_id = json_resp.get("requestId")
        if not request_id:
            logger.error(f"Bad response without any request ID. Json response = {json_resp}")
            return

        # 1. Handle async request
        if request_id in self._async_request_pool:
            logger.debug(f"Successfully received async response. Json response = {json_resp}")
            dispatch: DispatchCallback = self._async_request_pool[request_id]

            # 1.1 The request callback is a coroutine function
            if dispatch.use_coroutine:
                self._coroutine_processor(dispatch, json_resp, binary_body)
                logger.debug(
                    f"Executed callback func <{dispatch.callback_function.__name__}> "
                    + f"for request ID = {request_id} as a coroutine."
                )

            # 1.2 The request callback is a normal function
            else:
                self._thread_processor(dispatch, json_resp, binary_body)
                logger.debug(
                    f"Executed callback func <{dispatch.callback_function.__name__}> "
                    + f"for request ID = {request_id} in a separate thread."
                )

            # Call completion
            dispatch.completion(self, dispatch, json_resp, binary_body)

        # 2. Handle sync request
        elif request_id in self._sync_response_pool:
            self._sync_response_pool[request_id] = (json_resp, binary_body)
            logger.debug(f"Stored response for sync request ID = {request_id}.")

        # 3. Registered handler
        elif self._send_request_to_handlers(json_resp, binary_body):
            logger.info(f"Successfully send subscription to registerd handlers. Json subscription = {json_resp}. ")

        else:
            logger.error(f"Received request with unknown request ID = {request_id}. Json response = {json_resp}")

    def _send_request_to_handlers(self, json_resp: Dict, binary_body: bytes) -> bool:
        is_accepted: bool = False
        accepted_times: int = 0
        accepted_by: List[str] = []
        for handler in self._response_handler_list:
            # handler: Callable[[Dict, bytes], bool]
            if handler(json_resp, binary_body):
                is_accepted = True
                accepted_times += 1
                accepted_by.append(handler.__name__)
        logger.debug(
            f"Registered handlers finished handling subscription. "
            + f"Accepted times = {accepted_times}. Receiver list = {accepted_by}"
        )
        return is_accepted

    """
    PRIVATE:
    """

    def __write(self, request: dict) -> int:
        """Send a request to the server.

        Args:
            request (dict): A dictionary containing the command and its arguments.

        Returns:
            int: The length of the sent data.
        """
        request = json.dumps(request).encode("utf-8")
        data_len = len(request)
        packed_len = struct.pack("<I", data_len)
        with self._lock:
            self._sock.sendall(packed_len + request)
        return data_len

    def __read(self) -> Tuple[dict, bytes]:
        """Receive a response from the server.

        Returns:
            Tuple[dict, bytes]: A tuple containing the JSON response and any binary data received.
        """
        with self._lock:  # Protect read operation
            body_size = struct.unpack("<I", self.__read_bytes(4))[0]
            json_size = struct.unpack("<I", self.__read_bytes(4))[0]
            json_resp = json.loads(self.__read_bytes(json_size))
            logger.debug(
                f"Recv: len(body) = {body_size:d}, "
                + f"len(json) = {json_size:d}, "
                + f"json: {str(self.__pretty_json(json_resp))[:500]}"
            )
            binary_data = b""
            if body_size >= json_size + 4:
                binary_data = self.__read_bytes(body_size - json_size - 4)
            else:
                raise SocketConnectionException(f"Read error: len(body) = {body_size}, len(json) = {json_size}")
        return json_resp, binary_data

    def __read_bytes(self, size: int) -> bytes:
        """Read a specified number of bytes from the socket.

        Args:
            size (int): The number of bytes to read.

        Returns:
            bytes: The bytes read from the socket.
        """
        buffer = b""
        while len(buffer) < size:
            packet = self._sock.recv(size - len(buffer))
            if not packet:
                raise SocketConnectionException("socket connection broken")
            buffer += packet
        return buffer

    def __insert_request_id(self, request: dict, id: str) -> dict:
        """Insert a request ID into a given request dictionary.

        Args:
            request (dict): The request dictionary to insert the request ID into.

        Returns:
            dict: The request dictionary with the inserted request ID.
        """
        request_id = id
        request["requestId"] = request_id
        return request

    def __get_request_id_and_iter(self) -> str:
        """Get the next request ID and increment the iterator.

        Returns:
            str: The next request ID.
        """
        return str(next(self._id_iter))

    def __pretty_json(self, contents: Any) -> str:
        return json.dumps(contents, indent=4, sort_keys=True)
