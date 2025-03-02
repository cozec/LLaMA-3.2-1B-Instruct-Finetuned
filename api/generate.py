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

def handler(event, context):
    """
    Standard handler for Vercel Python serverless functions
    """
    logger.info("Handler function called")
    
    try:
        # Get API URL from environment
        api_url = os.environ.get("MODEL_API_URL")
        if not api_url:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "response": "Error: MODEL_API_URL environment variable not set. Please configure it in Vercel."
                })
            }
        
        # Parse request body
        try:
            body = json.loads(event.get('body', '{}'))
            prompt = body.get('prompt', '')
        except:
            logger.error("Failed to parse request body")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "response": "Error: Invalid request format"
                })
            }
            
        if not prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "response": "Error: No prompt provided"
                })
            }
            
        # Log request
        logger.info(f"Sending request to model API: {api_url}")
        logger.info(f"Prompt: {prompt[:50]}...")
            
        # Call model API
        try:
            response = requests.post(
                api_url,
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "response": result.get("response", "No response from model API")
                    })
                }
            else:
                error_msg = f"Model API returned status code {response.status_code}"
                logger.error(error_msg)
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "response": f"Error: {error_msg}"
                    })
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting to model API: {str(e)}"
            logger.error(error_msg)
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "response": error_msg
                })
            }
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "response": error_msg
            })
        }