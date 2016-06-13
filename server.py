#!/usr/bin/env python3

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

import yaml

config = {
    'filename': sys.argv[1] if len(sys.argv) >= 2 else './links.yml',
    'port': int(sys.argv[2]) if len(sys.argv) >= 3 else 9000,
}


def handler(filename):
    links = yaml.load(open(filename))
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            name = self.path.strip('/')
            if name in links:
                self.send_response(302)
                self.send_header('Location', links[name])
            else:
                self.send_response(404)
            self.end_headers()
    return Handler


if __name__ == '__main__':
    try:
        server = HTTPServer(('', config['port']), handler(config['filename']))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down')
        server.socket.close()
