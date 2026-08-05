from __future__ import annotations

import os
import re
import tempfile
import uuid
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import gradio as gr
import spaces

from evaluator import sanity_check_submission, validate_and_score
from mounted_storage import MountedStorage


MAX_SUBMISSIONS_PER_DAY = int(os.environ.get("MAX_SUBMISSIONS_PER_DAY", "5"))
TIMEZONE = os.environ.get("EVAL_TIMEZONE", "America/Toronto")
PARTICIPANTS_PATH = "metadata/participants.json"
SUBMISSIONS_PATH = "metadata/submissions.json"


@spaces.GPU(duration=1)
def zerogpu_startup_probe() -> None:
    return None


def load_datasets() -> list[str]:
    raw = os.environ.get("EVAL_DATASETS", "").strip()
    if raw:
        return [item.strip() for item in raw.split(",") if item.strip()]
    return ["goldenviewvqa", "littraceqa-test", "littraceqa-test-extra"]


DATASETS = load_datasets()

COMMON_LEADERBOARD_COLUMNS = ["Rank", "Team", "Score", "Submitted at"]
GOLDENVIEW_LEADERBOARD_METRICS = [
    "joint_accuracy",
    "view_accuracy",
    "view_macro_accuracy",
    "answer_accuracy",
]
LITTRACE_LEADERBOARD_METRICS = [
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
]


def now_iso() -> str:
    return datetime.now(ZoneInfo(TIMEZONE)).isoformat(timespec="seconds")


def today_key() -> str:
    return datetime.now(ZoneInfo(TIMEZONE)).date().isoformat()


def profile_value(profile: gr.OAuthProfile | None, key: str) -> str:
    if profile is None:
        return ""
    if isinstance(profile, dict):
        return str(profile.get(key) or "")
    return str(getattr(profile, key, "") or "")


def get_hf_username(profile: gr.OAuthProfile | None) -> str:
    username = profile_value(profile, "username") or profile_value(profile, "preferred_username")
    return username.strip()


def clean_team_name(value: str) -> str:
    value = re.sub(r"\s+", " ", (value or "").strip())
    if len(value) < 2:
        raise ValueError("Team name must contain at least 2 characters.")
    if len(value) > 60:
        raise ValueError("Team name must contain at most 60 characters.")
    return value


def clean_email(value: str) -> str:
    value = (value or "").strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
        raise ValueError("Please enter a valid email address.")
    return value


def storage() -> MountedStorage:
    return MountedStorage()


def load_participants(store: MountedStorage) -> list[dict]:
    return store.read_json(PARTICIPANTS_PATH, [])


def save_participants(store: MountedStorage, participants: list[dict]) -> None:
    store.write_json(PARTICIPANTS_PATH, participants)


def load_submissions(store: MountedStorage) -> list[dict]:
    return store.read_json(SUBMISSIONS_PATH, [])


def save_submissions(store: MountedStorage, submissions: list[dict]) -> None:
    store.write_json(SUBMISSIONS_PATH, submissions)


def participant_for(participants: list[dict], hf_username: str) -> dict | None:
    for participant in participants:
        if participant["hf_username"] == hf_username:
            return participant
    return None


def register(team_name: str, email: str, profile: gr.OAuthProfile | None):
    hf_username = get_hf_username(profile)
    if not hf_username:
        return "Please sign in with Hugging Face first.", refresh_account(profile), refresh_leaderboard(DATASETS[0])
    try:
        team_name = clean_team_name(team_name)
        email = clean_email(email)
        store = storage()
        with store.lock():
            participants = load_participants(store)
            existing = participant_for(participants, hf_username)
            if existing:
                return (
                    f"Already registered as team '{existing['team_name']}'. Registration is immutable.",
                    refresh_account(profile),
                    refresh_leaderboard(DATASETS[0]),
                )
            if any(row["email"].lower() == email for row in participants):
                return "This email is already registered.", refresh_account(profile), refresh_leaderboard(DATASETS[0])
            if any(row["team_name"].lower() == team_name.lower() for row in participants):
                return "This team name is already registered.", refresh_account(profile), refresh_leaderboard(DATASETS[0])
            participants.append(
                {
                    "hf_username": hf_username,
                    "email": email,
                    "team_name": team_name,
                    "created_at": now_iso(),
                    "status": "active",
                }
            )
            save_participants(store, participants)
        return f"Registered team '{team_name}'.", refresh_account(profile), refresh_leaderboard(DATASETS[0])
    except Exception as exc:
        return f"Registration failed: {exc}", refresh_account(profile), refresh_leaderboard(DATASETS[0])


