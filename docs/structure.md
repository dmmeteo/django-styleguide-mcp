### Structure

Tasks are located in `tasks.py` modules in different apps.

We follow the same rules as with everything else (APIs, services, selectors): **if the tasks for a given app grow too big, split them by domain.**

Meaning, you can end up with `tasks/domain_a.py` and `tasks/domain_b.py`. All you need to do is import them in `tasks/__init__.py` for Celery to autodiscover them.

The general rule of thumb is - split your tasks in a way that'll make sense to you.
