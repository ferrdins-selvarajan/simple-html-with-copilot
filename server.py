import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

INDEX_PATH = Path(__file__).with_name("index.html")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return

        content = INDEX_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(content_length))
            message = payload["message"]
            if not isinstance(message, str):
                raise ValueError("message must be a string")
        except (json.JSONDecodeError, KeyError, ValueError):
            self.send_error(400, "Expected JSON with a string message")
            return

        response = f"Generated response for: {message}".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), RequestHandler)
    print("Serving on http://localhost:8000")
    server.serve_forever()