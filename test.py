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
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map='mps')
    
    # prompt = "Solve this equation: 2x + 3 = 7. Find x."
    prompt = "The length of a rectangular frame is 5 inches more than twice its width. If the area of the frame is 84 square inches, find its dimensions."
    
    print(f"\nProcessing prompt: {prompt}")
    
    inputs = tokenizer(prompt, return_tensors="pt")
    # Move inputs to the same device as the model
    if hasattr(model, 'device'):
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    outputs = model.generate(**inputs, max_length=1000)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print("\nResponse:")
    print(response)

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
