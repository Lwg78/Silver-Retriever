"""
RobustEngine V2
---------------
Upgrades:
1. Smart Overlapping Chunking (Context Preservation)
2. Query Expansion (Synonyms)
3. Better Error Handling
"""

import os
import re
import pickle
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
STORAGE_FILE = os.path.join(BASE_DIR, "data", "storage.pkl")

# SYNONYM DICTIONARY (Simple AI)
SYNONYM_MAP = {
    "neural network": ["deep learning", "ann", "model"],
    "deadline": ["due date", "submission", "cutoff", "1900 hrs"],
    "aiap": ["apprenticeship", "assessment"],
    "task": ["deliverable", "requirement", "part"],
}

class RobustEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
        self.documents = []
        self.metadata = []
        self.vectors = None

        os.makedirs(DATA_PATH, exist_ok=True)
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, "rb") as f:
                    data = pickle.load(f)
                    self.documents = data["documents"]
                    self.metadata = data["metadata"]
                if self.documents:
                    self.vectors = self.vectorizer.fit_transform(self.documents)
            except Exception:
                self.documents = []
                self.metadata = []

    def _save_memory(self):
        with open(STORAGE_FILE, "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "metadata": self.metadata
            }, f)

    def _expand_query(self, query):
        """Adds synonyms to the search query for better matching."""
        terms = query.lower().split()
        expanded = terms.copy()
        for term in terms:
            if term in SYNONYM_MAP:
                expanded.extend(SYNONYM_MAP[term])
        return " ".join(expanded)

    def ingest_file(self, file_path):
        filename = os.path.basename(file_path)
        if filename in self.get_loaded_files():
            return False

        text = ""
        try:
            if file_path.endswith(".pdf"):
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text += (page.extract_text() or "") + " "
            else:
                with open(file_path, encoding="utf-8") as f:
                    text = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return False

        # --- NEW: SMART OVERLAP CHUNKING ---
        # Instead of splitting by sentence, we split by size with overlap.
        # This prevents breaking a "Deadline: <date>" across two chunks.
        clean_text = re.sub(r"\s+", " ", text).strip()
        
        chunk_size = 500  # Characters
        overlap = 100     # Characters
        
        for i in range(0, len(clean_text), chunk_size - overlap):
            chunk = clean_text[i : i + chunk_size]
            if len(chunk) > 50: # Ignore tiny fragments
                self.documents.append(chunk)
                self.metadata.append({
                    "text": chunk,
                    "source": filename
                })

        self.vectors = self.vectorizer.fit_transform(self.documents)
        self._save_memory()
        return True

    def search(self, query, top_k=10):
        if self.vectors is None:
            return []

        # 1. Expand Query (Add Synonyms)
        expanded_query = self._expand_query(query)
        
        # 2. Vector Search
        query_vec = self.vectorizer.transform([expanded_query])
        tfidf_scores = cosine_similarity(query_vec, self.vectors).flatten()

        # 3. Keyword Boosting (Exact Match Bonus)
        keywords = set(query.lower().split())
        results = []

        for i, base_score in enumerate(tfidf_scores):
            # boost slightly if exact original keywords exist
            text = self.documents[i].lower()
            overlap_count = sum(1 for k in keywords if k in text)
            final_score = base_score + (0.05 * overlap_count)

            if final_score > 0.05:
                results.append({
                    "score": final_score,
                    "payload": self.metadata[i]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_loaded_files(self):
        return list({m["source"] for m in self.metadata})

    def nuke_library(self):
        shutil.rmtree(DATA_PATH, ignore_errors=True)
        if os.path.exists(STORAGE_FILE):
            os.remove(STORAGE_FILE)
        os.makedirs(DATA_PATH, exist_ok=True)
        self.documents = []
        self.metadata = []
        self.vectors = None