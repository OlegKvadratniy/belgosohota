# AGENTS.md

## What this is

A Russian-language `customtkinter` desktop app for preparing for the Belarusian hunting exam. Questions are in `questions.json` (topics 1-4). Uses bundled tk/tcl (no system tk).

## Quick start

```bash
./launch.sh          # recommended — sets env vars + uses .venv
./.venv/bin/python main.py   # manual: must set LD_LIBRARY_PATH, TCL_LIBRARY, TK_LIBRARY first
```

## Project structure

```
main.py                    — entry point (HuntExamApp)
ui/main_menu_frame.py      — topic/exam/test selection
ui/question_frame.py       — question display + answering
ui/results_frame.py        — results + confetti animation
utils/question_loader.py   — loads + shuffles questions from JSON
questions.json             — question bank
questionsBackup.json       — backup copy
test_backend.py            — standalone test for QuestionLoader
launch.sh                  — portable launcher
run.sh                     — uses /home/went/.local/lib (not portable)
```

## Developer commands

| Action | Command |
|---|---|
| Run app | `./launch.sh` |
| Run test | `./.venv/bin/python test_backend.py` |
| Run app manually | set `LD_LIBRARY_PATH`, `TCL_LIBRARY`, `TK_LIBRARY` then `./.venv/bin/python main.py` |

No linter, formatter, typechecker, CI, or packaging configs exist in the repo.

## Active virtual environment

`.venv/` (Python 3.14, customtkinter 5.2.2, darkdetect 0.8.0). Others (`venv/`, `venv2/`, `test_env/`) are stale.

## Known bug

`results_frame.py:244` — `KeyError: 'color'` in `_animate_confetti`. The confetti `_burst` method sets `'color'` on pieces, but stale pieces from prior runs or cross-frame confetti calls can reach the animation without it.

## Key conventions

- Questions format: `topic` (1-4), `options` (list), `correct_answers` (0-based indices), `is_multiple` (bool), `explanation` (str)
- **251 questions total**: T1=54, T2=113, T3=59, T4=25
- Modes: topic (10 random), exam (2+3+3+2=10), **all** (all 251), **topic_all** (all from one topic)
- Keyboard shortcuts: `1-4` → topics, `5` → exam, `6` → all questions; `X` → toggle explanation; `Enter` → check/next; `1-9` → select option
- Passing: ≤1 error (≥9/10 correct) — applies to all modes
- Options are shuffled per-session; `correct_answers` indices are remapped accordingly
