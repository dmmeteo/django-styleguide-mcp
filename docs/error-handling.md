### Error handling

Sometimes, our service can fail and we might want to handle the error on the task level. For example - we might want to retry the task.

This error handling code needs to live in the task.

Lets expand the `email_send` task example from above, by adding error handling:

```python
from celery import shared_task
from celery.utils.log import get_task_logger

from styleguide_example.emails.models import Email


logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_failed

    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send

    try:
        email_send(email)
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
```

As you can see, we do a bunch of retries and if all of them fail, we handle this in the `on_failure` callback.

The callback follows the naming pattern of `_{task_name}_failure` and it calls the service layer, just like an ordinary task.