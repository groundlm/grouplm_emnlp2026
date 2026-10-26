# Program Schedule Filters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three in-place schedule filters for Talks / Panel, Poster / Oral, and All.

**Architecture:** Keep the existing `PROGRAM` data and `renderProgram()` in `js/main.js`. Add filter metadata to schedule rows and filter controls in `sections/program.html`; use a small delegated click handler and CSS for accessible selected-button styling.

**Tech Stack:** Existing static HTML, CSS, and browser JavaScript; no dependencies.

## Global Constraints

- Preserve the existing site branding and schedule content.
- All is selected by default and shows every schedule row.
- Talks / Panel shows talks and panel; Poster / Oral shows poster rows and oral presentations.
- Coffee/lunch rows containing posters belong to Poster / Oral; other breaks and remarks appear only in All.
- Buttons must be keyboard accessible and expose active state with `aria-pressed`.
- Do not add dependencies or persist filter state.

---

### Task 1: Add program filter controls and metadata

**Files:**
- Modify: `sections/program.html`
- Modify: `data/config.js`

**Interfaces:**
- Each `PROGRAM` entry gains a `filterGroup` string: `talks-panel`, `poster-oral`, or `all-only`.
- Filter buttons use `data-program-filter` values `talks-panel`, `poster-oral`, and `all`.

- [x] Add a labelled button group above `#program-rows`, with All initially `aria-pressed="true"`.
- [x] Assign `talks-panel` to invited talk and panel entries, `poster-oral` to poster-containing sessions and the oral session, and `all-only` to opening, standalone breaks, closing, and end-of-workshop.
- [x] Keep `PROGRAM` as the sole schedule data source.

### Task 2: Implement filtering and style active controls

**Files:**
- Modify: `js/main.js`
- Modify: `css/styles.css`

**Interfaces:**
- `renderProgram()` emits `data-filter-group` on each rendered `.program-row`.
- Clicking a `[data-program-filter]` button updates row visibility and all buttons' `aria-pressed` values.

- [x] Add click handling that filters in place without a reload; All restores all rows.
- [x] Add responsive button styles with a clear active state and visible keyboard focus.

### Task 3: Validate behavior

**Files:**
- Verify: `sections/program.html`, `data/config.js`, `js/main.js`, `css/styles.css`

- [x] Run `git diff --check`.
- [x] Check schedule metadata and JavaScript syntax for the filter categories.
- [x] Confirm no dependency changes.
