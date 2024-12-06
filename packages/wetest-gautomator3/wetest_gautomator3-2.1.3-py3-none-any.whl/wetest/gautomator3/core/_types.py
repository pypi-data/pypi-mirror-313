#!/usr/bin/env python3
# coding: utf-8


import typing
from enum import Enum
from dataclasses import dataclass, field


CMD_DICT = typing.Dict[str, typing.Any]
T_JSON_DICT = typing.Dict[str, typing.Any]

AKEY_EVENT_ACTION_DOWN = 0x00
AKEY_EVENT_ACTION_UP = 0x01
AKEY_EVENT_ACTION_MOVE = 0x10
MOD_LEFT_SHIFT = 0x01 << 2
MOD_RIGHT_SHIFT = 0x01 << 3
MOD_LEFT_CONTROL = 0x01 << 4
MOD_RIGHT_CONTROL = 0x01 << 5
MOD_LEFT_ALT = 0x01 << 6
MOD_RIGHT_ALT = 0x01 << 7
MOD_LEFT_COMMAND = 0x01 << 8
MOD_RIGHT_COMMAND = 0x01 << 9
MOD_CAPS_LOCKED = 0x01 << 10

CVLIB_IMPORT_ERROR = "pip install python-opencv and wetest-cvlib first. run: pip install wetest-cvlib python-opencv --upgrade --extra-index-url https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple"


class HoldExceededMaxTimeError(Exception):
    pass


class RespStatus(Enum):
    INIT = 100
    ERROR = 101
    SUCCESS_JSON = 102
    SUCCESS_BINARY = 103
    MOCK = 104

    def json_status(resp: dict) -> bool:
        return resp["status"] == RespStatus.SUCCESS_JSON.value

    def binary_status(resp: dict) -> bool:
        return resp["status"] == RespStatus.SUCCESS_BINARY.value

    def error_status(resp: dict) -> bool:
        return resp["status"] == RespStatus.ERROR.value


class Context(str, Enum):
    Umg = "umg"
    Slate = "slate"


class By(str, Enum):
    Xpath = "xpath"
    Name = "name"
    Classname = "className"
    Text = "text"
    WidgetPath = "widgetPath"
    Type = "type"
    AccessibleText = "accessibleText"


@dataclass
class UWidgetBasicInfo:
    unique_id: int  #: Widget UObject UniqueID
    serial_number: str  #: Widget UObject Serial Number
    name: str  #: Widget Name

    def to_json(self) -> typing.Dict[str, any]:
        json: typing.Dict[str, any] = dict()
        json["uniqueId"] = int(self.unique_id)
        json["serialNumber"] = int(self.serial_number)
        json["name"] = self.name
        return json

    @classmethod
    def from_json(cls, json: typing.Dict[str, any]):
        return cls(
            unique_id=int(json["uniqueID"]),
            serial_number=str(json["serialNumber"]),
            name=str(json["name"]),
        )


class ElementType(str, Enum):
    UWIDGET = "UWidget"
    SWIDGET = "SWidget"
    GAMEOBJECT = "GameObject"


class ClickType(object):
    AUTO = "auto"
    TRIGGERING_EVENT = "triggeringEvent"
    SIMULATED_LOCATION_TOUCH = "simulatedLocationTouch"


@dataclass
class Point:
    #: position x
    x: float

    #: position y
    y: float

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json["X"] = self.x
        json["Y"] = self.y
        return json


@dataclass
class ScreenSize:
    #: screen width
    width: int

    #: screen height
    height: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json["X"] = self.width
        json["Y"] = self.height
        return json


@dataclass
class Position:
    #: point
    point: Point

    #: screen size
    screen_size: ScreenSize

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json["point"] = self.point.to_json()
        json["screenSize"] = self.screen_size.to_json()
        return json


@dataclass
class OPFunction:
    is_static: bool

    def __post_init__(self):
        self.validate()
        for i in range(len(self.params)):
            self.params[i] = str(self.params[i])

    def validate(self):
        assert isinstance(self.params, list), "params should be list"


@dataclass
class OPStaticFunction(OPFunction):
    package_name: str
    class_name: str
    function_name: str
    params: typing.List[str] = field(default_factory=list)
    op_name: str = ""

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json["opName"] = self.op_name
        json["isStatic"] = self.is_static
        json["packageName"] = self.package_name
        json["className"] = self.class_name
        json["functionName"] = self.function_name
        json["params"] = self.params
        return json


@dataclass
class OPNonStaticFunction(OPFunction):
    object_name: str
    function_name: str
    params: typing.List[str] = field(default_factory=list)
    op_name: str = ""

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json["opName"] = self.op_name
        json["isStatic"] = self.is_static
        json["objectName"] = self.object_name
        json["functionName"] = self.function_name
        json["params"] = self.params
        return json
