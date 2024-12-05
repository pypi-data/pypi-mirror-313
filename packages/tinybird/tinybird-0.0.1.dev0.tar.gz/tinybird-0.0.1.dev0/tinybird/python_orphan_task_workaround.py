import asyncio

# It's important to keep a reference to the task
# If not, the GC will destroy it eventually,
# causing "Task was destroyed but it is pending!" errors
# See https://bugs.python.org/issue21163

tasks = []
_counter = 0


def workaround_orphan_task(task: asyncio.Task):
    """
    Use this method with care. Take into account that neither the method
    nor the tasks are thread-safe. So, this means that this method can
    only be called from the same thread *all tasks* are created.
    """
    global tasks, _counter
    tasks.append(task)
    _counter += 1
    if (_counter % 20) != 0:
        return
    # Remove "done" tasks to avoid leaking memory
    tasks = [t for t in tasks if not t.done()]
    # Add the new task
