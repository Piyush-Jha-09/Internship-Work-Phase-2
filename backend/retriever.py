"""FAQ retrieval module for the CollegeQuery prototype.

This module provides the ``FAQRetriever`` class, which loads a CSV
knowledge-base of frequently asked questions, encodes them using a
sentence-transformer model, and answers natural-language queries by
ranking FAQ entries with cosine similarity.

Design notes
------------
* The FAQ documents are encoded once at initialisation; subsequent
  queries only encode the query string, keeping latency low.
* The class is stateless after init and safe to reuse across multiple
  queries (e.g. behind a FastAPI endpoint).
* Normalised embeddings are used so that ``np.dot`` is equivalent to
  cosine similarity, avoiding a separate sklearn call.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity  # kept for reference / optional use

logger = logging.getLogger(__name__)

DEFAULT_DATA_PATH: Path = Path(__file__).resolve().parents[1] / "data" / "college_faq.csv"
DEFAULT_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

_REQUIRED_CSV_COLUMNS = {"id", "category", "question", "answer"}


class FAQRetriever:
    """Retrieve the most relevant FAQ rows for a natural-language query.

    Parameters
    ----------
    data_path : str | Path
        Path to the CSV file containing FAQ entries.
        Must include columns: ``id``, ``category``, ``question``, ``answer``.
    model_name : str
        HuggingFace model identifier for the sentence-transformer to use.

    Raises
    ------
    FileNotFoundError
        If *data_path* does not exist.
    ValueError
        If the CSV is empty or is missing required columns.
    """

    def __init__(
        self,
        data_path: str | Path = DEFAULT_DATA_PATH,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        self.data_path = Path(data_path)
        self._validate_file()

        self.faqs: list[dict[str, str]] = self._load_csv()
        self._validate_rows()

        logger.info("Loading sentence-transformer model: %s", model_name)
        self.model: SentenceTransformer = SentenceTransformer(model_name)

        # Build a rich document string for each FAQ so the embedding captures
        # category, question, *and* answer semantics.
        self.documents: list[str] = [
            f"Category: {row['category']}. Question: {row['question']} Answer: {row['answer']}"
            for row in self.faqs
        ]

        # Encode all FAQ documents once; normalise so dot-product == cosine sim.
        self.document_embeddings: np.ndarray = self.model.encode(
            self.documents, convert_to_numpy=True, normalize_embeddings=True
        )
        logger.info(
            "Indexed %d FAQ documents (%d-dim embeddings).",
            len(self.faqs),
            self.document_embeddings.shape[1],
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """Return the *top_k* FAQ entries most similar to *query*.

        Each result dict contains the CSV fields (``id``, ``category``,
        ``question``, ``answer``) plus a ``score`` key with the cosine
        similarity rounded to four decimal places.

        Parameters
        ----------
        query : str
            A natural-language question from the user.
        top_k : int
            Number of results to return (must be ≥ 1).

        Raises
        ------
        ValueError
            If *query* is blank or *top_k* < 1.
        """
        query = query.strip()
        if not query:
            raise ValueError("Query must not be empty.")
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be a positive integer (>= 1).")

        query_embedding: np.ndarray = self.model.encode(
            [query], convert_to_numpy=True, normalize_embeddings=True
        )

        # Dot product of normalised vectors == cosine similarity.
        scores: np.ndarray = np.dot(self.document_embeddings, query_embedding[0])

        # Rank indices by descending score; cap at available FAQ count.
        effective_k = min(top_k, len(self.faqs))
        ranked_indices = np.argsort(scores)[::-1][:effective_k]

        results: list[dict[str, Any]] = []
        for idx in ranked_indices:
            row = dict(self.faqs[int(idx)])
            row["score"] = round(float(scores[idx]), 4)
            results.append(row)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_file(self) -> None:
        """Raise ``FileNotFoundError`` if the CSV path does not exist."""
        if not self.data_path.exists():
            raise FileNotFoundError(
                f"FAQ data file not found: {self.data_path}"
            )

    def _load_csv(self) -> list[dict[str, str]]:
        """Read the CSV file and return a list of row dicts."""
        with self.data_path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        return rows

    def _validate_rows(self) -> None:
        """Ensure the loaded CSV has the required columns and is not empty."""
        if not self.faqs:
            raise ValueError(f"No FAQ rows found in {self.data_path}")

        present_columns = set(self.faqs[0].keys())
        missing = _REQUIRED_CSV_COLUMNS - present_columns
        if missing:
            raise ValueError(
                f"FAQ CSV is missing required columns: {sorted(missing)}. "
                f"Found columns: {sorted(present_columns)}"
            )
