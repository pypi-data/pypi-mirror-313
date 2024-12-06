#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

import time
import socket
import typing
from numpy import ndarray
from typing import Union, Callable, Tuple, List
from lxml import etree
from wetest.gautomator3.core._exceptions import GAutomatorException

from wetest.gautomator3.utils import Context, GAutomatorException, socket

from .core._socket import AsyncSocket, DispatchCallback, default_async_response_callback
from .core._exceptions import *
from .core._types import *
from .core._types import *
from .core._types import Context, RespStatus as Resp
from .core._event import GAEventHandler, GAEvent
from .core._reflection import GameMethods

from .utils import *
from .element import GAElement


class GAClient:
    def __init__(
        self,
        addr: Union[str, Tuple[str, int], socket.socket],
        timeout: float = 15,
        auto_connect: bool = True,
        log_request: bool = False,
    ):
        self._addr = addr
        self._log_request = log_request
        self._auto_connect = auto_connect
        self._timeout = timeout
        self._sock: AsyncSocket = None
        self._event_handler: GAEventHandler = None

        if auto_connect:
            self.connect(timeout=timeout, check_engine=True)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self, timeout: float = None, check_engine: bool = False) -> bool:
        timeout = self._timeout if timeout is None else timeout
        self.init_socket(timeout)
        if check_engine:
            self.check_engine(timeout)

    def close(self):
        self._sock.close()

    def enable_log(self):
        logger.enable_log()

    def disable_log(self):
        logger.disable_log()

    def enable_request_log(self):
        self._log_request = True
        self._sock._log = True

    def disable_request_log(self):
        self._log_request = False
        self._sock._log = False

    def enable_socket_log(self):
        self._sock.logger.enable_log()

    def disable_socket_log(self):
        self._sock.logger.disable_log()

    @property
    def logger(self):
        return logger

    @classmethod
    def mock(cls, source: str, enable_log: bool = True) -> GAClient:
        class AsyncSocketMock(AsyncSocket):
            def __init__(self, addr: Union[str, Tuple[str, int], socket.socket]):
                pass

            def sync_send(
                self, request: dict, timeout: float = 10.0, raise_timeout_error: bool = False
            ) -> Tuple[dict, bytes]:
                print(f"Mocked socket receives {request}")
                return {"status": RespStatus.MOCK, "body": None}, None

        class GAClientMock(GAClient):
            def __init__(self, source: str, enable_log: bool = True):
                super().__init__(None, auto_connect=False, log_request=enable_log)
                self.source = source
                self._sock = AsyncSocketMock(None)

            def get(
                self,
                request: dict,
                *args,
                **kwargs,
            ) -> Tuple[dict, bytes]:
                return self._sock.sync_send(request)

            def page_source(self, context: Context) -> str:
                return self.source

        return GAClientMock(source, enable_log=enable_log)

    def init_socket(self, timeout: float):
        @hold(
            timeout=timeout,
            retry=5,
            interval=1,
            timeout_error=ClientInitException("tcp connection refused"),
            new_thread=False,
        )
        def init_socket_hold():
            self._sock = AsyncSocket(self._addr, start_watch=True)
            self._sock.register_response_handler(handler=GAEventHandler.event_response_handler())
            self._event_handler = GAEventHandler(self._sock)
            return

        logger.info(f"initializing sokect (timeout = {timeout:.1f}s)")
        init_socket_hold()

    def check_engine(self, timeout: float):
        is_ready, version = self.engine_info()
        if not is_ready:
            raise EngineNotReadyException("engine offline")
        logger.info(f"engine online: {version}")

    def set_client_timeout(self, timeout: float):
        self._timeout = timeout

    def get(
        self,
        request: dict,
        async_get: bool = False,
        async_callback: Callable = default_async_response_callback,
        *args,
        **kwargs,
    ) -> Tuple[dict, bytes]:
        """
        Send a request to the server and get the response.

        Args:
            request (dict): Request dictionary.
            async_get (bool, optional): Whether to get asynchronously, default is False.
            async_callback (Callable, optional): Asynchronous response callback, default is default_async_response_callback.
            *args: Variable arguments.
            **kwargs: Keyword arguments.

        Returns:
            Tuple[dict, bytes]: Returns a Tuple containing JSON response and binary data.
        """
        assert self._sock, "socket not initialized, execute GAClient.connect() first."
        if async_get:
            return self._sock.send(request, async_callback)
        return self._sock.sync_send(request, self._timeout)

    def subscribe(self, event_name: str, event_callback: Callable[[GAEvent], None]) -> None:
        """
        Send a request to the server and get the response.

        Args:
            request (dict): Request dictionary.
            async_get (bool, optional): Whether to get asynchronously, default is False.
            async_callback (Callable, optional): Asynchronous response callback, default is default_async_response_callback.
            *args: Variable arguments.
            **kwargs: Keyword arguments.

        Returns:
            Tuple[dict, bytes]: Returns a Tuple containing JSON response and binary data.
        """
        return self._event_handler.subscribe(event_name, event_callback)

    def unsubscribe(self, event_name: str) -> None:
        """
        Send a request to the server and get the response.

        Args:
            request (dict): Request dictionary.
            async_get (bool, optional): Whether to get asynchronously, default is False.
            async_callback (Callable, optional): Asynchronous response callback, default is default_async_response_callback.
            *args: Variable arguments.
            **kwargs: Keyword arguments.

        Returns:
            Tuple[dict, bytes]: Returns a Tuple containing JSON response and binary data.
        """
        return self._event_handler.subscribe(event_name)

    def unsubscribe_all_event(self):
        """
        Unsubscribe from all events.
        """
        return self._event_handler.unsubscribe_all()

    """ ===========================================================================
        Add GAutomator Public <Request> APIs Here!
        Usage:
            json_response: dict, binary_data: bytes = self.get(request_body: dict)
        ===========================================================================
    """

    def page_source(self, context: Context) -> str:
        """
        Get the page source of the specified context.

        Args:
            context (Context): The context to get the page source from.

        Returns:
            str: The page source as a string.
        """
        json_resp, _ = self.get({"object": context, "command": "getSource"})
        return json_resp["body"]["source"]

    def engine_info(self) -> Tuple[bool, str]:
        """
        Get engine status and version.

        Returns:
            Tuple[bool, str]: Response status and a string of version info.
        """
        json_resp, _ = self.get({"object": "status", "command": "engine"})
        return Resp.json_status(json_resp), json_resp["body"]["version"]

    def screenshot(self, save_path: str = None, all_windows: bool = False) -> bytes:
        """
        Take screenshot and save to path. For slate only

        Args:
            save_path (str, optional): Save path for the screenshot to be taken. Defaults to None.
            all_windows (bool, optional): True for capture all windows under slate. Defaults to False.

        Returns:
            bytes: Decoded, raw bytes data.
        """
        request = {"object": "slate", "command": "screenshot"}
        if all_windows:
            request["body"] = {"showAllWindows": True}
        json_resp, data = self.get(request)
        logger.info(f"screenshot {'succeeded' if Resp.binary_status(json_resp) else 'failed'}")
        if save_path:
            with open(save_path, "wb") as img:
                img.write(data)
            logger.info(f"Screenshot saved to path <{save_path}>")
        return data

    def find_element(
        self,
        context: Context = Context.Slate,
        find_by: By = By.Name,
        value: str = None,
        timeout: float = 10,
        interval: float = 1.0,
        retry: int = 0,
    ) -> GAElement:
        """
        Finds game element based on the specified locator strategy and value.

        Args:
            value (str): The value to search for. Defaults to None.
            find_by (By): The locator strategy. Defaults to By.Name.
            object (Context): The context to search in. Defaults to Context.Slate.
            timeout (float): Raise error after timeout
        Returns:
            Optional[GameElement]: The game element that were found, or None.
        """
        res: List[GAElement] = self.find_elements(context, find_by, value, timeout, interval, retry)
        if res:
            return res[0]
        return None

    def find_elements(
        self,
        context: Context = Context.Slate,
        find_by: By = By.Name,
        value: str = None,
        timeout: float = 10,
        interval: float = 1.0,
        retry: int = 0,
    ) -> List[GAElement]:
        """
        Finds game elements based on the specified locator strategy and value.

        Args:
            value (str): The value to search for. Defaults to None.
            find_by (By): The locator strategy. Defaults to By.Name.
            object (Context): The context to search in. Defaults to Context.Slate.
            timeout (float): Raise error after timeout
        Returns:
            List[GameElement]: A list of the game element that were found.
        """
        find_timeout = timeout if timeout else self._timeout

        def find(value: str, find_by: By, context: Context):
            source = self.page_source(context)
            return GAElement._find_elements(
                by=find_by,
                value=value,
                socket=self._sock,
                xml=source,
                context=context,
            )

        @hold(
            timeout=find_timeout,
            retry=retry,
            interval=interval,
            loop_only_with_exc=False,
            timeout_error=NoSuchElementException(f"Cannot find <{value}> by <{find_by}>"),
        )
        def find_elements_hold():
            res = find(value=value, find_by=find_by, context=context)
            if res:
                return res

        # find_elements main body here
        return find_elements_hold()

    def exist(self) -> bool:
        pass

    def get_parent(self, element: GAElement) -> GAElement:
        """
        Get the parent element of the given element.

        Args:
            element (GAElement): The element to find the parent of.

        Returns:
            GAElement: The parent element of the given element.
        """
        return self.get_parents(element)[0]

    def get_parents(self, element: GAElement) -> List[GAElement]:
        """
        Get all parent elements of the given element.

        Args:
            element (GAElement): The element to find the parents of.

        Returns:
            List[GAElement]: A list of parent elements of the given element.
        """

        def find_by_attribute_and_get_parents(find_by: str = None, value: str = None):
            res = []
            if type in (ElementType.UWIDGET, ElementType.SWIDGET, ElementType.GAMEOBJECT):
                root = etree.XML(source)
                all = root.findall(".//" + type)
                for element in all:
                    if element.get(find_by) == value:
                        parent = element.getparent()
                        if parent and parent.tag == type:
                            res.append(GAElement._construct_element_from_lxml(parent, type, self._sock, context))
                            return res
            return res

        # Parse search keywords from the GameElement
        context, type = element._context, element._element_type
        source = self.page_source(context)
        if type == ElementType.UWIDGET:
            find_by, value = "uniqueID", str(element.unique_id)
        elif type == ElementType.SWIDGET:
            find_by, value = "address", element.address
        else:
            return []

        # Dive into the xml tree
        all, res = etree.XML(source).findall(".//" + type), []
        for each in all:
            if each.get(find_by) == value:
                parent = each.getparent()
                if parent is not None and parent.tag == type:
                    res.append(GAElement._construct_element_from_lxml(parent, type, self._sock, context))

        # Return
        if len(res) > 0:
            return res
        else:
            raise NoSuchElementException()

    def is_alive(self) -> bool:
        """
        Check if the device is online.

        Returns:
            bool: True if the device is online, False otherwise.
        """
        # This function checks if the device is alive by sending a ping command and waiting for a response.
        request = {"object": "status", "command": "isAlive"}
        json_resp, _ = self.get(request)
        return json_resp["status"]

    def cv_find(
        self, pattern: Union[ndarray, str], to_gray=False, match_distance: float = 0.6, draw_matches: bool = False
    ):
        """
        Find a template match in the current screenshot.
        Args:
            pattern (Union[ndarray, str]): The pattern to match.
            to_gray (bool, optional): True for convert to gray scale. Defaults to False.
            match_distance (float, optional):
                The match threshold. The minor the match more strict.
                Defaults to 0.6.
            draw_matches (bool, optional):
                True for pop up a drawing match window, which will BLOCK THE MAIN THREAD.
                Defaults to False.
        Raises:
            ImportError: Raised when wetest-cvlib, python-opencv or numpy cannot be imported.
        Returns:
            Tuple[float, float]: Position of the match.
        """
        try:
            import cv2 as cv, wetest.cvlib as cvlib, numpy as np
        except ImportError as e:
            logger.error(CVLIB_IMPORT_ERROR)
            raise e from None

        src_bytes = self.screenshot()
        src = cv.imdecode(np.frombuffer(src_bytes, np.uint8), -1)
        return cvlib.cv.sift_match(pattern, src, to_gray, match_distance, draw_matches)

    def cv_click(self, pattern: Union[ndarray, str], duration: float = 0.1, to_gray=False, match_distance: float = 0.6):
        """
        Click the matched point in the current screenshot.
        Args:
            pattern (Union[ndarray, str]): The pattern to match.
            duration (float, optional): The duration of the click. Defaults to 0.1.
            to_gray (bool, optional): True for convert to gray scale. Defaults to False.
            match_distance (float, optional):
                The match threshold. The minor the match more strict.
                Defaults to 0.6.
        Raises:
            ImportError: Raised when wetest-cvlib, python-opencv or numpy cannot be imported.
        """
        return self.touch(pos=self.cv_find(pattern, to_gray, match_distance), duration=duration)

    def cv_find_by_template(
        self,
        pattern: Union[ndarray, str],
        threshold: float = 0.8,
        pos: Union[tuple, list] = None,
        pos_weight: float = 0.05,
        ratio_lv: int = 21,
        is_translucent: bool = False,
        to_gray: bool = False,
        tpl_l: Union[ndarray, str] = None,
        deviation: Union[tuple, list] = None,
        scale: Tuple[float, float, float, float] = None,
        detail: bool = False,
    ) -> Tuple[float, float]:
        try:
            import cv2 as cv, wetest.cvlib as cvlib, numpy as np
        except ImportError as e:
            logger.error(CVLIB_IMPORT_ERROR)
            raise e from None

        src_bytes = self.screenshot()
        src = cv.imdecode(np.frombuffer(src_bytes, np.uint8), -1)

        def get_match_res(_img):
            return cvlib.cv.template_match(
                template=_img,
                source=src,
                threshold=threshold,
                pos=pos,
                pos_weight=pos_weight,
                ratio=ratio_lv,
                is_translucent=is_translucent,
                to_gray=to_gray,
                tpl_l=tpl_l,
                deviation=deviation,
                detail=True,
            )

        res = None
        if scale:
            """
            The arg 'scale' represents: w'/w, h'/h, x'/w, y'/h
            This arg should be automatically generated by WeAutomator
            """
            from wetest.cvlib.core.utils import resize_image

            screen_x, screen_y = self._get_screen_size()
            x_relative, y_relative, _, _ = scale
            x_ratio, y_ratio = x_relative * screen_x / pattern.shape[1], y_relative * screen_y / pattern.shape[0]

            images, max_coff = [resize_image(pattern, x_ratio), resize_image(pattern, y_ratio)], 0
            for image in images:
                temp: dict = get_match_res(image)
                if temp.get("val", 0) > max_coff:
                    res = temp
                    max_coff = temp.get("val", 0)
        else:
            res = get_match_res(pattern)

        if not res:
            logger.error(f"cv find not found.")
            return None
        return res if detail else res["pos"]

    def cv_touch_by_template(
        self,
        pattern: Union[ndarray, str],
        duration: float = 0.1,
        threshold: float = 0.8,
        pos: Union[tuple, list] = None,
        pos_weight: float = 0.05,
        ratio_lv: int = 21,
        is_translucent: bool = False,
        to_gray: bool = False,
        tpl_l: Union[ndarray, str] = None,
        deviation: Union[tuple, list] = None,
        scale: Tuple[float, float, float, float] = None,
    ):
        self.touch(
            pos=self.cv_find_by_template(
                pattern=pattern,
                threshold=threshold,
                pos=pos,
                pos_weight=pos_weight,
                ratio_lv=ratio_lv,
                is_translucent=is_translucent,
                to_gray=to_gray,
                tpl_l=tpl_l,
                deviation=deviation,
                scale=scale,
                detail=False,
            ),
            duration=duration,
        )

    def ocr_get_text(self, text_type: str = "ch"):
        """
        Find target text by OCR in the current screenshot.

        Args:
            text_type (str, optional): The type of text. Defaults to "ch".
        Raises:
            ImportError: Raised when wetest-cvlib, python-opencv or numpy cannot be imported.
        Returns:
            list[OcrItem]: A list of a dataclass.
        """
        try:
            import cv2 as cv, wetest.cvlib as cvlib, numpy as np
        except ImportError as e:
            logger.error(CVLIB_IMPORT_ERROR)
            raise e from None

        src_bytes = self.screenshot()
        src = cv.imdecode(np.frombuffer(src_bytes, np.uint8), -1)
        res = cvlib.ocr.get_text(src, text_type=text_type)

        if not res:
            logger.error(f"no text found on the current screen.")
            return None
        return res

    def ocr_find(
        self,
        text: str,
        regular: bool = True,
        detail: bool = True,
    ) -> list:
        """
        Find target text by OCR in the current screenshot.

        Args:
            text (str): The target text.
            regular (bool, optional): True for ise regular expression to match. Defaults to True.
            detail (bool, optional):
                True for return a list of dataclass else a list of tuple(x, y).
                Defaults to True.
        Raises:
            ImportError: Raised when wetest-cvlib, python-opencv or numpy cannot be imported.
        Returns:
            list[OcrItem]: A list of a dataclass if detail == True else a list of tuple(x, y).
        """
        try:
            import cv2 as cv, wetest.cvlib as cvlib, numpy as np
        except ImportError as e:
            logger.error(CVLIB_IMPORT_ERROR)
            raise e from None

        src_bytes = self.screenshot()
        src = cv.imdecode(np.frombuffer(src_bytes, np.uint8), -1)
        res = cvlib.ocr.find_by_text(img=src, text=text, regular=regular)

        if not res:
            logger.error(f"ocr text '{text}' not found on the current screen.")
            return None

        if detail:
            return res

        ret = []
        for each in res:
            x, y = each.center()
            ret.append((x / src.shape[1], y / src.shape[0]))
        return ret

    # FIXME: How to handle and click multiple targets found by OCR has not yet been decided.
    # def ocr_touch(
    #     self,
    #     text: str,
    #     duration: float = 0.01,
    #     regular: bool = True,
    #     index: int = None,
    # ):
    #     self.touch(pos=self.ocr_find(text, regular), duration=duration)

    """ ===========================================================================
        Add GAutomator Public <Control> APIs Here!
        Usage:
            json_response: dict, binary_data: bytes = self.get(request_body: dict)
        ===========================================================================
    """

    """ Warning:
            Touch/swipe related APIs need refactoring! 

            The process now:
                pos (tuple[float, float]): relative points, 0.0 <= x <= 1.0
                size (struct Screensize) = screensize .* pos

                <Client> ---(screensize, size)---> <Server>

                <Server>:
                    pos = size ./ screensize 
                    # Recalculate the relative point values again! Why???

            Apparently this is absurdly awful...
            All we need to do is:
                <Client> ---(pos)---> <Server>
            
            So I rewrapped a _to_position() function for reuse. Remember to edit it when fixing this pile.
    """

    def call_reflection(self, method: GameMethods) -> any:
        """
        Call a reflection method.

        Args:
            method (GameMethods): The method to call.

        Returns:
            any: The result of the reflection call.
        """
        request = {
            "object": "reflection",
            "command": "callFunc",
            "body": {"ops": method._ops_dict, "outOp": method._out},
        }
        json_resp, _ = self.get(request)
        if Resp.json_status(json_resp):
            return json_resp["body"]["OutValue"]
        elif Resp.error_status(json_resp):
            return json_resp["body"]["failure"]
        else:
            return json_resp["body"]

    def touch_down(self, pos: Tuple[float, float], pointer_id: int = 0, by_scrycpy: bool = True) -> bool:
        """
        Simulate a touch down event at the given position.

        Args:
            pos (Tuple[float, float]): The position to touch down.
            pointer_id (int, optional): The pointer ID. Defaults to 0.
            by_scrycpy (bool, optional): Whether to use scrycpy. Defaults to True.

        Returns:
            bool: True if the touch down event was successful, False otherwise.
        """
        if by_scrycpy:
            return self._touch_event(AKEY_EVENT_ACTION_DOWN, pointer_id, self._to_postion(pos))
        else:
            res, body = self._slate_begin_touch({"x": pos[0], "y": pos[1]})
            return res

    def touch_up(
        self,
        pos: Tuple[float, float],
        pointer_id: int = 0,
        index: int = 0,
        by_scrycpy: bool = True,
    ) -> bool:
        """
        Simulate a touch up event at the given position.

        Args:
            pos (Tuple[float, float]): The position to touch up.
            pointer_id (int, optional): The pointer ID. Defaults to 0.
            index (int, optional): The index. Defaults to 0.
            by_scrycpy (bool, optional): Whether to use scrycpy. Defaults to True.

        Returns:
            bool: True if the touch up event was successful, False otherwise.
        """
        if by_scrycpy:
            return self._touch_event(AKEY_EVENT_ACTION_UP, pointer_id, self._to_postion(pos))
        else:
            res, body = self._slate_end_touch(index)
            return res

    def touch_move(
        self,
        pos: Tuple[float, float],
        pointer_id: int = 0,
        index: int = 0,
        by_scrycpy: bool = True,
    ) -> bool:
        """
        Simulate a touch move event at the given position.

        Args:
            pos (Tuple[float, float]): The position to touch move.
            pointer_id (int, optional): The pointer ID. Defaults to 0.
            index (int, optional): The index. Defaults to 0.
            by_scrycpy (bool, optional): Whether to use scrycpy. Defaults to True.

        Returns:
            bool: True if the touch move event was successful, False otherwise.
        """
        if by_scrycpy:
            return self._touch_event(AKEY_EVENT_ACTION_MOVE, pointer_id, self._to_postion(pos))
        else:
            res, body = self._slate_move_touch(index, {"x": pos[0], "y": pos[1]}, 1)
            return res

    def touch(self, pos: Tuple[float, float], duration: float = 0.01, by_scrycpy: bool = True) -> bool:
        """
        Simulate a touch event at the given position with an optional duration.

        Args:
            pos (Tuple[float, float]): The position to touch.
            duration (float, optional): The duration of the touch event. Defaults to 0.01.
            by_scrycpy (bool, optional): Whether to use scrycpy. Defaults to True.

        Returns:
            bool: True if the touch event was successful, False otherwise.
        """
        if not pos:
            raise ValueError("touch position cannot be none")
        # Long press for duration: float
        if duration < 0:
            logger.error("duration must be non-negative")
            return False
        res_down = self.touch_down(pos=pos, pointer_id=0, by_scrycpy=by_scrycpy)
        time.sleep(duration)
        res_up = self.touch_up(pos=pos, pointer_id=0, by_scrycpy=by_scrycpy)
        return res_down and res_up

    def swipe(
        self,
        source: Tuple[float, float],
        dest: Tuple[float, float],
        steps: int = 15,
        step_duration: float = 0.05,
        down_duration: float = 0.05,
        up_duration: float = 0.05,
    ) -> bool:
        """
        Simulate a swipe event from the source position to the destination position.

        Args:
            source (Tuple[float, float]): The source position.
            dest (Tuple[float, float]): The destination position.
            steps (int, optional): The number of steps in the swipe. Defaults to 15.
            step_duration (float, optional): The duration of each step. Defaults to 0.05.
            down_duration (float, optional): The duration of the touch down event
        """
        if steps < 1:
            logger.error("steps must be greate than 1")
            return False
        if step_duration < 0:
            logger.error("step_duration must be non-negative")
            return False
        if down_duration < 0:
            logger.error("down_duration must be non-negative")
            return False
        if up_duration < 0:
            logger.error("up_duration must be non-negative")
            return False

        source_pos, dest_pos = self._to_postion(source), self._to_postion(dest)

        res_down = self._touch_event(AKEY_EVENT_ACTION_DOWN, 0, source_pos)
        if not res_down:
            return False

        time.sleep(down_duration)
        step_x = (
            abs(dest_pos.point.x - source_pos.point.x) / steps * (-1 if dest_pos.point.x < source_pos.point.x else 1)
        )
        step_y = (
            abs(dest_pos.point.y - source_pos.point.y) / steps * (-1 if dest_pos.point.y < source_pos.point.y else 1)
        )
        logger.debug(f"step_x = {int(step_x)}, step_y = {int(step_y)}")

        current_pos = source_pos
        for i in range(steps):
            x, y = current_pos.point.x + step_x, current_pos.point.y + step_y
            pos = Position(Point(x, y), source_pos.screen_size)
            res_move = self._touch_event(AKEY_EVENT_ACTION_MOVE, 0, pos)
            if not res_move:
                return False
            current_pos = pos
            time.sleep(step_duration)

        time.sleep(up_duration)
        res_up = self._touch_event(AKEY_EVENT_ACTION_UP, 0, dest_pos)
        return res_up

    def key_press(self, key_code: int, key_mod: int = 0x00):
        """
        Simulate a key press event.

        Args:
            key_code (int): The key code of the key to press.
            key_mod (int, optional): The modifier key. Defaults to 0x00.

        Returns:
            bool: True if the key press event was successful, False otherwise.
        """
        res, body = self._slate_key_event(key_code, AKEY_EVENT_ACTION_DOWN | key_mod)
        if not res:
            logger.warning(f"keycode {key_code:03d} press failed due to {body}")
        return res

    def key_release(self, key_code: int, key_mod: int = 0x00):
        """
        Simulate a key release event.

        Args:
            key_code (int): The key code of the key to release.
            key_mod (int, optional): The modifier key. Defaults to 0x00.

        Returns:
            bool: True if the key release event was successful, False otherwise.
        """
        res, body = self._slate_key_event(key_code, AKEY_EVENT_ACTION_UP | key_mod)
        if not res:
            logger.warning(f"keycode {key_code:03d} release failed due to {body}")
        return res

    def key(self, key_code: int, duration: float = 0.05, key_mod: int = 0x00):
        """
        Simulate a key event.

        Args:
            key_code (int): The key code of the key to press and release.
            duration (float, optional): The duration of the key press. Defaults to 0.05.
            key_mod (int, optional): The modifier key. Defaults to 0x00.

        Returns:
            bool: True if the key event was successful, False otherwise.
        """
        res_press = self.key_press(key_code, key_mod)
        time.sleep(duration)
        res_release = self.key_release(key_code, key_mod)
        return res_press and res_release

    def set_filter(self, object: str, show_invisilbe: bool) -> bool:
        """
        Set the filter for an object.

        Args:
            object (str): The object to set the filter for.
            show_invisilbe (bool): Whether to show invisible widgets.

        Returns:
            bool: True if the filter was set successfully, False otherwise.
        """
        request = {
            "object": object,
            "command": "setFilter",
            "body": {"showInvisibleWgt": show_invisilbe},
        }
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp)

    def exec_console_cmd(self, cmd: str) -> bool:
        """
        Execute a console command.

        Args:
            cmd (str): The command to execute.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # Function to get the source code of an object
        request = {"object": "gameLogic", "command": "execCmd", "body": {"str": cmd}}
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp)

    def enable_user_event(self) -> Tuple[int, dict]:
        """
        Enable user events.

        Returns:
            Tuple[int, dict]: The status and body of the response.
        """
        request = {"object": "gameLogic", "command": "enableUserEvent"}
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp), json_resp["body"]

    def call_user_command(self, param: str, event_name: str) -> Tuple[bool, str]:
        """
        Call a user command.

        Args:
            param (str): The parameter for the command.
            event_name (str): The name of the event.

        Returns:
            Tuple[bool, str]: The result of the command and the response.
        """
        request = {
            "object": "gameLogic",
            "command": "callUserEvent",
            "body": {"userEvent": event_name, "param": param},
        }
        json_resp, _ = self.get(request)
        body = json_resp["body"]
        if Resp.json_status(json_resp):
            return body["result"], body["response"]
        elif Resp.error_status(json_resp):
            return False, body["response"]
        else:
            return False, body

    """ ===========================================================================
        Add GAutomator Actor APIs Here!
        ===========================================================================
    """

    @property
    def location(self):
        return self.get_location()

    @property
    def rotation(self):
        return self.get_rotation()

    @property
    def yaw(self):
        return self.get_rotation()["yaw"]

    @property
    def roll(self):
        return self.get_rotation()["roll"]

    @property
    def pitch(self):
        return self.get_rotation()["pitch"]

    def get_rotation(self) -> dict:
        """
        Get the rotation of the actor.

        Returns:
            dict: A dictionary containing the rotation information.
        """
        json_resp, _ = self.get({"object": "actor", "command": "getRotation"})
        return json_resp["body"]

    def get_location(self) -> dict:
        """
        Get the location of the actor.

        Returns:
            dict: A dictionary containing the location information.
        """
        json_resp, _ = self.get({"object": "actor", "command": "getLocation"})
        return json_resp["body"]

    @location.setter
    def location(self, pos: Tuple[float, float, float]) -> bool:
        self.set_location(pos)

    @yaw.setter
    def yaw(self, value: float):
        self.set_yaw(value)

    @roll.setter
    def roll(self, value: float):
        self.set_roll(value)

    @pitch.setter
    def pitch(self, value: float):
        self.set_pitch(value)

    def set_location(self, pos: Tuple[float, float, float]) -> bool:
        """
        Set the location of the actor.

        Args:
            pos (Tuple[float, float, float]): The new location as a Tuple of 3 floats.

        Returns:
            bool: True if the location was set successfully, False otherwise.
        """
        if not isinstance(pos, Tuple[float, float, float]):
            raise ValueError("location must be an tuple with length of 3")
        json_resp, _ = self.get(
            {
                "object": "actor",
                "command": "setLocation",
                "body": {"x": pos[0], "y": pos[1], "z": pos[2]},
            }
        )
        return Resp.json_status(json_resp)

    def set_yaw(self, value: float) -> bool:
        """
        Set the yaw of the actor.

        Args:
            value (float): The new yaw value.

        Returns:
            bool: True if the yaw was set successfully, False otherwise.
        """
        json_resp, _ = self.get({"object": "actor", "command": "yaw", "body": {"value": value}})
        return Resp.json_status(json_resp)

    def set_roll(self, value: float) -> bool:
        """
        Set the roll of the actor.

        Args:
            value (float): The new roll value.

        Returns:
            bool: True if the roll was set successfully, False otherwise.
        """
        json_resp, _ = self.get({"object": "actor", "command": "roll", "body": {"value": value}})
        return Resp.json_status(json_resp)

    def set_pitch(self, value: float) -> bool:
        """
        Set the pitch of the actor.

        Args:
            value (float): The new pitch value.

        Returns:
            bool: True if the pitch was set successfully, False otherwise.
        """
        json_resp, _ = self.get({"object": "actor", "command": "pitch", "body": {"value": value}})
        return Resp.json_status(json_resp)

    def line_trace(self) -> dict:
        """
        Perform a line trace.

        Returns:
            dict: A dictionary containing the line trace information.
        """
        json_resp, _ = self.get({"object": "actor", "command": "lineTrace"})
        return json_resp["body"]

    def move_forward(self, value: float) -> bool:
        """
        Move the actor forward.

        Args:
            value (float): The distance to move forward.

        Returns:
            bool: True if the actor moved forward successfully, False otherwise.
        """
        json_resp, _ = self.get({"object": "actor", "command": "moveForward", "body": {"value": value}})
        return Resp.json_status(json_resp)

    def move_right(self, value: float) -> bool:
        """
        Move the actor to the right.

        Args:
            value (float): The distance to move to the right.

        Returns:
            bool: True if the actor moved to the right successfully, False otherwise.
        """
        json_resp, _ = self.get({"object": "actor", "command": "lineTrace", "body": {"value": value}})
        return Resp.json_status(json_resp)

    """ ===========================================================================
        Add GAutomator Private APIs Here!
        ===========================================================================
    """

    def _get_screen_size(self) -> Tuple[int, int]:
        json_resp, _ = self.get({"object": "slate", "command": "getWindowSize"})
        return (json_resp["body"]["width"], json_resp["body"]["height"]) if Resp.json_status(json_resp) else (0, 0)

    def _to_postion(self, pos: Tuple[float, float]) -> Position:
        size = ScreenSize(width=1920, height=1080)
        return Position(screen_size=size, point=Point(size.width * pos[0], size.height * pos[1]))

    def _touch_event(self, action: int, pointerId: int, position: Position) -> bool:
        """
        Basic touch event request creating func for all touches and swipes
        """
        request = {
            "object": "touch",
            "command": "touchEvent",
            "body": {
                "action": action,
                "pointerId": pointerId,
                "position": position.to_json(),
            },
        }
        json_resp, _ = self.get(request)
        if not Resp.json_status(json_resp):
            logger.warning(
                "touch event action={:d} position=({:.2f},{:.2f}) failed".format(
                    action, position.point.x, position.point.y
                )
            )
        return Resp.json_status(json_resp)

    """ ===========================================================================
        Add GAutomator Slate APIs Here!
        ===========================================================================
    """

    def _slate_click(self, name: str, address: typing.Optional[str] = None) -> Tuple[bool, dict]:
        """Function to simulate a click on a slate object
        Args:
            name (str): The name of the slate object
            address (Optional[str]): The address of the slate object, if any
        Returns:
            The status and body of the response
        """
        request = {
            "object": "slate",
            "command": "click",
            "body": {"name": name, "address": address},
        }
        json_resp, data = self.get(request)
        logger.info("slate_click recv json:" + str(json_resp))
        logger.info("slate_click recv data:" + str(data))
        return Resp.json_status(json_resp), json_resp["body"]

    def _slate_key_event(self, key_code: float, action: float) -> Tuple[bool, dict]:
        """Function to handle key events for the slate object
        Args:
            key_code (float): The key code of the key event
            action (float): The action of the key event
        Returns:
            Generator: Yields a Tuple (status, body) where status is an int and body is a str
        """
        request = {
            "object": "slate",
            "command": "keyEvent",
            "body": {"keyCode": key_code, "action": action},
        }
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp), json_resp["body"]

    def _slate_begin_touch(self, start_position: dict) -> Tuple[bool, dict]:
        """slate_begin_touch: Initiates a touch event on a slate.
        Args:
        start_position (dict): The starting position of the touch event.
        """
        request = {
            "object": "slate",
            "command": "keyEvent",
            "body": {"startPosition": start_position},
        }
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp), json_resp["body"]

    def _slate_move_touch(self, touch_index: float, screen_delta: dict, duration_seconds: float) -> Tuple[bool, dict]:
        """Function to simulate a touch event on a slate, moving the touch point according to the given parameters
        Args:
            touch_index (float): The index of the touch event
            screen_delta (dict): The change in screen position
            duration_seconds (float): The duration of the touch event in seconds
        Returns:
            Generator: Yields a Tuple (status, body) where status is an int and body is a string
        """
        request = {
            "object": "slate",
            "command": "keyEvent",
            "body": {
                "touchIndex": touch_index,
                "screenDelta": screen_delta,
                "durationSeconds": duration_seconds,
            },
        }
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp), json_resp["body"]

    def _slate_end_touch(self, touch_index: float) -> Tuple[bool, dict]:
        """Function to handle the end of a touch event with slate object
        Args:
            touch_index: float - The index of the touch event
        Returns:
            Generator - Yields a Tuple (status: int, body: str) containing the status and body of the response
        """
        request = {
            "object": "slate",
            "command": "keyEvent",
            "body": {"touchIndex": touch_index},
        }
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp), json_resp["body"]

    """ ===========================================================================
        Add GAutomator UMG APIs Here!
        ===========================================================================
    """

    def _umg_set_checkbox(self, name: str, check_state: bool, unique_id: int = -1) -> bool:
        body = {"name": name, "state": check_state}
        if unique_id >= 0:
            body["uniqueID"] = unique_id
        json_resp, _ = self.get({"object": "umg", "command": "setCheckBox", "body": body})
        return Resp.json_status(json_resp)

    def _umg_load_attributes(self, widget_info) -> List[Tuple[str, str]]:
        json_resp, _ = self.get({"object": "umg", "command": "GetAttrs", "body": widget_info.to_json()})
        attrs = json_resp["body"]["attributes"]
        res = []
        for attr in attrs:
            res.append((attr["name"], attr["value"]))
        return res

    def _umg_set_text(self, name: str, text: str, unique_id: int = -1) -> bool:
        body = {"name": name, "text": text}
        if unique_id:
            body["uniqueID"] = unique_id
        request = {"object": "umg", "command": "setText", "body": body}
        json_resp, _ = self.get(request)
        return Resp.json_status(json_resp)

    """ ===========================================================================
        Add aliases Here!
        ===========================================================================
    """

    disconnect = close

    find = find_element
    element = find_element
    find_game_element = find_element

    finds = find_elements
    elements = find_elements
    find_game_elements = find_elements

    parent = get_parent

    parents = get_parents

    cv_exist = cv_find_by_template
