# todo-cli · 命令行待办清单
# 数据存在同目录的 task.json 里
import json
from pathlib import Path

DATA_FILE = "task.json"


def load_tasks():
    """读文件，返回任务列表。文件不存在、是空的、或内容坏了，都返回 []。"""
    path = Path(DATA_FILE)

    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8").strip()

    # 空文件：直接当空清单，不要送去 json.loads（它会报错）
    if not content:
        return []

    # 内容坏了也不能让程序崩，捕获 JSON 解析错误
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("警告：task.json 内容不是合法 JSON，本次当作空清单处理。")
        return []


def save_tasks(tasks):
    """把列表写回文件。"""
    path = Path(DATA_FILE)
    # indent=2 让文件带缩进，人更容易读
    content = json.dumps(tasks, ensure_ascii=False, indent=2)
    path.write_text(content, encoding="utf-8")


def show_tasks(tasks):
    """打印全部任务，带序号和完成状态。"""
    if not tasks:
        print("  （清单是空的）")
        return

    for i, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"  {i}. [{mark}] {task['text']}")


def add_task(tasks, text):
    """加一条新任务，默认未完成。"""
    tasks.append({"text": text, "done": False})


def done_task(tasks, number):
    """把第 number 条标成完成。序号越界就返回 False。"""
    if not 1 <= number <= len(tasks):
        return False
    tasks[number - 1]["done"] = True
    return True


def delete_task(tasks, number):
    """删掉第 number 条。序号越界就返回 False。"""
    if not 1 <= number <= len(tasks):
        return False
    tasks.pop(number - 1)
    return True


def ask_number(prompt):
    """问用户要一个序号。输入的不是数字就返回 None。"""
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print(f"「{raw}」不是数字，请输入序号。")
        return None


def main():
    tasks = load_tasks()

    while True:
        # Ctrl+C 或输入流结束时不抛异常，安静退出
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        parts = line.split()
        if not parts:
            continue

        command = parts[0]

        if command == "quit":
            break

        elif command == "list":
            show_tasks(tasks)

        elif command == "add":
            text = input("要加什么：").strip()
            if not text:
                print("内容不能为空。")
                continue
            add_task(tasks, text)
            save_tasks(tasks)
            print(f"已添加：{text}")

        elif command == "done":
            number = ask_number("要完成第几条：")
            if number is None:
                continue
            if done_task(tasks, number):
                save_tasks(tasks)
                print(f"第 {number} 条已完成。")
            else:
                print(f"没有第 {number} 条。")

        elif command == "del":
            number = ask_number("要删除第几条：")
            if number is None:
                continue
            if delete_task(tasks, number):
                save_tasks(tasks)
                print(f"第 {number} 条已删除。")
            else:
                print(f"没有第 {number} 条。")

        else:
            print(f"不认识的命令：{command}　（可用：list / add / done / del / quit）")


if __name__ == "__main__":
    main()
