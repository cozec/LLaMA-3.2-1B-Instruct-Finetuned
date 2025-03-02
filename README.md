# LLaMA-3.2-1B Web Interface

A simple web interface for interacting with the LLaMA-3.2-1B-Instruct fine-tuned model.

## Architecture

This project is split into two parts:

1. **Frontend + API Proxy** - A lightweight web interface and API handler that can be deployed on Vercel
2. **Model Server** - A separate Flask server that hosts the actual LLaMA model

This architecture is necessary because:
- Language models like LLaMA are too large (several GB) to be deployed directly to serverless platforms like Vercel
- Vercel has size limits for serverless functions and deployment bundles

## Features

- Clean, responsive user interface
- Easy input of prompts and questions
- Display of model-generated responses
- Lightweight API proxy for model inference

## Vercel Deployment

1. Deploy the frontend and API proxy to Vercel
2. Set the `MODEL_API_URL` environment variable in Vercel to point to your model server

## Model Server Setup

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
5. In a separate terminal window, set the environment variable and run the local server:
   ```
   export MODEL_API_URL=http://localhost:5000/generate
   python local_server.py
   ```
6. Open your browser to `http://localhost:8000`

## Notes

- The model may take a few seconds to load initially
- The API endpoint uses lazy loading to initialize the model only when needed
- The model requires approximately 5GB of RAM to run efficiently

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- API Proxy: Python (Vercel Serverless Functions)
- Model Server: Flask, PyTorch, Transformers
- Model: LLaMA-3.2-1B-Instruct fine-tuned 