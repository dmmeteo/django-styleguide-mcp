### The basics

We try to treat Celery as if it's just another interface to our core logic - meaning - **don't put business logic there.**

Lets look at an example of a **service** that sends emails (example taken from [`Django-Styleguide-Example`](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/emails/tasks.py))

```python
from django.db import transaction
from django.core.mail import EmailMultiAlternatives

from styleguide_example.core.exceptions import ApplicationError
from styleguide_example.common.services import model_update
from styleguide_example.emails.models import Email


@transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email.status}")

    subject = email.subject
    from_email = "styleguide-example@hacksoft.io"
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={
            "status": Email.Status.SENT,
            "sent_at": timezone.now()
        }
    )
    return email
```

Email sending has business logic around it, **but we still want to trigger this particular service from a task.**

Our task looks like that:

```python
from celery import shared_task

from styleguide_example.emails.models import Email


@shared_task
def email_send(email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send
    email_send(email)
```

As you can see, **we treat the task as an API:**

1. Fetch the required data.
2. Call the appropriate service.

Now, imagine we have a different service, that triggers the email sending.

It may look like that:

```python
from django.db import transaction

# ... more imports here ...

from styleguide_example.emails.tasks import email_send as email_send_task


@transaction.atomic
def user_complete_onboarding(user: User) -> User:
    # ... some code here

    email = email_get_onboarding_template(user=user)

    transaction.on_commit(lambda: email_send_task.delay(email.id))

    return user
```

2 important things to point out here:

1. We are importing the task (which has the same name as the service), but we are giving it a `_task` suffix.
1. And when the transaction commits, we'll call the task.

**So, in general, the way we use Celery can be described as:**

1. Tasks call services.
2. We import the service in the function body of the task.
3. When we want to trigger a task, we import the task, at module level, giving the `_task` suffix.
4. We execute tasks, as a side effect, whenever our transaction commits.

This way of mixing tasks & services also **prevents circular imports**, which may occurr often enough when using Celery.
