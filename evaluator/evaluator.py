from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any


CAMERA_VIEWS = {
    "CAM_FRONT",
    "CAM_FRONT_LEFT",
    "CAM_FRONT_RIGHT",
    "CAM_BACK",
    "CAM_BACK_LEFT",
    "CAM_BACK_RIGHT",
}
PREDICTED_VIEWS = CAMERA_VIEWS | {"NONE_OF_THE_ABOVE"}
ANSWER_IDS = {"A", "B", "C", "D"}
GOLDENVIEW_FIELDS = {"question_id", "predicted_view", "predicted_answer_id"}


class SubmissionValidationError(ValueError):
    pass


def read_jsonl(path: str | Path, *, allow_blank_lines: bool = False) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                if allow_blank_lines:
                    continue
                raise SubmissionValidationError(f"{Path(path).name}:{line_number}: blank lines are not allowed")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SubmissionValidationError(f"{Path(path).name}:{line_number}: invalid JSON") from exc
            if not isinstance(record, dict):
                raise SubmissionValidationError(f"{Path(path).name}:{line_number}: each line must be a JSON object")
            records.append(record)
    if not records:
        raise SubmissionValidationError(f"{Path(path).name}: file is empty")
    return records


def normalize(value: Any) -> str:
    return str(value or "").strip()


def normalize_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = text.strip("\"'“”‘’`")
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_id(value: Any) -> str:
    return str(value or "").strip()


