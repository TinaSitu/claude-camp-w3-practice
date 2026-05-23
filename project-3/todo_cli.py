"""
todo_cli.py — 命令行 Todo 管理器

Usage:
    python todo_cli.py add "买牛奶"
    python todo_cli.py list
    python todo_cli.py done 1
    python todo_cli.py delete 1
    python todo_cli.py clear
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

TODOS_PATH = Path(__file__).parent / "todos.json"


def load_todos(path: Path = TODOS_PATH) -> list:
    """从 JSON 文件加载任务列表。若文件不存在则返回空列表。"""
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos: list, path: Path = TODOS_PATH) -> None:
    """将任务列表保存到 JSON 文件。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(title: str, path: Path = TODOS_PATH) -> dict:
    """新增一条任务。

    Raises:
        ValueError: 标题为空时抛出。
    """
    if not title.strip():
        raise ValueError("任务标题不能为空")
    todos = load_todos(path)
    next_id = max((t["id"] for t in todos), default=0) + 1
    todo = {"id": next_id, "title": title.strip(),
            "done": False, "created_at": datetime.now().isoformat(timespec="seconds")}
    todos.append(todo)
    save_todos(todos, path)
    return todo


def list_todos(path: Path = TODOS_PATH) -> list:
    """返回所有任务列表。"""
    return load_todos(path)


def mark_done(todo_id: int, path: Path = TODOS_PATH) -> dict:
    """将指定 ID 的任务标记为已完成。

    Raises:
        ValueError: ID 不存在时抛出。
    """
    todos = load_todos(path)
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            save_todos(todos, path)
            return todo
    raise ValueError(f"找不到 ID 为 {todo_id} 的任务")


def delete_todo(todo_id: int, path: Path = TODOS_PATH) -> dict:
    """删除指定 ID 的任务。

    Raises:
        ValueError: ID 不存在时抛出。
    """
    todos = load_todos(path)
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos, path)
            return removed
    raise ValueError(f"找不到 ID 为 {todo_id} 的任务")


def clear_todos(path: Path = TODOS_PATH) -> int:
    """清空所有任务，返回被删除的数量。"""
    todos = load_todos(path)
    count = len(todos)
    save_todos([], path)
    return count


def print_todos(todos: list) -> None:
    """格式化打印任务列表。"""
    if not todos:
        print("📭 暂无任务")
        return
    print(f"\n📋 共 {len(todos)} 条任务：")
    for t in todos:
        status = "✅" if t["done"] else "⬜"
        print(f"   {status} [{t['id']}] {t['title']}  ({t['created_at']})")
    print()


def main():
    parser = argparse.ArgumentParser(description="命令行 Todo 管理器")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="新增任务")
    add_p.add_argument("title", help="任务标题")
    sub.add_parser("list", help="列出所有任务")
    done_p = sub.add_parser("done", help="标记任务完成")
    done_p.add_argument("id", type=int, help="任务 ID")
    del_p = sub.add_parser("delete", help="删除任务")
    del_p.add_argument("id", type=int, help="任务 ID")
    sub.add_parser("clear", help="清空所有任务")

    args = parser.parse_args()

    if args.command == "add":
        todo = add_todo(args.title)
        print(f"✅ 已添加：[{todo['id']}] {todo['title']}")
    elif args.command == "list":
        print_todos(list_todos())
    elif args.command == "done":
        todo = mark_done(args.id)
        print(f"✅ 已完成：[{todo['id']}] {todo['title']}")
    elif args.command == "delete":
        todo = delete_todo(args.id)
        print(f"🗑️  已删除：[{todo['id']}] {todo['title']}")
    elif args.command == "clear":
        count = clear_todos()
        print(f"🗑️  已清空 {count} 条任务")


if __name__ == "__main__":
    main()
