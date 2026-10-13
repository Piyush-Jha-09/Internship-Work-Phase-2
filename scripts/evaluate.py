"""Run the 10 evaluation queries and print results for retrieval-results.md."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.retriever import FAQRetriever

QUERIES = [
    "What documents do I need for admission?",
    "When are admission applications open?",
    "Where can I check my tuition fee?",
    "Is there any scholarship information?",
    "Where can I find the syllabus?",
    "How do I get the examination timetable?",
    "Where can I see my results?",
    "What are the library opening hours?",
    "How can I contact the placement cell?",
    "How do I request a bonafide certificate?",
]


def main() -> None:
    print("Loading model...")
    retriever = FAQRetriever()
    print(f"Loaded {len(retriever.faqs)} FAQs.\n")

    for i, query in enumerate(QUERIES, start=1):
        results = retriever.search(query, top_k=3)
        top = results[0]
        print(f"--- Query {i}: {query}")
        print(f"    Top-1 Category: {top['category']}")
        print(f"    Top-1 Question: {top['question']}")
        print(f"    Top-1 Score:    {top['score']:.4f}")
        for rank, r in enumerate(results, 1):
            print(f"    [{rank}] ({r['score']:.4f}) [{r['category']}] {r['question']}")
        print()


if __name__ == "__main__":
    main()
