# load_dataset.py
import json

def load_golden(path="golden_dataset.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

#if __name__ == "__main__":
#    data = load_golden()
#    print(f"Loaded {len(data)} entries")
#    print(data[0]["input"])

if __name__ == "__main__":
    golden = load_golden("golden_dataset.json")
    v1 = load_golden("outputs_v1.json")
    v2 = load_golden("outputs_v2.json")
    print(len(golden), len(v1), len(v2))