# My Advanced Task Runner

This package provides an advanced way to execute a function concurrently using either a thread pool or a process pool. It supports retries for failed tasks and collects task results.

## Installation

```bash
  pip install xh-advanced-task-runner
```

## Example
    
```python
from task_runner.task_runner import run_task_in_pool, fetch_url
    
if __name__ == '__main__':
    # Run 5 tasks in parallel using thread pool
    results = run_task_in_pool(fetch_url, 5, url="https://example.com", iterations=10)
    print(results)
```
    