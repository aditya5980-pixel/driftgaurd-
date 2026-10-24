from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from load_dataset import load_golden

THRESHOLD = 0.45   # minimum similarity to the expected answer
DROP = 0.10        # largest allowed fall compared with v1
REAL_REGRESSIONS = {2, 3, 4, 5, 8, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20}


def compare(expected_texts, new_texts):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(expected_texts + new_texts)
    a = vectorizer.transform(expected_texts)
    b = vectorizer.transform(new_texts)
    return [cosine_similarity(a[i], b[i])[0][0] for i in range(len(expected_texts))]


def verdict(old_score, new_score):
    if new_score < THRESHOLD or (old_score - new_score) > DROP:
        return "FAIL"
    return "PASS"


def metrics(ids, verdicts):
    tp = sum(1 for i, v in zip(ids, verdicts) if v == "FAIL" and i in REAL_REGRESSIONS)
    fp = sum(1 for i, v in zip(ids, verdicts) if v == "FAIL" and i not in REAL_REGRESSIONS)
    fn = sum(1 for i, v in zip(ids, verdicts) if v == "PASS" and i in REAL_REGRESSIONS)
    tn = len(ids) - tp - fp - fn
    accuracy = (tp + tn) / len(ids) * 100
    precision = tp / (tp + fp) * 100 if (tp + fp) else 0
    recall = tp / (tp + fn) * 100 if (tp + fn) else 0
    return tp, fp, fn, tn, accuracy, precision, recall


def write_report(golden, s1, s2, verdicts, filename="report.txt"):
    passed = verdicts.count("PASS")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("DriftGuard Regression Report\n")
        f.write("=" * 30 + "\n")
        f.write(f"Rule: FAIL if score < {THRESHOLD} or drop vs v1 > {DROP}\n\n")
        for i in range(len(golden)):
            f.write(f"{golden[i]['id']} | {golden[i]['input']} | v1 {s1[i]:.2f} | v2 {s2[i]:.2f} | {verdicts[i]}\n")
        f.write(f"\nPass rate: {passed / len(verdicts) * 100:.1f}%\n")


if __name__ == "__main__":
    golden = load_golden("golden_dataset.json")
    v1 = load_golden("outputs_v1.json")
    v2 = load_golden("outputs_v2.json")

    ids = [g["id"] for g in golden]
    assert ids == [o["id"] for o in v1] == [o["id"] for o in v2], "ids out of order"

    expected = [g["expected"] for g in golden]
    s1 = compare(expected, [o["output"] for o in v1])
    s2 = compare(expected, [o["output"] for o in v2])
    verdicts = [verdict(s1[i], s2[i]) for i in range(len(golden))]

    print("id   v1     v2     verdict")
    for i in range(len(golden)):
        print(f"{ids[i]:<4} {s1[i]:.2f}   {s2[i]:.2f}   {verdicts[i]}")

    tp, fp, fn, tn, acc, prec, rec = metrics(ids, verdicts)
    print(f"Pass rate: {verdicts.count('PASS') / len(verdicts) * 100:.1f}%")
    print(f"Caught {tp}, missed {fn}, false alarms {fp}, correct passes {tn}")
    print(f"Accuracy {acc:.1f}%  Precision {prec:.1f}%  Recall {rec:.1f}%")

    write_report(golden, s1, s2, verdicts)