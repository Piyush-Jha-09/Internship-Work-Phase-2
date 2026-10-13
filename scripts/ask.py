"""Interactive command-line demo for CollegeQuery FAQ retrieval.

Run from the project root:
    python scripts/ask.py

The script loads the FAQ knowledge base, encodes it using a sentence-
transformer model, and then enters an interactive loop where the user
can type natural-language questions.  The top matching FAQ entries are
displayed together with their cosine-similarity scores.

This is a *retrieval* prototype — it does not generate answers.
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so ``backend`` can be imported
# regardless of the working directory.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.retriever import FAQRetriever  # noqa: E402


WELCOME_MESSAGE = r"""
╔══════════════════════════════════════════════════════════════╗
║         CollegeQuery — FAQ Retrieval Prototype              ║
╠══════════════════════════════════════════════════════════════╣
║  Ask any college-related question and the system will       ║
║  retrieve the most relevant FAQ entries from the knowledge  ║
║  base using semantic similarity.                            ║
║                                                             ║
║  • Results are retrieved from SAMPLE FAQ data.              ║
║  • This prototype does NOT generate AI answers.             ║
║  • Type 'exit' or 'quit' to leave.                          ║
╚══════════════════════════════════════════════════════════════╝
""".strip()

SEPARATOR = "─" * 62


def _print_results(results: list[dict]) -> None:
    """Pretty-print retrieved FAQ results to the console."""
    print(f"\n{SEPARATOR}")
    print(f"  Top {len(results)} Retrieved FAQ(s)")
    print(SEPARATOR)
    for rank, entry in enumerate(results, start=1):
        print(f"\n  [{rank}]  Category : {entry['category']}")
        print(f"       Question : {entry['question']}")
        print(f"       Answer   : {entry['answer']}")
        print(f"       Score    : {entry['score']:.4f}")
    print(f"\n{SEPARATOR}")
    print("  Note: Results are sample FAQ entries, not verified official policy.")
    print(SEPARATOR)


def main() -> None:
    """Entry point for the interactive FAQ retrieval demo."""
    print(WELCOME_MESSAGE)
    print("\nLoading embedding model (first run may download ~80 MB)…")

    try:
        retriever = FAQRetriever()
    except FileNotFoundError as exc:
        print(f"\n[Error] Could not find the FAQ data file:\n  {exc}")
        print("Make sure 'data/college_faq.csv' exists in the project root.")
        sys.exit(1)
    except Exception as exc:
        print(f"\n[Error] Failed to initialise the retriever:\n  {exc}")
        sys.exit(1)

    print(f"Ready — {len(retriever.faqs)} FAQ entries loaded.\n")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            print("  Please enter a question.\n")
            continue

        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            results = retriever.search(query, top_k=3)
            _print_results(results)
        except ValueError as exc:
            print(f"  [Input error] {exc}\n")
        except Exception as exc:
            print(f"  [Error] Something went wrong: {exc}\n")

        print()  # blank line before next prompt


if __name__ == "__main__":
    main()
