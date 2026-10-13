# CollegeQuery — AI-Powered College Information Chatbot

A semantic-search prototype that retrieves relevant college FAQ entries in response to natural-language student questions, built as part of an AI internship project.

> **Status — Week 2 Milestone:** This repository implements FAQ retrieval using sentence embeddings and cosine similarity. It is a retrieval system, not a complete LLM-powered chatbot. The included FAQ data is **illustrative sample data** and must be replaced with verified information before any real use.

---

## Problem Statement

Students frequently need quick, reliable answers to common questions about admissions, fees, examinations, placements, and campus facilities. Traditional FAQ pages require browsing through long lists. CollegeQuery uses **semantic search** to understand the intent behind a question and surface the most relevant FAQ entries automatically.

## Features Implemented (Week 2)

- ✅ CSV-based FAQ knowledge base with **35 entries** across 10 categories
- ✅ Sentence-embedding retrieval using `sentence-transformers/all-MiniLM-L6-v2`
- ✅ Cosine-similarity ranking of FAQ entries against user queries
- ✅ Interactive command-line query interface with formatted output
- ✅ Comprehensive automated test suite (16 tests — integration + unit)
- ✅ Retrieval evaluation documentation with real test results
- ✅ Clean, modular, documented Python code with type hints

## Features Planned (Future Milestones)

- ⬜ FastAPI REST endpoint for the retrieval module
- ⬜ React or web-based chat interface
- ⬜ RAG-based answer generation using an LLM
- ⬜ Verified, institution-specific FAQ content
- ⬜ User authentication and chat history
- ⬜ Deployment to a cloud platform

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Similarity | NumPy dot product (normalised embeddings) |
| Data | CSV with Python `csv` module |
| Testing | `unittest` (stdlib) + `pytest` |
| Version Control | Git / GitHub |

No paid APIs, API keys, or cloud infrastructure are required for this milestone.

## Repository Structure

```text
CollegeQuery-Chatbot/
├── README.md                  ← This file
├── requirements.txt           ← Python dependencies
├── .gitignore                 ← Files excluded from version control
├── data/
│   └── college_faq.csv        ← 35 illustrative FAQ entries
├── backend/
│   ├── __init__.py
│   └── retriever.py           ← FAQRetriever class (core module)
├── scripts/
│   └── ask.py                 ← Interactive CLI demo
├── tests/
│   ├── __init__.py
│   └── test_retrieval.py      ← 16 automated tests
└── docs/
    └── retrieval-results.md   ← Retrieval evaluation notes
```

## Setup Instructions (Windows)

### 1. Clone the repository
```powershell
git clone https://github.com/<your-username>/CollegeQuery-Chatbot.git
cd CollegeQuery-Chatbot
```

### 2. Create and activate a virtual environment
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, use Command Prompt instead:
```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the prototype
```powershell
python scripts/ask.py
```
The first run downloads the embedding model (~80 MB). Subsequent runs use the cached model.

### 5. Run the automated tests
```powershell
python -m pytest tests/ -v
```
Or using unittest:
```powershell
python -m unittest discover -s tests -v
```

## Sample Queries

At the interactive prompt, try questions like:

| Query | Expected Category |
|---|---|
| What documents do I need for admission? | Admissions |
| How much are the tuition fees? | Fees |
| Is there any scholarship for merit students? | Fees |
| Where can I find the syllabus? | Academics |
| When is the exam timetable released? | Examinations |
| What are the library hours? | Library |
| How do I contact the placement cell? | Placements |
| Is hostel accommodation available? | Campus Facilities |
| How do I get a bonafide certificate? | Student Support |
| Where are official announcements posted? | General |

Type `exit` or `quit` to leave the interactive session.

## How Retrieval Works

```
┌──────────────┐     ┌───────────────────┐     ┌──────────────┐
│  User Query  │────▶│ Sentence Encoder  │────▶│ Query Vector │
└──────────────┘     │ (all-MiniLM-L6-v2)│     └──────┬───────┘
                     └───────────────────┘            │
                                                      │ cosine
┌──────────────┐     ┌───────────────────┐            │ similarity
│  FAQ CSV     │────▶│ Pre-encoded FAQ   │────────────┤
│  (35 entries)│     │ Embeddings        │            │
└──────────────┘     └───────────────────┘            ▼
                                               ┌──────────────┐
                                               │ Ranked       │
                                               │ Results      │
                                               │ (top-k)      │
                                               └──────────────┘
```

1. FAQ entries are loaded from `data/college_faq.csv` and encoded **once** at startup.
2. Each user query is encoded into the same vector space.
3. Cosine similarity between the query vector and all FAQ vectors determines relevance.
4. The top-k most similar FAQ entries are returned with their scores.

Similarity scores are **relative ranking signals**, not calibrated confidence probabilities.

## Limitations

- The FAQ CSV contains **generic, illustrative sample data** — not verified policies for any specific institution.
- Semantic retrieval can surface a related but incorrect FAQ; always review results critically.
- No user accounts, chat history, database, frontend, API endpoint, or LLM answer generation is implemented in this milestone.
- The embedding model requires an initial download (~80 MB) and compatible hardware.
- The prototype has been tested on a small dataset; retrieval quality on large datasets has not been evaluated.

## Future Development Roadmap

| Milestone | Description |
|---|---|
| Week 3 | Expose retrieval via FastAPI; add basic frontend |
| Week 4 | Integrate RAG with an LLM for answer generation |
| Week 5 | Replace sample data with verified college content |
| Week 6 | Deploy, evaluate end-to-end, and document findings |

## Git Commands

```bash
git add .
git commit -m "Implement Week 2: FAQ retrieval prototype with tests and evaluation"
git push origin main
```

## License

This project is developed as part of an AI internship programme. See repository settings for licence details.
