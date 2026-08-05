---
title: GroundLM 2026 Eval
sdk: gradio
app_file: app.py
python_version: 3.11
hf_oauth: true
hf_oauth_scopes:
  - email
---

# GroundLM 2026 Eval

This Space is a lightweight evaluator for the two GroundLM 2026 challenge tasks:

- `goldenviewvqa`
- `littraceqa-test`
- `littraceqa-test-extra`

## Behavior

- Participants sign in with a Hugging Face account.
- On first use, they register one immutable `team_name` and `email`.
- `hf_username`, `email`, and `team_name` must each be unique.
- Each Hugging Face account can submit at most `MAX_SUBMISSIONS_PER_DAY=5` times per task per day.
- Submissions that fail sanity checks do not count toward the daily limit.
- The leaderboard is filtered per task and displays `team_name`, not email.
- Gold files, uploaded predictions, metadata, and results live in the mounted bucket.

## Space Variables

Mount `hf://buckets/YimuWang/GroundLM-2026-Eval-storage` at `data`, then set:

```text
EVAL_DATASETS=goldenviewvqa,littraceqa-test,littraceqa-test-extra
MAX_SUBMISSIONS_PER_DAY=5
EVAL_TIMEZONE=America/Toronto
EVAL_DATA_ROOT=data
```

No `HF_TOKEN` is needed by the app when the bucket is mounted into the Space.
If `EVAL_DATA_ROOT` is not set, the app auto-detects `./data` first, then `/data`.

## Mounted Bucket Layout

Create this layout inside the mounted bucket:

```text
data/
  gold/
    goldenviewvqa_gold.jsonl
    littraceqa-test_gold.jsonl
    littraceqa-test-extra_gold.jsonl
  metadata/
    participants.json      # optional; auto-created if missing
    submissions.json       # optional; auto-created if missing
    evaluator.lock         # auto-created
  submissions/
  results/
```

The metadata files can start as empty arrays:

```json
[]
```

## GoldenViewVQA Submission

One JSON object per line:

```json
{"question_id": "sfall_0001_counterfactual", "predicted_view": "CAM_FRONT", "predicted_answer_id": "A"}
```

Sanity checks:

- valid non-empty JSONL
- every row is a JSON object
- exactly one row for every gold `question_id`
- no duplicate or unexpected `question_id`
- only these fields are accepted: `question_id`, `predicted_view`, `predicted_answer_id`
- `predicted_view` must be one of the six nuScenes camera names or `NONE_OF_THE_ABOVE`
- `predicted_answer_id` must be `A`, `B`, `C`, or `D`

Metrics:

- primary score: `joint_accuracy`
- displayed metrics: `joint_accuracy`, `view_accuracy`, `view_macro_accuracy`, `answer_accuracy`

## LitTraceQA Submissions

The evaluator exposes two independent LitTraceQA entries:

- `littraceqa-test`
- `littraceqa-test-extra`

They use the same submission format and metrics, but separate gold files,
leaderboard rows, and daily quota counts.

One JSON object per line:

```json
{
  "query_id": "q_001",
  "gold_papers": [{"paper_id": "acl2025_00005"}],
  "evidence": [
    {
      "paper_id": "acl2025_00005",
      "source_type": "table",
      "locator": {"page": 6, "table_id": "Table 4"}
    }
  ],
  "answer": {
    "freeform": {"text": "..."},
    "multiple_choice": {"gold": "C"},
    "table": {"rows": []}
  }
}
```

Sanity checks:

- valid non-empty JSONL
- every row is a JSON object
- exactly one row for every gold `query_id`
- no duplicate or unexpected `query_id`
- `gold_papers`, if present, must be a list
- `evidence`, if present, must be a list
- `answer`, if present, must be an object

Metrics:

- retrieval: `paper_precision_macro`, `paper_recall_macro`, `paper_f1_macro`
- evidence: `evidence_precision_macro`, `evidence_recall_macro`, `evidence_f1_macro`
- answer: `multiple_choice_accuracy`, `freeform_exact_match`, `table_row_f1_macro`,
  `table_cell_accuracy_macro`, `table_cell_accuracy_micro`
- primary score: mean of `paper_f1_macro`, `evidence_f1_macro`, and the average available answer score
- displayed metrics: `paper_precision_macro`, `paper_recall_macro`, `paper_f1_macro`,
  `evidence_precision_macro`, `evidence_recall_macro`, `evidence_f1_macro`,
  `multiple_choice_accuracy`, `freeform_exact_match`, `table_row_f1_macro`,
  `table_cell_accuracy_macro`, `table_cell_accuracy_micro`
