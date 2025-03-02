from http.server import BaseHTTPRequestHandler
import json
import os
import requests

# Instead of loading the model directly, we'll point to an external API
# You'll need to host the model inference elsewhere

def generate_response(prompt):
    """
    This is a placeholder function that should be implemented to call your actual model endpoint.
    For example, you might host the model on Hugging Face Inference API, your own server, etc.
    """
    try:
        # Replace with your actual model API endpoint
        API_URL = os.environ.get("MODEL_API_URL", "")
        
        if not API_URL:
            return "Error: MODEL_API_URL environment variable not set"
        
        # Make a request to your model API
        response = requests.post(
            API_URL,
            json={"prompt": prompt}
        )
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: API request failed with status code {response.status_code}"
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Vercel serverless function handler
def handler(request):
    # Parse the incoming request
    if request.method == "POST":
        try:
            # Parse the request body
            body = json.loads(request.body)
            prompt = body.get("prompt", "")
            
            if not prompt:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "No prompt provided"}),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                }
            
            # Call the external API for the model inference
            response = generate_response(prompt)
            
            return {
                "statusCode": 200,
                "body": json.dumps({"response": response}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }
    
    # Handle OPTIONS request for CORS
    elif request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            }
        }
    
    # Handle other HTTP methods
    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }