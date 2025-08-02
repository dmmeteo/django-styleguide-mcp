### Integrations

Since everything should be imported in `base.py`, but sometimes we don't want to configure a certain integration for local development, we derived the following approach:

- Integration-specific settings are placed in `config/settings/some_integration.py`
- There's always a boolean setting called `USE_SOME_INTEGRATION`, which reads from the environment & defaults to `False`.
- If the value is `True`, then proceed reading other settings & failing if things are not present in the environment.

For example, lets take a look at `config/settings/sentry.py`:

```python
from config.env import env

SENTRY_DSN = env('SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    # ... we proceed with sentry settings here ...
    # View the full file here - https://github.com/HackSoftware/Styleguide-Example/blob/master/config/settings/sentry.py
```
