import json
from pathlib import Path
import todo

# 1. 中文往返
Path("task.json").write_text(
    json.dumps([{"text": "买牛奶", "done": False}, {"text": "写作业", "done": True}], ensure_ascii=False),
    encoding="utf-8")

t = todo.load_tasks()
print("1) load_tasks      :", t)

todo.add_task(t, "买水果")
print("2) add_task        :", [x["text"] for x in t])

todo.done_task(t, 1)
print("3) done_task(1)    :", [(x["text"], x["done"]) for x in t])

todo.delete_task(t, 2)
print("4) delete_task(2)  :", [x["text"] for x in t])

todo.save_tasks(t)
t2 = todo.load_tasks()
print("5) 存盘再读回来    :", t2)
print("6) 往返一致        :", t == t2)

print("7) show_tasks 输出 :")
todo.show_tasks(t)
