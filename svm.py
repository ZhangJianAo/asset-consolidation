import numpy as np
from numpy.linalg import norm

import asset_data

one_hot_vectors = asset_data.one_hot_encodes()


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def jaccard_similarity(a, b):
    total = len(a.union(b))
    inter = len(a.intersection(b))
    return inter / total


for i in range(3, len(asset_data.ASSETS)):
    query_vec = one_hot_vectors[i]
    print("\n=============\n")
    print("query: ", asset_data.ASSETS[i])
    for j in range(0, 3):
        print(asset_data.ASSETS[j])
        print(
            " -> cosine similarity score = ", cosine_similarity(query_vec, one_hot_vectors[j]),
            " -> jaccard similarity score = ", jaccard_similarity(asset_data.ASSET_BAGS[i], asset_data.ASSET_BAGS[j])
        )
