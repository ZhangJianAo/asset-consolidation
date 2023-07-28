import json

import numpy as np

from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

import asset_data


# Define the model we want to use (it'll download itself)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

sentences = [json.dumps(i) for i in asset_data.ASSETS]

# vector embeddings created from dataset
embeddings = model.encode(sentences)


def similarity_match(query_text):
    global cosine_similarity, e, s

    # query vector embedding
    query_embedding = model.encode(query_text)

    # define our distance metric
    def cosine_similarity(a, b):
        return np.dot(a, b) / (norm(a) * norm(b))

    # run semantic similarity search
    print(f"Query: {query_text}")
    for e, s in zip(embeddings, sentences):
        print(s, " -> similarity score = ",
              cosine_similarity(e, query_embedding))


for f in asset_data.FIND_ASSETS:
    print("=============\n")
    similarity_match(json.dumps(f))
