import json
import urllib.parse
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse
from hm3.search import bool_search
from hw5.search import search

def get_params(url):
    query = urlparse(url).query
    return urllib.parse.parse_qs(query)


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = get_params(self.path)
        search_text = params['search'][0]
        search_type = params['type'][0]
        docs = []
        if search_type == 'index':
            docs = list(bool_search(search_text))
        else:
            docs = [r['index'] for r in search(search_text)[0:5]]
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(docs).encode())


if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8080), DemoHandler).serve_forever()
