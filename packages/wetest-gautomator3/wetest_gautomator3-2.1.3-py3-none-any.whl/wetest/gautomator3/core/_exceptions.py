#!/usr/bin/env python3
# coding: utf-8


import logging
import time
import inspect
import ctypes


class GAutomatorException(Exception):
    pass


class NotImplementedException(GAutomatorException):
    pass


"""
Client exceptions
"""


class ClientInitException(GAutomatorException):
    pass


class EngineNotReadyException(GAutomatorException):
    pass


class NoSuchElementException(GAutomatorException):
    pass


"""
Socket exceptions
"""


class SocketInitException(GAutomatorException, OSError):
    pass


class SocketTimeoutException(GAutomatorException, TimeoutError):
    pass


class SocketConnectionException(GAutomatorException, ConnectionError):
    pass


"""
GALogger
"""


class GALogger(logging.getLoggerClass()):
    def __init__(self, name: str = "GAutomator"):
        self.formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.isShowLog = True
        self.logger = logging.getLogger(name)
        self.set_log_level(logging.INFO)

        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def set_log_level(self, level):
        self.logger.setLevel(level)

    def enable_log(self):
        self.isShowLog = True
        self.set_log_level(logging.INFO)

    def disable_log(self):
        self.isShowLog = False
        self.set_log_level(logging.CRITICAL)

    def debug(self, msg, *args):
        if self.isShowLog:
            self.logger.debug(msg, *args)

    def info(self, msg, *args):
        if self.isShowLog:
            self.logger.info(msg, *args)

    def warning(self, msg, *args):
        if self.isShowLog:
            self.logger.warning(msg, *args)

    def error(self, msg, *args):
        if self.isShowLog:
            self.logger.error(msg, *args)

    # GAutomatorException error handler

    def error_handler(self, e: GAutomatorException):
        self.error(f"{e.__class__.__name__}: {str(e)}")

    # def error_handler(self, e: GAutomatorException, request: dict):
    #     suffix = f". Error occured when requesting with: {str(request)}"
    #     self.warning(f"{e.__class__.__name__}: {str(e)}" + suffix)


logger = GALogger(name="GAutomator")
logger.set_log_level(logging.INFO)


"""
Async Raise Tool
"""


def _async_raise(tid, exctype, traceback: bool = False):
    """Raises an exception in the threads with id tid"""
    # print(f"raise {str(exctype)} in thread {tid}")
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    if traceback:
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    else:
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(SystemExit))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
