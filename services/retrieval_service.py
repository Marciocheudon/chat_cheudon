# services/retrieval_service.py
import faiss
import numpy as np
import pandas as pd
import logging

class RetrievalService:
    def __init__(self, index_path, data_path):
        try:
            self.index = faiss.read_index(index_path)
            self.data = pd.read_csv(data_path)
        except Exception as e:
            logging.error(f"Erro ao carregar índice FAISS ou dados CSV: {e}")
            raise e

    def search_similar(self, embedding, top_k=5):
        try:
            distances, indices = self.index.search(np.array([embedding]).astype('float32'), top_k)
            results = self.data.iloc[indices[0]].to_dict('records')
            logging.info(f"Dados recuperados: {results}")
            return results
        except Exception as e:
            logging.error(f"Erro na busca similar: {e}")
            return []
