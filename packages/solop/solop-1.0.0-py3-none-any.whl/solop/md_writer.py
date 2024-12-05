import re
from solop.task_utils import (
    get_of_status,
    sort_tasks,
    get_status_list,
    as_task_object,
    get_task,
    get_task_object
)

def _br(number):
    output = ""
    for n in range(number):
        output = output + "\n"
    return output

def _ind(number):
    output = ""
    for n in range(number):
        output = output + "\t"
    return output

def as_header(header, level=1):
    output = ""
    for x in range(level):
        output = output + "#"
    header = re.sub(r"_", " ", header)
    output = output + " " + header.upper()
    return output

class MDWriter:
    def __init__(self, name, tasks, headers):
        self.name = name
        self.tasks = tasks
        self.headers = headers

    def write_md_file(self, render_all=False):
        with open('SOLOP.md', 'w') as writer:
            writer.write(as_header(self.name))
            writer.write(_br(2))
            if render_all:
                statuses = self.extend_headers()
            else:
                statuses = self.headers
            for status in statuses:
                tasks = get_of_status(self.tasks, status)
                section = Section(status, tasks)
                lines = section.render_section()
                for line in lines:
                    writer.write(line + "\n")
                writer.write(_br(1))
            writer.write("This document was generated with SoloP")
            
    def extend_headers(self):
        all_headers = get_status_list(self.tasks)
        extended_headers = self.headers.copy()
        for header in all_headers:
            if header not in self.headers:
                extended_headers.append(header)
        return extended_headers

       
class Section:
    def __init__(self, header, tasks):
        self.header = header
        self.tasks = tasks
        self.ids = self.get_ids(tasks)
        self.layout = self.get_layout(tasks)

    def get_layout(self, tasks):
        layout_map = {}
        for task in tasks:
            if len(task.setdefault('parent',[])) == 0 or (set(task.setdefault('parent',[])).isdisjoint(self.ids)):

                layout_map[str(task['id'])] = self.get_children(task['id'])
        return layout_map
    
    def get_ids(self, tasks):
        ids = set({})
        for task in tasks:
            ids.add(task['id'])
        return ids
            
    
    def get_children(self, id):
        output = [] 
        task = get_task(self.tasks, id)
        if len(task.setdefault("children",[])) > 0:
            children = {}
            for child in task['children']:
                try:    
                    children[str(child)] = self.get_children(child)
                except(StopIteration):
                    continue
            output.append(children)
        return output

    def render_section(self):
        lines = []
        lines.append(as_header(self.header, 2) + ":\n")
        lines.extend(self.render_tier(self.layout, 0))
        return lines

    def get_tier_priority_order(self, tier):
        tasks = []
        for id in tier:
            task = get_task(self.tasks, int(id))
            tasks.append(task)
        tasks = sort_tasks(tasks, "priority")
        order = []
        for task in tasks:
            order.append(task['id'])
        return order

    def render_tier(self, tier, level):
        tier_strings = []
        task_ids = tier.keys()
        order = self.get_tier_priority_order(task_ids)
        for id in order:
            task = get_task_object(self.tasks, id)
            tier_strings.append(_ind(level) + task.as_string())
            if len(tier[str(id)]) > 0:
                nested_strings = self.render_tier(tier[str(id)][0], level+1)
                tier_strings.extend(nested_strings)
        return tier_strings

