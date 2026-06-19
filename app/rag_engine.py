import numpy as np
from app.embeddings import model


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors
    """
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def find_similar(embeddings, data, query):
    """
    Find top matching incidents for a given issue
    """

    # ✅ Step 1: Convert query to embedding
    query_vector = model.encode([query])[0]

    # ✅ Step 2: Compute similarity scores
    similarity_scores = []
    for emb in embeddings:
        score = cosine_similarity(query_vector, emb)
        similarity_scores.append(score)

    # ✅ Step 3: Get indices of top matches (top 2)
    top_indices = np.argsort(similarity_scores)[-2:][::-1]

    # ✅ Step 4: Fetch matching records
    results = [data[i] for i in top_indices]
    top_scores = [similarity_scores[i] for i in top_indices]

    # ✅ Step 5: Return results + scores
    return results, top_scores