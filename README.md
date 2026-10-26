# DriftGuard

Automated regression detection for LLM-based applications (scoped-down student version).

DriftGuard checks whether a change to an AI feature, such as a prompt edit, has silently made its answers worse. It compares the feature's new answers against a fixed "golden" dataset and produces a pass/fail report.

## The problem

When a prompt is edited, the AI feature can start giving worse answers without any error message: it may drop key details, hedge ("I can't confirm..."), refuse, or state wrong facts. These silent regressions are easy to miss by hand, especially across many questions. DriftGuard automates the check.

## How it works

DriftGuard has five components.

| Component | What it does | Where it lives |
|---|---|---|
| AI feature | Produces answers before (v1) and after (v2) a prompt change | `outputs_v1.json`, `outputs_v2.json` |
| Golden dataset | Fixed questions with expected answers; never changes between runs | `golden_dataset.json` |
| Test runner | Loads the files and pairs answers by question id | `load_dataset.py`, main block of `comparator.py` |
| Comparator | Turns texts into TF-IDF vectors and measures cosine similarity to the expected answer | `compare()` in `comparator.py` |
| Report generator | Applies the verdict rules and writes the results | `write_report()` in `comparator.py`, output `report.txt` |

An architecture diagram is in `DESIGN.md`.

### Verdict rules

A v2 answer is marked **FAIL** if either rule triggers:

1. Its similarity to the expected answer is below **0.45**, or
2. Its similarity dropped by more than **0.10** compared with v1.

Rule 2 exists because a fixed threshold alone misses answers that reuse the expected wording but change the facts or hedge.

## Results (20 questions)

15 of the 20 v2 answers are deliberate regressions (wrong facts, refusals, or hedging); 5 are correct rewordings.

| Metric | Result |
|---|---|
| Regressions caught | 15 of 15 |
| False alarms | 0 |
| Accuracy / precision / recall | 100% / 100% / 100% |
| Pass rate of v2 | 25% |

With the threshold rule alone, two regressions (ids 2 and 19) were missed, so recall was 86.7%. Adding the drop-versus-v1 rule fixed both.

Caveat: the two numbers (0.45 and 0.10) were chosen by looking at this same 20-question set, and the data is small and written by hand. The result shows the method works, not that it would score 100% on new data.

## Run it

Requires Python 3 on Windows (commands for PowerShell).

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe comparator.py
```

This prints a table of similarity scores and verdicts, prints the metrics, and writes `report.txt`.

## Project files

| File | Purpose |
|---|---|
| `comparator.py` | Comparator, verdict rules, metrics, report generator |
| `load_dataset.py` | Loads the JSON files |
| `golden_dataset.json` | Questions and expected answers |
| `outputs_v1.json` | Baseline answers (correct) |
| `outputs_v2.json` | Answers after a simulated prompt change |
| `report.txt` | Latest generated report |
| `DESIGN.md` | Design notes and architecture |
| `PROGRESS.md` | Day-by-day progress log |

## Limitations

- Cosine similarity over TF-IDF measures shared wording, not meaning. An answer with the right words but wrong facts can still score high (library timings, id 2).
- Correct answers phrased with different vocabulary can score low (for example, "declaration" versus "declared" count as different words).
- Scores depend on the whole dataset, because TF-IDF learns word weights from all texts, so adding questions shifts every score slightly.
- The "AI feature" outputs are simulated, not generated live by a model.
- Small, synthetic dataset; thresholds tuned on the same data.

## Future work

- Generate v1 and v2 answers live from an LLM API instead of saved files.
- Replace TF-IDF with sentence embeddings to handle synonyms and paraphrase.
- Run DriftGuard automatically on every commit with GitHub Actions.
- Larger dataset with a separate tuning set and test set.

## Author

Aditya Parashar 
(BTCD25O1004)
Computer Science and Design
Dept. of CSD