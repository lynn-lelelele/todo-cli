"""Tests for todo-cli.

Run with:  python -m unittest -v
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

import todo


class TodoTests(unittest.TestCase):
    """Each test runs in its own empty directory, so the real task.json is never touched."""

    def setUp(self):
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    # --- load_tasks -------------------------------------------------

    def test_load_returns_empty_list_when_file_missing(self):
        self.assertEqual(todo.load_tasks(), [])

    def test_load_returns_empty_list_when_file_is_empty(self):
        Path("task.json").write_text("", encoding="utf-8")
        self.assertEqual(todo.load_tasks(), [])

    def test_load_returns_empty_list_when_json_is_broken(self):
        Path("task.json").write_text("{ this is not json", encoding="utf-8")
        self.assertEqual(todo.load_tasks(), [])

    def test_load_reads_chinese_text(self):
        Path("task.json").write_text(
            json.dumps([{"text": "买牛奶", "done": False}], ensure_ascii=False),
            encoding="utf-8",
        )
        self.assertEqual(todo.load_tasks(), [{"text": "买牛奶", "done": False}])

    # --- save_tasks -------------------------------------------------

    def test_save_then_load_round_trip(self):
        tasks = [{"text": "买牛奶", "done": False}, {"text": "写作业", "done": True}]
        todo.save_tasks(tasks)
        self.assertEqual(todo.load_tasks(), tasks)

    def test_save_writes_readable_chinese(self):
        todo.save_tasks([{"text": "买牛奶", "done": False}])
        raw = Path("task.json").read_text(encoding="utf-8")
        self.assertIn("买牛奶", raw)

    # --- add_task ---------------------------------------------------

    def test_add_task_appends_incomplete_task(self):
        tasks = []
        todo.add_task(tasks, "写作业")
        self.assertEqual(tasks, [{"text": "写作业", "done": False}])

    def test_add_task_keeps_existing_tasks(self):
        tasks = [{"text": "买牛奶", "done": True}]
        todo.add_task(tasks, "打电话")
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0], {"text": "买牛奶", "done": True})

    # --- done_task --------------------------------------------------

    def test_done_task_marks_the_right_task(self):
        tasks = [{"text": "a", "done": False}, {"text": "b", "done": False}]
        self.assertTrue(todo.done_task(tasks, 2))
        self.assertFalse(tasks[0]["done"])
        self.assertTrue(tasks[1]["done"])

    def test_done_task_out_of_range_returns_false(self):
        tasks = [{"text": "a", "done": False}]
        self.assertFalse(todo.done_task(tasks, 5))
        self.assertFalse(todo.done_task(tasks, 0))
        self.assertFalse(tasks[0]["done"])

    # --- delete_task ------------------------------------------------

    def test_delete_task_removes_the_right_task(self):
        tasks = [{"text": "a", "done": False}, {"text": "b", "done": False}]
        self.assertTrue(todo.delete_task(tasks, 1))
        self.assertEqual([t["text"] for t in tasks], ["b"])

    def test_delete_task_out_of_range_returns_false(self):
        tasks = [{"text": "a", "done": False}]
        self.assertFalse(todo.delete_task(tasks, 9))
        self.assertFalse(todo.delete_task(tasks, 0))
        self.assertEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()
