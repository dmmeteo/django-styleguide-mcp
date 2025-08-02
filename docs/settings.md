## Settings

When it comes to Django settings, we tend to follow the folder structure from [`cookiecutter-django`](https://github.com/cookiecutter/cookiecutter-django), with few adjustments:

- We separate Django specific settings from other settings.
- Everything should be included in `base.py`.
  - There should be nothing that's only included in `production.py`.
  - Things that need to only work in production are controlled via environment variables.

Here's the folder structure of our [`Styleguide-Example`](https://github.com/HackSoftware/Styleguide-Example) project:

```
config
├── __init__.py
├── django
│   ├── __init__.py
│   ├── base.py
│   ├── local.py
│   ├── production.py
│   └── test.py
├── settings
│   ├── __init__.py
│   ├── celery.py
│   ├── cors.py
│   ├── sentry.py
│   └── sessions.py
├── urls.py
├── env.py
└── wsgi.py
├── asgi.py
```

In `config/django`, we put everything that's Django related:

- `base.py` contains most of the settings & imports everything else from `config/settings`
- `production.py` imports from `base.py` and then overwrites some specific settings for production.
- `test.py` imports from `base.py` and then overwrites some specific settings for running tests.
  - This should be used as the settings module in `pytest.ini`.
- `local.py` imports from `base.py` and can overwrite some specific settings for local development.
  - If you want to use that, point to `local` in `manage.py`. Otherwise stick with `base.py`

In `config/settings`, we put everything else:

- Celery configuration.
- 3rd party configurations.
- etc.

This gives you a nice separation of modules.

Additionally, we usually have `config/env.py` with the following code:

```python
import environ

env = environ.Env()
```

And then, whenever we need to read something from the environment, we import like that:

```python
from config.env import env
```

Usually, at the end of the `base.py` module, we import everything from `config/settings`:

```python
from config.settings.cors import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.sentry import *  # noqa
```
