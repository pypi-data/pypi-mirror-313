#!/usr/bin/env python3
# coding: utf-8


import time
import socket
import adbutils
import tidevice
import subprocess
import platform

from functools import wraps
from threading import Thread, ThreadError
from tidevice._relay import relay

from .core._exceptions import *
from .core._exceptions import _async_raise
from .core._types import *


def socket_from_android_forward(port=27029, device_index: int = 0):
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = adb.device_list()

    if not devices:
        raise Exception("adbutils cannot find any Android devices")
    if device_index >= len(devices):
        raise ValueError("device index out of bounds")

    device = devices[device_index]
    device.forward("tcp:{}".format(port), "tcp:{}".format(port))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))

    return s


def remove_all_adb_forwards():
    popenargs = ["adb", "forward", "--remove-all"]
    if platform.system().lower() == "windows":
        popenargs = ["cmd", "/c"] + popenargs

    try:
        result = subprocess.run(popenargs, stdout=subprocess.PIPE, check=True)
        if not result.returncode:
            logger.info("Removed all adb forwards.")
        else:
            logger.error("Error removing adb forwards.")
    except subprocess.CalledProcessError as e:
        logger.error_handler(e)


def socket_from_ios_relay(port=27029, device_index: int = 0):
    devices = tidevice.Usbmux().device_list()

    if not devices:
        raise Exception("adbutils cannot find any iOS devices")
    if device_index >= len(devices):
        raise ValueError("device index out of bounds")

    device = devices[device_index]
    d = tidevice.Device(device.udid)
    relay(d, port, port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))

    return s


def hold(
    timeout: float = 10,
    retry: int = 1,
    interval: float = 0.1,
    timeout_error: Exception = None,
    loop_only_with_exc: bool = True,
    new_thread: bool = True,
    raise_default_error: bool = False,
    check_alive_freq: float = 0.1,
    make_daemon: bool = True,
):
    """A general holder to automatically timeout and retry functions
    You can use it to solve:
        * APIs that have long wait time and need termination.
        * requests or inspections that might have infinite loops (due to continuous requests or bad timeout checks).
        * GAClient instance calls that need retries after errors raised.
    Usage:
        @hold(timeout = 10)
        def foo(*args, **kwargs):
            ...
    Args:
        timeout (float): holding time.
        retry (int): number of retries.
                     0 for unlimited retries.
                     default to be 1 (no retry).
        interval (float): time interval between each retry.
        timeout_error (Exception): exception to raise when timed out.
        loop_only_with_exc (bool): True for retrying only when meeting exceptions.
                                   False for always retrying unless returning sth. is not None.
        new_thread (bool): flag for creating new thread for your task.
                           False for running task in the main thread.
        ---------- (arguments that are NOT recommended to pass) ----------
        raise_default_error (bool): True for raise RuntimeError when timeout_error is not passed.
        check_alive_freq (float): thread life check frequncy.
        make_daemon (bool): set thread.daemon.
    Returns:
        None if your func times out, else returns what your func returns.
        Note that the thread will NOT be abruptly ternimated (unless the main thread is over) due to python thread-safety mechanism.
    """

    class ReturnableThread(Thread):
        """Derive threading.Thread() to catch the target's return value"""

        def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
            super().__init__(group, target, name, args, kwargs)
            self._return = None

        def _get_tid(self):
            if not self.is_alive():
                raise ThreadError("the thread is not alive")
            return self.ident

        def run(self):
            if self._target:
                self._return = self._target(*self._args, **self._kwargs)

        def join(self, timeout=None, *args) -> any:
            super().join(timeout=timeout, *args)
            return self._return

        def raiseExc(self, exctype):
            _async_raise(self._get_tid(), exctype)

    def exc_handler(e: Exception, f):
        error_msg = "{}: {}".format(e.__class__.__name__, str(e))
        logger.error(f"While holding {f.__name__}(), an error occured:\n{error_msg}")

    def timeout_handler(f):
        retry_hint = f", retry = {retry}" if retry > 0 else ""
        msg = f"Holding {f.__name__}() exceeded max time (timeout = {timeout:.1f}{retry_hint})"
        logger.error(msg)
        if not (raise_default_error or timeout_error):
            return
        if not timeout_error:
            raise RuntimeError(msg)
        raise timeout_error

    def decorated(f):
        if timeout < 0:
            raise ValueError("holder timeout cannot be less than 0 sec")
        if timeout_error and (not isinstance(timeout_error, Exception)):
            raise ValueError("Holder's timeout_error must be an Exception instance")

        @wraps(f)
        def wrapper(*args, **kwargs):
            """Hold the decorated func without using thread
            holding_time = max(timeout, func_running_time)
            Might be stuck in infinite loops or long wait
            """
            deadline, count = time.time() + timeout, 0
            # Check both timeout and retry count
            while time.time() < deadline and (count < retry if retry > 0 else True):
                try:
                    ret = f(*args, **kwargs)
                    if loop_only_with_exc or ret:
                        return ret
                except HoldExceededMaxTimeError as e:
                    return
                except Exception as e:
                    exc_handler(e, f)
                count += 1
                time.sleep(interval)
            timeout_handler(f)
            return

        @wraps(f)
        def thread_wrapper(*args, **kwargs):
            """Hold the decorated func using thread
            holding_time = min(timeout, func_running_time)
            Will not block the main thread after timeout
            Will not be stuck in infinite loops or long wait
            """

            def loop():
                count = 0
                while count < retry if retry > 0 else True:
                    try:
                        ret = f(*args, **kwargs)
                        if loop_only_with_exc or ret:
                            return ret
                    except HoldExceededMaxTimeError as e:
                        return
                    except Exception as e:
                        exc_handler(e, f)
                    count += 1
                    time.sleep(interval)
                timeout_handler(f)

            t = ReturnableThread(target=loop)
            t.daemon = make_daemon  # a daemon thread does not block the main thread from exiting
            t.start()
            deadline = time.time() + timeout
            # wait for timeout and do thread life check
            while time.time() < deadline and t.is_alive():
                time.sleep(check_alive_freq)
            # t being alive means the thread does not complete its execution yet.
            if t.is_alive():
                t.raiseExc(HoldExceededMaxTimeError)
                timeout_handler(f)
                return None
            return t.join()

        return thread_wrapper if new_thread else wrapper

    return decorated
