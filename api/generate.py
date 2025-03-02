from http.server import BaseHTTPRequestHandler
import json
import traceback
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize model and tokenizer
MODEL_NAME = "ai-nexuz/llama-3.2-1b-instruct-fine-tuned"
tokenizer = None
model = None

def initialize_model():
    global tokenizer, model
    if tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    if model is None:
        # Check if CUDA is available
        if torch.cuda.is_available():
            device_map = "auto"  # Let the library decide the optimal device mapping
        else:
            device_map = "auto"  # Will default to CPU when CUDA is not available
            
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map=device_map)

def generate_response(prompt):
    # Initialize model if not already initialized
    initialize_model()
    
    # Process the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Move inputs to the same device as the model
    if hasattr(model, 'device'):
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    # Generate response
    outputs = model.generate(**inputs, max_length=600)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# HTTP handler for Vercel
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get('prompt', '')
            if not prompt:
                self._send_response(400, {'error': 'No prompt provided'})
                return
                
            response = generate_response(prompt)
            
            # Send response
            self._send_response(200, {'response': response})
            
        except Exception as e:
            print(f"Error: {str(e)}")
            traceback.print_exc()
            self._send_response(500, {'error': str(e)})
    
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

# Vercel serverless function handler
def lambda_handler(event, context):
    try:
        # Handle HTTP requests
        if event.get('httpMethod') == 'POST':
            body = json.loads(event.get('body', '{}'))
            prompt = body.get('prompt', '')
            
            if not prompt:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No prompt provided'}),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                }
                
            response = generate_response(prompt)
            
            return {
                'statusCode': 200,
                'body': json.dumps({'response': response}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        # Handle OPTIONS requests for CORS
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                }
            }
            
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        } 