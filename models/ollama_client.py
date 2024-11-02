# models/ollama_client.py
import aiohttp
import yaml
import logging
import json

with open('configs/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

OLLAMA_API_ENDPOINT = config['ollama_api_endpoint']
MODEL_NAME = config['ollama_model_name']

class OllamaClient:
    async def get_response(self, prompt):
        payload = {
            'model': MODEL_NAME,
            'prompt': prompt
        }
        logging.info("Enviando requisição para o Ollama...")
        async with aiohttp.ClientSession() as session:
            async with session.post(OLLAMA_API_ENDPOINT, json=payload) as resp:
                resp.raise_for_status()
                response_text = ''
                # Ler a resposta NDJSON linha por linha
                async for line in resp.content:
                    line = line.decode('utf-8').strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        # Extrair o conteúdo gerado
                        content = data.get('response') or data.get('generated_text') or data.get('data') or ''
                        response_text += content
                    except json.JSONDecodeError:
                        continue
                logging.info(f"Resposta do Ollama: {response_text}")
                return response_text
