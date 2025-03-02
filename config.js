// Hugging Face API Configuration
const CONFIG = {
    // Replace with your actual Hugging Face API token
    API_TOKEN: "YOUR_HUGGING_FACE_API_TOKEN_HERE",
    
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
        }
    ]
}; 