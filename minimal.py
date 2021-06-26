#!/usr/bin/env python
import http.server
import socketserver
import os, sys
from urllib.request import urlopen
import logging

done = False

class Server(socketserver.TCPServer):
    logging = False 
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if self.server.logging:
            http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        global done
        if (str(self.path)[1:9] == 'data.csv'):
            done = True
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            with open(str(self.path)[1:], 'rb') as file: 
                self._set_headers()
                self.wfile.write(file.read())

def run():
    with Server(("", 8888), Handler) as httpd:
        while not done:
            httpd.handle_request()

if __name__ == "__main__":
    run()