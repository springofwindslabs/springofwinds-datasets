# Validation Evidence (measured, reproducible)

_Last measured: 2026-09-27 — every number below is produced by running `validate_jsonl.py` against the shipped `dataset.jsonl` files. No sampling: 100% of rows are validated._

## Schema validation pass rate

| Edition | Track | Rows | Pass | Pass rate | Invalid JSON |
|---|---|---:|---:|---:|---:|
| 1K Edition (Lot1) | `agent_cot` | 2190 | 2190 | 100.00% | 0 |
| 1K Edition (Lot1) | `function_calling` | 1521 | 1521 | 100.00% | 0 |
| 1K Edition (Lot1) | `function_calling_ja` | 1808 | 1808 | 100.00% | 0 |
| 1K Edition (Lot1) | `mcp_tool_use` | 1003 | 1003 | 100.00% | 0 |
| 2K Edition (Lot1) | `agent_cot` | 2300 | 2300 | 100.00% | 0 |
| 2K Edition (Lot1) | `function_calling` | 2300 | 2300 | 100.00% | 0 |
| 2K Edition (Lot1) | `function_calling_ja` | 2300 | 2300 | 100.00% | 0 |
| 2K Edition (Lot1) | `mcp_tool_use` | 2300 | 2300 | 100.00% | 0 |
| 1K Edition (Lot2) | `agent_cot` | 1000 | 1000 | 100.00% | 0 |
| 1K Edition (Lot2) | `function_calling` | 1000 | 1000 | 100.00% | 0 |
| 1K Edition (Lot2) | `function_calling_ja` | 1000 | 1000 | 100.00% | 0 |
| 1K Edition (Lot2) | `mcp_tool_use` | 1000 | 1000 | 100.00% | 0 |
| 2K Edition (Lot2) | `agent_cot` | 2300 | 2300 | 100.00% | 0 |
| 2K Edition (Lot2) | `function_calling` | 2300 | 2300 | 100.00% | 0 |
| 2K Edition (Lot2) | `function_calling_ja` | 2300 | 2300 | 100.00% | 0 |
| 2K Edition (Lot2) | `mcp_tool_use` | 2300 | 2300 | 100.00% | 0 |
| **Total** | | **28922** | **28922** | **100.00%** | |

## What the validator enforces (deterministic, not LLM-judged)

- **mcp_tool_use / function_calling(_ja)**: every `fc` step may only call declared tools with declared argument keys — undeclared tool names or phantom arguments fail the row. Strict message-role alternation.
- **agent_cot**: case/steps/conclusion structure with minimum-substance thresholds; conclusion must be grounded in the cited provisions.
- Near-duplicate exclusion: 3-gram Jaccard >= 0.85 against all prior rows (including previously shipped lots via blacklists).

## Mutation smoke coverage (validator self-test)

The validators themselves are regression-tested: gold rows must pass, and deliberately corrupted variants (undeclared tools, broken step ordering, contradictory audit records, etc.) must be caught. Current suites: `scripts/smoke_lot3.py`, `scripts/smoke_nextgen.py`, `scripts/smoke_future.py` (23 mutation classes).

## Reproduce it yourself

```bash
python validate_jsonl.py --track mcp_tool_use path/to/dataset.jsonl
```

`validate_jsonl.py` in this folder is dependency-free (stdlib only) and applies the same structural rules as our production PreQC gate.