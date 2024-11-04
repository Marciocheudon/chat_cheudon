# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.response_generator import generate_response
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question_request: QuestionRequest):
    question = question_request.question
    logging.info(f"Pergunta recebida: {question}")

    if not question:
        raise HTTPException(status_code=400, detail="A pergunta não pode ser vazia.")

    try:
        response = await generate_response(question)
        logging.info(f"Resposta gerada: {response}")
        return {"response": response}
    except Exception as e:
        logging.error(f"Erro ao gerar resposta: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")