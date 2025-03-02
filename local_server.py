#!/usr/bin/env python3
import http.server
import socketserver
import json
import sys
import os
import requests

PORT = 8000

# Get the model API URL from environment variable
MODEL_API_URL = os.environ.get("MODEL_API_URL", "http://localhost:5000/generate")

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
                
                # Forward the request to the model server
                try:
                    response = requests.post(
                        MODEL_API_URL,
                        json={"prompt": prompt},
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        model_response = response.json()
                        self._send_json_response(200, model_response)
                    else:
                        error_message = f"Model API returned status code {response.status_code}"
                        print(error_message)
                        self._send_json_response(500, {'error': error_message})
                
                except requests.RequestException as e:
                    error_message = f"Error connecting to model API: {str(e)}"
                    print(error_message)
                    self._send_json_response(500, {'error': error_message})
                
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
        print(f"Using model API at: {MODEL_API_URL}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)

if __name__ == "__main__":
    if not MODEL_API_URL:
        print("WARNING: MODEL_API_URL environment variable not set!")
        print("Set it with: export MODEL_API_URL=http://your-model-server:port/generate")
    run_server() 