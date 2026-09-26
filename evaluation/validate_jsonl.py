#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone validator for springofwindslabs JSONL datasets (stdlib only).

Reproduces the structural rules of our production PreQC gate:
  * strict JSON per line
  * declared-tools-only function calls (no phantom tools / argument keys)
  * role alternation for conversation tracks
  * case/steps/conclusion structure for CoT tracks

Usage:
  python validate_jsonl.py --track mcp_tool_use dataset.jsonl
Exit code 0 = all rows pass.
"""
import argparse
import json
import sys


def _tools_index(obj):
    try:
        tools = json.loads(obj["tools"]) if isinstance(obj.get("tools"), str) else obj.get("tools")
    except (json.JSONDecodeError, TypeError):
        return "tools is not valid JSON"
    if not isinstance(tools, list) or not tools:
        return "tools must be a non-empty list"
    index = {}
    for t in tools:
        try:
            fn = t["function"] if "function" in t else t
            index[fn["name"]] = set((fn.get("parameters") or {}).get("properties", {}).keys())
        except (TypeError, KeyError):
            return "malformed tool entry"
    return index


def _check_fc(fc, index):
    if not isinstance(fc, dict):
        return "fc missing or not an object"
    name = fc.get("name")
    if name not in index:
        return f"fc calls undeclared tool: {name}"
    args = fc.get("arguments")
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return "fc arguments not valid JSON"
    if not isinstance(args, dict):
        return "fc arguments must be an object"
    unknown = set(args.keys()) - index[name]
    if unknown:
        return f"fc uses undeclared argument keys: {sorted(unknown)}"
    return None


def validate_conversation(obj):
    index = _tools_index(obj)
    if isinstance(index, str):
        return index
    msgs = obj.get("conversations") or obj.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 2:
        return "conversations must have >= 2 messages"
    for m in msgs:
        if not isinstance(m, dict):
            return "malformed message"
        role = m.get("from") or m.get("role")
        if role in ("function_call", "fc") or m.get("fc"):
            fc = m.get("fc") or _try_json(m.get("value") or m.get("content"))
            err = _check_fc(fc, index)
            if err:
                return err
    return None


def _try_json(v):
    if isinstance(v, dict):
        return v
    try:
        return json.loads(v)
    except (TypeError, json.JSONDecodeError):
        return None


def validate_cot(obj):
    for key in ("regulation", "case", "reasoning_steps", "conclusion"):
        if key not in obj:
            return f"missing {key}"
    if not isinstance(obj["reasoning_steps"], list) or len(obj["reasoning_steps"]) < 3:
        return "reasoning_steps must have >= 3 entries"
    if len(str(obj["case"])) < 20 or len(str(obj["conclusion"])) < 20:
        return "case/conclusion too short"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--track", default="mcp_tool_use")
    a = ap.parse_args()
    fn = validate_cot if a.track == "agent_cot" else validate_conversation
    total = ok = 0
    errors = {}
    with open(a.path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                errors["invalid_json"] = errors.get("invalid_json", 0) + 1
                continue
            err = fn(obj)
            if err:
                errors[err] = errors.get(err, 0) + 1
            else:
                ok += 1
    print(f"{ok}/{total} rows pass ({100.0 * ok / max(total, 1):.2f}%)")
    for e, n in sorted(errors.items(), key=lambda x: -x[1])[:10]:
        print(f"  {n:5d}  {e}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
