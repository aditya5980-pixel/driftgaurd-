# DriftGuard — Design Document

## 1. Problem Statement

LLM-based applications rely heavily on prompt engineering. Every time a prompt is edited — to fix a bug, add a feature, or improve tone — there's a risk of **silent regression**: the new prompt breaks behavior that used to work, without throwing any error. Because LLM outputs are unstructured text, these regressions aren't caught by normal software testing (unit tests, type checks, etc.). They're usually caught by users, after deployment.

**Goal:** Build a lightweight tool that automatically flags these regressions *before* a prompt change goes live, by comparing outputs against a known baseline.

## 2. The Golden Dataset

A **golden dataset** is a fixed, curated set of (input, expected/reference output) pairs representative of real use cases.

**Why it must stay fixed:**
If the test data changes between the "before" and "after" runs, any difference observed in output quality could be caused by either (a) the prompt change, or (b) the data change — and we'd have no way to isolate which one caused it. Freezing the dataset removes that confound, isolating the prompt as the only variable.

**Example golden dataset entry (email classification use case):**
```json
{
  "id": "email_001",
  "input": "Subject: Urgent - verify your account now or it will be suspended...",
  "expected_label": "phishing",
  "notes": "Classic urgency + account-suspension phishing pattern"
}
```

## 3. System Architecture

```
                    ┌─────────────────┐
                    │  Golden Dataset  │  (fixed inputs + expected outputs)
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌─────────────────┐          ┌──────────────────┐
     │  AI Feature      │          │  AI Feature       │
     │  (OLD prompt)    │          │  (NEW prompt)      │
     └────────┬─────────┘          └─────────┬─────────┘
              │                              │
              ▼                              ▼
        Old Outputs                    New Outputs
              │                              │
              └──────────────┬───────────────┘
                              ▼
                     ┌─────────────────┐
                     │   Comparator      │  (cosine similarity, etc.)
                     └────────┬──────────┘
                              ▼
                     ┌─────────────────┐
                     │ Report Generator  │  (pass/fail per test case)
                     └─────────────────┘
```

## 4. Component Breakdown

| Component | Responsibility | Scoped-down version (student build) |
|---|---|---|
| AI Feature | The actual LLM call being tested | Simple wrapper function calling one LLM API endpoint |
| Golden Dataset | Fixed test cases | JSON/CSV file, manually curated, 10–20 entries |
| Test Runner | Runs dataset through AI feature twice (old/new prompt) | Python script looping through dataset, storing outputs |
| Comparator | Measures output similarity | Cosine similarity on sentence embeddings |
| Report Generator | Human-readable pass/fail summary | Console output or simple CSV/HTML report |

**Full production version would add** (deferred to stretch goals): async request handling, Pydantic schema validation, Docker containerization, GitHub Actions CI integration for automated runs on every prompt commit.

## 5. Why Cosine Similarity

Cosine similarity measures how close two output texts are in "meaning space" (via embeddings), rather than requiring exact text match. This matters because LLM outputs are rarely word-for-word identical even when they're semantically equivalent — so exact string matching would produce false positives on regressions.

A threshold (e.g., similarity < 0.85) flags a potential regression for human review.

## 6. Open Questions / Risks

- What similarity threshold meaningfully separates "acceptable variation" from "real regression"? (Needs experimentation once Phase 2 begins.)
- How large does the golden dataset need to be to catch edge cases without becoming unwieldy to maintain by hand?
- Which embedding model to use for comparison — tradeoff between simplicity and accuracy.
