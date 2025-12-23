# 🥈 Silver Retriever (V1)

**A Modular, Offline RAG System for Low-Resource Environments.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![Scikit-Learn](https://img.shields.io/badge/Engine-Scikit_Learn-orange) ![Status](https://img.shields.io/badge/Status-Operational-success)

## 📖 Introduction
Silver Retriever is a "Study Buddy" search engine designed to run entirely offline on legacy hardware (e.g., MacBook Air 2017). Unlike modern RAG systems that require heavy GPUs for Neural Embeddings (BERT/LLMs), Silver Retriever uses a hybrid approach:
1.  **Statistical Search (TF-IDF)** for speed and efficiency.
2.  **Rule-Based Plugins (The Brain)** for domain-specific intelligence (finding deadlines, definitions, etc.).

## 🚀 Key Features
* **100% Offline:** No API keys, no internet required. Privacy-first.
* **Plugin System:** Auto-detects intents (e.g., "When is the deadline?" triggers the `Admin` plugin).
* **Smart Chunking:** Uses overlapping windows to preserve context across sentences.
* **Visual Feedback:** UI badges indicate *why* a result was chosen (e.g., "Contains Date").
* **Multi-Subject:** Supports any PDF/TXT file (AIAP, Feng Shui, Novels, etc.).

## 🏗️ Architecture

The system follows a 3-Layer Modular Architecture:

```mermaid
graph TD
    User[User Query] --> UI[app.py (Streamlit)]
    UI --> Brain[src/brain.py]
    
    subgraph "The Brain (Logic)"
    Brain --> CheckPlugins{Check Triggers}
    CheckPlugins -->|Match| Plugin[src/plugins/*.py]
    CheckPlugins -->|No Match| Fallback[General Search]
    end
    
    subgraph "The Engine (Muscle)"
    Brain --> Engine[src/engine.py]
    Engine -->|TF-IDF| Storage[(data/storage.pkl)]
    end
    
    Plugin -->|Boost Score| UI
    Engine -->|Raw Results| UI
```

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
git clone [https://github.com/YOUR_USERNAME/Silver-Retriever.git](https://github.com/YOUR_USERNAME/Silver-Retriever.git)
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