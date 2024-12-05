from unittest.mock import  patch, Mock
import pytest
import json
from src.solop.file_utils import *

mock_data = {
"project":"Name",
"tasks":{
    "id":1,
    "description": "Existing Task",
    "status": "backlog"
}
}

mock_tasks = {
    "id":2,
    "description":"New Task",
    "status": "in_progress"
}

def mock_json_data():
    return json.dumps(mock_data)

def test_load_tasks():
    with patch("src.solop.file_utils.load_file", return_value=mock_data.copy()):
        tasks = load_tasks()
        assert tasks == mock_data["tasks"]

def test_save_tasks():
    with patch("src.solop.file_utils.load_file", return_value=mock_data.copy()), \
        patch("src.solop.file_utils.save_file") as mock_save_file:
        save_tasks(mock_tasks)
        expected = {
            "project":"Name",
            "tasks": mock_tasks
        }
        mock_save_file.assert_called_once_with(expected)
        mock_save_file.reset_mock()

def test_change_meta_name():
    with patch("src.solop.file_utils.load_file", return_value=mock_data.copy()), \
        patch("src.solop.file_utils.save_file") as mock_save_file:
        change_meta('project','New Name')
        args, kwargs = mock_save_file.call_args
        assert args[0]['project'] == "New Name"
        mock_save_file.reset_mock()

def test_change_meta_not_existing():
    with patch("src.solop.file_utils.load_file", return_value=mock_data), \
        pytest.raises(InvalidAttrError):
        change_meta('foo','bar')

def test_runs_validations():
    mock_validation1 = Mock(return_value=["Called 1"])
    mock_validation2 = Mock()
    validations = [mock_validation1, mock_validation2]
    validate_tasks([], validations )
    mock_validation1.assert_called_once()
    mock_validation2.assert_called_once_with(["Called 1"])
    
@pytest.mark.parametrize("tasks, expected",[
    pytest.param([],[], id="no tasks"),
    pytest.param(
        [
            {"id":1, "description":"Task 1"},
            {"id":2, "description":"Task 2"},
            {"id":3, "description":"Task 3"},
        ],[
            {"id":1, "description":"Task 1"},
            {"id":2, "description":"Task 2"},
            {"id":3, "description":"Task 3"},
        ], id="no changes needed"
    ),
    pytest.param(
        [
            {"id":1, "description":"Task 1"},
            {"id":1, "description":"Task 2"},
            {"id":2, "description":"Task 3"},
        ],[
            {"id":1, "description":"Task 1"},
            {"id":3, "description":"Task 2"},
            {"id":2, "description":"Task 3"},
        ], id="simple change needed"
    ),
    pytest.param(
        [
            {"id":3, "description":"Task 1"},
            {"id":3, "description":"Task 2"},
            {"id":2, "description":"Task 3"},
        ],[
            {"id":3, "description":"Task 1"},
            {"id":1, "description":"Task 2"},
            {"id":2, "description":"Task 3"},
        ], id="adds lower id if available"
    ),
    pytest.param(
        [
            {"id":1, "description":"Task 1"},
            {"id":1, "description":"Task 2"},
            {"id":1, "description":"Task 3"},
        ],[
            {"id":1, "description":"Task 1"},
            {"id":2, "description":"Task 2"},
            {"id":3, "description":"Task 3"},
        ], id="several changes needed"
    ),
])
def test_validates_ids(tasks, expected):
    newtasks = validate_duplicate_ids(tasks)
    assert newtasks == expected