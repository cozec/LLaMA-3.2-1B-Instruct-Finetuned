// Hugging Face API Configuration
const CONFIG = {
    // Default model to use
    DEFAULT_MODEL: "ai-nexuz/llama-3.2-1b-instruct-fine-tuned",
    
    // Available models
    MODELS: [
        {
            id: "ai-nexuz/llama-3.2-1b-instruct-fine-tuned",
            name: "LLaMA-3.2-1B (Default)"
        },
        {
            id: "meta-llama/Meta-Llama-3-8B-Instruct",
            name: "Meta-Llama-3-8B (Larger)"
        },
        {
            id: "microsoft/phi-2",
            name: "Microsoft Phi-2 (Faster)"
        },
        {
            id: "gpt2", 
            name: "GPT-2 (Always available)"
        },
        {
            id: "deepseek-ai/deepseek-math-7b-rl",
            name: "DeepSeek Math 7B (Specialized)"
        },
        {
            id: "google/gemma-7b-it",
            name: "Gemma 7B (Strong at math)"
        },
        {
            id: "mistralai/Mistral-7B-Instruct-v0.2",
            name: "Mistral 7B (Good math capabilities)"
        },
        {
            id: "abacusai/Smaug-34B-v0.1",
            name: "Smaug 34B (Advanced math, larger model)"
        },
        {
            id: "WizardLM/WizardMath-7B-V1.0",
            name: "WizardMath 7B (Math-focused)"
        },
        {
            id: "TIGER-Lab/MAmmoTH-7B",
            name: "MAmmoTH 7B (Math Assistant)"
        }
    ]
}; 