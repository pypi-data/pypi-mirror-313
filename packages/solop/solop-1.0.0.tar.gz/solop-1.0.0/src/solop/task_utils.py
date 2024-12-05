import re

class Task:
    def __init__(self, id, description, status="backlog", children=[], parent=[], priority=1) -> None:
        self.id = id
        self.description = description
        self.status = status
        self.priority = priority
        self.children = children
        self.parent = parent
    
    def as_string(self):
        return f"- [{self.id}]: {self.description}"
        
class InvalidTaskError(Exception):
    """
    Exception raised for invalid task inputs (ie. Empty descriptions)
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def as_task_object(task):
    """
    Converts the dictionaries from JSON to Task objects
    """
    return Task(id = task['id'],
                description= task['description'],
                status=task.setdefault("status","backlog"),
                priority=task.setdefault("priority",1),
                children=task.setdefault("children",[]),
                parent=task.setdefault("parent",None)
                )

def get_task_object(tasks, task_id):
    assert isinstance(task_id, int), f"get_task_object expects an integer"
    task = get_task(tasks, task_id)
    return as_task_object(task)

def get_task(tasks, task_id):
    assert isinstance(task_id, int), f"get_task expects an integer"
    task = next(task for task in tasks if task['id'] == task_id)
    return task

def get_of_status(tasks, status):
    of_status = []
    for task in tasks:
        if "status" not in task.keys():
            continue
        if task['status'] == status:
            of_status.append(task)
    return of_status

def get_status_list(tasks):
    status_list = dict()
    for task in tasks:
        status_list[task["status"]] = task
    return [*status_list.keys()]

def add_task(tasks, description):
    assert isinstance(description, str), f"Expected a string, got {type(description).__name__}"
    if (len(description) == 0):
        raise InvalidTaskError("Invalid Task Description")
    newlines = re.findall("^", description, flags=re.M)
    if len(newlines) > 1:
        raise InvalidTaskError("Multi-line tasks not supported")
    new_task = Task(id=len(tasks)+1, description=description)
    new_tasks = tasks.copy()
    new_tasks.append(new_task.__dict__)
    return new_tasks

def delete_task(tasks, task_id):
    delete_task = find_task(tasks, task_id)
    for parent in delete_task.setdefault('parent', []):
        parent_task = find_task(tasks, parent)
        tasks = remove_child(tasks, parent_task, delete_task['id'])
        tasks = inherit_children(tasks, parent_task, delete_task['children'])
    for child in delete_task.setdefault('children',[]):
        child_task = find_task(tasks, child)
        tasks = inherit_parent(tasks, child_task, delete_task['id'], delete_task['parent'])
    new_tasks = [task for task in tasks if task != delete_task]
    return new_tasks

def change_status(tasks, task_id, status):
    task = find_task(tasks, task_id)
    tasks[tasks.index(task)]['status'] = re.sub(r'\s', '_', status.lower())
    return tasks

def change_priority(tasks, task_id, priority):
    assert isinstance(priority, int), f"Expected an int, got {type(priority).__name__}"
    task = find_task(tasks, task_id)
    tasks[tasks.index(task)]['priority'] = priority
    return tasks

def find_task(tasks, task_id):
    task = next(task for task in tasks if task['id'] == task_id)
    return task

def set_as_child(tasks, child_id, parent_id):
    child = find_task(tasks, child_id)
    parent = find_task(tasks, parent_id)
    tasks[tasks.index(child)].setdefault("parent",[]).append(parent_id)
    tasks[tasks.index(parent)].setdefault("children",[]).append(child_id)
    return tasks
    
def unset_as_child(tasks, child_id, inherit=False):
    child = find_task(tasks, child_id)
    parents = child['parent']
    if len(parents) == 0:
        return tasks
    for parent in parents:
        parent_task = find_task(tasks, parent)
        tasks = remove_child(tasks, parent_task, child['id'])
        if inherit:
            tasks = inherit_children(tasks, parent_task, child['children'])

    "inherit mode attaches grandchildren onto the parent node"
    if inherit:
        for grandchild in child['children']:
            grandchild_task = find_task(tasks, grandchild)
            tasks = inherit_parent(tasks, grandchild_task, child['id'], child['parent'])
        tasks[tasks.index(child)]["children"] = []
    tasks[tasks.index(child)]["parent"] = []
    return tasks


def remove_child(tasks, parent, child):
    tasks[tasks.index(parent)]['children'].remove(child)
    return tasks

def inherit_children(tasks, parent, children):
    tasks[tasks.index(parent)]['children'].extend(children)
    return tasks
    
def inherit_parent(tasks, grandchild, child, parent):
    tasks[tasks.index(grandchild)]['parent'].remove(child)
    tasks[tasks.index(grandchild)]['parent'].extend(parent)
    return tasks

def sort_tasks(tasks, attr):
    if len(tasks) <= 1:
        return tasks
    mid = len(tasks) // 2
    left = tasks[:mid]
    right = tasks[mid:]

    left = sort_tasks(left, attr)
    right = sort_tasks(right, attr)
    return _merge(left, right, attr)

def _merge(left, right, attr):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        leftsort = rightsort = 0
        if attr not in left[i]:
            leftsort = 1
        else:
            leftsort = left[i][attr]
        if attr not in right[j]:
            rightsort = 1
        else:
            rightsort = right[j][attr]
        if leftsort <= rightsort:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result
 