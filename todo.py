# todo-cli
# 参考笔记：C:\Users\19918\Desktop\python_notes\08_文件与JSON\
import json
from pathlib import Path


def load_tasks():#这个是用来json转python
    path = Path('task.json')
    if path.exists():

        
        content = path.read_text(encoding='utf-8')
        #有中文要用encoding
        #用这个方法的是字符串

        task = json.loads(content)#json转python

    else:
        task = []
    return task



def save_tasks(task):#这个是用来python转json
    path = Path('task.json')
    content = json.dumps(task ,ensure_ascii=False) #python转json，
    #ensure_ascii=False这个保证json文件里也是中文
    path.write_text(content,encoding='utf-8') #再把json写入
    
    
tasks = load_tasks()
tasks.append({"text": "打电话", "done": False})
save_tasks(tasks)
print(load_tasks())
    
    


