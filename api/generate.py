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