import pytest
from unittest.mock import patch
import copy

from src.solop.task_utils import (
    Task,
)

from src.solop.md_writer import (
    MDWriter,
    Section
)

def new_as_string():
    return "- [1]: Test Task"


mock_list = [
    {
        "id":1,
        "description":"Task 1",
        "status":"backlog"
    },
    {
        "id":2,
        "description":"Task 2",
        "status":"backlog"
    }
    ]

mock_tree = [
    {"id":1, "description":"Task 1", "priority":1, "parent":[], "children":[]},
    {"id":2, "description":"Task 2", "priority":2, "parent":[], "children":[3,5]},
    {"id":3, "description":"Task 3", "priority":5, "parent":[2], "children": []},
    {"id":4, "description":"Task 4", "priority":3, "parent":[], "children": []},
    {"id":5, "description":"Task 5", "priority":2, "parent":[2], "children": [6,3]},
    {"id":6, "description":"Task 6", "priority":1, "parent":[5], "children": []},
]

mock_tree_orphaned = copy.deepcopy(mock_tree)
mock_tree_orphaned.append({
    "id":7,
    "description":"Orphaned Task",
    "priority":1,
    "parent":[8],
    "children":[]
})

mock_layout = {
    "1":[],
    "2":[{
        "3":[],
        "5":[{
            "6":[],
            "3":[]
        }]
    }],
    "4":[]
}

mock_lines = [
    "## TEST:\n",
    "- [1]: Task 1",
    "- [2]: Task 2",
    "\t- [5]: Task 5",
    "\t\t- [6]: Task 6",
    "\t\t- [3]: Task 3",
    "\t- [3]: Task 3",
    "- [4]: Task 4",
]

@pytest.mark.parametrize("id, expected", [
    pytest.param(1, [], id="no children"),
    pytest.param(5,[{"6":[]}], id="single child"),
    pytest.param(2,[{"3":[],"5":[{"6":[], "3":[]}]}], id="multi-tiered"),
    pytest.param(3,[], id="multi-parented item")
])
def test_get_children(id, expected):
    section = Section("test", mock_tree)
    section.get_children(id)

def test_get_children_no_params():
    section = Section("test", [{"id":1},{"id":2}])
    children = section.get_children(1)
    assert children == []  

def test_get_layout():
    section = Section("test", mock_tree)
    layout = section.get_layout(mock_tree.copy())
    assert layout == mock_layout

@pytest.mark.parametrize("tier, expected", [
    pytest.param([1,2,6],[1,6,2], id="sort 1"),
    pytest.param([3,4,5],[5,4,3], id="sort 2"),
    pytest.param([5],[5], id="one element"),
    pytest.param([],[], id="no elements"),
])
def test_get_tier_order(tier, expected):
    section = Section("test", mock_tree)
    order = section.get_tier_priority_order(tier)
    assert order == expected

def test_render_section():
    section = Section("test", mock_tree)
    lines = section.render_section()
    assert lines == mock_lines

def test_render_orphaned_tasks():
    print(mock_tree_orphaned)
    section = Section("test", mock_tree_orphaned)
    lines = section.render_section()
    print(lines)
    assert "- [7]: Orphaned Task" in lines