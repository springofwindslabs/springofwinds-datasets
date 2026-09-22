# -*- coding: utf-8 -*-
"""Unsloth loading check for springofwindslabs conversation datasets.

Usage:
    python unsloth_load.py path/to/data.jsonl

Converts every row to the tokenizer's chat template and reports
formatting errors (expected: zero). Requires: unsloth, datasets.
"""
import json
import sys

from unsloth import FastLanguageModel

MODEL = "unsloth/Qwen2.5-0.5B-Instruct"  # small on purpose (loading check)

ROLE_MAP = {"human": "user", "gpt": "assistant", "observation": "tool"}


def main():
    path = sys.argv[1]
    _, tokenizer = FastLanguageModel.from_pretrained(MODEL, max_seq_length=4096, load_in_4bit=True)

    ok, fail = 0, 0
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            try:
                row = json.loads(line)
                conv = row.get("conversations") or row.get("messages")
                messages = [
                    {
                        "role": ROLE_MAP.get((t.get("from") or t.get("role")), (t.get("from") or t.get("role"))),
                        "content": t.get("value") or t.get("content"),
                    }
                    for t in conv
                ]
                tokenizer.apply_chat_template(messages, tokenize=True)
                ok += 1
            except Exception as e:
                fail += 1
                print(f"row {i}: {type(e).__name__}: {e}")
    print(f"formatted OK: {ok}, failed: {fail}")


if __name__ == "__main__":
    main()
