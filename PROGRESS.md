# DriftGuard Progress Log

Final submission: 2 Nov 2026.
Plan: scoped-down student version with a TF-IDF + cosine similarity comparator.

## Foundations (to Oct 16)
- Completed Python basics and set up the local environment (Windows, Python, VS Code).
- Completed the math videos (linear algebra and statistics fundamentals).
- Designed the system: 5 components (AI Feature, Golden Dataset, Test Runner, Comparator, Report Generator). See DESIGN.md.

## Oct 17
- Created `golden_dataset.json` (10 college-helpdesk question/answer pairs).
- Wrote `load_dataset.py` to load JSON files.
- Created `outputs_v1.json` (correct answers) and `outputs_v2.json` (after a simulated prompt change, with some answers broken).

## Oct 18
- Built the comparator with scikit-learn: TF-IDF vectors plus cosine similarity.
- Chose a pass/fail threshold of 0.45 from the score table.
- Added the report generator, which writes `report.txt`.
- Results on 10 questions: 50% pass rate, accuracy 90%, precision 100%, recall 83.3%.
- Finding: wording-based similarity missed one wrong answer (library timings) that reused the expected words. Correct answers with different vocabulary also scored lower than expected.
- Pushed the working pipeline to GitHub.

## Oct 24
- Replaced the sample data with my own 20-question dataset (v2 answers hedge or refuse instead of answering).
- Added a second rule: FAIL if the score drops by more than 0.10 compared with v1.
- Added automatic metrics. Result: 15 of 15 regressions caught, 0 false alarms (accuracy, precision and recall 100% on this set; thresholds tuned on the same set).
- Findings: the threshold alone missed ids 2 and 19; the drop rule caught them.

## Oct 26
- Tried adding a live LLM mode (Gemini API); hit free-tier quota limits, so it moved to future work. The controlled v1/v2 test remains the evaluation.

## Next
- Grow the golden dataset to 20 entries.
- Add a baseline-drop mode and GitHub Actions.
- Try a real LLM API for the AI feature.
- Screenshots, architecture diagram, written report, poster.

