# services/retrieval_service.py
import faiss
import numpy as np
import pandas as pd

class RetrievalService:
    def __init__(self, index_path, data_path):
        self.index = faiss.read_index(index_path)
        self.data = pd.read_csv(data_path)
    
    def search_similar(self, embedding, top_k=5):
        distances, indices = self.index.search(np.array([embedding]), top_k)
        results = self.data.iloc[indices[0]].to_dict('records')
        return results
