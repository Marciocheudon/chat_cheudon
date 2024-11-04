# models/ollama_client.py

import aiohttp
import yaml
import logging
import json
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, config_path='configs/config.yaml'):
       
        self.api_endpoint, self.model_name = self.load_config(config_path)

    def load_config(self, config_path):
      
        if not os.path.exists(config_path):
            logger.error(f"Arquivo de configuração '{config_path}' não encontrado.")
            raise FileNotFoundError(f"Arquivo de configuração '{config_path}' não encontrado.")

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                api_endpoint = config['ollama_api_endpoint']
                model_name = config['ollama_model_name']
                logger.info(f"Configurações carregadas: Endpoint={api_endpoint}, Modelo={model_name}")
                return api_endpoint, model_name
        except yaml.YAMLError as e:
            logger.error(f"Erro ao analisar o arquivo YAML: {e}")
            raise
        except KeyError as e:
            logger.error(f"Chave de configuração faltando: {e}")
            raise

    async def get_response(self, prompt):
      
        payload = {
            'model': self.model_name,
            'prompt': prompt,
            'max_tokens': 150,      # 50 a 200 tokens. Um valor mais alto, como 500 a 1000 tokens
            'temperature': 0.5,     # 0.0 a 1.0. Um valor mais baixo gera respostas mais conservadoras
            'top_p': 0.9            # 0.0 a 1.0. Um valor mais alto permite mais diversidade nas respostas
        }

        logger.info("Enviando requisição para o Ollama...")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_endpoint, json=payload) as resp:
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
                            logger.warning(f"Falha ao decodificar linha: {line}")
                            continue

                    logger.info(f"Resposta do Ollama: {response_text}")
                    return response_text

            except aiohttp.ClientError as e:
                logger.error(f"Erro na requisição ao Ollama: {e}")
                raise
            except Exception as e:
                logger.error(f"Erro inesperado ao obter resposta: {e}")
                raise


# Resumo de Configurações Recomendadas
# Respostas Curtas e Diretas:

# python
# Copiar código
# 'max_tokens': 100,
# 'temperature': 0.5,
# 'top_p': 0.7
# Respostas Longas e Detalhadas com Criatividade:

# python
# Copiar código
# 'max_tokens': 500,
# 'temperature': 0.8,
# 'top_p': 0.9
# Respostas Altamente Focadas e Determinísticas:

# python
# Copiar código
# 'max_tokens': 150,
# 'temperature': 0.2,
# 'top_p': 0.5