def refresh_account(profile: gr.OAuthProfile | None):
    hf_username = get_hf_username(profile)
    if not hf_username:
        return [["Signed in", "No"], ["HF username", ""], ["Team", ""], ["Email", ""]]
    try:
        store = storage()
        participant = participant_for(load_participants(store), hf_username)
    except Exception:
        participant = None
    return [
        ["Signed in", "Yes"],
        ["HF username", hf_username],
        ["Team", participant["team_name"] if participant else "Not registered"],
        ["Email", participant["email"] if participant else ""],
    ]


def count_today(submissions: list[dict], hf_username: str, dataset: str) -> int:
    date = today_key()
    return sum(
        1
        for row in submissions
        if row["hf_username"] == hf_username
        and row["dataset"] == dataset
        and row["date"] == date
        and row["status"] in {"queued", "running", "succeeded", "failed"}
    )


def save_uploaded_file(uploaded_file) -> Path:
    if isinstance(uploaded_file, dict):
        source_path = uploaded_file.get("path") or uploaded_file.get("name")
    else:
        source_path = getattr(uploaded_file, "path", None) or getattr(uploaded_file, "name", None) or str(uploaded_file)
    if not source_path:
        raise ValueError("Uploaded file path is missing.")
    source = Path(source_path)
    if not source.exists():
        raise ValueError(f"Uploaded file is not accessible on the server: {source}")
    suffix = Path(source_path).suffix or ".jsonl"
    target = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    target.close()
    Path(target.name).write_bytes(source.read_bytes())
    return Path(target.name)


def submit_outputs(message: str, dataset: str, profile: gr.OAuthProfile | None):
    selected_dataset = dataset if dataset in DATASETS else DATASETS[0]
    return (
        message,
        gr.update(value=selected_dataset),
        refresh_leaderboard(selected_dataset),
        refresh_history(profile),
    )


def submit(dataset: str, uploaded_file, profile: gr.OAuthProfile | None):
    hf_username = get_hf_username(profile)
    if not hf_username:
        return submit_outputs("Please sign in with Hugging Face first.", dataset, profile)
    if dataset not in DATASETS:
        return submit_outputs("Unknown dataset.", DATASETS[0], profile)
    if uploaded_file is None:
        return submit_outputs("Please upload a JSONL prediction file.", dataset, profile)

    local_prediction_path: Path | None = None
    try:
        store = storage()
        submission_id = uuid.uuid4().hex[:12]
        created_at = now_iso()
        date = today_key()
        try:
            local_prediction_path = save_uploaded_file(uploaded_file)
        except Exception as exc:
            return submit_outputs(
                f"Sanity check failed and did not count toward today's limit: {exc}",
                dataset,
                profile,
            )
        gold_path = store.path(f"gold/{dataset}_gold.jsonl")
        if not gold_path.exists():
            return submit_outputs(f"Missing gold file: {gold_path}", dataset, profile)

        try:
            sanity_check_submission(dataset, local_prediction_path, gold_path)
        except Exception as exc:
            return submit_outputs(
                f"Sanity check failed and did not count toward today's limit: {exc}",
                dataset,
                profile,
            )

        with store.lock():
            participants = load_participants(store)
            participant = participant_for(participants, hf_username)
            if not participant:
                return submit_outputs("Please register your team before submitting.", dataset, profile)
            if participant.get("status") != "active":
                return submit_outputs("This account is not active.", dataset, profile)

            submissions = load_submissions(store)
            used = count_today(submissions, hf_username, dataset)
            if used >= MAX_SUBMISSIONS_PER_DAY:
                return submit_outputs(
                    f"Daily limit reached for {dataset}: {used}/{MAX_SUBMISSIONS_PER_DAY}.",
                    dataset,
                    profile,
                )

            record = {
                "submission_id": submission_id,
                "hf_username": hf_username,
                "team_name": participant["team_name"],
                "dataset": dataset,
                "date": date,
                "created_at": created_at,
                "status": "running",
            }
            submissions.append(record)
            save_submissions(store, submissions)

        result = validate_and_score(dataset, local_prediction_path, gold_path)
        status = "succeeded"
        error = ""

        with store.lock():
            submissions = load_submissions(store)
            for index, existing in enumerate(submissions):
                if existing.get("submission_id") == submission_id:
                    record = {
                        **existing,
                        "status": status,
                        "completed_at": now_iso(),
                        **result,
                    }
                    if error:
                        record["error"] = error
                    submissions[index] = record
                    break
            store.copy_file(local_prediction_path, f"submissions/{dataset}/{hf_username}/{submission_id}.jsonl")
            store.write_json(f"results/{dataset}/{hf_username}/{submission_id}.json", record)
            save_submissions(store, submissions)
            remaining = MAX_SUBMISSIONS_PER_DAY - count_today(submissions, hf_username, dataset)
        message = (
            f"Submission succeeded. Score={record['score']:.6f}, "
            f"{record['primary_metric']}={record['score']:.6f}. "
            f"{record['metrics_summary']}. "
            f"Remaining submissions today for {dataset}: {remaining}."
        )
        return submit_outputs(message, dataset, profile)
    except Exception as exc:
        return submit_outputs(f"Submission failed: {exc}", dataset, profile)
    finally:
        if local_prediction_path is not None:
            local_prediction_path.unlink(missing_ok=True)


