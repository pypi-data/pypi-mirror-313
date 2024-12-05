import json
from json import JSONDecodeError

class InvalidAttrError(Exception):
    """
    Exception raised when an invalid attribute is requested
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def load_file():
    try:
        with open('solop.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return new_file_format()
    except JSONDecodeError:
        return new_file_format()

def save_file(content):
    with open('solop.json', 'w') as f:
        json.dump(content, f, indent=4)

def load_tasks():
    file = load_file()
    tasks = file['tasks']
    return tasks
    
def save_tasks(tasks):
    file = load_file()
    file["tasks"] = tasks
    save_file(file) 

def change_tasks(action, *args, **kwargs):
    tasks = load_tasks()
    modified = action(tasks, *args, **kwargs)
    modified = validate_tasks(modified, validations)
    save_tasks(modified)
    return modified

def validate_tasks(tasks, validations):
    for validation in validations:
        tasks = validation(tasks)
    return tasks

def validate_duplicate_ids(tasks):
    present = set({})
    duplicates = []
    for task in tasks:
        if task['id'] not in present:
            present.add(task['id'])
        else:
            duplicates.append(task)
    
    for task in duplicates:
        id = 1
        while id in present:
            id = id+1
        present.add(id)
        tasks[tasks.index(task)]['id'] = id
        print(f"Task [{task['description']}] uses an existing ID. Reallocating to ID: {id}") 
    
    return tasks

validations = [
    validate_duplicate_ids,
]

def change_meta(attr, new):
    project = load_file()
    if attr not in project.keys():
        raise InvalidAttrError(f"Attribute {attr} does not exist")
    project[attr] = new
    save_file(project)

def new_file_format():
    return dict({
        "project":"Project",
        "tasks":[],
        "headers":["backlog","in_progress","done"]
        })

