#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import hashlib

PORT = 8000
ADDRESS = '127.0.0.1'
MESSAGES_POST_PATH = '/messages'
MESSAGES_GET_PATH = '/messages/'
messages_by_sha = {}
class MessageRequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
    path = self.path
    print(path)
    if path == MESSAGES_POST_PATH:
      self.handle_messages_post()
    elif path.startswith(MESSAGES_GET_PATH):
      self.send_errror_response(400, 'Only GET allowed for /messages/SHA')
    else:
      self.send_error_response(404, 'Invalid URL')

  def do_GET(self):
    path = self.path
    if path == MESSAGES_POST_PATH:
      self.send_errror_response(400, 'Only POST allowed for /messages')
    elif path.startswith(MESSAGES_GET_PATH):
      self.handle_messages_get()
    else:
      self.send_error_response(404, 'Invalid URL')

  def handle_messages_post(self):
    content_length = int(self.headers['Content-Length'])
    content_type = self.headers['Content-Type']
    if content_type != 'application/json':
      self.send_error_response(400, 'Invalid Content-Type, must be "application/json"')
      return
    post_body = self.rfile.read(content_length)
    try:
      json_body = json.loads(post_body)
    except:
      self.send_error_response(400, 'Unable to parse JSON body')
      return
    if not isinstance(json_body, dict):
      self.send_error_response(400, 'JSON body must be an object with the key "message"')
      return
    if 'message' not in json_body:
      self.send_error_response(400, 'JSON body missing the key "message"')
      return
    message = json_body['message']
    hash = hashlib.sha256()
    hash.update(bytes(message, 'utf8'))
    hex_sha = hash.hexdigest()
    messages_by_sha[hex_sha] = message
    self.send_json_response(200, {'digest':hex_sha})

  def handle_messages_get(self):
    path = self.path
    hex_sha = path[len(MESSAGES_GET_PATH):]
    if hex_sha not in messages_by_sha:
      self.send_error_response(404, 'Mssage not found')
      return
    self.send_json_response(200, {'message':messages_by_sha[hex_sha]})

  def send_error_response(self, status_code, error_message):
    self.send_json_response(status_code, {'error_message':error_message})

  def send_json_response(self, status_code, json_data):
    response_content = json.dumps(json_data, separators=(',', ':'))
    self.send_response(status_code)
    self.send_header('Content-Type','application/json')
    self.end_headers()
    self.wfile.write(bytes(response_content, 'utf8'))

def start_server():
  server = HTTPServer((ADDRESS, PORT), MessageRequestHandler)
  print('messages server running...')
  server.serve_forever()

start_server()
