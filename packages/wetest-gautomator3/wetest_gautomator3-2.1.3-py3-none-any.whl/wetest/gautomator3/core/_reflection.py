#!/usr/bin/env python3
# coding: utf-8


import logging
import typing
from functools import partial
from collections import OrderedDict

from ._types import OPFunction, OPStaticFunction, OPNonStaticFunction


static_method = partial(OPStaticFunction, True)
non_static_method = partial(OPNonStaticFunction, False)

ga_private = partial(static_method, "/Script/GAExtension", "GAReflectionExtension")
GameplayStatics = partial(static_method, "/Script/Engine", "GameplayStatics")
WidgetBlueprintLibrary = partial(static_method, "/Script/UMG", "WidgetBlueprintLibrary")
KismetSystemLibrary = partial(static_method, "/Script/Engine", "KismetSystemLibrary")
AbilitySystemBlueprintLibrary = partial(static_method, "/Script/GameplayAbilities", "AbilitySystemBlueprintLibrary")
GPASC = partial(static_method, "/Script/GPAbility", "GPASC")
GameFrameWork = partial(static_method, "/Script/GameFrameWork", "NZHelper")
AnalysisServiceBPLib = partial(static_method, "/Script/AnalysisService", "AnalysisServiceBPLib")
CitySampleBlueprintLibrary = partial(static_method, "/Script/CitySample", "CitySampleBlueprintLibrary")


class GameMethods:
    def __init__(self, methods: typing.OrderedDict[str, OPFunction], out: str):
        assert isinstance(methods, OrderedDict), "functions must be ordered dict"
        assert out in methods.keys(), "return function name not in " + str(methods.keys())

        self._out = out
        self._ops_dict = []
        for k, v in methods.items():
            v.op_name = k
            self._ops_dict.append(v.to_json())
