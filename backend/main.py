from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import traceback
from dotenv import load_dotenv
load_dotenv()

from rag import RAGPipeline
from quiz import QuizEngine

app = FastAPI(title="TopicMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGPipeline()
quiz = QuizEngine()

FRONTEND = os.path.join(os.path.dirname(__file__), "../frontend")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND, "index.html"))

@app.get("/style.css")
def serve_css():
    return FileResponse(os.path.join(FRONTEND, "style.css"))

@app.get("/app.js")
def serve_js():
    return FileResponse(os.path.join(FRONTEND, "app.js"))

class TopicRequest(BaseModel):
    topic: str

class AnswerRequest(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    topic: str

@app.post("/api/generate-quiz")
async def generate_quiz(req: TopicRequest):
    try:
        context = rag.retrieve(req.topic)
        questions = quiz.generate_questions(req.topic, context)
        return {"questions": questions, "context_used": context[:300] + "..."}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check-answer")
async def check_answer(req: AnswerRequest):
    try:
        feedback = quiz.evaluate_answer(
            req.question, req.user_answer, req.correct_answer, req.topic
        )
        return feedback
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/topics")
def get_topics():
    topics = []
    knowledge_dir = os.path.join(os.path.dirname(__file__), "../knowledge")
    for f in os.listdir(knowledge_dir):
        if f.endswith(".txt"):
            topics.append(f.replace(".txt", "").replace("_", " ").title())
    return {"topics": topics}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
