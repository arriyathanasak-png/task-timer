#!/usr/bin/env python3
"""A simple CLI tool to track task time."""

import json
import sys
import time
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("tasks.json")


def load_tasks():
    """Load tasks from JSON file."""
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)


def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def start_task(name):
    """Start tracking a new task."""
    tasks = load_tasks()
    if "current" in tasks:
        print(f"⚠️  Already tracking '{tasks['current']['name']}'. Stop it first.")
        return

    tasks["current"] = {"name": name, "start_time": time.time()}
    save_tasks(tasks)
    print(f"✓ Started tracking '{name}'")


def stop_task():
    """Stop tracking the current task."""
    tasks = load_tasks()
    if "current" not in tasks:
        print("⚠️  No task is currently being tracked.")
        return

    current = tasks.pop("current")
    elapsed = time.time() - current["start_time"]

    if "completed" not in tasks:
        tasks["completed"] = []

    tasks["completed"].append({
        "name": current["name"],
        "duration": elapsed,
        "timestamp": datetime.now().isoformat()
    })
    save_tasks(tasks)
    print(f"✓ Stopped tracking '{current['name']}' ({elapsed:.1f}s)")


def report():
    """Show a report of completed tasks."""
    tasks = load_tasks()
    completed = tasks.get("completed", [])

    if not completed:
        print("No tasks completed yet.")
        return

    print("\n📊 Task Report:")
    print("-" * 40)

    total_time = 0
    for task in completed:
        duration = task["duration"]
        total_time += duration
        print(f"  {task['name']}: {duration:.1f}s")

    print("-" * 40)
    print(f"Total time: {total_time:.1f}s\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: task_timer.py [start|stop|report]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            print("Usage: task_timer.py start <task_name>")
            sys.exit(1)
        start_task(sys.argv[2])
    elif command == "stop":
        stop_task()
    elif command == "report":
        report()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
