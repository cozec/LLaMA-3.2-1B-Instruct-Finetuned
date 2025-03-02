# LLaMA-3.2-1B Web Interface

A simple web interface for interacting with the LLaMA-3.2-1B-Instruct fine-tuned model.

## Features

- Clean, responsive user interface
- Easy input of prompts and questions
- Display of model-generated responses
- Serverless API for model inference

## Local Development

To run the project locally:

1. Ensure you have Python 3.9 installed
2. Create a virtual environment:
   ```
   python3.9 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the local development server:
   ```
   python local_server.py
   ```
5. Open your browser to `http://localhost:8000`

## Notes

- The model may take a few seconds to load initially
- The API endpoint uses lazy loading to initialize the model only when needed
- The model requires approximately 5GB of RAM to run efficiently

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python
- Model: LLaMA-3.2-1B-Instruct fine-tuned 