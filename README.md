# todo-cli

![CI](https://github.com/lynn-lelelele/todo-cli/actions/workflows/ci.yml/badge.svg)

A small command-line to-do list in pure Python. Tasks are stored in a JSON file next to the script, so they survive restarts.

**This is my first project written from scratch** — no tutorial to follow, no AI-generated code.
I wrote the spec, designed the data format, and implemented every function myself, then fixed four bugs with the debugger workflow (`path` ordering, a typo, a UTF-8 error, and a missing JSON comma).

## Features

- Add a task
- List every task with its number and status
- Mark a task as done
- Delete a task
- Data persists in `task.json`
- Handles bad input instead of crashing: missing file, empty file, corrupt JSON, out-of-range numbers, non-numeric input

## Usage

```bash
python todo.py
```

The interface is in Chinese. A session looks like this:

```
> list
  1. [ ] 买牛奶
  2. [x] 写作业
  3. [ ] 打电话

> add
要加什么：买水果
已添加：买水果

> done
要完成第几条：1
第 1 条已完成。

> del
要删除第几条：3
第 3 条已删除。

> quit
```

## Commands

| Command | What it does |
|---|---|
| `list` | show every task |
| `add` | add a task — then asks for the text |
| `done` | mark a task complete — then asks for the number |
| `del` | delete a task — then asks for the number |
| `quit` | exit |

Unknown commands print a hint instead of crashing.

## Tests

```bash
python -m unittest -v```

12 unit tests covering file I/O, round-trip persistence, bad input, and out-of-range numbers. They run in CI on every push.

## Requirements

Python 3.10 or newer. No third-party packages.

## Files

| File | Purpose |
|---|---|
| `todo.py` | the whole program |
| `task.json` | where tasks are stored (created on first save) |

## Design notes

- `load_tasks()` and `save_tasks()` are the **only** functions that touch the file. Everything else works on a plain Python list.
- **Task numbers are not stored in the JSON.** They are generated at display time from the list index (`enumerate(tasks, start=1)`), so deleting a task never leaves a stale number behind.
- `done_task()` and `delete_task()` return `False` when the number is out of range, instead of raising an exception.
- `load_tasks()` treats a missing, empty, or corrupt file as "no tasks" and carries on.

## Bug notes

The four bugs I hit while building this, and what they taught me:

| Bug | Lesson |
|---|---|
| `UnboundLocalError: path` | A variable assigned inside an `if` block is local to the whole function — assign before you use it |
| `UnicodeDecodeError: gbk codec` | `Path.read_text()` needs `encoding="utf-8"` on Windows, or any non-ASCII text breaks |
| `json.load()` on a string | `json.load()` takes a **file object**; `json.loads()` takes a **string** |
| Missing comma in JSON | JSON is strict — two objects in a list need a comma between them |

And a fifth, found while testing:

| Bug | Lesson |
|---|---|
| `if path.exists:` | Without `()`, that is the method object — always truthy — so the branch always runs. Silent, no error. Same trap as writing `==` instead of `=`. |

