# services/response_generator.py
import asyncio
from models.embedding_model import EmbeddingModel
from services.retrieval_service import RetrievalService
from services.context_builder import ContextBuilder
from models.ollama_client import OllamaClient
import yaml
import logging

with open('configs/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

embedding_model = EmbeddingModel(config['embedding_model_name'])
retrieval_service = RetrievalService(
    config['faiss_index_path'],
    config['personal_data_path']
)
context_builder = ContextBuilder()
ollama_client = OllamaClient()

async def generate_response(question):
    logging.info("Gerando embedding da pergunta...")
    question_embedding = await asyncio.to_thread(embedding_model.generate_embedding, question)

    logging.info("Buscando dados relevantes...")
    retrieved_data = await asyncio.to_thread(
        retrieval_service.search_similar,
        question_embedding,
        config['top_k']
    )

    logging.info("Construindo o contexto...")
    context = await asyncio.to_thread(context_builder.build_context, retrieved_data)

    prompt = f"{context}\n\nPergunta: {question}\nResposta:"

    logging.info("Enviando prompt para o Ollama...")
    response = await ollama_client.get_response(prompt)  # Remova asyncio.to_thread

    return response