def refresh_leaderboard(dataset: str):
    if dataset not in DATASETS:
        dataset = DATASETS[0]
    metric_columns = leaderboard_metric_columns(dataset)
    try:
        submissions = load_submissions(storage())
    except Exception:
        return gr.update(headers=COMMON_LEADERBOARD_COLUMNS + metric_columns, value=[])
    best: dict[tuple[str, str], dict] = {}
    for row in submissions:
        if row.get("status") != "succeeded":
            continue
        if row.get("dataset") != dataset:
            continue
        key = (row["dataset"], row["team_name"])
        current = best.get(key)
        if current is None or row["score"] > current["score"]:
            best[key] = row
    rows = sorted(best.values(), key=lambda row: (-row["score"], row["created_at"]))
    values = []
    for rank, row in enumerate(rows, start=1):
        values.append(
            [
                rank,
                row["team_name"],
                format_score(row.get("score")),
                row["created_at"],
                *[format_score(metric_value(row, column)) for column in metric_columns],
            ]
        )
    return gr.update(headers=COMMON_LEADERBOARD_COLUMNS + metric_columns, value=values)


def leaderboard_metric_columns(dataset: str) -> list[str]:
    if dataset == "goldenviewvqa":
        return GOLDENVIEW_LEADERBOARD_METRICS
    return LITTRACE_LEADERBOARD_METRICS


def metric_value(row: dict, key: str):
    return row.get("details", {}).get(key, row.get("metrics", {}).get(key))


def format_score(value):
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}"
    return value


def refresh_history(profile: gr.OAuthProfile | None):
    hf_username = get_hf_username(profile)
    if not hf_username:
        return []
    try:
        submissions = load_submissions(storage())
    except Exception:
        return []
    rows = [row for row in submissions if row["hf_username"] == hf_username]
    rows.sort(key=lambda row: row["created_at"], reverse=True)
    return [
        [
            row["created_at"],
            row["dataset"],
            row["submission_id"],
            row["status"],
            row.get("score", ""),
            json.dumps(row.get("metrics", {}), ensure_ascii=False),
        ]
        for row in rows
    ]


with gr.Blocks(title="Evaluation Server") as demo:
    gr.Markdown(
        f"# GroundLM 2026 Evaluation\n"
        f"Sign in with Hugging Face and register your team before submitting. "
        f"Each registered HF account can submit up to {MAX_SUBMISSIONS_PER_DAY} times per task per day. "
        f"Sanity-check failures do not count toward the limit."
    )
    gr.LoginButton()

    with gr.Tab("Account"):
        account = gr.Dataframe(headers=["Field", "Value"], interactive=False, value=[])
        with gr.Row():
            team_name = gr.Textbox(label="Team name")
            email = gr.Textbox(label="Email")
        register_button = gr.Button("Register")
        register_status = gr.Textbox(label="Status", interactive=False)

    with gr.Tab("Submit"):
        dataset = gr.Dropdown(choices=DATASETS, value=DATASETS[0], label="Dataset")
        upload = gr.File(label="prediction.jsonl", file_types=[".jsonl", ".json"], type="filepath")
        submit_button = gr.Button("Submit")
        submit_status = gr.Textbox(label="Status", interactive=False)
        history = gr.Dataframe(
            headers=["Created at", "Dataset", "Submission ID", "Status", "Score", "Metrics JSON"],
            interactive=False,
            value=[],
        )

    with gr.Tab("Leaderboard"):
        leaderboard_dataset = gr.Dropdown(choices=DATASETS, value=DATASETS[0], label="Task")
        leaderboard = gr.Dataframe(
            headers=COMMON_LEADERBOARD_COLUMNS + GOLDENVIEW_LEADERBOARD_METRICS,
            interactive=False,
            value=[],
        )
        refresh_button = gr.Button("Refresh")

    demo.load(fn=refresh_account, inputs=None, outputs=account)
    demo.load(fn=refresh_history, inputs=None, outputs=history)
    demo.load(fn=refresh_leaderboard, inputs=leaderboard_dataset, outputs=leaderboard)
    register_button.click(fn=register, inputs=[team_name, email], outputs=[register_status, account, leaderboard])
    submit_button.click(
        fn=submit,
        inputs=[dataset, upload],
        outputs=[submit_status, leaderboard_dataset, leaderboard, history],
    )
    leaderboard_dataset.change(fn=refresh_leaderboard, inputs=leaderboard_dataset, outputs=leaderboard)
    refresh_button.click(fn=refresh_leaderboard, inputs=leaderboard_dataset, outputs=leaderboard)


if __name__ == "__main__":
    demo.launch()
