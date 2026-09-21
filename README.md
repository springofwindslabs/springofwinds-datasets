# Enterprise Synthetic Datasets (Strict JSONL)

[![15-second demo: strict JSONL trajectories, 7-point rubric validation](assets/demo_preview.gif)](assets/demo_15s.mp4)

*15s demo — strict JSONL structure, 7-point rubric validation (click for MP4).*

Structured synthetic datasets for enterprise LLM alignment.
All datasets follow deterministic schema and multi-turn consistency.

## Datasets
| Dataset | Schema | Samples | Trial (HF) | Full (Gumroad) |
|---|---|---|---|---|
| [mcp-agent-trajectory](mcp-agent-trajectory/) | [schema](mcp-agent-trajectory/schema.json) | [samples](mcp-agent-trajectory/samples/) | [HF](https://huggingface.co/datasets/springofwindslabs/mcp-agent-trajectory-benchmark) | [Gumroad](https://springofwindslabs.gumroad.com/l/mcp-agent-trajectory) |
| [function-calling-en](function-calling-en/) | [schema](function-calling-en/schema.json) | [samples](function-calling-en/samples/) | [HF](https://huggingface.co/datasets/springofwindslabs/function-calling-en-trial) | [Gumroad](https://springofwindslabs.gumroad.com/l/function-calling-en) |
| [function-calling-ja](function-calling-ja/) | [schema](function-calling-ja/schema.json) | [samples](function-calling-ja/samples/) | [HF](https://huggingface.co/datasets/springofwindslabs/function-calling-ja-trial) | [Gumroad](https://springofwindslabs.gumroad.com/l/function-calling-ja) |
| [regulatory-compliance-cot](regulatory-compliance-cot/) | [schema](regulatory-compliance-cot/schema.json) | [samples](regulatory-compliance-cot/samples/) | [HF](https://huggingface.co/datasets/springofwindslabs/regulatory-compliance-cot-trial) | [Gumroad](https://springofwindslabs.gumroad.com/l/regulatory-compliance-cot) |

## Structure
- Strict JSONL
- Deterministic schema
- Error recovery included
- Token-efficient formatting

## Samples
Each dataset directory includes a `samples/` folder with 5-row previews.

## Trial Versions
Available on Hugging Face:
https://huggingface.co/springofwindslabs

## Full Versions
Available on Gumroad:
https://springofwindslabs.gumroad.com

## Get Started: Trial → Full

| Step | What you get | Link |
|---|---|---|
| 1. **Validate free** | 50-row trial per dataset (Apache-2.0, no gating) | [Hugging Face](https://huggingface.co/springofwindslabs) |
| 2. **Inspect schema** | `schema.json` + 5-row samples in this repo | [Datasets table above](#datasets) |
| 3. **Go production** | 1,000+ row volumes, perpetual commercial license, instant delivery | [Gumroad](https://springofwindslabs.gumroad.com?utm_source=github&utm_medium=readme_funnel&utm_campaign=springofwinds-datasets) |

Questions before purchase? → springofwinds@gmail.com

## License
Apache-2.0
