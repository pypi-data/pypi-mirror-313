#!/usr/bin/env python3
# coding: utf-8


import argparse
from typing import Tuple

from .core._types import Context, By
from .gautomator import GAClient


_all_commands = []
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 27029


def _host_and_port_from_args(args: argparse.Namespace) -> Tuple[str, int]:
    if args.address:
        ret_add = args.address.split(":")
        try:
            return (ret_add[0], int(ret_add[1]))
        except Exception as e:
            print(f'input argument "--address" has wrong format: {args.address}')
    ret_host = args.host if args.host else DEFAULT_HOST
    ret_port = args.port if args.port else DEFAULT_PORT
    return (ret_host, ret_port)


def _start_new_client(args: argparse.Namespace) -> GAClient:
    return GAClient(addr=_host_and_port_from_args(args))


def cmd_take_screentshot(args: argparse.Namespace):
    c = _start_new_client(args)
    c.screenshot(args.path)
    return


def cmd_dump_elements(args: argparse.Namespace):
    c = _start_new_client(args)
    context = Context.Slate if not args.umg else Context.Slate
    print(c.page_source(context=context))
    return


_commands = [
    dict(
        action=cmd_take_screentshot,
        command="screenshot",
        flags=[
            dict(
                args=["-p", "--path"],
                type=str,
                default="D:\screenshot.png",
                help="save path of the screentshot",
            )
        ],
        help="take screentshot from GA server",
    ),
    dict(
        action=cmd_dump_elements,
        command="dump",
        flags=[
            dict(
                args=["-s", "--slate"],
                action="store_true",
                help="dump elements of slate context",
            ),
            dict(
                args=["-u", "--umg"],
                action="store_true",
                help="dump elements of UMG context",
            ),
        ],
        help="dump elements from GA server",
    ),
]


def main():
    parser = argparse.ArgumentParser(
        description="A Python client for communicate with the GAutomator Plugins. Created by Tencent WeTest",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Basic arguments here
    parser.add_argument("-i", "--host", type=str, help="set client host")
    parser.add_argument("-p", "--port", type=int, help="set client port")
    parser.add_argument("-a", "--address", type=str, help="set client address with format <ip>:<port>")

    subparser = parser.add_subparsers(dest="subparser")
    actions = {}
    for c in _commands:
        cmd_name = c["command"]
        cmd_aliases = c.get("aliases", [])
        for alias in [cmd_name] + cmd_aliases:
            actions[alias] = c["action"]
        sp = subparser.add_parser(
            cmd_name,
            aliases=cmd_aliases,
            help=c.get("help"),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        for f in c.get("flags", []):
            args = f.get("args")
            if not args:
                args = ["-" * min(2, len(n)) + n for n in f["name"]]
            kwargs = f.copy()
            kwargs.pop("name", None)
            kwargs.pop("args", None)
            sp.add_argument(*args, **kwargs)

    args = parser.parse_args()

    if not args.subparser:
        parser.print_help()
        # show_upgrade_message()
        return

    actions[args.subparser](args)


if __name__ == "__main__":
    main()
