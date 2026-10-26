# Program schedule filters

## Goal

Help visitors scan the GroundLM workshop schedule by presentation format without changing the underlying schedule or hiding it by default.

## Design

Add three accessible filter buttons immediately above the program schedule: **Talks / Panel**, **Poster / Oral**, and **All**. **All** is selected by default. Selecting a filter updates the visible program rows in place and marks the active button; it does not navigate or reload the page.

- **Talks / Panel** shows invited talks and the panel.
- **Poster / Oral** shows poster sessions (including coffee/lunch sessions that include posters) and the oral presentation session.
- **All** shows every program row, including opening, breaks, closing remarks, and end-of-workshop.

## Implementation notes

Keep the existing `PROGRAM` data source and `renderProgram()` flow. Add explicit filter metadata to program entries where presentation-format membership differs from the existing broad row type (notably oral presentations, currently typed as `talk`). Keep the buttons keyboard-accessible with a clear selected state and `aria-pressed`; do not add dependencies or persist the choice across visits.

## Validation

Check that each button displays only its intended rows, All restores the complete schedule, the initial state is All, and the active state is perceivable. Run repository-appropriate checks and `git diff --check`.
