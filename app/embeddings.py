from sentence_transformers import SentenceTransformer
import json
import os

# ✅ Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def load_data():
    # ✅ Safe file path handling
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, 'data', 'incidents.json')

    with open(file_path, 'r') as f:
        return json.load(f)


def build_index(data):
    # ✅ Convert incident text into embeddings
    texts = [d["incident"] for d in data]

    embeddings = model.encode(texts)

    return embeddings