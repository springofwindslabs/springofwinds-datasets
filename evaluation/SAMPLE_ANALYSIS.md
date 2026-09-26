# Sample Analysis — why these rows train recovery, not just success

_Annotated excerpts from shipped datasets (2026-09-27). Rows truncated for readability; structure is exactly as shipped._

## `mcp_tool_use` — Multi-turn MCP agent trajectories with error recovery (429/403/locks)

```json
{
  "id": "healthcare_admin_sales_query_001",
  "tools": "[{\"name\": \"execute_sql_query\", \"description\": \"Execute a read-only SQL query against the healthcare database.\", \"inputSchema\": {\"type\": \"object\", \"properties\": {\"query\": {\"type\": \"string\"}}, \"required\": [\"query\"]}}, {\"name\": \"describe_table\", \"description\": \"Get schema information for a specific table.\", \"inputSchema\": {\"type\": \"object\", \"properties\": {\"table_name\": {\"type\": \"string\"}}, \"required\": [\"table_name\"]}}]",
  "conversations": [
    {
      "from": "user",
      "value": "I'm looking at the clinic's monthly report. Can you find the total revenue from 'premium_service' and tell me how many patients were billed for it last month?"
    },
    {
      "from": "assistant",
      "value": "{\"name\": \"execute_sql_query\", \"arguments\": {\"query\": \"SELECT SUM(amount) as total_revenue, COUNT(patient_id) as patient_count FROM billing_records WHERE service_type = 'premium_service' AND billing_date >= '2023-10-01' AND billing_date <= '2023-10-31'\"}}"
    },
    {
      "from": "tool",
      "value": "{\"error\": {\"code\": \"SQLSTATE_ERROR\", \"message\": \"Column 'service_type' does not exist in table 'billing_records'\"}}"
    },
    {
      "from": "assistant",
      "value": "{\"name\": \"describe_table\", \"arguments\": {\"table_name\": \"billing_records\"}}"
    },
    {
      "from": "tool",
      "value": "{\"columns\": [\"id\", \"patient_id\", \"service_code\", \"amount\", \"billing_date\", \"status\"]}"
    },
    {
      "from": "assistant",
      "value": "{\"name\": \"execute_sql_query\", \"arguments\": {\"query\": \"SELECT SUM(amount) as total_revenue, COUNT(patient_id) as patient_count FROM billing_records WHERE service_code = 'PRM_01' AND billing_date >= '2023-10-01' AND billing_date <= '2023-10-31'\"}}"
    },
    {
      "from": "tool",
      "value": "{\"results\": [{\"total_revenue\": 12500.50, \"patient_count\": 42}]}"
    },
    {
      "from": "assistant",
      "value": "Based on the billing records for October, the total revenue from 'PRM_01' (the code corresponding to premium services) was $12,500.50 across 42 patients."
   
  ... (truncated)
```

**What to look at:** the trajectory includes a *failed* tool call and the agent's recovery — updated assumption, then a corrected next action. Public tool-use sets mostly show success paths; recovery is the part real agents need.

## `function_calling` — Schema-validated function calling (EN)