def unique_ids(records: list[dict[str, Any]], id_field: str, label: str) -> list[str]:
    ids = [record.get(id_field) for record in records]
    missing = [index for index, item_id in enumerate(ids, start=1) if not isinstance(item_id, str) or not item_id]
    if missing:
        raise SubmissionValidationError(f"{label}: missing {id_field} on rows {missing[:10]}")
    duplicates = sorted(item_id for item_id, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise SubmissionValidationError(f"{label}: duplicate {id_field} values: {duplicates[:10]}")
    return ids


def check_id_coverage(expected_ids: list[str], predicted_ids: list[str], label: str = "submission") -> None:
    expected = set(expected_ids)
    predicted = set(predicted_ids)
    missing = sorted(expected - predicted)
    extra = sorted(predicted - expected)
    if missing:
        raise SubmissionValidationError(f"{label}: missing predictions: {missing[:10]}")
    if extra:
        raise SubmissionValidationError(f"{label}: unexpected predictions: {extra[:10]}")


def validate_goldenview_submission(gold_records: list[dict[str, Any]], pred_records: list[dict[str, Any]]) -> None:
    expected_ids = unique_ids(gold_records, "question_id", "gold")
    predicted_ids = unique_ids(pred_records, "question_id", "submission")
    check_id_coverage(expected_ids, predicted_ids)

    for row_number, record in enumerate(pred_records, start=1):
        fields = set(record)
        missing_fields = sorted(GOLDENVIEW_FIELDS - fields)
        extra_fields = sorted(fields - GOLDENVIEW_FIELDS)
        if missing_fields:
            raise SubmissionValidationError(f"submission row {row_number}: missing fields: {missing_fields}")
        if extra_fields:
            raise SubmissionValidationError(f"submission row {row_number}: unexpected fields: {extra_fields}")
        if record["predicted_view"] not in PREDICTED_VIEWS:
            raise SubmissionValidationError(
                f"submission row {row_number}: invalid predicted_view: {record['predicted_view']!r}"
            )
        if record["predicted_answer_id"] not in ANSWER_IDS:
            raise SubmissionValidationError(
                f"submission row {row_number}: invalid predicted_answer_id: {record['predicted_answer_id']!r}"
            )


def evaluate_goldenview(gold_records: list[dict[str, Any]], pred_records: list[dict[str, Any]]) -> dict[str, Any]:
    validate_goldenview_submission(gold_records, pred_records)
    gold_by_id = {record["question_id"]: record for record in gold_records}
    pred_by_id = {record["question_id"]: record for record in pred_records}

    view_correct = 0
    answer_correct = 0
    joint_correct = 0
    view_totals: Counter[str] = Counter()
    view_correct_by_class: Counter[str] = Counter()

    for question_id, gold in gold_by_id.items():
        pred = pred_by_id[question_id]
        is_view_correct = normalize(pred.get("predicted_view")) == normalize(gold.get("golden_view"))
        is_answer_correct = normalize(pred.get("predicted_answer_id")).upper() == normalize(
            gold.get("gold_answer_id")
        ).upper()
        view_correct += int(is_view_correct)
        answer_correct += int(is_answer_correct)
        joint_correct += int(is_view_correct and is_answer_correct)
        view_label = normalize(gold.get("golden_view"))
        view_totals[view_label] += 1
        view_correct_by_class[view_label] += int(is_view_correct)

    total = len(gold_records)
    view_recall_by_class = {
        label: view_correct_by_class[label] / count
        for label, count in sorted(view_totals.items())
    }
    metrics = {
        "view_accuracy": view_correct / total if total else 0.0,
        "view_macro_accuracy": (
            sum(view_recall_by_class.values()) / len(view_recall_by_class)
            if view_recall_by_class
            else 0.0
        ),
        "answer_accuracy": answer_correct / total if total else 0.0,
        "joint_accuracy": joint_correct / total if total else 0.0,
    }
    details = {
        "total": total,
        "view_correct": view_correct,
        "answer_correct": answer_correct,
        "joint_correct": joint_correct,
        "view_recall_by_class": view_recall_by_class,
    }
    return format_result(
        dataset_type="goldenviewvqa",
        score=metrics["joint_accuracy"],
        metrics=metrics,
        details=details,
        primary_metric="joint_accuracy",
        leaderboard_metrics=["joint_accuracy", "view_accuracy", "view_macro_accuracy", "answer_accuracy"],
    )


def paper_id_set(record: dict[str, Any]) -> set[str]:
    papers = record.get("gold_papers") or record.get("papers") or []
    paper_ids: set[str] = set()
    if not isinstance(papers, list):
        return paper_ids
    for item in papers:
        if isinstance(item, str):
            paper_id = item
        elif isinstance(item, dict):
            paper_id = item.get("paper_id", "")
        else:
            paper_id = ""
        paper_id = normalize_id(paper_id)
        if paper_id:
            paper_ids.add(paper_id)
    return paper_ids


def normalize_visible_id(value: Any, prefix: str) -> str:
    text = normalize_text(value)
    if not text:
        return ""
    match = re.fullmatch(rf"{prefix.lower()}\s*(\d+[a-z]?)", text)
    if match:
        return f"{prefix.lower()} {match.group(1)}"
    if re.fullmatch(r"\d+[a-z]?", text):
        return f"{prefix.lower()} {text}"
    return text


def coarse_evidence_key(item: dict[str, Any]) -> tuple[str, str, str, str]:
    paper_id = normalize_id(item.get("paper_id"))
    source_type = normalize_id(item.get("source_type"))
    locator = item.get("locator") if isinstance(item.get("locator"), dict) else {}
    location = str(locator.get("page") or locator.get("section") or "").strip()
    object_id = ""
    if source_type == "table":
        object_id = normalize_visible_id(locator.get("table_id"), "table")
    elif source_type == "figure":
        object_id = normalize_visible_id(locator.get("figure_id"), "figure")
    elif source_type == "equation_algorithm":
        object_id = normalize_visible_id(
            locator.get("equation_id") or locator.get("algorithm_id"),
            "equation",
        )
    elif source_type == "citation_context":
        object_id = normalize_visible_id(locator.get("citation_id"), "citation")
    return (paper_id, source_type, location, object_id)


def evidence_set(record: dict[str, Any]) -> set[tuple[str, str, str, str]]:
    evidence = record.get("evidence") or []
    if not isinstance(evidence, list):
        return set()
    keys = set()
    for item in evidence:
        if isinstance(item, dict):
            key = coarse_evidence_key(item)
            if key[0] and key[1] and (key[2] or key[3]):
                keys.add(key)
    return keys


def prf(gold: set[Any], pred: set[Any]) -> tuple[float, float, float]:
    if not gold and not pred:
        return (1.0, 1.0, 1.0)
    if not pred:
        return (0.0, 0.0 if gold else 1.0, 0.0)
    correct = len(gold & pred)
    precision = correct / len(pred) if pred else 0.0
    recall = correct / len(gold) if gold else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return (precision, recall, f1)


def prediction_answer(record: dict[str, Any]) -> dict[str, Any]:
    answer = record.get("answer")
    return answer if isinstance(answer, dict) else {}


def multiple_choice_prediction(record: dict[str, Any]) -> str:
    answer = prediction_answer(record)
    mc = answer.get("multiple_choice")
    if isinstance(mc, dict):
        return normalize_id(mc.get("gold") or mc.get("answer") or mc.get("predicted_answer_id")).upper()
    return normalize_id(record.get("predicted_answer_id") or record.get("gold") or record.get("gold_answer")).upper()


def multiple_choice_gold(record: dict[str, Any]) -> str:
    mc = record.get("answer", {}).get("multiple_choice", {})
    return normalize_id(mc.get("gold")).upper() if isinstance(mc, dict) else ""


def freeform_prediction(record: dict[str, Any]) -> str:
    answer = prediction_answer(record)
    freeform = answer.get("freeform")
    if isinstance(freeform, dict):
        return normalize_text(freeform.get("text"))
    return normalize_text(record.get("answer_text") or record.get("freeform"))


def freeform_gold(record: dict[str, Any]) -> str:
    freeform = record.get("answer", {}).get("freeform", {})
    return normalize_text(freeform.get("text")) if isinstance(freeform, dict) else ""


def normalize_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").strip().replace("%", "")
    try:
        return float(text)
    except ValueError:
        return None


def row_key_value(row: dict[str, Any], row_key_columns: list[str]) -> tuple[str, ...]:
    return tuple(normalize_text(row.get(column)) for column in row_key_columns)


def cell_equal(gold_value: Any, pred_value: Any, column_type: str) -> bool:
    if gold_value is None or pred_value is None:
        return gold_value is None and pred_value is None
    if column_type == "number":
        gold_number = normalize_number(gold_value)
        pred_number = normalize_number(pred_value)
        if gold_number is None or pred_number is None:
            return False
        return math.isclose(gold_number, pred_number, rel_tol=1e-6, abs_tol=1e-6)
    if column_type == "boolean":
        return bool(gold_value) == bool(pred_value)
    return normalize_text(gold_value) == normalize_text(pred_value)


def table_metrics(gold: dict[str, Any], pred: dict[str, Any]) -> dict[str, float | int]:
    gold_table = gold.get("answer", {}).get("table", {})
    pred_table = prediction_answer(pred).get("table", {})
    if not isinstance(gold_table, dict) or not isinstance(pred_table, dict):
        return {
            "row_precision": 0.0,
            "row_recall": 0.0,
            "row_f1": 0.0,
            "cell_accuracy": 0.0,
            "cell_correct": 0,
            "cell_total": 0,
        }

    schema = gold_table.get("schema") if isinstance(gold_table.get("schema"), list) else []
    gold_rows = gold_table.get("rows") if isinstance(gold_table.get("rows"), list) else []
    pred_rows = pred_table.get("rows") if isinstance(pred_table.get("rows"), list) else []
    row_keys = [column["name"] for column in schema if isinstance(column, dict) and column.get("is_row_key")]
    if not row_keys and schema:
        row_keys = [str(schema[0].get("name", ""))]

    gold_by_key = {
        row_key_value(row, row_keys): row
        for row in gold_rows
        if isinstance(row, dict) and row_key_value(row, row_keys)
    }
    pred_by_key = {
        row_key_value(row, row_keys): row
        for row in pred_rows
        if isinstance(row, dict) and row_key_value(row, row_keys)
    }
    row_precision, row_recall, row_f1 = prf(set(gold_by_key), set(pred_by_key))

    cell_correct = 0
    cell_total = 0
    comparable_columns = [
        (str(column.get("name", "")), str(column.get("type", "string")))
        for column in schema
        if isinstance(column, dict) and str(column.get("name", "")) and not column.get("is_row_key")
    ]
    for key, gold_row in gold_by_key.items():
        pred_row = pred_by_key.get(key)
        if not isinstance(pred_row, dict):
            cell_total += len(comparable_columns)
            continue
        for column_name, column_type in comparable_columns:
            cell_total += 1
            if cell_equal(gold_row.get(column_name), pred_row.get(column_name), column_type):
                cell_correct += 1
    cell_accuracy = cell_correct / cell_total if cell_total else row_f1
    return {
        "row_precision": row_precision,
        "row_recall": row_recall,
        "row_f1": row_f1,
        "cell_accuracy": cell_accuracy,
        "cell_correct": cell_correct,
        "cell_total": cell_total,
    }


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def validate_littrace_submission(gold_records: list[dict[str, Any]], pred_records: list[dict[str, Any]]) -> None:
    expected_ids = unique_ids(gold_records, "query_id", "gold")
    predicted_ids = unique_ids(pred_records, "query_id", "submission")
    check_id_coverage(expected_ids, predicted_ids)
    for row_number, record in enumerate(pred_records, start=1):
        if not isinstance(record.get("gold_papers", []), list):
            raise SubmissionValidationError(f"submission row {row_number}: gold_papers must be a list")
        if not isinstance(record.get("evidence", []), list):
            raise SubmissionValidationError(f"submission row {row_number}: evidence must be a list")
        if "answer" in record and not isinstance(record["answer"], dict):
            raise SubmissionValidationError(f"submission row {row_number}: answer must be an object")


def evaluate_littrace(gold_records: list[dict[str, Any]], pred_records: list[dict[str, Any]]) -> dict[str, Any]:
    validate_littrace_submission(gold_records, pred_records)
    gold_by_id = {normalize_id(record.get("query_id")): record for record in gold_records}
    pred_by_id = {normalize_id(record.get("query_id")): record for record in pred_records}

    paper_precision: list[float] = []
    paper_recall: list[float] = []
    paper_f1: list[float] = []
    evidence_precision: list[float] = []
    evidence_recall: list[float] = []
    evidence_f1: list[float] = []
    mc_correct = 0
    mc_total = 0
    freeform_exact_correct = 0
    freeform_total = 0
    table_row_f1: list[float] = []
    table_cell_accuracy: list[float] = []
    table_cell_correct = 0
    table_cell_total = 0

    for query_id, gold in gold_by_id.items():
        pred = pred_by_id[query_id]
        evaluation_targets = set(
            gold.get("evaluation_targets") or ["paper", "evidence", "answer"]
        )

        if "paper" in evaluation_targets:
            p, r, f = prf(paper_id_set(gold), paper_id_set(pred))
            paper_precision.append(p)
            paper_recall.append(r)
            paper_f1.append(f)

        if "evidence" in evaluation_targets:
            p, r, f = prf(evidence_set(gold), evidence_set(pred))
            evidence_precision.append(p)
            evidence_recall.append(r)
            evidence_f1.append(f)

        answer_types = set(gold.get("answer_types") or [])
        if "answer" in evaluation_targets and "multiple_choice" in answer_types:
            mc_total += 1
            mc_correct += int(multiple_choice_prediction(pred) == multiple_choice_gold(gold))

        if "answer" in evaluation_targets and "freeform" in answer_types:
            freeform_total += 1
            freeform_exact_correct += int(freeform_prediction(pred) == freeform_gold(gold))

        if "answer" in evaluation_targets and "table" in answer_types:
            metrics = table_metrics(gold, pred)
            table_row_f1.append(float(metrics["row_f1"]))
            table_cell_accuracy.append(float(metrics["cell_accuracy"]))
            table_cell_correct += int(metrics["cell_correct"])
            table_cell_total += int(metrics["cell_total"])

    metrics = {
        "paper_precision_macro": mean(paper_precision) if paper_precision else None,
        "paper_recall_macro": mean(paper_recall) if paper_recall else None,
        "paper_f1_macro": mean(paper_f1) if paper_f1 else None,
        "evidence_precision_macro": mean(evidence_precision) if evidence_precision else None,
        "evidence_recall_macro": mean(evidence_recall) if evidence_recall else None,
        "evidence_f1_macro": mean(evidence_f1) if evidence_f1 else None,
        "multiple_choice_accuracy": mc_correct / mc_total if mc_total else None,
        "freeform_exact_match": freeform_exact_correct / freeform_total if freeform_total else None,
        "table_row_f1_macro": mean(table_row_f1),
        "table_cell_accuracy_macro": mean(table_cell_accuracy),
        "table_cell_accuracy_micro": table_cell_correct / table_cell_total if table_cell_total else None,
    }
    answer_scores = [
        value
        for value in [
            metrics["multiple_choice_accuracy"],
            metrics["freeform_exact_match"],
            metrics["table_row_f1_macro"] if table_row_f1 else None,
            metrics["table_cell_accuracy_macro"] if table_cell_accuracy else None,
        ]
        if value is not None
    ]
    answer_score = mean([float(value) for value in answer_scores])
    score = mean(
        [
            float(value)
            for value in [metrics["paper_f1_macro"], metrics["evidence_f1_macro"], answer_score]
            if value is not None
        ]
    )
    details = {
        "total": len(gold_records),
        "table_cell_correct": table_cell_correct,
        "table_cell_total": table_cell_total,
        "multiple_choice_total": mc_total,
        "freeform_total": freeform_total,
        "table_total": len(table_row_f1),
        "answer_score": answer_score,
    }
    return format_result(
        dataset_type="littraceqa",
        score=score,
        metrics=metrics,
        details=details,
        primary_metric="composite_score",
        leaderboard_metrics=[
            "paper_precision_macro",
            "paper_recall_macro",
            "paper_f1_macro",
            "evidence_precision_macro",
            "evidence_recall_macro",
            "evidence_f1_macro",
            "multiple_choice_accuracy",
            "freeform_exact_match",
            "table_row_f1_macro",
            "table_cell_accuracy_macro",
            "table_cell_accuracy_micro",
        ],
    )


def dataset_type(dataset: str) -> str:
    normalized = dataset.lower().replace("-", "").replace("_", "")
    if normalized in {"goldenviewvqa", "goldenview", "groundlm", "groundlmvqa"}:
        return "goldenviewvqa"
    if normalized in {"littraceqa", "littrace", "littraceqatest", "littraceqatestextra"}:
        return "littraceqa"
    if normalized.startswith("littraceqa"):
        return "littraceqa"
    raise SubmissionValidationError(
        f"Unknown dataset '{dataset}'. Use one of: goldenviewvqa, littraceqa."
    )


def format_metric_value(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def metrics_summary(result: dict[str, Any]) -> str:
    metrics = result.get("metrics", {})
    details = result.get("details", {})
    pieces = []
    for key in result.get("leaderboard_metrics", []):
        value = details.get(key, metrics.get(key))
        pieces.append(f"{key}={format_metric_value(value)}")
    return ", ".join(pieces)


def format_result(
    *,
    dataset_type: str,
    score: float,
    metrics: dict[str, Any],
    details: dict[str, Any],
    primary_metric: str,
    leaderboard_metrics: list[str],
) -> dict[str, Any]:
    rounded_metrics = {
        key: (round(value, 6) if isinstance(value, float) else value)
        for key, value in metrics.items()
    }
    rounded_details = {
        key: (round(value, 6) if isinstance(value, float) else value)
        for key, value in details.items()
    }
    result = {
        "dataset_type": dataset_type,
        "score": round(score, 6),
        "primary_metric": primary_metric,
        "metrics": rounded_metrics,
        "details": rounded_details,
        "leaderboard_metrics": leaderboard_metrics,
    }
    result["metrics_summary"] = metrics_summary(result)
    return result


def sanity_check_submission(dataset: str, prediction_path: str | Path, gold_path: str | Path) -> None:
    task = dataset_type(dataset)
    gold_records = read_jsonl(gold_path, allow_blank_lines=True)
    pred_records = read_jsonl(prediction_path, allow_blank_lines=False)
    if task == "goldenviewvqa":
        validate_goldenview_submission(gold_records, pred_records)
    elif task == "littraceqa":
        validate_littrace_submission(gold_records, pred_records)


def validate_and_score(dataset: str, prediction_path: str | Path, gold_path: str | Path) -> dict[str, Any]:
    task = dataset_type(dataset)
    gold_records = read_jsonl(gold_path, allow_blank_lines=True)
    pred_records = read_jsonl(prediction_path, allow_blank_lines=False)
    if task == "goldenviewvqa":
        return evaluate_goldenview(gold_records, pred_records)
    if task == "littraceqa":
        return evaluate_littrace(gold_records, pred_records)
    raise AssertionError(f"Unhandled dataset type: {task}")
