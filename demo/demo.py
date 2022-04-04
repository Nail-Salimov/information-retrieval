import urllib.parse
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import json
from io import BytesIO
from urllib.parse import urlparse


def get_params(url):
    query = urlparse(url).query
    return urllib.parse.parse_qs(query)


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = get_params(self.path)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(params).encode())


if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8080), DemoHandler).serve_forever()