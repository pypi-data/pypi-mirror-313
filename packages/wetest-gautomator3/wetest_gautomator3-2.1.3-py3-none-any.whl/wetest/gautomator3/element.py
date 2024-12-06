#!/usr/bin/env python3
# coding: utf-8


import logging

from typing import Dict, Optional, Union, Tuple, List
from numbers import Number
from xml.dom import minidom
from lxml import etree

from .core._types import *
from .core._exceptions import *
from .core._socket import AsyncSocket, DispatchCallback
from .core._types import RespStatus as Resp


class GAElement:
    def __init__(
        self,
        socket: AsyncSocket,
        element_type: str,
        data,
        context: Context = Context.Slate,
        widget_info=None,
        deferred_load=False,
        log_request: bool = False,
    ):
        self._async_socket = socket
        self._element_type = element_type
        self._data = dict(data)
        self._widget_info = widget_info
        self._deferred_load = deferred_load
        self._context = context

    """ ===========================================================================
        GameElement instance methods
        ===========================================================================
    """

    def get_attribute(self, name: str, default_value: str = None) -> Optional[Union[str, Dict]]:
        """
        Get an attribute of the element.

        Args:
            name (str): The name of the attribute to get.
            default_value (str, optional): The default value to return if the attribute is not found. Defaults to None.

        Returns:
            Optional[Union[str, Dict]]: The value of the attribute, or the default value if the attribute is not found.
        """
        if name in self._data:
            return self._data.get(name)

        if self._deferred_load:
            self._load_attributes()

        return self._data.get(name, default_value)

    @property
    def visible(self) -> bool:
        """Whether the element is visible to a user."""
        visibility = self.get_attribute("visibility", "hidden")
        return visibility == "Visible" or visibility == "HitTestInvisible" or visibility == "SelfHitTestInvisible"

    @property
    def enabled(self) -> bool:
        """Whether the element is enabled."""
        return self.get_attribute("isEnabled", "false") == "true"

    @property
    def checked(self) -> bool:
        """Whether the checkbox is checked."""
        return self.get_attribute("isChecked", "false") == "true"

    @property
    def interactable(self) -> bool:
        """Whether the checkbox is checked."""
        return self.get_attribute("isInteractable", "false") == "true"

    @property
    def volatile(self) -> bool:
        """Whether the checkbox is checked."""
        return self.get_attribute("isVolatile", "false") == "true"

    @property
    def accessible(self) -> bool:
        """Whether the checkbox is checked."""
        return self.get_attribute("isAccessible", "false") == "true"

    @property
    def accessible_text(self) -> bool:
        """Whether the checkbox is checked."""
        return self.get_attribute("accessibleText", "")

    @property
    def name(self) -> str:
        return self.get_attribute("name", "")

    @property
    def class_name(self) -> str:
        return self.get_attribute("className", "")

    @property
    def map_name(self) -> str:
        return self.get_attribute("map", "")

    @property
    def x(self) -> Number:
        return float(self.get_attribute("x", "0"))

    @property
    def y(self) -> Number:
        return float(self.get_attribute("y", "0"))

    @property
    def unique_id(self) -> str:
        return int(self.get_attribute("uniqueID", "-1"))

    @property
    def serial_number(self) -> str:
        return self.get_attribute("serialNumber", None)

    @property
    def id(self) -> str:
        return self.get_attribute("id", None)

    @property
    def type(self) -> str:
        return self.get_attribute("type", None)

    @property
    def title(self) -> str:
        return self.get_attribute("title", None)

    @property
    def address(self) -> str:
        return self.get_attribute("address", None)

    @property
    def text(self) -> str:
        return self.get_attribute("text", None)

    def set_text(self, text: str = "") -> bool:
        """
        Sends text to the element.

        Args:
            text (str, optional): The text to send. Defaults to "".

        Returns:
            bool: True if the text was set successfully, False otherwise.
        """
        if self._context is not Context.Umg:
            raise NotImplementedException("Cannot set checked state outside UMG")
        return self._umg_set_text(self.name, text, self.unique_id)

    def click(self, click_type: str = ClickType.SIMULATED_LOCATION_TOUCH) -> bool:
        """
        Click the element.

        Args:
            click_type (str, optional): The type of click. Defaults to ClickType.SIMULATED_LOCATION_TOUCH.

        Returns:
            bool: True if the click was successful, False otherwise.
        """
        logging.debug("click: _element_type:%s", self._element_type)
        unique_identifier = ""
        if self._element_type == ElementType.UWIDGET:
            unique_identifier = self.unique_id
        elif self._element_type == ElementType.SWIDGET:
            unique_identifier = self.address
        return self._click(self._context, click_type, self.name, unique_identifier)

    def set_checked_state(self, checked_state: bool) -> bool:
        """
        Set the checked state of the element.

        Args:
            checked_state (bool): The new checked state.

        Returns:
            bool: True if the checked state was set successfully, False otherwise.
        """
        if self._context is Context.Umg:
            return self._umg_set_checkbox(self.name, checked_state, self.unique_id)
        else:
            raise NotImplementedException("Cannot set checked state outside UMG")

    def _load_attributes(self):  # non-threadsafe function
        if self._context is not Context.Umg:
            raise NotImplementedException("Cannot load attributes outside UMG")
        attributes = self._umg_load_attributes(self._widget_info)
        self._data = dict(attributes)
        self._deferred_load = False
        pass

    def _umg_load_attributes(self, widget_info) -> List[Tuple[str, str]]:
        json_resp, _ = self._async_socket.sync_send(
            {"object": "umg", "command": "GetAttrs", "body": widget_info.to_json()}
        )
        attrs = json_resp["body"].get("attributes", {})
        res = []
        for attr in attrs:
            res.append((attr["name"], attr["value"]))
        return res

    def _umg_set_checkbox(self, name: str, check_state: bool, unique_id: int = -1) -> bool:
        body = {"name": name, "state": check_state}
        if unique_id >= 0:
            body["uniqueID"] = unique_id
        json_resp, _ = self._async_socket.sync_send({"object": "umg", "command": "setCheckBox", "body": body})
        return Resp.json_status(json_resp)

    def _umg_set_text(self, name: str, text: str, unique_id: int = -1) -> bool:
        body = {"name": name, "text": text}
        if unique_id:
            body["uniqueID"] = unique_id
        request = {"object": "umg", "command": "setText", "body": body}
        json_resp, _ = self._async_socket.sync_send(request)
        return Resp.json_status(json_resp)

    def _click(
        self,
        context: Context,
        click_type: str,
        name: str,
        unique_identifier: Union[str, int],
    ) -> Tuple[bool, dict]:
        request = dict()
        if context == Context.Slate:
            request = {
                "object": "slate",
                "command": "click",
                "body": {"name": name, "address": unique_identifier},
            }
        elif context == Context.Umg:
            request = {
                "object": "umg",
                "command": "click",
                "body": {
                    "name": name,
                    "clickType": click_type,
                    "uniqueID": unique_identifier,
                },
            }
        json_resp, _ = self._async_socket.sync_send(request)
        return Resp.json_status(json_resp), json_resp["body"]

    """ ===========================================================================
        GameElement class methods
        ===========================================================================
    """

    def _construct_element(dom_element, element_type: str, socket: AsyncSocket, context: Context):
        return GAElement(socket, element_type, dom_element.attributes.items(), context=context)

    def _construct_element_from_lxml(xpath_element, element_type: str, socket: AsyncSocket, context: Context):
        return GAElement(socket, element_type, xpath_element.items(), context=context)

    def _construct_elements_from_uwidget(socket: AsyncSocket, uwidget_info, context=Context):
        res = []
        if uwidget_info[0]:
            widget_info = uwidget_info[1]
            res.append(
                GAElement(
                    socket,
                    "UWidget",
                    widget_info.to_json().items(),
                    context=context,
                    widget_info=widget_info,
                    deferred_load=True,
                )
            )
        return res

    def _find_elements(by: str, value: str, socket: AsyncSocket, xml: str, context: Context):
        def find_by_attribute(attribute_name: str = None, attribute_value: str = None):
            res = []
            if element_type in (ElementType.UWIDGET, ElementType.SWIDGET, ElementType.GAMEOBJECT):
                all = xml_doc.getElementsByTagName(element_type)
                for element in all:
                    if element.getAttribute(attribute_name) == attribute_value:
                        res.append(GAElement._construct_element(element, element_type, socket, context))
            return res

        def find_by_xpath(xpath):
            res = []
            root = etree.XML(xml)
            all = root.xpath(xpath)
            for xpath_element in all:
                res.append(GAElement._construct_element_from_lxml(xpath_element, element_type, socket, context))
            return res

        if len(xml) > 0:
            xml_doc = minidom.parseString(xml)
            element_type = xml_doc.documentElement.getAttribute("elementType")
        if by == By.Xpath:
            return find_by_xpath(value)
        else:
            if element_type in (ElementType.UWIDGET, ElementType.SWIDGET, ElementType.GAMEOBJECT):
                return find_by_attribute(by, value)
        return []
