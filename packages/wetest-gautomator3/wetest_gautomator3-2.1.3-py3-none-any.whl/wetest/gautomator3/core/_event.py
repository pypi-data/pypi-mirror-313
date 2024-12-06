#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

import json
import asyncio
import logging
import threading

from abc import ABC, abstractmethod
from typing import Dict, Callable
from numbers import Number
from xml.dom import minidom
from lxml import etree

from ._types import *
from ._exceptions import *
from ._socket import AsyncSocket
from ._types import RespStatus as Resp


g_SHOULD_HANDLE_EVENT_WITH_MULTITHREAD = True
g_event_pool: Dict[str, Callable[[GAEvent], None]] = {}
g_coroutine_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()


def _start_event_loop():
    asyncio.set_event_loop(g_coroutine_loop)
    g_coroutine_loop.run_forever()


def launch():
    threading.Thread(target=_start_event_loop, daemon=True).start()


def event_response_handler(json_resp: Dict, binary_body: bytes) -> bool:
    body = json_resp.get("body")
    if not body or not isinstance(body, Dict):
        return False
    event_name, message, timestamp = body.get("name", ""), body.get("msg", ""), body.get("timestamp", "")
    if event_name not in g_event_pool:
        return False
    callback_function = g_event_pool.get(event_name)
    if not g_SHOULD_HANDLE_EVENT_WITH_MULTITHREAD:
        coro = callback_function(GAEvent(event_name, message, timestamp))
        asyncio.run_coroutine_threadsafe(coro, g_coroutine_loop)
    else:
        thread = threading.Thread(target=callback_function, args=(GAEvent(event_name, message, timestamp),))
        thread.start()
    return True


# Launch the coroutine thread both as the main entrance or as a module imported
launch()


class GAEvent:
    event_name: str
    message: str
    timestamp: str

    def __init__(self, event_name: str, message: str, timestamp: str) -> None:
        self.event_name, self.message, self.timestamp = event_name, message, timestamp


class GAEventHandler(ABC):
    def __init__(
        self,
        socket: AsyncSocket,
    ):
        self._async_socket = socket

    @classmethod
    def event_response_handler(cls) -> Callable[[Dict, bytes], bool]:
        return event_response_handler

    def subscribe(self, event_name: str, event_callback: Callable[[GAEvent], None]) -> None:
        if not isinstance(event_callback, Callable):
            raise TypeError(f"{event_callback.__class__} is not a valid event callback function!")
        request = {"object": "gameLogic", "command": "subscribeUserEvent", "body": {"str": event_name}}
        json_resp, _ = self._async_socket.sync_send(request)
        if Resp.json_status(json_resp):
            # Register to event pool!
            g_event_pool[event_name] = event_callback
            logger.info(
                f"Successfully subscribed event <{event_name}> "
                + f"with callback function <{event_callback.__name__}>. "
                + f"Currently subscribed {len(g_event_pool)} events."
            )
        else:
            logger.error(f"Failed to subscribe event <{event_name}>. Response: {json_resp}")

    def unsubscribe(self, event_name: str) -> None:
        def unsubscribe_callback(json_resp: dict, _: bytes):
            if Resp.json_status(json_resp):
                del g_event_pool[event_name]
                logger.info(f"Successfully unsubscribed event <{event_name}>")
            else:
                logger.error(f"Failed to unsubscribe event <{event_name}>. Response: {json_resp}")

        request = {"object": "gameLogic", "command": "unSubscribeUserEvent", "body": {"str": event_name}}
        self._async_socket.send(request, unsubscribe_callback)

    def unsubscribe_all(self):
        event_names = g_event_pool.keys()
        for event_name in event_names:
            self.unsubscribe(event_name)
