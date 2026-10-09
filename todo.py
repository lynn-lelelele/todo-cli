# todo-cli
# 参考笔记：C:\Users\19918\Desktop\python_notes\08_文件与JSON\
import json
from pathlib import Path


def load_tasks():
    path = Path('task.json')
    if path.exists():

        
        content = path.read_text(encoding='utf-8')
        #有中文要用encoding
        #用这个方法的是字符串

        task = json.loads(content)

    else:
        task = []
    return task

print(load_tasks())
