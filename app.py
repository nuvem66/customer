# API Customer

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Queue:
    def __init__(self):
        self.current_queue = []
        self.next_number = 1

    def generate_next(self):
        number = self.next_number
        self.current_queue.append(number)
        self.next_number += 1
        return number
    
    def call_current(self):
        return self.current_queue.pop(0) if self.current_queue else None
    
    def list_all(self):
        return self.current_queue
    
class RequestHandler(BaseHTTPRequestHandler):
    queue = Queue()
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()    

    def do_POST(self):
        if self.path == '/queue':
            self._set_headers(201)
            self.wfile.write(json.dumps({"senha": self.queue.generate_next()}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Not found."}).encode )

    def do_GET(self):
        if self.path == '/queue':
            self._set_headers(200)
            self.wfile.write(json.dumps({"queue": self.queue.list_all()}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Not found."}).encode )
    
    def do_DELETE(self):
        if self.path == '/queue':
            self._set_headers(201)
            self.wfile.write(json.dumps({"current": self.queue.call_current(), "remaining" : len(self.queue.current_queue)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"message": "Not found."}).encode )

# Initializes the server
def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("API rodando em http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()    
    