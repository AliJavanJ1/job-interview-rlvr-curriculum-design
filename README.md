# Take-home — Excalidraw Browser-Use Curriculum

> **[Internal — before sending to candidate]**
> - Share the zip with the candidate via Kula
> - Share an OpenRouter API key with a $200 cap
> - Expect the candidate's submission reply in the same Kula thread

---

## Prerequisites

**Understand RLVR** — before diving in, read [A Primer on RLVR](docs/a-primer-on-rlvr.md). It explains why we need calibrated tasks and what makes a good reward signal.

Then orient yourself in the repo:

```
.
├── agent/                          # Browser-use agent that attempts tasks (you shouldnt need to edit that but can be insightfull to check it)
├── curriculum/
│   ├── sdk.py                      # Helpers for graders & generators
│   ├── seed_generator.py           # Seed generation utilities
│   └── tasks/
│       └── yellow-circle-in-blue-box/   # <-- Example task (reference only)
│           ├── task.yaml                #     Prompt shown to the agent
│           ├── seed.json                #     Initial canvas state
│           ├── generator.py             #     Regenerates seed.json
│           └── grader.py                #     Scores the result (0 or 1)
├── docs/                           # Background reading
```

---

## Your assignment

Build a calibrated curriculum of browser-use tasks for `claude-opus-4-8` to perform on an Excalidraw canvas.

**Deliverable:** 2 novel tasks, each with a `pass_at_1` between 10% and 50% on `claude-opus-4-8`. Tasks that are trivially easy or nearly impossible don't count.

> **⚠️ IMPORTANT — task ideas must be human-made.** You're welcome to use AI to help write prompts, graders, generators, and code, but **do not use AI to come up with the task ideas themselves**. We want legit, human-made ideas. The same goes for `SUBMISSION.md`: **write it by hand, yourself — no AI allowed on this file.**

**Requirements:**
- **Realistic tasks** — each task should look like something a real user could actually ask the model to do, and be interesting to train on: a genuine capability worth improving, not an arbitrary puzzle.
- **Task calibration** — each task must be empirically calibrated with 10 attempts, with `pass_at_1` landing in the 10–50% window.
- **Task fit for RLVR** — each task must have a deterministic, binary grader (0 or 1) with no LLM-based scoring; the task and its reward signal must be unambiguous.
- **No prompt/grader mismatch** — the grader must score exactly what the prompt asks for: every requirement stated in the prompt must be checked by the grader, and the grader must not check for anything beyond what the prompt asks for.
- **Unique failure modes** — each task must target a different capability or failure mode. The example task (`yellow-circle-in-blue-box`) tests assessment of visual containment — your tasks should exercise something different. Don't just write variations of "move X into Y".

Notes:
- Add new tasks under `curriculum/tasks/`. There is one example task there (`yellow-circle-in-blue-box`) with a full task + grader — use it as a reference only, do not modify it.
- You can ship more tasks if you want but keep it to a maximum of 10.
- When you iterate on a task, don't edit it in place — duplicate the folder with a version suffix (`my-task-v2`, `my-task-v3`, ...) so your execution history stays intact. Calibration usually takes a few iterations to land in the window; that's expected, and we're interested in seeing your thought process while calibrating.
- You can use the whole $200 API budget — budget consumption is not graded. More attempts and more tasks give us more signal.
- If you do not manage to create calibrated tasks this is not a hard fail. In any case we encourage you to push what you have, tasks you created... tell us what you tried.

---

## Submission

**Steps:**

1. Work locally
2. Add a `SUBMISSION.md` at the repo root (do **not** overwrite this README). **Write it by hand, yourself — no AI allowed on this file.** It should cover:
   - **Thought process** — approach and key design decisions
   - **Curriculum thinking** — why these tasks, how they vary
   - **Generation method** — how you built and iterated on tasks, seeds, graders
   - **Model capability / failure mode** — per task, the capability probed and failure mode triggered in `claude-opus-4-8`
   - **Scale** — how you'd grow this to a much larger curriculum
   - **Results** — calibration numbers and anything else worth noting
