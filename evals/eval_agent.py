import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))
from agent import run_agent  # reuse the real agent code, not a copy


def main():
    cases = json.load(open("evals/agent_testset.json", encoding="utf-8"))
    passed = 0

    for c in cases:
        print(f"\n--- {c['question']} ---")
        answer = run_agent(c["question"])
        answer_lower = answer.lower()
        matched = any(kw.lower() in answer_lower for kw in c["expect_keywords"])

        print(f"[{c['type']}] {'PASS' if matched else 'FAIL'}")
        print(f"answer: {answer[:200]}")

        passed += matched

    print(f"\nOverall: {passed}/{len(cases)} = {passed/len(cases):.0%}")


if __name__ == "__main__":
    main()