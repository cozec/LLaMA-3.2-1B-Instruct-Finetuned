from http.server import BaseHTTPRequestHandler
import json
import os
import requests
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            error_msg = "Error: MODEL_API_URL environment variable not set. Please set it in Vercel project settings."
            logger.error(error_msg)
            return error_msg
        
        logger.info(f"Sending request to model API: {API_URL}")
        
        # Make a request to your model API
        response = requests.post(
            API_URL,
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"},
            timeout=60  # 60 second timeout
        )
        
        if response.status_code == 200:
            logger.info("Received successful response from model API")
            return response.json().get("response", "")
        else:
            error_msg = f"Error: API request failed with status code {response.status_code}. Response: {response.text[:200]}"
            logger.error(error_msg)
            return error_msg
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to model API at {API_URL}: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error generating response: {str(e)}"
        logger.error(error_msg)
        return error_msg

# Handler for Vercel Python Serverless Functions
def handler(request):
    """
    Main handler for Vercel Python serverless functions
    This follows Vercel's expected format for Python handlers
    """
    try:
        # Get request body
        body = request.get('body', '{}')
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        # Parse JSON
        data = json.loads(body)
        prompt = data.get('prompt', '')
        
        if not prompt:
            logger.warning("No prompt provided in request")
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "No prompt provided"})
            }
        
        logger.info(f"Processing prompt: {prompt[:50]}...")
        
        # Call the model API
        response = generate_response(prompt)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"response": response})
        }
        
    except Exception as e:
        error_msg = f"Error in handler: {str(e)}"
        logger.error(error_msg)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": error_msg})
        }