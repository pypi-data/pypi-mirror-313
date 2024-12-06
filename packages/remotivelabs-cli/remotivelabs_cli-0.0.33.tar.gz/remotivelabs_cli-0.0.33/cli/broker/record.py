from __future__ import annotations

from typing import List

import grpc
import typer

from cli.errors import ErrorPrinter

from .lib.broker import Broker

app = typer.Typer(help=help)  # type: ignore


@app.command()
def start(
    filename: str = typer.Argument(..., help="Path to local file to upload"),
    namespace: List[str] = typer.Option(..., help="Namespace to record"),
    url: str = typer.Option(..., help="Broker URL", envvar="REMOTIVE_BROKER_URL"),
    api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token", envvar="REMOTIVE_BROKER_API_KEY"),
) -> None:
    try:
        broker = Broker(url, api_key)
        broker.record_multiple(namespace, filename)
    except grpc.RpcError as rpc_error:
        ErrorPrinter.print_grpc_error(rpc_error)


@app.command()
def stop(
    filename: str = typer.Argument(..., help="Path to local file to upload"),
    namespace: List[str] = typer.Option(..., help="Namespace to record"),
    url: str = typer.Option(..., help="Broker URL", envvar="REMOTIVE_BROKER_URL"),
    api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token", envvar="REMOTIVE_BROKER_API_KEY"),
) -> None:
    try:
        broker = Broker(url, api_key)
        broker.stop_multiple(namespace, filename)
        print("Successfully stopped recording")
    except grpc.RpcError as rpc_error:
        ErrorPrinter.print_grpc_error(rpc_error)
