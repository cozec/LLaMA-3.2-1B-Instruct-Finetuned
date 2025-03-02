from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gradio as gr

# Load the fine-tuned model and tokenizer
model_name = "ai-nexuz/llama-3.2-1b-instruct-fine-tuned"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=600)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

model = AutoModelForCausalLM.from_pretrained(model_name)


gr.Interface(fn=generate_response, inputs="text", outputs="text").launch()

