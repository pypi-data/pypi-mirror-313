from unittest.mock import patch
import copy
import pytest
from src.solop.task_utils import *

mock_data = [
{
    "id":1,
    "description": "Existing Task",
    "status": "backlog"
}]

mock_data_extended = [
{
    "id":1,
    "description":"Backlog 1",
    "status": "backlog"
},
{
    "id":2,
    "description":"Backlog 2",
    "status": "backlog",
    "priority":1
},
{
    "id":3,
    "description":"Progress 2",
    "status": "in_progress"
}]

mock_data_test_children = [
    {
        "id":1,
        "description":"Test, tier 1",
        "status": "backlog",
        "parent":[],
        "children":[2]
    },
    {
        "id":2,
        "description":"Test, tier 2",
        "status": "backlog",
        "parent":[1],
        "children":[3]
    },
    {
        "id":3,
        "description":"Test, tier 3",
        "status": "backlog",
        "parent":[2],
        "children":[4]
    },
    {
        "id":4,
        "description":"Test, tier 4",
        "status": "backlog",
        "parent":[3],
        "children":[]
    },
]

def test_add_task():
    modified_tasks = add_task(mock_data,"Test Task")
    assert len(modified_tasks) == 2
    assert modified_tasks[-1]['description'] == "Test Task"

def test_cannot_add_empty_description_task():
    with pytest.raises(InvalidTaskError):
        add_task(mock_data,"")
        
def test_cannot_add_null_task():
    with pytest.raises(AssertionError):
        add_task(mock_data,None)
    
def test_added_tasks_default_to_backlog():
    modified_tasks = add_task(mock_data, "Test Task")
    assert modified_tasks[-1]['status'] == "backlog"

def test_add_task_with_newline():
    with pytest.raises(InvalidTaskError):
        add_task(mock_data, "Task with new line \n")

def test_delete_task():
    task_id = mock_data[0]['id']
    modified_tasks = delete_task(mock_data, task_id)
    assert task_id not in [task['id'] for task in modified_tasks]

@pytest.mark.parametrize("delete,expected", [
    pytest.param(1, {2:([],[3]),3:([2],[4]),4:([3],[])}, id="delete top"),
    pytest.param(2, {1:([],[3]),3:([1],[4]),4:([3],[])}, id="delete mid"),
    pytest.param(4, {1:([],[2]),2:([1],[3]),3:([2],[])}, id="delete last"),
])
def test_delete_nested_task(delete, expected):
    newtasks = delete_task(copy.deepcopy(mock_data_test_children),delete)
    assert len(newtasks) == 3
    for task in newtasks:
        assert task['id'] is not delete
        assert task['parent'] == expected[task['id']][0] 
        assert task['children'] == expected[task['id']][1] 
    
def test_cannot_delete_missing_task():
    with pytest.raises(StopIteration):
        delete_task([],1)
    
@pytest.mark.parametrize("new, expected", 
    [
        pytest.param("in_progress", "in_progress", id="changes simple"),
        pytest.param("Done", "done", id="change is case insensitive"),
        pytest.param("in progress", "in_progress", id="deals with whitespace"),
    ]
)
def test_change_status(new, expected):
    modified_tasks = change_status(mock_data.copy(), 1, new) 
    assert modified_tasks[0]['status'] == expected


def test_cannot_change_status_missing_task():
    with pytest.raises(StopIteration):
        change_status(mock_data,2,"in_progress")

def test_get_task():
    task = get_task(mock_data,1)
    assert task["description"] == "Existing Task"

def test_get_task_as_object():
    task = get_task_object(mock_data,1)
    assert task.description == "Existing Task"
    assert type(task) is Task

def test_get_task_throws_missing_task():
    with pytest.raises(StopIteration):
        task = get_task(mock_data, 2)

def test_get_of_status():
    backlog = get_of_status(mock_data_extended, "backlog")
    assert type(backlog) is list
    assert len(backlog) == 2

def test_get_of_status_no_status():
    empty_list = get_of_status([{"id":1, "description":"Test Task"}], "backlog")
    assert len(empty_list) == 0
        
@pytest.mark.parametrize("values,length,expected",
    [
        pytest.param([{"status":"backlog"}], 1, ["backlog"], id="one item"),
        pytest.param([{"status":"backlog"}, {"status":"backlog"},{"status":"backlog"}], 1, ["backlog"], id="three items, same status"),
        pytest.param([{"status":"backlog"},{"status":"done"},{"status":"done"}], 2, ["backlog","done"], id="three items, two statuses"),
    ]
)
def test_get_status_list(values,length,expected):
    statuses = get_status_list(values)
    assert len(statuses) == length
    assert statuses == expected


