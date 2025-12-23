# 🥈 Silver Retriever (V1)

**A Modular, Offline RAG System for Low-Resource Environments.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![Scikit-Learn](https://img.shields.io/badge/Engine-Scikit_Learn-orange) ![Status](https://img.shields.io/badge/Status-Operational-success)

## 📖 Introduction

Silver Retriever is a specialized, offline-first RAG system. **Inspired by AI Singapore's (AISG) robust "Golden Retriever,"** this project represents my initiative to "walk the walk" in AI Engineering.

My goal was to reverse-engineer the core concepts of retrieval systems (like the Golden Retriever) but adapt them for **extreme resource constraints**. While modern systems rely on heavy GPUs for Neural Embeddings (BERT/LLMs), Silver Retriever proves that effective search pipelines can be built on legacy hardware (e.g., a old MacBook) by using a smart hybrid approach:

1.  **Statistical Search (TF-IDF):** Delivers instant, CPU-friendly retrieval speed.
2.  **Rule-Based Plugins (The Brain):** Simulates "reasoning" by using domain-specific logic to extract deadlines, definitions, and tasks.

## 🚀 Key Features
* **100% Offline:** No API keys, no internet required. Privacy-first.
* **Plugin System:** Auto-detects intents (e.g., "When is the deadline?" triggers the `Admin` plugin).
* **Smart Chunking:** Uses overlapping windows to preserve context across sentences.
* **Visual Feedback:** UI badges indicate *why* a result was chosen (e.g., "Contains Date").
* **Multi-Subject:** Supports any PDF/TXT file (AIAP, Feng Shui, Novels, etc.).

## 🏗️ Architecture

The system follows a 3-Layer Modular Architecture:

[ User Query ]
      ⬇
[ Interface (app.py) ] 
      ⬇
[ The Brain (src/brain.py) ] ────➡ [ Check Plugins ]
      ⬇                                   ⬇
      ⬇                           (Admin, Feng Shui, AI...)
      ⬇                                   ⬇
[ The Engine (src/engine.py) ] ⬅── [ Boost Scores ]
      ⬇
[ TF-IDF Index (data/storage.pkl) ]

## 📂 Project Structure

```plaintext
Silver_Retriever/
├── app.py                 # The User Interface (Streamlit)
├── src/
│   ├── engine.py          # The Core: Ingestion, Chunking, Vectorization
│   ├── brain.py           # The Manager: Routes queries to plugins
│   └── plugins/           # The Skills Folder
│       ├── admin.py       # Detects dates/tasks
│       ├── marketing.py   # Detects SEO/SEM terms
│       ├── feng_shui.py   # Detects placement advice
│       └── ...
├── data/
│   └── raw/               # (GitIgnored) Where your PDFs live
├── .github/workflows/     # CI/CD Pipelines
└── requirements.txt       # Dependencies
```
## 🛠️ Installation & Usage

1. Clone the repo
```bash
git clone https://github.com/Lwg78/Silver-Retriever.git
cd Silver-Retriever
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Run the App
```bash
streamlit run app.py
```

## 📊 Insights & Limitations
* **Why TF-IDF?** On a dual-core CPU with 8GB RAM, embedding models (like ChromaDB + SentenceTransformers) introduce 2-3 seconds of latency per query. TF-IDF is instant (<0.1s).

* **The Trade-off**: TF-IDF searches for keywords, not meaning. "What is the cost?" might not match "The price is $50".

* **The Fix**: We implemented **Query Expansion** (synonyms) and **Plugins** to bridge this gap without upgrading hardware.

## 🔜 Future Roadmap
* [ ] Add BM25 Ranking for better document length normalization.

* [ ] Add "Fuzzy Matching" for typo tolerance.

* [ ] Export search results to CSV.


---
