from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from load_dataset import load_golden

THRESHOLD = 0.45


def compare(expected_texts, new_texts):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(expected_texts + new_texts)   # learn the vocabulary
    a = vectorizer.transform(expected_texts)     # texts -> vectors
    b = vectorizer.transform(new_texts)
    return [cosine_similarity(a[i], b[i])[0][0] for i in range(len(expected_texts))]


def verdict(score):
    return "PASS" if score >= THRESHOLD else "FAIL"


def write_report(golden, scores, filename="report.txt"):
    passed = sum(1 for s in scores if s >= THRESHOLD)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("DriftGuard Regression Report\n")
        f.write("=" * 30 + "\n")
        for i in range(len(golden)):
            f.write(f"{golden[i]['id']} | {golden[i]['input']} | {scores[i]:.2f} | {verdict(scores[i])}\n")
        f.write(f"\nPass rate: {passed / len(scores) * 100:.1f}%\n")


if __name__ == "__main__":
    golden = load_golden("golden_dataset.json")
    v1 = load_golden("outputs_v1.json")
    v2 = load_golden("outputs_v2.json")

    expected = [g["expected"] for g in golden]
    v1_text = [o["output"] for o in v1]
    v2_text = [o["output"] for o in v2]

    s1 = compare(expected, v1_text)
    s2 = compare(expected, v2_text)

    print("id   v1     v2     verdict(v2)")
    for i in range(len(golden)):
        print(f"{golden[i]['id']:<4} {s1[i]:.2f}   {s2[i]:.2f}   {verdict(s2[i])}")

    passed = sum(1 for s in s2 if s >= THRESHOLD)
    print(f"Pass rate: {passed / len(s2) * 100:.1f}%")

    write_report(golden, s2)