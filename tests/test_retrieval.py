"""Automated tests for the CollegeQuery FAQ retrieval system.

Test categories
---------------
1. Dataset loading and validation
2. Search result shape and content
3. Input validation (empty queries, bad top_k)
4. Error handling (missing files, empty datasets, malformed CSVs)

Mocking is used for error-handling tests so they run quickly without
loading the real embedding model.
"""

from __future__ import annotations

import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.retriever import FAQRetriever, DEFAULT_DATA_PATH


# ---------------------------------------------------------------------------
# Helper: create a tiny CSV in a temp file for isolated testing
# ---------------------------------------------------------------------------

def _write_temp_csv(
    rows: list[dict[str, str]],
    fieldnames: tuple[str, ...] = ("id", "category", "question", "answer"),
) -> str:
    """Write *rows* to a temporary CSV and return the file path."""
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


# ===================================================================
# Tests that use the REAL model + dataset (integration tests)
# ===================================================================

class TestFAQRetrieverIntegration(unittest.TestCase):
    """Integration tests that load the real model and FAQ data.

    The model is loaded once per class to keep the test suite fast.
    These tests require the embedding model to be available (downloaded
    on first run).
    """

    retriever: FAQRetriever  # set in setUpClass

    @classmethod
    def setUpClass(cls) -> None:
        cls.retriever = FAQRetriever()

    # -- Dataset loading --------------------------------------------------

    def test_faq_dataset_loads_successfully(self) -> None:
        """The default CSV should load at least 30 FAQ entries."""
        self.assertGreaterEqual(len(self.retriever.faqs), 30)

    def test_faq_entries_have_required_fields(self) -> None:
        """Every loaded FAQ row must contain id, category, question, answer."""
        required = {"id", "category", "question", "answer"}
        for row in self.retriever.faqs:
            self.assertTrue(
                required.issubset(row.keys()),
                f"Row missing fields: {required - row.keys()}",
            )

    def test_document_embeddings_shape_matches_faq_count(self) -> None:
        """The embedding matrix should have one row per FAQ entry."""
        self.assertEqual(
            self.retriever.document_embeddings.shape[0],
            len(self.retriever.faqs),
        )

    # -- Search result count ----------------------------------------------

    def test_returns_requested_number_of_results(self) -> None:
        results = self.retriever.search("Where is the exam timetable?", top_k=2)
        self.assertEqual(len(results), 2)

    def test_returns_default_three_results(self) -> None:
        results = self.retriever.search("Tell me about admissions")
        self.assertEqual(len(results), 3)

    def test_top_k_capped_at_faq_count(self) -> None:
        """Requesting more results than FAQs should return all FAQs."""
        results = self.retriever.search("anything", top_k=9999)
        self.assertEqual(len(results), len(self.retriever.faqs))

    # -- Search result content --------------------------------------------

    def test_results_include_expected_fields(self) -> None:
        result = self.retriever.search("How can I contact the library?", top_k=1)[0]
        for field in ("id", "category", "question", "answer", "score"):
            self.assertIn(field, result, f"Missing field: {field}")

    def test_scores_are_floats_between_minus_one_and_one(self) -> None:
        results = self.retriever.search("scholarship eligibility", top_k=5)
        for r in results:
            self.assertIsInstance(r["score"], float)
            self.assertGreaterEqual(r["score"], -1.0)
            self.assertLessEqual(r["score"], 1.0)

    def test_results_are_sorted_by_descending_score(self) -> None:
        results = self.retriever.search("hostel accommodation", top_k=5)
        scores = [r["score"] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    # -- Input validation -------------------------------------------------

    def test_blank_query_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.retriever.search("   ")

    def test_empty_string_query_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.retriever.search("")

    def test_nonpositive_top_k_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.retriever.search("admission dates", top_k=0)

    def test_negative_top_k_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.retriever.search("fees", top_k=-3)


# ===================================================================
# Tests that use MOCKING (no real model needed)
# ===================================================================

class TestFAQRetrieverErrorHandling(unittest.TestCase):
    """Unit tests for error paths, using mocks to avoid model downloads."""

    def test_missing_file_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            FAQRetriever(data_path="/nonexistent/path/faq.csv")

    def test_empty_csv_raises_value_error(self) -> None:
        """A CSV with headers but no data rows should be rejected."""
        path = _write_temp_csv([])
        try:
            with patch(
                "backend.retriever.SentenceTransformer"
            ) as MockModel:
                with self.assertRaises(ValueError) as ctx:
                    FAQRetriever(data_path=path)
                self.assertIn("No FAQ rows", str(ctx.exception))
        finally:
            os.unlink(path)

    def test_csv_missing_columns_raises_value_error(self) -> None:
        """A CSV missing required columns should be rejected."""
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["id", "question"])
            writer.writeheader()
            writer.writerow({"id": "1", "question": "test?"})
        try:
            with patch(
                "backend.retriever.SentenceTransformer"
            ) as MockModel:
                with self.assertRaises(ValueError) as ctx:
                    FAQRetriever(data_path=path)
                self.assertIn("missing required columns", str(ctx.exception))
        finally:
            os.unlink(path)

    def test_invalid_top_k_type_raises_value_error(self) -> None:
        """Passing a non-integer top_k should raise ValueError."""
        path = _write_temp_csv([
            {"id": "1", "category": "Test", "question": "Q?", "answer": "A."},
        ])
        try:
            import numpy as np
            with patch("backend.retriever.SentenceTransformer") as MockModel:
                mock_instance = MagicMock()
                mock_instance.encode.return_value = np.random.randn(1, 384).astype(np.float32)
                MockModel.return_value = mock_instance

                retriever = FAQRetriever(data_path=path)
                with self.assertRaises(ValueError):
                    retriever.search("test", top_k=2.5)  # type: ignore[arg-type]
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