def test_as_task_object():
    task_object = as_task_object({"id":1, "description": "Test Task","status":"backlog"})
    assert type(task_object) is Task

def test_as_task_object_no_id():
    with pytest.raises(KeyError):
        task_object = as_task_object({"description": "Test Task","status":"backlog"})

def test_as_task_object_no_description():
    with pytest.raises(KeyError):
        task_object = as_task_object({"id":1,"status":"backlog"})

def test_as_task_object_no_status():
    task_object = as_task_object({"id":1,"description": "Test Task"})
    assert type(task_object) is Task
    assert task_object.status == "backlog"
        
def test_task_as_string():
    task_object = Task(id=1, description="Test Task")
    assert task_object.as_string() == "- [1]: Test Task"

def test_change_priority_not_found():
    with pytest.raises(StopIteration):
        change_priority(mock_data,2,2)

def test_change_priority():
    newtasks = change_priority(mock_data_extended.copy(),1,3)
    assert newtasks[0]['priority'] == 3

@pytest.mark.parametrize("given, attr, expected", [
    pytest.param([{"a":3},{"a":2},{"a":1}],"a",[{"a":1},{"a":2},{"a":3}], id="sort attr present"),
    pytest.param([{"a":1}],"a",[{"a":1}], id="sort one attr present"),
    pytest.param([{"a":1}],"b",[{"a":1}], id="sort one attr missing"),
    pytest.param([{"a":3},{"a":2},{"a":1}],"b",[{"a":3},{"a":2},{"a":1}], id="sort many, attr missing"),
]
)
def test_sort_tasks(given, attr, expected):
    sorted = sort_tasks(given, attr)
    assert sorted == expected

def test_set_as_child():
    newtasks = set_as_child(mock_data_extended.copy(),1,3)
    print(newtasks)
    assert newtasks[2]['children'] == [mock_data_extended[0]["id"]]
    assert newtasks[0]['parent'] == [mock_data_extended[2]["id"]]

@pytest.mark.parametrize("tasks, child_id,parent_id", [
    pytest.param(mock_data_extended,4,1,id="child missing"),
    pytest.param(mock_data_extended,1,4,id="parent missing"),
    pytest.param([],1,1,id="tasks missing")
])
def test_set_as_child_missing_task(tasks, child_id,parent_id):
    with pytest.raises(StopIteration):
        data = tasks.copy()
        set_as_child(data,child_id, parent_id)
    assert data == tasks

@pytest.mark.parametrize("tasks, remove, expected", [
    pytest.param(copy.deepcopy(mock_data_test_children), 1, {1:([],[2]),2:([1],[3]),3:([2],[4]),4:([3],[])}, id="remove top"),
    pytest.param(copy.deepcopy(mock_data_test_children), 2, {1:([],[]),2:([],[3]),3:([2],[4]),4:([3],[])}, id="remove second"),
    pytest.param(copy.deepcopy(mock_data_test_children), 3, {1:([],[2]),2:([1],[]),3:([],[4]),4:([3],[])}, id="remove third"),
    pytest.param(copy.deepcopy(mock_data_test_children), 4, {1:([],[2]),2:([1],[3]),3:([2],[]),4:([],[])}, id="remove fourth"),
])
def test_unset_as_child(tasks, remove, expected):
    newtasks = unset_as_child(tasks, remove)
    for task in newtasks:
        assert task['parent'] == expected[task['id']][0]
        assert task['children'] == expected[task['id']][1]

@pytest.mark.parametrize("tasks, remove, expected", [
    pytest.param(copy.deepcopy(mock_data_test_children), 1, {1:([],[2]),2:([1],[3]),3:([2],[4]),4:([3],[])}, id="remove top"),
    pytest.param(copy.deepcopy(mock_data_test_children), 2, {1:([],[3]),2:([],[]),3:([1],[4]),4:([3],[])}, id="remove second"),
    pytest.param(copy.deepcopy(mock_data_test_children), 3, {1:([],[2]),2:([1],[4]),3:([],[]),4:([2],[])}, id="remove third"),
    pytest.param(copy.deepcopy(mock_data_test_children), 4, {1:([],[2]),2:([1],[3]),3:([2],[]),4:([],[])}, id="remove fourth"),
])
def test_unset_as_child_with_inherit(tasks, remove, expected):
    newtasks = unset_as_child(tasks, remove, inherit=True)
    for task in newtasks:
        print(f"Task {task['id']}:", task)
        assert task['parent'] == expected[task['id']][0]
        assert task['children'] == expected[task['id']][1]