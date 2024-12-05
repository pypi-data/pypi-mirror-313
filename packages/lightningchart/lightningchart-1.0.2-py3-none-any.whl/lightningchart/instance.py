from __future__ import annotations
import threading
import uuid
import json
import msgpack
import requests
import socket
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from IPython.display import IFrame, display
from lightningchart import conf

def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((conf.LOCALHOST, 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def start_server():
    from lightningchart.server import start_thread
    try:
        conf.server_port = get_free_port()
        start_thread(conf.server_port)
    except:
        raise Exception('The server could not be started.')


def display_html(html_content, notebook=False, width: int | str = '100%', height: int | str = 600):
    html_bytes = html_content.encode("utf-8")

    class Server(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_bytes)

    server_address = (conf.LOCALHOST, 0)
    server = HTTPServer(server_address, Server)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = False
    server_thread.start()
    if notebook:
        return display(IFrame(src=f"http://{conf.LOCALHOST}:{server.server_port}", width=width, height=height))
    else:
        webbrowser.open(f"http://{conf.LOCALHOST}:{server.server_port}")
    server_thread.join()


def js_functions():
    import pkgutil
    import sys
    import os

    base_dir = '.'
    if hasattr(sys, '_MEIPASS'):
        base_dir = os.path.join(sys._MEIPASS)

    js_code = pkgutil.get_data(__name__,  os.path.join(base_dir, 'static/lcpy.js')).decode()
    return js_code


def create_html(items):
    serialized_items = []
    for i in items:
        serialized_items.append(json.dumps(i))
    html = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="shortcut icon" href="#">
        <title>LightningChart Python</title>
        <script src="https://cdn.jsdelivr.net/npm/@lightningchart/lcjs@6.1.1/dist/lcjs.iife.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@lightningchart/lcjs-themes@4.1.0/dist/iife/lcjs-themes.iife.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/msgpack-lite@0.1.26/dist/msgpack.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/socket.io@4.8.1/client-dist/socket.io.min.js"></script>
        <style>
            body {{
                height: 100%;
                margin: 0;
            }}
        </style>
    </head>
    <body>
    <script>
        {js_functions()}
    </script>
    <script>
        lcpy.initStatic({serialized_items});
    </script>
    </body>
</html>
"""
    return html


class Instance:

    def __init__(self):
        self.id = str(uuid.uuid4()).split('-')[0]
        self.session = requests.Session()
        retry_adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', retry_adapter)
        self.items = []
        self.live = False
        self.seq_num = 0

    def open_static(self):
        html = create_html(self.items)
        display_html(html)

    def open_in_browser(self):
        if self.live:
            webbrowser.open(f'http://{conf.LOCALHOST}:{conf.server_port}/?id={self.id}')
            try:
                response = self.session.get(f'http://{conf.LOCALHOST}:{conf.server_port}/room_response?id={self.id}')
                if response.ok:
                    return
            except requests.exceptions.ConnectionError as e:
                print(e)
        else:
            self.open_static()

    def open_in_notebook(self, width: int | str = '100%', height: int | str = 600):
        if self.live:
            return display(IFrame(src=f'http://{conf.LOCALHOST}:{conf.server_port}/?id={self.id}', width=width, height=height))
        else:
            html = create_html(self.items)
            return display_html(html, notebook=True, width=width, height=height)

    def send(self, id: str, command: str, arguments: dict = None):
        if not self.live:
            self.items.append({
                'id': str(id),
                'command': command,
                'args': arguments or {}
            })
        else:
            binary_data = msgpack.packb({
                'seq': self.seq_num,
                'id': str(id),
                'command': command,
                'args': arguments
            })
            self.seq_num += 1
            try:
                response = self.session.post(
                    f'http://{conf.LOCALHOST}:{conf.server_port}/item?id={self.id}',
                    data=binary_data,
                    headers={'Content-Type': 'application/msgpack'}
                )
                if response.ok:
                    return True
            except requests.RequestException as e:
                print(e)

    def set_preservation(self, enabled: bool):
        if enabled:
            url = f'http://{conf.LOCALHOST}:{conf.server_port}/enable_preservation'
        else:
            url = f'http://{conf.LOCALHOST}:{conf.server_port}/disable_preservation'
        try:
            response = self.session.get(url)
            if response.ok:
                return True
        except requests.RequestException as e:
            print(e)
