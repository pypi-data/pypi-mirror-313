import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse


# HTTP handler for processing the token sent from the web browser
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        params = parse_qs(url.query)
        access_token = params.get("access_token", [""])[0]
        refresh_token = params.get("refresh_token", [""])[0]

        if access_token and access_token != "null":
            self.server.access_token = access_token

        if refresh_token and refresh_token != "null":
            self.server.refresh_token = refresh_token

        self.send_response(302)
        self.send_header("Location", f"{self.server.app_domain}/signup/cli/success")
        self.end_headers()
        self.server._stop()

    # Suppress logging
    def log_message(self, format, *args):
        pass


# Temporary HTTP server to handle the login process
class Server(HTTPServer):
    port = None
    access_token = None
    refresh_token = None
    thread = None

    def __init__(self, app_domain: str):
        super().__init__(("localhost", 0), Handler)
        self.port = self.server_address[1]
        self.app_domain = app_domain

    def get_tokens(self):
        self._start()
        self._open_browser()

        try:
            while self.thread is not None:
                time.sleep(1)
        except KeyboardInterrupt:
            self._stop()

        return self.access_token, self.refresh_token

    def get_url(self):
        return f"{self.app_domain}/signup?cli={self.port}"

    def _open_browser(self):
        webbrowser.open(self.get_url())

    def _start(self):
        thread = Thread(target=self.serve_forever)
        thread.start()
        self.thread = thread

    def _stop(self):
        Thread(target=self.shutdown).start()
        self.thread = None
