## Celery

We use [Celery](http://www.celeryproject.org/) for the following general cases:

- Communicating with 3rd party services (sending emails, notifications, etc.)
- Offloading heavier computational tasks outside the HTTP cycle.
- Periodic tasks (using Celery beat)
