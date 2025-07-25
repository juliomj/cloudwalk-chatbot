# cloudwalk_chatbot.py (versão sem OpenAI)

"""
Chatbot com RAG que responde perguntas sobre a CloudWalk e seus produtos,
usando modelo de linguagem local via HuggingFace (sem precisar da OpenAI).
"""

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import os

# Inicializa app FastAPI
app = FastAPI()

# Base de conhecimento estática (simulando busca por documentos)
DOCUMENTS = [
    {
        "source": "cloudwalk.io",
        "text": "CloudWalk é uma fintech brasileira que oferece soluções de pagamento como o InfinitePay. Sua missão é levar prosperidade aos empreendedores do Brasil por meio da tecnologia."
    },
    {
        "source": "infinitepay.io",
        "text": "InfinitePay é uma solução da CloudWalk com maquininhas, conta digital e Tap to Pay com taxas acessíveis para pequenos negócios."
    }
]

# Carrega modelo de embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Carrega modelo de linguagem local via HuggingFace (Mistral ou Phi3 são bons)
generator = pipeline("text-generation", model="microsoft/phi-1_5", max_new_tokens=300)


# Função de recuperação de contexto (RAG simples)
def retrieve_context(query: str, top_k: int = 2) -> List[str]:
    query_embedding = embedding_model.encode([query])
    doc_texts = [doc["text"] for doc in DOCUMENTS]
    doc_embeddings = embedding_model.encode(doc_texts)

    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]

    return [doc_texts[i] for i in top_indices]

# Modelo da entrada da pergunta
class UserQuery(BaseModel):
    question: str

# Endpoint principal
@app.post("/ask")
def ask_bot(user_query: UserQuery):
    context = retrieve_context(user_query.question)
    prompt = f"""
Você é um assistente especializado em responder perguntas sobre a CloudWalk, seus produtos e missão.
Use o contexto abaixo para formular a resposta:

Contexto:
{chr(10).join(context)}

Pergunta: {user_query.question}
Resposta:
"""
    result = generator(prompt)
    return {"answer": result[0]["generated_text"].split("Resposta:")[-1].strip()}
