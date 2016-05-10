#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from urlparse import parse_qs
import SocketServer
import MySQLdb

import zmq
import sys

class S(BaseHTTPRequestHandler):

  topic = 999
  socket = None
  def get_socket(self):
    if not self.socket:
        context = zmq.Context()
        port = "5556"
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
    return self.socket

  def parse_POST(self):
    ctype, pdict = parse_header(self.headers['content-type'])
    if ctype == 'multipart/form-data':
      postvars = parse_multipart(self.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
      length = int(self.headers['content-length'])
      postvars = parse_qs(
          self.rfile.read(length),
          keep_blank_values=1)
    else:
      postvars = {}
    return postvars

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self._set_headers()
    self.wfile.write("<html><body><h1>hi!</h1></body></html>")

  def do_HEAD(self):
    self._set_headers()

  def do_POST(self):
    # Inserts posted data in a ZMQ queue
      postvars = self.parse_POST()
      value = postvars.get("value")[0]
      socket = self.get_socket()

      self.wfile.write("Sending message: '%r' with topic '%s'" % (value, self.topic))
      socket.send_multipart([
        b"%03d" % self.topic,
        b"%s" % value
      ])

      self._set_headers()
      self.wfile.write("<html><body><h1>POST reuse!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=80):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print 'Starting httpd...'
  httpd.serve_forever()

if __name__ == "__main__":
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
