from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the fine-tuned model and tokenizer
model_name = "ai-nexuz/llama-3.2-1b-instruct-fine-tuned"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Check if CUDA is available and provide info
if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
    device_map = "auto"  # Let the library decide the optimal device mapping
else:
    print("CUDA is not available. Using CPU instead.")
    device_map = "auto"  # Will default to CPU when CUDA is not available

try:
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map=device_map)
    
    # prompt = "Solve this equation: 2x + 3 = 7. Find x."
    prompt = "A photographer wants to create a rectangular frame for a photo. The frame's width is 2 inches more than its height. If the area of the frame (including the empty space) is 48 square inches, what are the dimensions of the frame?"
    
    print(f"\nProcessing prompt: {prompt}")
    
    inputs = tokenizer(prompt, return_tensors="pt")
    # Move inputs to the same device as the model
    if hasattr(model, 'device'):
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    outputs = model.generate(**inputs, max_length=600)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print("\nResponse:")
    print(response)

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
