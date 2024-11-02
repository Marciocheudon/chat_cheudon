# data_processing.py
from models.embedding_model import EmbeddingModel
import pandas as pd
import numpy as np
import faiss

def create_faiss_index(data_path, index_path):
    data = pd.read_csv(data_path)
    embedding_model = EmbeddingModel()
    embeddings = np.array([embedding_model.generate_embedding(text) for text in data['info']])
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, index_path)

if __name__ == "__main__":
    create_faiss_index('data/personal_data.csv', 'data/embeddings/embeddings_index.faiss')
