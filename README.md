# TopicMind — AI-Powered Quiz Assistant

An AI-native learning tool that uses **Retrieval-Augmented Generation (RAG)** to generate topic-specific quiz questions and provide intelligent feedback on answers.

## Features

- **RAG Pipeline** — Retrieves relevant knowledge chunks from a local vector database (ChromaDB) before generating questions
- **LLM Integration** — Uses Claude (Anthropic) to generate contextual MCQs and evaluate answers
- **Adaptive Difficulty** — Questions progress from easy to hard
- **AI Feedback** — Detailed explanations and study tips for every answer
- **REST API** — FastAPI backend with clean endpoints

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI / LLM | Anthropic Claude API |
| RAG / Vector DB | ChromaDB + sentence-transformers |
| Frontend | HTML, CSS, JavaScript |

## Project Structure

```
topicmind/
├── backend/
│   ├── main.py          # FastAPI server + routes
│   ├── rag.py           # RAG pipeline (embed + retrieve)
│   ├── quiz.py          # Question generation + answer evaluation
│   └── requirements.txt
├── frontend/
│   ├── index.html       # Main UI
│   ├── style.css        # Styling
│   └── app.js           # Frontend logic + API calls
├── knowledge/           # Topic knowledge files (RAG source)
│   ├── python_basics.txt
│   └── machine_learning.txt
└── .env                 # API keys (never commit this)
```

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/topicmind.git
cd topicmind
```

### 2. Add your API key
Edit `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the backend
```bash
python main.py
```

### 5. Open the frontend
Open `frontend/index.html` in your browser, or visit `http://localhost:8000`

## How RAG Works Here

1. Topic text files in `/knowledge/` are split into chunks
2. Each chunk is embedded using `sentence-transformers`
3. Embeddings are stored in ChromaDB (local vector DB)
4. When a user enters a topic, the query is embedded and similar chunks are retrieved
5. Retrieved context is sent to Claude along with the quiz generation prompt
6. Claude generates questions grounded in the retrieved knowledge

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate-quiz` | Generate 5 MCQs for a topic |
| POST | `/api/check-answer` | Evaluate a user's answer |
| GET | `/api/topics` | List available knowledge topics |

## Adding More Topics

Simply add a `.txt` file to the `/knowledge/` folder and restart the server. The RAG pipeline will automatically index it.

---

Built with Python, FastAPI, ChromaDB, and Anthropic Claude.
