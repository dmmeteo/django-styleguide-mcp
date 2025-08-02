### Periodic Tasks

Managing periodic tasks is quite important, especially when you have tens or hundreds of them.

We use [Celery Beat](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) + `django_celery_beat.schedulers:DatabaseScheduler` + [`django-celery-beat`](https://github.com/celery/django-celery-beat) for our periodic tasks.

The extra thing that we do is to have a management command, called [`setup_periodic_tasks`](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/tasks/management/commands/setup_periodic_tasks.py), which holds the definition of all periodic tasks within the system. This command is located in the `tasks` app, discussed above.

Here's how `project.tasks.management.commands.setup_periodic_tasks.py` looks like:

```python
from django.core.management.base import BaseCommand
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from project.app.tasks import some_periodic_task


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {some_periodic_task.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Deleting all periodic tasks and schedules...\n')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                'task': some_periodic_task
                'name': 'Do some peridoic stuff',
                # https://crontab.guru/#15_*_*_*_*
                'cron': {
                    'minute': '15',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **periodic_task['cron']
            )

            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled']
            )
```

Few key things:

- We use this task as part of a deploy procedure.
- We always put a link to [`crontab.guru`](https://crontab.guru) to explain the cron. Otherwise it's unreadable.
- Everything is in one place.
- ⚠️ We use, almost exclusively, a cron schedule. **If you plan on using the other schedule objects, provided by Celery, please read thru their documentation** & the important notes - <https://django-celery-beat.readthedocs.io/en/latest/#example-creating-interval-based-periodic-task> - about pointing to the same schedule object. ⚠️