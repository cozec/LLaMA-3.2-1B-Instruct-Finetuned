#!/usr/bin/env python3
"""
Standalone Model Server for LLaMA-3.2-1B

This script creates a Flask API that serves the LLaMA model.
You can host this on any server that can run Python and has enough resources
(e.g., a cloud VM with sufficient RAM).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the port
PORT = os.environ.get("PORT", 5000)

# Model configuration
MODEL_NAME = "ai-nexuz/llama-3.2-1b-instruct-fine-tuned"
tokenizer = None
model = None

def initialize_model():
    """Initialize the model and tokenizer."""
    global tokenizer, model
    
    if tokenizer is None:
        logger.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    if model is None:
        logger.info("Loading model...")
        # Check if CUDA is available
        if torch.cuda.is_available():
            device_map = "auto"
            logger.info(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            device_map = "auto"  # Will default to CPU
            logger.info("CUDA is not available. Using CPU instead.")
            
        # Special case for Apple Silicon (M1/M2)
        if hasattr(torch, 'has_mps') and torch.has_mps:
            logger.info("Apple MPS (Metal Performance Shaders) is available.")
            device_map = "mps"
            
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map=device_map)
        logger.info("Model loaded successfully!")

@app.route('/generate', methods=['POST'])
def generate():
    """Generate text based on the provided prompt."""
    try:
        # Initialize model if not already done
        if model is None or tokenizer is None:
            initialize_model()
        
        # Get prompt from request
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        logger.info(f"Processing prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
        
        # Process the prompt
        inputs = tokenizer(prompt, return_tensors="pt")
        
        # Move inputs to the same device as the model
        if hasattr(model, 'device'):
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate response
        outputs = model.generate(**inputs, max_length=600)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return jsonify({'response': response})
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

if __name__ == '__main__':
    logger.info(f"Starting model server on port {PORT}...")
    # Initialize the model at startup
    initialize_model()
    app.run(host='0.0.0.0', port=int(PORT), debug=False) 