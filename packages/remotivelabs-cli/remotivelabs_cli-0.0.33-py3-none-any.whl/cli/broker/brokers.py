from __future__ import annotations

import os
from time import sleep

import typer
from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf,
)

from . import export, files, licenses, playback, record, scripting, signals

app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def main(
    url: str = typer.Option(None, is_eager=False, help="Broker URL", envvar="REMOTIVE_BROKER_URL"),
) -> None:
    # This can be used to override the --url per command, lets see if this is a better approach
    if url is not None:
        os.environ["REMOTIVE_BROKER_URL"] = url
    # Do other global stuff, handle other global options here
    return


@app.command(help="Discover brokers on this network")
def discover() -> None:
    # print("Not implemented")

    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)

    services = ["_remotivebroker._tcp.local."]
    # services = list(ZeroconfServiceTypes.find(zc=zeroconf))

    print("\nLooking for RemotiveBrokers on your network, press Ctrl-C to exit...\n")
    ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()


def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
    # print(f"Service {name} state changed: {state_change}")

    if state_change is ServiceStateChange.Removed:
        print(f"Service {name} was removed")

    if state_change is ServiceStateChange.Updated:
        print(f"Service {name} was updated")

    if state_change is ServiceStateChange.Added:
        print(f"[ {name} ]")
        info = zeroconf.get_service_info(service_type, name)
        # print("Info from zeroconf.get_service_info: %r" % (info))

        if info:
            # addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            for addr in info.parsed_scoped_addresses():
                print(f"RemotiveBrokerApp: http://{addr}:8080")
                print(f"RemotiveBroker http://{addr}:50051")
            # print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            # print(f"  Server: {info.server}")
            # if info.properties:
            #    print("  Properties are:")
            #    for key, value in info.properties.items():
            #        print(f"    {key}: {value}")
            # else:
            #    print("  No properties")
        else:
            print("  No info")
        print("\n")


app.add_typer(playback.app, name="playback", help="Manage playing recordings")
app.add_typer(record.app, name="record", help="Record data on buses")
app.add_typer(files.app, name="files", help="Upload/Download configurations and recordings")
app.add_typer(signals.app, name="signals", help="Find and subscribe to signals")
app.add_typer(export.app, name="export", help="Export to external formats")
app.add_typer(scripting.app, name="scripting", help="LUA scripting utilities")
app.add_typer(licenses.app, name="license", help="View and request license to broker")

if __name__ == "__main__":
    app()
