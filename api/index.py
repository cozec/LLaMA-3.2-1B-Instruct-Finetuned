from http.server import BaseHTTPRequestHandler
import json
import os
import requests

def handler(event, context):
    """
    Minimal handler for Vercel Python serverless functions
    """
    try:
        # Get the model API URL from environment variable
        api_url = os.environ.get("MODEL_API_URL", "")
        
        # Parse the request body
        body_str = event.get('body', '{}')
        if isinstance(body_str, bytes):
            body_str = body_str.decode('utf-8')
        
        body = json.loads(body_str)
        prompt = body.get('prompt', '')
        
        if not api_url:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "response": "Error: MODEL_API_URL environment variable not set"
                })
            }
        
        if not prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "response": "Error: No prompt provided"
                })
            }
        
        # Forward the request to the model API
        response = requests.post(
            api_url,
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "response": response.json().get("response", "")
                })
            }
        else:
            return {
                "statusCode": response.status_code,
                "body": json.dumps({
                    "response": f"Error: Model API returned status code {response.status_code}"
                })
            }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "response": f"Error: {str(e)}"
            })
        } 