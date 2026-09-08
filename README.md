# DriftGuard 🛡️

**Automated Regression Detection System for LLM-Based Applications**

## The Problem

LLM-based applications are fragile in a quiet way. A developer tweaks a prompt to fix one issue — and unknowingly breaks five other things the model used to handle correctly. Unlike traditional software, there's no compiler error, no failed test suite alert. The output still *looks* like a normal response. It just quietly got worse.

This is a **silent regression** — and right now, most teams catch it by accident, in production, from a user complaint.

**Example:** An email classifier prompt gets updated to better detect spam. Before the change, it correctly flagged phishing emails 95% of the time. After the "improvement," phishing detection drops to 80% — but nobody notices because the team only tested the specific case they were trying to fix.

## The Solution

DriftGuard automatically compares an LLM application's outputs **before and after a prompt change**, using a fixed set of test cases (the "golden dataset"), and generates a pass/fail report — so regressions get caught before deployment, not after.

## Core Concept: The Golden Dataset

The golden dataset is a **fixed** set of input/expected-output pairs that never changes between test runs. This is critical: if the dataset changed along with the prompt, you couldn't tell whether output differences were caused by the prompt change or the data change. Keeping it constant means **any measured difference in output quality can be attributed solely to the prompt change.**

## How It Works (Planned Architecture)

1. **AI Feature** — the LLM-based feature/prompt being tested
2. **Golden Dataset** — fixed inputs + expected/reference outputs
3. **Test Runner** — runs the golden dataset through the AI feature (old prompt vs. new prompt)
4. **Comparator** — measures similarity between old and new outputs (e.g., cosine similarity)
5. **Report Generator** — produces a pass/fail summary highlighting regressions

## Project Roadmap

- [x] Phase 0: Project selection & scoping
- [ ] **Phase 1 (Weeks 1–4):** Python fundamentals + math foundations (linear algebra, statistics)
- [ ] **Phase 2 (Weeks 5–8):** ML fundamentals (scikit-learn), API basics — begin build (Piece 1)
- [ ] **Phase 3 (Weeks 9–10):** Neural network concepts
- [ ] **Phase 4 (Weeks 11–15):** Build core pieces — golden dataset, test runner, comparator, report generator
- [ ] **Week 16:** Buffer / stretch goals (e.g., GitHub Actions CI integration)

## Tech Stack (Planned)

- **Language:** Python
- **ML/Comparison:** scikit-learn, cosine similarity for output comparison
- **LLM Access:** LLM provider API (TBD)
- **Testing:** Custom test runner (scoped-down version of production-grade tools like async pipelines, Pydantic validation, Docker, GitHub Actions)

## Status

🚧 In active development — currently in Phase 1 (fundamentals). See `PROGRESS.md` for a running log.

## Author

Aditya — B.Tech Computer Science
