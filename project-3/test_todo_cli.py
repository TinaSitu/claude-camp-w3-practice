"""
test_todo_cli.py — todo_cli 单元测试

运行方式：
    pytest project-3/test_todo_cli.py -v
"""

import pytest
from pathlib import Path
from todo_cli import (
    load_todos, save_todos, add_todo,
    list_todos, mark_done, delete_todo, clear_todos,
)


@pytest.fixture
def tmp_path_todos(tmp_path):
    return tmp_path / "todos.json"


def test_load_todos_missing_returns_empty(tmp_path_todos):
    assert load_todos(tmp_path_todos) == []

def test_save_and_load(tmp_path_todos):
    save_todos([{"id": 1, "title": "test", "done": False}], tmp_path_todos)
    todos = load_todos(tmp_path_todos)
    assert len(todos) == 1
    assert todos[0]["title"] == "test"

def test_add_todo_returns_dict(tmp_path_todos):
    todo = add_todo("买牛奶", tmp_path_todos)
    assert todo["title"] == "买牛奶"
    assert todo["done"] is False
    assert todo["id"] == 1

def test_add_todo_increments_id(tmp_path_todos):
    add_todo("任务A", tmp_path_todos)
    todo2 = add_todo("任务B", tmp_path_todos)
    assert todo2["id"] == 2

def test_add_todo_empty_title(tmp_path_todos):
    with pytest.raises(ValueError):
        add_todo("   ", tmp_path_todos)

def test_add_todo_persists(tmp_path_todos):
    add_todo("持久化测试", tmp_path_todos)
    todos = load_todos(tmp_path_todos)
    assert len(todos) == 1

def test_mark_done(tmp_path_todos):
    add_todo("完成我", tmp_path_todos)
    todo = mark_done(1, tmp_path_todos)
    assert todo["done"] is True

def test_mark_done_invalid_id(tmp_path_todos):
    with pytest.raises(ValueError):
        mark_done(999, tmp_path_todos)

def test_delete_todo(tmp_path_todos):
    add_todo("删除我", tmp_path_todos)
    delete_todo(1, tmp_path_todos)
    assert load_todos(tmp_path_todos) == []

def test_delete_todo_invalid_id(tmp_path_todos):
    with pytest.raises(ValueError):
        delete_todo(999, tmp_path_todos)

def test_clear_todos(tmp_path_todos):
    add_todo("A", tmp_path_todos)
    add_todo("B", tmp_path_todos)
    count = clear_todos(tmp_path_todos)
    assert count == 2
    assert load_todos(tmp_path_todos) == []

def test_clear_todos_empty(tmp_path_todos):
    count = clear_todos(tmp_path_todos)
    assert count == 0
