from __future__ import annotations

import binascii
import ntpath
import os
import posixpath
import queue
import signal as os_signal
import tempfile
import time
import zipfile
from dataclasses import dataclass
from threading import Thread
from typing import Any, Callable, Dict, Iterable, List, Sequence, Union

import grpc
import remotivelabs.broker.generated.sync.traffic_api_pb2 as traffic_api
import remotivelabs.broker.sync as br
import remotivelabs.broker.sync.helper as br_helper
import typer
from google.protobuf.json_format import MessageToDict
from rich.console import Console

from cli import settings
from cli.errors import ErrorPrinter

err_console = Console(stderr=True)


@dataclass
class SubscribableSignal:
    name: str
    namespace: str


@dataclass
class LicenseInfo:
    valid: bool
    expires: str
    email: str
    machine_id: str


class Broker:
    def __init__(self, url: str, api_key: Union[str, None] = None) -> None:
        self.url = url
        self.api_key = api_key
        self.q: queue.Queue[Any] = queue.Queue()
        """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads."""
        # Setting up stubs and configuration

        if api_key is None or api_key == "":
            if url.startswith("https"):
                self.intercept_channel = br.create_channel(url, None, settings.read_secret_token())
                # TODO - Temporary solution to print proper error message, remove ENV once api-key is gone
                os.environ["ACCESS_TOKEN"] = "true"
            else:
                os.environ["ACCESS_TOKEN"] = "false"
                self.intercept_channel = br.create_channel(url, None, None)
        else:
            err_console.print(
                "Option --api-key will is deprecated and will be removed. " "Use access access tokens by logging in with cli."
            )
            os.environ["ACCESS_TOKEN"] = "false"
            self.intercept_channel = br.create_channel(url, api_key, None)

        self.network_stub = br.network_api_pb2_grpc.NetworkServiceStub(self.intercept_channel)
        self.system_stub = br.system_api_pb2_grpc.SystemServiceStub(self.intercept_channel)
        self.traffic_stub = br.traffic_api_pb2_grpc.TrafficServiceStub(self.intercept_channel)
        self.signal_creator = br.SignalCreator(self.system_stub)

    @staticmethod
    def __check_playbackmode_result(status: br.traffic_api_pb2.PlaybackInfos) -> None:
        err_cnt = 0
        for mode in status.playbackInfo:
            if mode.playbackMode.errorMessage:
                print(mode.playbackMode.errorMessage)
                err_cnt = err_cnt + 1
        if err_cnt > 0:
            raise typer.Exit(1)

    def seek(self, recording_and_namespace: List[Any], offset: int, silent: bool = True) -> br.traffic_api_pb2.PlaybackInfos:
        def to_playback(rec: Any) -> Dict[str, Any]:
            return {"namespace": rec["namespace"], "path": rec["recording"], "mode": br.traffic_api_pb2.Mode.SEEK, "offsettime": offset}

        playback_list = map(to_playback, recording_and_namespace)

        infos = br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        status = self.traffic_stub.PlayTraffic(infos)
        if not silent:
            self.__check_playbackmode_result(status)
        return status

    def play(self, recording_and_namespace: List[Any], silent: bool = False) -> br.traffic_api_pb2.PlaybackInfos:
        def to_playback(rec: Any) -> Dict[str, Any]:
            return {
                "namespace": rec["namespace"],
                "path": rec["recording"],
                "mode": br.traffic_api_pb2.Mode.PLAY,
            }

        playback_list = map(to_playback, recording_and_namespace)

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )

        if not silent:
            self.__check_playbackmode_result(status)
        return status

    def stop_play(self, recording_and_namespace: List[Any], silent: bool = False) -> br.traffic_api_pb2.PlaybackInfos:
        def to_playback(rec: Any) -> Dict[str, Any]:
            return {
                "namespace": rec["namespace"],
                "path": rec["recording"],
                "mode": br.traffic_api_pb2.Mode.STOP,
            }

        playback_list = map(to_playback, recording_and_namespace)

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        if not silent:
            self.__check_playbackmode_result(status)
        return status

    def pause_play(self, recording_and_namespace: List[Any], silent: bool = False) -> br.traffic_api_pb2.PlaybackInfos:
        def to_playback(rec: Any) -> Dict[str, Any]:
            return {
                "namespace": rec["namespace"],
                "path": rec["recording"],
                "mode": br.traffic_api_pb2.Mode.PAUSE,
            }

        playback_list = map(to_playback, recording_and_namespace)

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        if not silent:
            self.__check_playbackmode_result(status)
        return status

    def record_multiple(self, namespaces: List[str], path: str) -> br.traffic_api_pb2.PlaybackInfos:
        def to_playback(namespace: str) -> Dict[str, Any]:
            return {
                "namespace": namespace,
                "path": path + "_" + namespace,
                "mode": br.traffic_api_pb2.Mode.RECORD,
            }

        playback_list = list(map(to_playback, namespaces))

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        self.__check_playbackmode_result(status)
        return status

    def record(self, namespace: str, path: str) -> br.traffic_api_pb2.PlaybackInfos:
        playback_list = [
            {
                "namespace": namespace,
                "path": path,
                "mode": br.traffic_api_pb2.Mode.RECORD,
            }
        ]

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        self.__check_playbackmode_result(status)
        return status

    def stop(self, namespace: str, path: str, silent: bool = False) -> br.traffic_api_pb2.PlaybackInfos:
        playback_list = [
            {
                "namespace": namespace,
                "path": path,
                "mode": br.traffic_api_pb2.Mode.STOP,
            }
        ]

        status: traffic_api.PlaybackInfos = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        if not silent:
            self.__check_playbackmode_result(status)
        return status

    def listen_on_playback(self, repeat: bool, recording_and_namespace: List[Any], callback: Callable[[int, int, str], None]) -> None:
        # include recording_and_namespace if we want to loop the recording
        # This can probably be improved
        def get_mode(mode: int) -> str:
            if mode == 0:
                return "playing"
            if mode == 1:
                return "paused"
            if mode == 2:
                return "stopped"
            raise ValueError("Unknown Mode")

        sub = self.traffic_stub.PlayTrafficStatus(br.common_pb2.Empty())
        for playback_state in sub:
            # p = typing.cast(br.traffic_api_pb2.PlaybackInfos, playback_state) # REDUNDANT CAST
            p = playback_state
            offset_length = int(p.playbackInfo[0].playbackMode.offsetTime / 1000000)
            start_time = p.playbackInfo[0].playbackMode.startTime
            end_time = p.playbackInfo[0].playbackMode.endTime
            mode = p.playbackInfo[0].playbackMode.mode

            total_length = int((end_time - start_time) / 1000000)

            if mode == 2 and repeat:
                # If we get a stop and is fairly (this is mostly not 100%) close to the end
                # we repeat the recording when files are included
                if abs(total_length - offset_length) < 5:
                    self.play(recording_and_namespace)
            callback(offset_length, total_length, get_mode(mode))

    def pause(self, namespace: str, path: str, silent: bool = False) -> br.traffic_api_pb2.PlaybackInfos:
        playback_list = [
            {
                "namespace": namespace,
                "path": path,
                "mode": br.traffic_api_pb2.Mode.PAUSE,
            }
        ]

        status: traffic_api.PlaybackInfos = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        if not silent:
            self.__check_playbackmode_result(status)
        return status

    def stop_multiple(self, namespaces: List[str], path: str) -> br.traffic_api_pb2.PlaybackInfos:
        def to_playback(namespace: str) -> Dict[str, Any]:
            return {
                "namespace": namespace,
                "path": path + "_" + namespace,
                "mode": br.traffic_api_pb2.Mode.STOP,
            }

        playback_list = list(map(to_playback, namespaces))

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(playbackInfo=list(map(self.__create_playback_config, playback_list)))
        )
        self.__check_playbackmode_result(status)
        return status

    def diagnose_stop(self, namespace: List[str]) -> None:
        recording_name = "diagnose__"
        self.stop_multiple(namespace, recording_name)

    def diagnose(self, namespace: List[str], wait_for_traffic: bool = False) -> None:
        recording_name = "diagnose__"

        keep_running = True
        keep_running_during_recording = True

        def exit_on_ctrlc(_sig: Any, _frame: Any) -> None:
            nonlocal keep_running
            keep_running = False
            nonlocal keep_running_during_recording
            keep_running_during_recording = False
            # progress.add_task(description=f"Cleaning up, please wait...", total=None)

        os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)

        while keep_running:
            keep_running = wait_for_traffic
            self.record_multiple(namespace, recording_name)
            for i in range(5):
                if keep_running_during_recording:
                    time.sleep(1)

            self.stop_multiple(namespace, recording_name)

            response = []
            with tempfile.TemporaryDirectory() as tmpdirname:
                for ns in namespace:
                    path = recording_name + "_" + ns
                    tmp_file = os.path.join(tmpdirname, path)
                    self.download(path, tmp_file)
                    self.delete_files([path], False)
                    with zipfile.ZipFile(tmp_file, "r") as zip_ref:
                        zip_ref.extractall(tmpdirname)

                        file_stat = os.stat(os.path.join(tmpdirname, path + ".raw"))
                        response.append({"namespace": ns, "data": file_stat.st_size > 0})

            for r in response:
                if r["data"]:
                    print(f'Successfully received traffic on {r["namespace"]}')
                    keep_running = False
                else:
                    if not wait_for_traffic or (not keep_running and not keep_running_during_recording):
                        print(f'Namespace {r["namespace"]} did not receive any traffic')

    def upload(self, file: str, dest: str) -> None:
        try:
            br.helper.upload_file(system_stub=self.system_stub, path=file, dest_path=dest)
        except grpc.RpcError as rpc_error:
            print(f"Failed to upload file - {rpc_error.details()} ({rpc_error.code()})")
            raise typer.Exit(1)

    def delete_files(self, path: List[str], exit_on_faliure: bool) -> None:
        for file in path:
            try:
                self.system_stub.BatchDeleteFiles(
                    br.system_api_pb2.FileDescriptions(
                        fileDescriptions=[br.system_api_pb2.FileDescription(path=file.replace(ntpath.sep, posixpath.sep))]
                    )
                )
            except grpc.RpcError as rpc_error:
                print(f"Failed to delete file - {rpc_error.details()} ({rpc_error.code()})")
                if exit_on_faliure:
                    raise typer.Exit(1)

    # rpc BatchDeleteFiles (FileDescriptions) returns (Empty) {}

    def upload_folder(self, folder: str) -> None:
        try:
            br.helper.upload_folder(system_stub=self.system_stub, folder=folder)
        except grpc.RpcError as rpc_error:
            print(f"Failed to upload file - {rpc_error.details()} ({rpc_error.code()})")
            raise typer.Exit(1)

    def download(self, file: str, dest: str, delegate_err: bool = False) -> None:
        try:
            br_helper.download_file(system_stub=self.system_stub, path=file, dest_path=dest)
        except grpc.RpcError as rpc_error:
            if delegate_err:
                raise rpc_error
            print(f"Failed to download file - {rpc_error.details()} ({rpc_error.code()})")
            # There will be an empty file if the download fails so remove that one here
            os.remove(dest)
            raise typer.Exit(1)

    def reload_config(self) -> None:
        try:
            request = br.common_pb2.Empty()
            response = self.system_stub.ReloadConfiguration(request, timeout=60000)
            if response.errorMessage:
                print(f"Failed to reload config: {response.errorMessage}")
                raise typer.Exit(1)
            # br.helper.reload_configuration(system_stub=self.system_stub)
        except grpc.RpcError as rpc_error:
            print(f"Failed to reload configuration - {rpc_error.details()} ({rpc_error.code()})")
            raise typer.Exit(1)

    def list_namespaces(self) -> List[str]:
        # Lists available signals
        configuration = self.system_stub.GetConfiguration(br.common_pb2.Empty())
        namespaces = []
        for network_info in configuration.networkInfo:
            namespaces.append(network_info.namespace.name)
        return namespaces

    def list_signal_names(self, prefix: Union[str, None], suffix: Union[str, None]) -> List[Dict[str, Any]]:
        # Lists available signals
        configuration = self.system_stub.GetConfiguration(br.common_pb2.Empty())

        signal_names = []
        for network_info in configuration.networkInfo:
            res = self.system_stub.ListSignals(network_info.namespace)
            for finfo in res.frame:
                if (prefix is None or finfo.signalInfo.id.name.startswith(prefix)) and (
                    suffix is None or finfo.signalInfo.id.name.endswith(suffix)
                ):
                    metadata_dict = MessageToDict(
                        finfo.signalInfo.metaData,
                        including_default_value_fields=True,
                        preserving_proto_field_name=True,
                    )
                    sig_dict = {
                        "signal": finfo.signalInfo.id.name,
                        "namespace": network_info.namespace.name,
                    }
                    signal_names.append({**sig_dict, **metadata_dict})

                for sinfo in finfo.childInfo:
                    # For signals we can simply skip if prefix and suffix exists does not match
                    if (prefix is not None and not sinfo.id.name.startswith(prefix)) or (
                        suffix is not None and not sinfo.id.name.endswith(suffix)
                    ):
                        continue

                    metadata_dict = MessageToDict(
                        sinfo.metaData,
                        including_default_value_fields=True,
                        preserving_proto_field_name=True,
                    )
                    sig_dict = {
                        "signal": sinfo.id.name,
                        "namespace": network_info.namespace.name,
                    }
                    signal_names.append({**sig_dict, **metadata_dict})

        return signal_names

    def subscribe_on_script(
        self,
        script: bytes,
        on_frame: Callable[[Sequence[br.network_api_pb2.Signal]], None],
        changed_values_only: bool = False,
    ) -> Any:
        client_id = br.common_pb2.ClientId(id="cli")
        # sync = queue.Queue()
        thread = Thread(
            target=br.act_on_scripted_signal,
            args=(
                client_id,
                self.network_stub,
                script,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self.__each_signal(frame, on_frame),
                lambda sub: (self.q.put(("cli", sub))),
            ),
        )
        thread.start()
        # wait for subscription to settle
        return self.q.get()

    def validate_and_get_subscribed_signals(
        self, subscribed_namespaces: List[str], subscribed_signals: List[str]
    ) -> List[SubscribableSignal]:
        # Since we cannot know which list[signals] belongs to which namespace we need to fetch
        # all signals from the broker and find the proper signal with namespace. Finally we
        # also filter out namespaces that we do not need since we might have duplicated signal names
        # over namespaces
        # Begin

        def verify_namespace(available_signal: List[Dict[str, str]]) -> List[str]:
            return list(filter(lambda namespace: available_signal["namespace"] == namespace, subscribed_namespaces))  # type: ignore

        def find_subscribed_signal(available_signal: List[Dict[str, str]]) -> List[str]:
            return list(filter(lambda s: available_signal["signal"] == s, subscribed_signals))  # type: ignore

        existing_signals = self.list_signal_names(prefix=None, suffix=None)
        existing_ns = set(map(lambda s: s["namespace"], existing_signals))
        ns_not_matching = []
        for ns in subscribed_namespaces:
            if ns not in existing_ns:
                ns_not_matching.append(ns)
        if len(ns_not_matching) > 0:
            ErrorPrinter.print_hint(
                f"Namespace(s) {ns_not_matching} does not exist on broker. " f"Namespaces found on broker: {existing_ns}"
            )
            exit(1)

        available_signals = list(filter(verify_namespace, existing_signals))  # type: ignore
        signals_to_subscribe_to = list(filter(find_subscribed_signal, available_signals))  # type: ignore

        # Check if subscription is done on signal that is not in any of these namespaces
        signals_subscribed_to_but_does_not_exist = set(subscribed_signals) - set(map(lambda s: s["signal"], signals_to_subscribe_to))

        if len(signals_subscribed_to_but_does_not_exist) > 0:
            ErrorPrinter.print_hint(f"One or more signals you subscribed to does not exist " f"{signals_subscribed_to_but_does_not_exist}")
            exit(1)

        return list(map(lambda s: SubscribableSignal(s["signal"], s["namespace"]), signals_to_subscribe_to))

    def long_name_subscribe(
        self, signals_to_subscribe_to: List[SubscribableSignal], on_frame: Callable[..., Any], changed_values_only: bool = True
    ) -> Any:
        client_id = br.common_pb2.ClientId(id="cli")

        # TODO - This can be improved moving forward and we also need to move the validation into api
        self.validate_and_get_subscribed_signals(
            list(map(lambda s: s.namespace, signals_to_subscribe_to)), (list(map(lambda s: s.name, signals_to_subscribe_to)))
        )

        def to_protobuf_signal(s: SubscribableSignal) -> br.common_pb2.SignalId:
            return self.signal_creator.signal(s.name, s.namespace)

        signals_to_subscribe_on = list(map(to_protobuf_signal, signals_to_subscribe_to))

        Thread(
            target=br.act_on_signal,
            args=(
                client_id,
                self.network_stub,
                signals_to_subscribe_on,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self.__each_signal(frame, on_frame),
                lambda sub: (self.q.put(("cloud_demo", sub))),
            ),
        ).start()
        # Wait for subscription
        ecu, subscription = self.q.get()
        return subscription

    def subscribe(
        self,
        subscribed_signals: list[str],
        subscribed_namespaces: list[str],
        on_frame: Callable[..., Any],
        changed_values_only: bool = True,
    ) -> Any:
        client_id = br.common_pb2.ClientId(id="cli")

        signals_to_subscribe_to: List[SubscribableSignal] = self.validate_and_get_subscribed_signals(
            subscribed_namespaces, subscribed_signals
        )

        def to_protobuf_signal(s: SubscribableSignal) -> br.common_pb2.SignalId:
            return self.signal_creator.signal(s.name, s.namespace)

        signals_to_subscribe_on = list(map(to_protobuf_signal, signals_to_subscribe_to))

        Thread(
            target=br.act_on_signal,
            args=(
                client_id,
                self.network_stub,
                signals_to_subscribe_on,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self.__each_signal(frame, on_frame),
                lambda sub: (self.q.put(("cloud_demo", sub))),
            ),
        ).start()
        # Wait for subscription
        ecu, subscription = self.q.get()
        return subscription

    def __each_signal(self, signals: Iterable[br.network_api_pb2.Signal], callback: Callable[..., Any]) -> None:
        callback(
            map(
                lambda s: {"timestamp_us": s.timestamp, "namespace": s.id.namespace.name, "name": s.id.name, "value": self.__get_value(s)},
                signals,
            )
        )

    @staticmethod
    def __get_value(signal: br.network_api_pb2.Signal) -> Any:
        if signal.raw != b"":
            return "0x" + binascii.hexlify(signal.raw).decode("ascii")
        if signal.HasField("integer"):
            return signal.integer
        if signal.HasField("double"):
            return signal.double
        if signal.HasField("arbitration"):
            return signal.arbitration
        return "empty"

    @staticmethod
    def __create_playback_config(item: Dict[str, Any]) -> br.traffic_api_pb2.PlaybackInfo:
        """Creating configuration for playback

        Parameters
        ----------
        item : dict
            Dictionary containing 'path', 'namespace' and 'mode'

        Returns
        -------
        PlaybackInfo
            Object instance of class

        """

        def get_offset_time() -> int:
            if "offsettime" in item:
                return int(item["offsettime"])
            return 0

        playback_config = br.traffic_api_pb2.PlaybackConfig(
            fileDescription=br.system_api_pb2.FileDescription(path=item["path"]),
            namespace=br.common_pb2.NameSpace(name=item["namespace"]),
        )
        return br.traffic_api_pb2.PlaybackInfo(
            playbackConfig=playback_config,
            playbackMode=br.traffic_api_pb2.PlaybackMode(mode=item["mode"], offsetTime=get_offset_time()),
        )

    def get_license(self) -> LicenseInfo:
        license_info = self.system_stub.GetLicenseInfo(br.common_pb2.Empty())
        return LicenseInfo(
            valid=license_info.status == br.system_api_pb2.LicenseStatus.VALID,
            expires=license_info.expires,
            email=license_info.requestId,
            machine_id=license_info.requestMachineId.decode("utf-8"),
        )

    def apply_license(self, license_data_b64: bytes) -> LicenseInfo:
        license = br.system_api_pb2.License()
        license.data = license_data_b64
        license.termsAgreement = True
        self.system_stub.SetLicense(license)
        return self.get_license()
