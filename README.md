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
2. Edit the `config.js` file to set your Hugging Face API token
3. Enter your question in the prompt field
4. Click "Get Answer" to get a response from the model

### Configuration

The project now uses a configuration file (`config.js`) to store your API token and model options:

```javascript
// config.js
const CONFIG = {
    // Replace with your actual Hugging Face API token
    API_TOKEN: "YOUR_HUGGING_FACE_API_TOKEN_HERE",
    
    // Default model to use
    DEFAULT_MODEL: "ai-nexuz/llama-3.2-1b-instruct-fine-tuned",
    
    // Available models - you can add/remove models as needed
    MODELS: [
        // ...model definitions...
    ]
};
```

To configure:
1. Edit `config.js` with a text editor
2. Replace `YOUR_HUGGING_FACE_API_TOKEN_HERE` with your actual Hugging Face API token
3. Save the file and refresh your browser

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