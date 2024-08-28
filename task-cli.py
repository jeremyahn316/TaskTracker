import argparse
import os.path
import json

TODO_FILE = "todo.json"
STATUS = {"NOT DONE": 'todo',
          "IN PROGRESS": 'in-progress',
          "DONE": 'done'}

def todo_exist_check():
    if not os.path.exists(TODO_FILE):
        print("json file does not exist")
        with open(TODO_FILE, "w") as json_file:
            json.dump({}, json_file)

def load_file():
    with open(TODO_FILE, "r") as json_file:
        data = json.load(json_file)
    return data

def save_file(data):
        with open(TODO_FILE, "w") as json_file:
            json.dump(data, json_file)

def output_list(list):
    if list:
        for elem in list:
            print(f"+{'-' * (len(elem) + 2)}+")
            print(f"| {elem} |")
        print(f"+{'-' * (len(list[0]) + 2)}+")

def check_data(data, id):
    prev_tasks = list(data[id])

    if not prev_tasks:
        print("Not a valid TODO ID")
        return
    
    prev_task = prev_tasks[0]
    status = data[id][prev_task]
    return prev_task, status


def add_task(task: str):
    # Load JSON file
    data = load_file()

    # Create an unique ID
    # If there aren't any task, start at one
    # Else get the last used id and use incremented id
    # TODO
    id = 1 if not data else max(data["id"]) + 1

    # Add new entry to JSON 
    data[id] = {task: "NOT DONE"}

    # Update the JSON file
    save_file(data)

def update_task(id: int, task: str):
    # Load JSON file
    data = load_file()

    # Get the previous status
    _, status = check_data(data, id)

    # Update the task description
    data[id] = {task: status}

    # Update the JSON file
    save_file(data)

def delete_task(id: int):
    # Load the JSON file
    data = load_file()

    # Check if the id exists
    if id not in data:
        print("Invalid ID; This TODO item doesn't exist")
        return
    
    # Delete the entry in JSON file
    del data[id]

    # Update the JSON file
    save_file(data)

def in_progress_status(id):
    # Load the JSON file
    data = load_file()

    # Get the task description of given id
    task, _ = check_data(data, id)

    # Update the status to IN PROGRESS
    data[id] = {task: "IN PROGRESS"}

    # Update the JSON file
    save_file(data)

def done_status(id):
    # Load the JSON file
    data = load_file()

    # Get the task description of given id
    task, _ = check_data(data, id)

    # Update the status to DONE
    data[id] = {task: "DONE"}

    # Update the JSON file
    save_file(data)

def list_todos(status):
    # Load the JSON file
    data = load_file()
    todos = []

    # If status is specified, need to get a list with matching status
    if status:
        # Go through all the task
        for id in data:
            task, cur_status = check_data(data, id)

            # If status matches, add task to output list
            if STATUS[cur_status] == status:
                todos.append(task)
    else:
        # Go through all the task and add all to output list
        for id in data:
            task, _ = check_data(data, id)
            todos.append(task)

    # Output the final list of tasks 
    output_list(todos)

def parse_argument():
    parser = argparse.ArgumentParser(description="CLI app to Track your task and manage your TODO list")
    subparser = parser.add_subparsers(dest="command", help="Commands for TODO list")

    # Need to add, update, delete todo item 
    add_parser = subparser.add_parser("add", help="Add a new tas to TODO list")
    add_parser.add_argument("task", type=str, help="Task Description")

    update_parser = subparser.add_parser("update", help="Update an existing TODO item")
    update_parser.add_argument("id", type=str, help="Unique identifier for TODO item")
    update_parser.add_argument("task", type=str, help="Updated Task Description")

    delete_parser = subparser.add_parser("delete", help="Delete a task if it exists")
    delete_parser.add_argument("id", type=str, help="Unique identifier for TODO item")

    # Need to update status
    in_progress_parser = subparser.add_parser("mark-in-progress", help="Change the status of id to In Progress")
    in_progress_parser.add_argument("id", type=str, help="Unique identifier for TODO item")

    done_parser = subparser.add_parser("mark-done", help="Change the status of id to Done")
    done_parser.add_argument("id", type=str, help="Unique identifier for TODO item")

    # Need to show list
    list_parser = subparser.add_parser("list", help="List tasks on the TODO list")
    list_parser.add_argument("status", nargs='?', type=str, help="Specify task with following status (done, todo, in-progress) to return")
    

    return parser

def main():
    todo_exist_check()
    parser = parse_argument()

    args = parser.parse_args()
    if args.command == "add":
        add_task(args.task)
    elif args.command == "update":
        update_task((args.id), args.task)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-in-progress":
        in_progress_status(args.id)
    elif args.command == "mark-done":
        done_status(args.id)
    elif args.command == "list":
        if args.status in [None, "done", "todo", "in-progress"]: # Instead of None, is it ""
            list_todos(args.status)
        else:
            print("Invalid status type, please try again")
            parser.print_help()
    else:
        print("Invalid command, please try again")
        parser.print_help()

if __name__ == '__main__':
    main()