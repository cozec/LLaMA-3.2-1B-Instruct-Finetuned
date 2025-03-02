#!/usr/bin/env python3
import http.server
import socketserver
import json
import sys
from api.generate import generate_response

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests for the /api/generate endpoint."""
        if self.path == '/api/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                prompt = data.get('prompt', '')
                
                if not prompt:
                    self._send_json_response(400, {'error': 'No prompt provided'})
                    return
                
                print(f"Processing prompt: {prompt}")
                response = generate_response(prompt)
                
                self._send_json_response(200, {'response': response})
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._send_json_response(500, {'error': str(e)})
        else:
            self.send_error(404, "Not Found")
    
    def _send_json_response(self, status_code, data):
        """Send a JSON response with the given status code and data."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server():
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)

if __name__ == "__main__":
    run_server() 