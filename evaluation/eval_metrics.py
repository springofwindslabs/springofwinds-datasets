# -*- coding: utf-8 -*-
"""Evaluation metrics for springofwindslabs trial datasets.

Usage:
    python eval_metrics.py path/to/data.jsonl

Auto-detects the schema (conversation-based vs reasoning_steps-based)
and reports the applicable metrics. No third-party dependencies.
"""
import json
import re
import sys

ROLES = {"user", "assistant", "tool", "system", "human", "gpt", "function_call", "observation"}


def eval_conversations(rows):
    n = len(rows)
    schema_ok = tools_ok = turns_ok = 0
    has_tools = False
    for r in rows:
        conv = r.get("conversations") or r.get("messages") or []
        if r.get("id") and conv:
            schema_ok += 1
        if r.get("tools") is not None:
            has_tools = True
            try:
                tl = r["tools"]
                tl = json.loads(tl) if isinstance(tl, str) else tl
                def named(x):
                    return isinstance(x, dict) and (
                        "name" in x
                        or ("function" in x and isinstance(x["function"], dict) and "name" in x["function"])
                    )
                if isinstance(tl, list) and tl and all(named(x) for x in tl):
                    tools_ok += 1
            except Exception:
                pass
        rs = [(t.get("from") or t.get("role") or "").lower() for t in conv]
        vals = [str(t.get("value") or t.get("content") or "").strip() for t in conv]
        if (
            rs
            and rs[0] in ("user", "human", "system")
            and any(x in ("assistant", "gpt") for x in rs)
            and all(x in ROLES for x in rs)
            and all(vals)
        ):
            turns_ok += 1
    print(f"rows: {n}")
    print(f"json_schema_pass_rate:   {schema_ok}/{n} ({100 * schema_ok / n:.1f}%)")
    if has_tools:
        print(f"tool_call_valid_rate:    {tools_ok}/{n} ({100 * tools_ok / n:.1f}%)")
    print(f"turn_consistency_rate:   {turns_ok}/{n} ({100 * turns_ok / n:.1f}%)")


def eval_cot(rows):
    n = len(rows)
    schema_ok = steps_ok = 0
    for r in rows:
        if all(r.get(k) for k in ("id", "regulation", "case", "reasoning_steps", "conclusion")):
            schema_ok += 1
        steps = r.get("reasoning_steps") or []
        if (
            isinstance(steps, list)
            and len(steps) >= 2
            and all(isinstance(s, str) and s.strip() for s in steps)
            and str(r.get("conclusion") or "").strip()
        ):
            steps_ok += 1
    print(f"rows: {n}")
    print(f"json_schema_pass_rate:       {schema_ok}/{n} ({100 * schema_ok / n:.1f}%)")
    print(f"reasoning_step_consistency:  {steps_ok}/{n} ({100 * steps_ok / n:.1f}%)")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    rows = []
    parse_fail = 0
    with open(sys.argv[1], encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                parse_fail += 1
    if parse_fail:
        print(f"WARNING: {parse_fail} line(s) failed strict JSONL parse")
    if not rows:
        print("no rows parsed")
        sys.exit(2)
    if "reasoning_steps" in rows[0]:
        eval_cot(rows)
    else:
        eval_conversations(rows)


if __name__ == "__main__":
    main()
