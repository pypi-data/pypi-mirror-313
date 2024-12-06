import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Any

from typing_extensions import override

from cli import settings
from cli.cloud.rest_helper import RestHelper as Rest

httpd: HTTPServer


class S(BaseHTTPRequestHandler):
    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    @override
    def log_message(self, format: Any, *args: Any) -> None:  # pylint: disable=W0622,
        return

    # Please do not change this into lowercase!
    @override
    # type: ignore
    def do_GET(self):  # pylint: disable=invalid-name,
        self._set_response()
        self.wfile.write("Successfully setup CLI, return to your terminal to continue".encode("utf-8"))
        path = self.path
        time.sleep(1)
        httpd.server_close()

        killerthread = Thread(target=httpd.shutdown)
        killerthread.start()

        settings.write_secret_token(path[1:])
        print("Successfully logged on, you are ready to go with cli")


def start_local_webserver(server_class: type = HTTPServer, handler_class: type = S, port: int = 0) -> None:
    server_address = ("", port)
    global httpd  # pylint: disable=W0603
    httpd = server_class(server_address, handler_class)


def login() -> None:
    """
    Initiate login using browser
    """
    start_local_webserver()
    webbrowser.open_new_tab(f"{Rest.get_base_url()}/login?redirectUrl=http://localhost:{httpd.server_address[1]}")
    httpd.serve_forever()
