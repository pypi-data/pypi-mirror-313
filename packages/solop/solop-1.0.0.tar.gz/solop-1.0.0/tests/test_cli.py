from unittest.mock import patch, Mock, call 
import pytest
from src.solop.cli import *



@pytest.mark.parametrize("args, func", [
    pytest.param({"xmake":True, "add":"desc"}, "add", id="test add"),
    pytest.param({"xmake":True, "delete":1}, "delete", id="test delete"),
    pytest.param({"xmake":True, "rename":"desc"}, "rename", id="test rename"),
    pytest.param({"xmake":True, "status":1}, "status", id="test status"),
    pytest.param({"xmake":True, "nest":1}, "nest", id="test nest"),
    pytest.param({"xmake":True, "xchild":1}, "xchild", id="test xchild"),
])
def test_add_executed(args, func):
    executer = CommandExecuter()
    mocked_call = Mock()
    executer.actions[func] = mocked_call
    executer.execute_commands(args)
    mocked_call.assert_called()

@patch("src.solop.cli.change_meta")
def test_rename(patched_change):
    executer = CommandExecuter()
    executer.rename({"rename":"New Title"})
    patched_change.assert_called_once_with('project', 'New Title')

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.add_task")
def test_add(patched_action, patched_change):
    executer = CommandExecuter()
    executer.add({"add":"New Task"})
    patched_change.assert_called_once_with(patched_action,'New Task')

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.delete_task")
@patch("src.solop.cli.CommandExecuter.get_confirmation", return_value="Y")
def test_delete(input, patched_action, patched_change):
    executer = CommandExecuter()
    executer.delete({"delete":[1]})
    patched_change.assert_called_once_with(patched_action,1)

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.delete_task")
@patch("src.solop.cli.CommandExecuter.get_confirmation", return_value="Y")
def test_delete_many(input, patched_action, patched_change):
    executer = CommandExecuter()
    executer.delete({"delete":[1,2,3]})
    calls = [
        call(patched_action,1),
        call(patched_action,2),
        call(patched_action,3),
    ]
    patched_change.assert_has_calls(calls)

@patch("src.solop.cli.change_tasks")
def test_delete_not_called(patched_change):
    executer = CommandExecuter()
    executer.delete({"delete":["New Status","Another Status"]})
    patched_change.assert_not_called()

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.change_status")
def test_status(patched_action, patched_change):
    executer = CommandExecuter()
    executer.status({"status":["New Status",1]})
    patched_change.assert_called_once_with(patched_action,1,'New Status')

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.change_status")
def test_status_many(patched_action, patched_change):
    executer = CommandExecuter()
    executer.status({"status":["New Status",1,2,3]})
    calls = [
        call(patched_action,1, "New Status"),
        call(patched_action,2, "New Status"),
        call(patched_action,3, "New Status"),
    ]
    patched_change.assert_has_calls(calls)

@patch("src.solop.cli.change_tasks")
def test_status_not_called(patched_change):
    executer = CommandExecuter()
    executer.status({"status":["New Status","Another Status"]})
    patched_change.assert_not_called()


@pytest.mark.parametrize("given, expected",[
    ([1,2,3],[1,2,3]),
    ([],[]),
    (["1",2,3],[1,2,3]),
    (["1","2","3"],[1,2,3])
])
def test_as_ints(given, expected):
    executer = CommandExecuter()
    ints = executer.as_ints(given)
    assert ints == expected

def test_as_ints_error():
    executer = CommandExecuter()
    with pytest.raises(ValueError):
        ints = executer.as_ints(["One"])

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.change_priority")
def test_priority(patched_action, patched_change):
    executer = CommandExecuter()
    executer.priority({"priority":[2,1]})
    patched_change.assert_called_once_with(patched_action,1,2)

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.change_priority")
def test_priority_many(patched_action, patched_change):
    executer = CommandExecuter()
    calls = [
        call(patched_action,1, 2),
        call(patched_action,2, 2),
        call(patched_action,3, 2),
    ]
    executer.priority({"priority":[2,1,2,3]})
    patched_change.assert_has_calls(calls)

@patch("src.solop.cli.change_tasks")
def test_priority_not_called(patched_change):
    executer = CommandExecuter()
    executer.priority({"priority":["New Status","Another Status"]})
    patched_change.assert_not_called()

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.set_as_child")
def test_nest(patched_action, patched_change):
    executer = CommandExecuter()
    executer.child({"nest":[2,1]})
    patched_change.assert_called_once_with(patched_action,2,1)

@patch("src.solop.cli.change_tasks")
def test_nest_not_called(patched_change):
    executer = CommandExecuter()
    executer.child({"nest":["New Status","Another Status"]})
    patched_change.assert_not_called()

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.unset_as_child")
def test_xchild_inherit(patched_action, patched_change):
    executer = CommandExecuter()
    executer.xchild({"xchild":[2], "inherit":True})
    patched_change.assert_called_once_with(patched_action,2,True)

@patch("src.solop.cli.change_tasks")
@patch("src.solop.cli.unset_as_child")
def test_xchild_not_inherit(patched_action, patched_change):
    executer = CommandExecuter()
    executer.xchild({"xchild":[2], "inherit":False})
    patched_change.assert_called_once_with(patched_action,2,False)

@patch("src.solop.cli.change_tasks")
def test_xchild_not_called(patched_change):
    executer = CommandExecuter()
    executer.xchild({"xchild":["New Status","Another Status"],"inherit":True})
    patched_change.assert_not_called()
