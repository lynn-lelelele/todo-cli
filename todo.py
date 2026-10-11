# todo-cli
# 参考笔记：C:\Users\19918\Desktop\python_notes\08_文件与JSON\
import json
from pathlib import Path


def load_tasks():#这个是用来json转python,或者说是显示备忘录
    path = Path('task.json')
    if path.exists():

        
        content = path.read_text(encoding='utf-8')
        #有中文要用encoding
        #用这个方法的是字符串

        tasks = json.loads(content)#json转python

    else:
        tasks = []
    return tasks



def save_tasks(task):
    #这个是用来python转json，重新写下一些备忘录并保存
    path = Path('task.json')
    content = json.dumps(task ,ensure_ascii=False) #python转json，
    #ensure_ascii=False这个保证json文件里也是中文
    path.write_text(content,encoding='utf-8') #再把json写入

def show_tasks(tasks):
    #让列表变得更加容易读，展示出来
    for i, task in enumerate(tasks, start=1):  
        if task["done"] == True:
            a = "yes"
        else:
            a = " "   

        print(f"  {i}. [{a}] {task['text']}")

def add_task(tasks, text):#增加一个未完成的事项
    tasks.append({
        "text":text,
        "done":False,
    })

def done_task(tasks, number):
    content = tasks[number-1]
    if content["done"] == False:
        content["done"] = True


def delete_task(tasks, number):
    tasks.pop(number-1)
    
    
def main():
    tasks = load_tasks()

    while True:
        line = input("> ")
        parts = line.split()

        if not parts:
            continue

        command = parts[0]

        if command == "quit":
            break

        elif command == "list":
            show_tasks(tasks)

        elif command == "add":
            text = input("需要加入的事项")
            add_task(tasks, text)           
            save_tasks(tasks)

        elif command == "done":
            number =int(input("需要完成哪一个任务"))
            done_task(tasks, number)          
            save_tasks(tasks)

        elif command == "del":
            num = int(input("需要删除哪一个任务"))
            delete_task(tasks, num)        
            save_tasks(tasks)


if __name__ == "__main__":
    main()
    
    


