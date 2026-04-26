import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class QuizEngine:

    def generate_questions(self, topic: str, context: str) -> list:
        prompt = f"""You are a quiz generator. Using the context below, generate 5 multiple choice questions about "{topic}".

CONTEXT:
{context}

Return ONLY a valid JSON array. No markdown, no explanation. Format exactly like this:
[
  {{
    "id": 1,
    "question": "What is ...?",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "correct": "A",
    "explanation": "A is correct because..."
  }}
]

Rules:
- Make questions progressively harder (easy → medium → hard)
- All 4 options must be plausible
- Explanations must be educational (2-3 sentences)
- Base questions on the context provided"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        questions = json.loads(raw)
        return questions

    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str, topic: str) -> dict:
        is_correct = user_answer.strip().upper() == correct_answer.strip().upper()

        prompt = f"""A student answered a quiz question about "{topic}".

Question: {question}
Student's answer: {user_answer}
Correct answer: {correct_answer}
Was correct: {is_correct}

Write a helpful 2-3 sentence feedback message.
- If correct: praise them and add an interesting extra fact
- If wrong: gently explain why the correct answer is right and what they might have confused

Return ONLY a JSON object:
{{"is_correct": {str(is_correct).lower()}, "feedback": "your feedback here", "tip": "one quick study tip for this topic"}}"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return result