3. Push to a private Git repo and add the following GitHub handle as a collaborator:

   ```
   @rlTaskReviewer
   ```

4. **Register your submission (run this ONCE)** — POST your repo to our intake
   endpoint so we know it's ready to review. 

   ```bash
   curl -s -X POST "https://tiger-modal--take-home-ce-reviewer-submit.modal.run" \
     -H "Content-Type: application/json" \
     -d '{"repo_url":"<YOUR_REPO_GIT_URL>","candidate":"<YOUR_FULL_NAME>"}'
   ```

   Replace `<YOUR_REPO_GIT_URL>` with your private repo's git URL and
   `<YOUR_FULL_NAME>` with your full name, e.g. `Jane Doe`.

   > **⚠️ IMPORTANT — run this command exactly ONCE.** Each call kicks off a
   > full review. Do not re-run it, loop it, or call it per commit.

5. **Reply in Kula** — many candidates forget this step!

   > **⚠️ IMPORTANT — don't forget to submit in Kula.** Go back to the Kula link you received and send a response along with your repo URL. Your submission is not complete until you've done this.

---

## Setup

```bash
# Frontend (Excalidraw canvas the agent will interact with)
cd app && pnpm install
./dev.sh          # runs on http://localhost:3001

# Python
uv sync
uv run playwright install chromium --with-deps

# API key — you'll receive an OpenRouter key hard-capped at $200 (you cannot exceed this amount)
echo "OPENROUTER_API_KEY=sk-or-..." >> .env

# If you use Claude Code, see: https://openrouter.ai/docs/guides/coding-agents/claude-code-integration
```

---

## Tasks

Each task lives in `curriculum/tasks/<task-name>/` and has four files:

| File | Purpose |
|------|---------|
| `task.yaml` | Prompt shown to the agent |
| `seed.json` | Initial canvas state (must grade 0 — task not yet done) |
| `generator.py` | Script that regenerates `seed.json` |
| `grader.py` | Scores the agent's completed canvas (0 or 1) |

Look at `curriculum/tasks/yellow-circle-in-blue-box/` as a concrete example. You can reuse `curriculum/sdk.py` and `curriculum/seed_generator.py` in your graders and generators, or build your own approach — your call.

---

## Running calibration

```bash
# Run N attempts of a task and record results (10 attempts expected per task)
uv run calibration run --task <task-name> --attempts 10 --model claude-opus-4-8

# Run graders only locally on previous executions
uv run calibration run-graders --task <task-name>
```

Results are appended to `calibration/claude-opus-4-8.yaml`:

```yaml
my-task:
- path: curriculum/tasks/my-task/.execs/claude-opus-4-8/20260321T120000Z
  score: 1
- path: curriculum/tasks/my-task/.execs/claude-opus-4-8/20260321T120500Z
  score: 0
  message: "some_rubric: reason it failed"
```

Commit this file along with your tasks, include executions as well.

---

## Tests

```bash
# Integration tests auto-skip if gym is unreachable
uv run pytest tests/ -v
```

---

## Scoring

1 point for each:

- **`SUBMISSION.md` quality** — clear thought process, generation method, per-task capability/failure mode write-up, curriculum thinking (why these tasks, how they vary), and a credible plan for scaling to a larger curriculum
- **At least one task calibrated** — `pass_at_1` lands in the 10–50% window with the required 10 attempts
- **One unique software-specific failure mode uncovered** for `claude-opus-4-8` — must be distinct from the visual-containment failure mode the example task (`yellow-circle-in-blue-box`) already covers
- **Engineering** — clean grader code, deterministic and well-structured, seeds generated programmatically, repo self-contained and runs end to end on a clean checkout

4 points = pass. 3 points = reviewer's discretion.


Good luck. 