```json
{
  "id": "airtable_batch_create_conflict_resolution_001",
  "tools": "[{\"type\": \"function\", \"function\": {\"name\": \"create_records\", \"description\": \"Create multiple records in a specific Airtable table.\", \"parameters\": {\"type\": \"object\", \"properties\": {\"base_id\": {\"type\": \"string\"}, \"table_name\": {\"type\": \"string\"}, \"records\": {\"type\": \"array\", \"items\": {\"type\": \"object\", \"properties\": {\"fields\": {\"type\": \"object\", \"additionalProperties\": {\"type\": \"string\"}}}}} }}, \"required\": [\"base_id\", \"table_name\", \"records\"]}}, {\"type\": \"function\", \"function\": {\"name\": \"get_table_schema\", \"description\": \"Retrieve the schema and field options for a specific table.\", \"parameters\": {\"type\": \"object\", \"properties\": {\"base_id\": {\"type\": \"string\"}, \"table_name\": {\"type\": \"string\"}}, \"required\": [\"base_id\", \"table_name\"]}}} ]",
  "conversations": [
    {
      "from": "user",
      "value": "I need to upload the new podcast episodes to the 'Content_Pipeline' table in our media base. There are two: 'The AI Revolution' and 'Future of Robotics'. Set the 'Category' to 'Tech_Talk' for both."
    },
    {
      "from": "assistant",
      "value": "{\"name\": \"create_records\", \"arguments\": {\"base_id\": \"app123456789\", \"table_name\": \"Content_Pipeline\", \"records\": [{\"fields\": {\"Title\": \"The AI Revolution\", \"Category\": \"Tech_Talk\"}}, {\"fields\": {\"Title\": \"Future of Robotics\", \"Category\": \"Tech_Talk\"}}]} }"
    },
    {
      "from": "tool",
      "value": "{\"error\": {\"type\": \"conflict\", \"message\": \"409 Conflict: The value 'Tech_Talk' is not a valid option for the multi-select field 'Category'. Available options are: 'Tech', 'Science', 'Education'.\"}}"
    },
    {
      "from": "assistant",
      "value": "{\"name\": \"get_table_schema\", \"arguments\": {\"base_id\": \"app123456789\", \"table_name\": \"Content_Pipeline\"}}"
    },
    {
      "from": "tool",
      "value": "{\"schema\": {\"fields\": {\"Title\": {\"type\": \"single_line_text\"}, \"Category\": {\"type\": \"multiple_select\", \"options\": [\"Tech\", \"Science\", \"Education\"]}, 
  ... (truncated)
```

**What to look at:** every argument key in the call exists in the declared tool schema. Our validator rejects phantom tools/arguments deterministically, so fine-tuning never sees a malformed call.

## `function_calling_ja` — Schema-validated function calling (JA, keigo/implicit requests)

```json
{
  "id": "f785e32c-9c8b-4e2d-9b8c-f4159837d884",
  "tools": "[{\"name\": \"stripe\", \"description\": \"Stripe API access\"}]",
  "conversations": [
    {
      "from": "user",
      "value": "先月決済に失敗した顧客の一覧を取得して返金処理を実行してください。"
    },
    {
      "from": "assistant",
      "value": "{\"name\": \"stripe\", \"arguments\": {\"method\": \"charges.list\", \"params\": {\"status\": \"failed\", \"created\": {\"$gt\": \"2023-09-01T00:00:00Z\", \"$lt\": \"2023-10-01T00:00:00Z\"}}}}"
    }
  ]
}
```

**What to look at:** the user request is indirect Japanese (keigo / omitted subjects). The row teaches mapping implicit intent to an exact, schema-valid tool call — rare in public Japanese data.

## `agent_cot` — Regulatory compliance chain-of-thought (EU AI Act / GDPR)

```json
{
  "id": "eu_ai_act_emotion_rec_hiring_1",
  "regulation": "EU AI Act",
  "case": "A European startup develops an emotion-recognition system to analyze candidates' facial expressions during job interviews. They claim it helps them identify the most suitable candidates based on their emotional responses.",
  "reasoning_steps": [
    "Identify the AI system's purpose: Hiring candidate selection based on emotional cues.",
    "Classify the system's risk level according to the EU AI Act: High risk due to potential for discrimination and impact on fundamental rights.",
    "Assess compliance with the requirements for high-risk AI systems: The system must undergo conformity assessment by a qualified body.",
    "Evaluate the data used for training: Ensure the dataset is representative, ethical, and free from bias that could lead to discriminatory outcomes.",
    "Consider the transparency and explainability requirements: The system's decision-making process should be transparent and explainable to candidates.",
    "Determine if alternative, less risky methods exist: Explore options like structured interviews and standardized assessments that minimize reliance on emotion recognition."
  ],
  "conclusion": "The emotion-recognition system for hiring interviews likely falls under high-risk AI and requires a conformity assessment. The startup must ensure ethical data practices, transparency, and consider less risky alternatives to mitigate potential discrimination."
}
```

**What to look at:** each reasoning step cites the applicable provision before the conclusion. The conclusion is structurally required to follow from cited provisions, giving audit-friendly reasoning traces.
