import os
import json
import signal
import threading


class Database:
    def __init__(self, path="history.json"):
        self.tasks = dict()
        self.task_count = 0
        self.path = path
        self.transient = ["dataset_loaded", "model_loaded"]
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)
        self._lock = threading.Lock()

    def remove(self, task):
        with self._lock:
            task_id = str(task["id"])
            del self.tasks[task_id]

    def register(self, task):
        with self._lock:
            self.task_count += 1
            task_id = str(self.task_count)
            task["id"] = task_id
            self.tasks[task_id] = task
            return task_id

    def get(self, task_id):
        with self._lock:
            return self.tasks.get(str(task_id), None)

    def replace(self, task, task_id=None):
        with self._lock:
            task_id = str(task.get("id", task_id))
            task["id"] = task_id
            self.tasks[task_id] = task
            return task_id

    def load_from_disk(self):
        with self._lock:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.tasks = data.get("tasks", dict())
                    self.task_count = data.get("task_count", 0)
            else:
                self.tasks = dict()
                self.task_count = 0

    def save_to_disk(self):
        with self._lock:
            for task in self.tasks.values():
                for field in self.transient:
                    task[field] = None
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "tasks": self.tasks,
                        "task_count": self.task_count,
                    },
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

    def handle_exit(self, signum, frame):
        if self.transient:
            print(f"Exiting and saving data")
            self.save_to_disk()
            self.transient = False
            exit(0)

    def __enter__(self):
        self.load_from_disk()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.transient:
            print(f"Exiting and saving data")
            self.save_to_disk()
            self.transient = False
        return False  # Ensure that any exception is propagated if it occurs.
