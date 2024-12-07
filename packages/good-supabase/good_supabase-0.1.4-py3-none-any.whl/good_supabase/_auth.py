import typing
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import threading
import functools
import time
import socket

class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, success_callback: typing.Callable[[str], None], **kwargs):
        self.success_callback = success_callback
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/auth/callback'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
            <html>
            <body>
                <script>
                    var hash = window.location.hash.substr(1);
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/token', true);
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.onload = function() {
                        document.body.innerHTML += '<p>Authentication successful! You can close this window.</p>';
                    };
                    xhr.send(hash);
                </script>
                <p>Processing authentication...</p>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/token':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Token received")
            self.success_callback(post_data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

class GoogleAuthCallbackHandler:
    def __init__(self, supabase, port: int = 9997):
        self.supabase = supabase
        self.response = None
        self.port = port
        self.httpd = None
        self.server_thread = None
        self.auth_event = threading.Event()
        
    def run_server(self):
        while True:
            try:
                self.httpd = ThreadedTCPServer(("", self.port), functools.partial(CallbackHandler, success_callback=self.handle_callback))
                print(f"Serving at port {self.port}")
                self.httpd.serve_forever()
            except OSError as e:
                if e.errno == 48:  # Address already in use
                    print(f"Port {self.port} is busy, retrying in 1 second...")
                    time.sleep(1)
                else:
                    raise
            else:
                break

    def __enter__(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()
        self.response = self.supabase.auth.sign_in_with_oauth({
            "provider": 'google',
            "options": {
                "redirect_to": f'http://localhost:{self.port}/auth/callback',
                'grant_type': 'id_token'
            }
        })
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.auth_event.wait()  # Wait for authentication to complete
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        if self.server_thread:
            self.server_thread.join()

    def handle_callback(self, post_data):
        query_params = parse_qs(post_data.strip('#'))
        try:
            self.supabase.auth.set_session(query_params['access_token'][0], query_params['refresh_token'][0])
            # print(r)
        finally:
            self.auth_event.set()  # Signal that authentication is complete
