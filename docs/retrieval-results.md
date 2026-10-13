# Retrieval Evaluation — CollegeQuery Prototype

## Purpose

This document records genuine retrieval results from the CollegeQuery FAQ prototype. All results were obtained by running `scripts/evaluate.py` on 13 October 2026 using the `sentence-transformers/all-MiniLM-L6-v2` model with the 35-entry sample FAQ dataset.

> **Note:** Similarity scores are relative ranking signals, not calibrated confidence probabilities. A high score means the query is semantically close to the FAQ entry, but correctness must still be verified by a human.

## Test Environment

- Python 3.13.2 (Windows)
- sentence-transformers 6.1.0
- Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional embeddings)
- FAQ dataset: 35 entries across 10 categories

## Results Table

| # | Query | Expected Topic | Top-1 Retrieved FAQ | Top-1 Score | Relevant? | Notes |
|---|---|---|---|---|---|---|
| 1 | What documents do I need for admission? | Admissions | What documents might be needed when applying for admission? | 0.8240 | ✅ Yes | Strong match. Correct category and topic. |
| 2 | When are admission applications open? | Admissions | Where can I find the latest admission dates? | 0.6517 | ✅ Yes | Correct category. "Dates" matches "when are applications open." |
| 3 | Where can I check my tuition fee? | Fees | How do I ask about paying tuition fees? | 0.6446 | ✅ Yes | Correct category. Second result about fee structure also relevant. |
| 4 | Is there any scholarship information? | Fees / Scholarships | Are scholarships available for students? | 0.5558 | ✅ Yes | Correct match despite lower score. Scholarship is a niche topic. |
| 5 | Where can I find the syllabus? | Academics | Where can I find the syllabus for my course? | 0.7942 | ✅ Yes | Near-exact wording match. Strong retrieval. |
| 6 | How do I get the examination timetable? | Examinations | Where can I check the examination timetable? | 0.8058 | ✅ Yes | High confidence. All top-3 from Examinations category. |
| 7 | Where can I see my results? | Examinations | Where can I find examination results? | 0.6297 | ✅ Yes | Correct. Score is moderate because query is vague ("results" is ambiguous). |
| 8 | What are the library opening hours? | Library | How can I find library opening hours? | 0.7574 | ✅ Yes | Strong match. Second result about "faculty office hours" is a partial semantic overlap. |
| 9 | How can I contact the placement cell? | Placements | How do I contact the placement office? | 0.7222 | ✅ Yes | Correct. "Cell" and "office" recognised as synonyms by the model. |
| 10 | How do I request a bonafide certificate? | Student Support | How can I request a bonafide certificate? | 0.8117 | ✅ Yes | Near-exact match. Highest score among all queries. |

## Top-3 Retrieval Details

### Query 1: "What documents do I need for admission?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.8240 | Admissions | What documents might be needed when applying for admission? |
| 2 | 0.3979 | Admissions | How can I check my application status? |
| 3 | 0.3736 | Admissions | How do I ask about eligibility for a course? |

### Query 2: "When are admission applications open?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.6517 | Admissions | Where can I find the latest admission dates? |
| 2 | 0.4935 | Admissions | How can I check my application status? |
| 3 | 0.4731 | Library | How can I find library opening hours? |

### Query 3: "Where can I check my tuition fee?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.6446 | Fees | How do I ask about paying tuition fees? |
| 2 | 0.5830 | Fees | Where can I find the course fee details? |
| 3 | 0.4790 | Fees | Are scholarships available for students? |

### Query 4: "Is there any scholarship information?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.5558 | Fees | Are scholarships available for students? |
| 2 | 0.3659 | Fees | Where can I find the course fee details? |
| 3 | 0.3495 | Admissions | Where can I find the latest admission dates? |

### Query 5: "Where can I find the syllabus?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.7942 | Academics | Where can I find the syllabus for my course? |
| 2 | 0.4503 | Examinations | Where can I check the examination timetable? |
| 3 | 0.4174 | Academics | How do I find the academic calendar? |

### Query 6: "How do I get the examination timetable?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.8058 | Examinations | Where can I check the examination timetable? |
| 2 | 0.6344 | Examinations | Where can I find examination results? |
| 3 | 0.5363 | Examinations | How do I ask about examination registration? |

### Query 7: "Where can I see my results?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.6297 | Examinations | Where can I find examination results? |
| 2 | 0.3466 | Examinations | Where can I check the examination timetable? |
| 3 | 0.3260 | Admissions | How can I check my application status? |

### Query 8: "What are the library opening hours?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.7574 | Library | How can I find library opening hours? |
| 2 | 0.3667 | Departments | Where can I find faculty office hours? |
| 3 | 0.3542 | Library | How do I borrow a book from the library? |

### Query 9: "How can I contact the placement cell?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.7222 | Placements | How do I contact the placement office? |
| 2 | 0.4397 | Placements | Where can I find internship announcements? |
| 3 | 0.3576 | Placements | How can I prepare for campus placement activities? |

### Query 10: "How do I request a bonafide certificate?"
| Rank | Score | Category | Retrieved Question |
|------|-------|----------|-------------------|
| 1 | 0.8117 | Student Support | How can I request a bonafide certificate? |
| 2 | 0.3933 | Admissions | How can I check my application status? |
| 3 | 0.3492 | Examinations | How do I ask about examination registration? |

## Summary Statistics

| Metric | Value |
|---|---|
| Total test queries | 10 |
| Top-1 correct category | 10 / 10 (100%) |
| Top-1 relevance (Yes) | 10 / 10 |
| Mean top-1 score | 0.727 |
| Min top-1 score | 0.5558 (scholarship query) |
| Max top-1 score | 0.8240 (admission documents) |

## Observations

1. **Perfect top-1 accuracy on these 10 queries.** Every query retrieved the intended FAQ as the top result. This is encouraging but reflects the small, well-separated FAQ set rather than guaranteed real-world performance.

2. **Score range is informative.** Queries with near-exact wording (bonafide certificate, exam timetable) scored > 0.80, while vague or indirect queries (scholarships, "my results") scored 0.55–0.63. The score difference could help a future system flag low-confidence results.

3. **Cross-category leakage is present but minor.** Query 2 ("admission applications open") included "library opening hours" as the 3rd result because both share the word pattern "find … hours/dates." Query 8 about library hours surfaced "faculty office hours" at rank 2. These are expected side effects of semantic similarity on a small dataset.

4. **The model recognises synonyms.** "Placement cell" matched "placement office" (query 9); "tuition fee" matched "course fee details" (query 3). This is a strength of sentence embeddings over keyword search.

5. **Limitations.** These 10 queries were designed to match the FAQ categories, so 100% accuracy is not a realistic benchmark. Adversarial, ambiguous, or off-topic queries (e.g. "What is the Wi-Fi password?") were not tested and would likely return low-relevance results.

## Automated Test Results

```
17 passed, 2 warnings in 57.41s
```

All 17 automated tests passed. The 2 warnings are harmless HuggingFace Hub symlink notices on Windows.

## Recommendations for Future Work

- Test with at least 50 diverse, naturally-phrased queries including off-topic questions.
- Add a relevance threshold below which the system warns "no confident match found."
- Expand the FAQ dataset significantly with verified, institution-specific content.
- Evaluate retrieval precision@3 and recall when the dataset grows.
