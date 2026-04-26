import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class RAGPipeline:
    def __init__(self):
        print("Loading embedding model...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma = chromadb.Client()
        self.collection = self.chroma.get_or_create_collection("topicmind")
        self._load_knowledge()

    def _load_knowledge(self):
        knowledge_dir = "../knowledge"
        if not os.path.exists(knowledge_dir):
            return
        for filename in os.listdir(knowledge_dir):
            if not filename.endswith(".txt"):
                continue
            filepath = os.path.join(knowledge_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            chunks = self._chunk_text(text)
            topic_name = filename.replace(".txt", "")
            for i, chunk in enumerate(chunks):
                doc_id = f"{topic_name}_{i}"
                embedding = self.embedder.encode(chunk).tolist()
                try:
                    self.collection.add(
                        ids=[doc_id],
                        embeddings=[embedding],
                        documents=[chunk],
                        metadatas=[{"topic": topic_name, "chunk": i}]
                    )
                except Exception:
                    pass
        print(f"RAG: Loaded knowledge from {knowledge_dir}")

    def _chunk_text(self, text, chunk_size=300, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

    def retrieve(self, topic: str, n_results: int = 5) -> str:
        query_embedding = self.embedder.encode(topic).tolist()
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, self.collection.count())
            )
            if results["documents"] and results["documents"][0]:
                return "\n\n".join(results["documents"][0])
        except Exception:
            pass

        # Fallback: ask Groq to generate context if no local knowledge found
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Give me 5 key facts about '{topic}' in 2-3 sentences each. Be educational and accurate."
            }]
        )
        return response.choices[0].message.content
