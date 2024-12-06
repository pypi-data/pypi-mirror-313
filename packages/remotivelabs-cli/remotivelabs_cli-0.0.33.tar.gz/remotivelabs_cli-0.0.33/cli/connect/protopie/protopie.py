# type: ignore
# pylint: skip-file
from __future__ import annotations

import json
import os
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import grpc
import socketio  # type: ignore
from remotivelabs.broker.sync import BrokerException, Client, SignalIdentifier, SignalsInFrame
from rich import print as pretty_print
from rich.console import Console
from socketio.exceptions import ConnectionError as SocketIoConnectionError  # type: ignore

from cli import settings
from cli.broker.lib.broker import SubscribableSignal
from cli.errors import ErrorPrinter

global PP_CONNECT_APP_NAME
PP_CONNECT_APP_NAME = "RemotiveBridge"

io = socketio.Client()

err_console = Console(stderr=True)

_has_received_signal = False
is_connected = False
config_path: Path
x_api_key: str
broker: Any


@io.on("connect")  # type: ignore
def on_connect() -> None:
    print("Connected to ProtoPie Connect")
    io.emit("ppBridgeApp", {"name": PP_CONNECT_APP_NAME})
    io.emit("PLUGIN_STARTED", {"name": PP_CONNECT_APP_NAME})

    global is_connected
    is_connected = True


# TODO - Receive message from ProtoPie connect


def get_signals_and_namespaces(
    config: Union[Path, None] = None, signals_to_subscribe_to: Union[List[SubscribableSignal], None] = None
) -> Tuple[List[str], List[str], Union[Dict[str, str], None]]:
    if config is not None:
        with open(config) as f:
            mapping = json.load(f)
            sub = mapping["subscription"]
            signals = list(sub.keys())
            namespaces = list(map(lambda x: sub[x]["namespace"], signals))
    else:
        if signals_to_subscribe_to is None:
            signals = []
            namespaces = []
        else:
            signals = list(map(lambda s: s.name, signals_to_subscribe_to))
            namespaces = list(map(lambda s: s.namespace, signals_to_subscribe_to))
        sub = None
    return signals, namespaces, sub


def get_signal_name(expression: str, s_name: str) -> str:
    if expression is not None:
        try:
            sig_name = eval(f"s_name.{expression}")
            return str(sig_name)
        except Exception as e:
            ErrorPrinter.print_generic_error(f"Failed to evaluate your python expression {expression}")
            err_console.print(e)
            # This was the only way I could make this work, exiting on another thread than main
            os._exit(1)
    else:
        return s_name


def _connect_to_broker(
    config: Union[Path, None] = None,
    signals_to_subscribe_to: Union[List[SubscribableSignal], None] = None,
    expression: str = "",
) -> None:  # noqa: C901
    signals, namespaces, sub = get_signals_and_namespaces(config, signals_to_subscribe_to)

    def on_signals(frame: SignalsInFrame) -> None:
        global _has_received_signal
        if not _has_received_signal:
            pretty_print("Bridge-app is properly receiving signals, you are good to go :thumbsup:")
            _has_received_signal = True

        for s in frame:
            if config and sub is not None:
                sig = sub[s.name()]
                sig = s.name() if "mapTo" not in sig.keys() else sig["mapTo"]
                if isinstance(sig, list):
                    for ss in sig:
                        io.emit("ppMessage", {"messageId": get_signal_name(expression, ss), "value": str(s.value())})
                else:
                    io.emit("ppMessage", {"messageId": get_signal_name(expression, sig), "value": str(s.value())})
            else:
                signal_name = get_signal_name(expression, s.name())
                io.emit("ppMessage", {"messageId": signal_name, "value": str(s.value())})

    grpc_connect(on_signals, signals_to_subscribe_to)


def grpc_connect(on_signals: Any, signals_to_subscribe_to: Union[List[SignalIdentifier], None] = None) -> None:
    try:
        pretty_print("Connecting and subscribing to broker...")
        subscription = None
        client = Client(client_id="cli")
        client.connect(url=broker, api_key=x_api_key)
        client.on_signals = on_signals

        if signals_to_subscribe_to is None:
            print("No sigs")
            return
        subscription = client.subscribe(signals_to_subscribe_to=signals_to_subscribe_to, changed_values_only=False)
        pretty_print("Subscription to broker completed")
        pretty_print("Waiting for signals...")

        while True:
            time.sleep(1)

    except grpc.RpcError as e:
        err_console.print(":boom: [red]Problems connecting or subscribing[/red]")
        if isinstance(e, grpc.Call):
            print(f"{e.code()} - {e.details()}")
        else:
            print(e)

    except BrokerException as e:
        print(e)
        if subscription is not None:
            subscription.cancel()

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Closing subscription.")
        if subscription is not None:
            subscription.cancel()

    except Exception as e:
        print(traceback.format_exc())
        err_console.print(f":boom: {e}")
        # exit(1)


def do_connect(
    address: str,
    broker_url: str,
    api_key: Union[str, None],
    config: Union[Path, None],
    signals: List[SubscribableSignal],
    expression: Union[str, None],
) -> None:
    global broker
    global x_api_key
    global config_path
    broker = broker_url

    if broker_url.startswith("https"):
        if api_key is None:
            print("No --api-key, reading token from file")
            x_api_key = settings.read_secret_token()
        else:
            x_api_key = api_key
    elif api_key is not None:
        x_api_key = api_key
    try:
        io.connect(address)
        # if config is None:
        #    raise ValueError("Config is None")
        config_path = config
        while is_connected is None:
            time.sleep(1)
        # if expression is not None:
        _connect_to_broker(signals_to_subscribe_to=signals, config=config, expression=expression)
    except SocketIoConnectionError as e:
        err_console.print(":boom: [bold red]Failed to connect to ProtoPie Connect[/bold red]")
        err_console.print(e)
        exit(1)
    except Exception as e:
        err_console.print(":boom: [bold red]Unexpected error[/bold red]")
        err_console.print(e)
        exit(1)
