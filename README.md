# TopicMind — AI Quiz Assistant

A web app that lets you test your knowledge on any topic using AI-generated questions and instant feedback.

## What it does

- Enter any topic and get 5 multiple choice questions generated instantly
- Get detailed feedback on every answer explaining why it's right or wrong
- Questions go from easy to hard automatically
- Uses a knowledge base to generate accurate, contextual questions

## Tech Stack

- **Backend** — Python, FastAPI
- **AI** — Llama 3 via Groq API
- **Vector DB** — ChromaDB with sentence-transformers for semantic search
- **Frontend** — HTML, CSS, JavaScript

## How to run locally

1. Clone the repo
2. Add your Groq API key to a `.env` file:


And then 
3. Install dependencies:
```bash
   cd backend
   pip install -r requirements.txt
   pip install groq
```
4. Run the server:
```bash
   python main.py
```
5. Open `http://127.0.0.1:8000` in your browser

## Adding new topics

Drop any `.txt` file into the `/knowledge/` folder and restart the server. The app will automatically index it.



<!-- Add your screenshots <img width="1915" height="834" alt="Screenshot 2026-04-26 200053" src="https://github.com/user-attachments/assets/a1392e2f-2f80-48ba-a7df-99c1cf84cc23" />
here -->



