# LLaMA-3.2-1B Web Interface

A simple web interface for interacting with the LLaMA-3.2-1B-Instruct fine-tuned model.

## Architecture

This project now uses a direct communication approach:

- The web interface directly communicates with the model server
- No intermediary API proxy is needed
- The URL to the model server is configurable in the UI

This approach solves deployment issues with serverless platforms and provides more flexibility.

## Features

- Clean, responsive user interface
- Easy input of prompts and questions
- Display of model-generated responses
- Wide selection of math-specialized models
- Configuration via dropdown menu
- Configurable model server URL

## Deployment

### Frontend Deployment

You can deploy the frontend (index.html) to any static hosting service:

1. Vercel, Netlify, GitHub Pages, etc.
2. Simply deploy the repository and the static file will be served

### Model Server Setup

The model server needs to be hosted separately on a machine with enough resources to run the LLaMA model:

1. Set up a server (e.g., AWS EC2, Google Cloud, DigitalOcean)
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r model_server_requirements.txt
   ```
4. Run the model server:
   ```
   python model_server.py
   ```
   
Alternatively, you can use a service like Hugging Face Inference API to host the model.

## Usage Instructions

1. Access the web interface
2. Enter your Hugging Face API token in the token field and click "Save Token"
3. Enter your question in the prompt field
4. Click "Get Answer" to get a response from the model

### Configuration

The project uses a configuration file (`config.js`) to store model options:

```javascript
// config.js
const CONFIG = {
    // Default model to use
    DEFAULT_MODEL: "ai-nexuz/llama-3.2-1b-instruct-fine-tuned",
    
    // Available models - you can add/remove models as needed
    MODELS: [
        // ...model definitions...
    ]
};
```

The Hugging Face API token is stored securely in your browser's local storage after you enter it in the user interface.

### Available Models

The application provides access to several AI models specialized in mathematics:

| Model | Description | Strengths |
|-------|-------------|-----------|
| LLaMA-3.2-1B | Default fine-tuned model | Balanced performance with small size |
| Meta-Llama-3-8B | Larger base model | More comprehensive reasoning |
| Microsoft Phi-2 | Smaller, faster model | Quick responses for simpler problems |
| DeepSeek Math 7B | Specialized for mathematics | Advanced mathematical reasoning |
| Gemma 7B | Google's instruction model | Strong general math capabilities |
| Mistral 7B | High-performance model | Good balance of speed and accuracy |
| Smaug 34B | Very large model | Complex multi-step problem solving |
| WizardMath 7B | Math-focused fine-tuning | Specialized mathematical explanations |
| MAmmoTH 7B | Math assistant model | Step-by-step solution walkthrough |

Different models may perform better on different types of math problems. If one model struggles with a particular question, try another from the dropdown menu.

## Local Development

To run the complete system locally:

1. Ensure you have Python 3.9 installed
2. Create a virtual environment:
   ```
   python3.9 -m venv venv
   source venv/bin/activate
   ```
3. Install all dependencies:
   ```
   pip install -r model_server_requirements.txt
   ```
4. Start the model server:
   ```
   python model_server.py
   ```
5. Open the index.html file directly in your browser or serve it with a simple HTTP server:
   ```
   python -m http.server
   ```
6. In the web interface, set the Model Server URL to `http://localhost:5000/generate`

## Notes

- The model may take a few seconds to load initially
- The model server uses lazy loading to initialize the model only when needed
- The model requires approximately 5GB of RAM to run efficiently
- CORS is enabled on the model server to allow direct browser access

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Model Server: Flask, PyTorch, Transformers
- Model: LLaMA-3.2-1B-Instruct fine-tuned 