### Reading from `.env`

Having a local `.env` is a nice way of providing values for your settings.

And the good thing is, [`django-environ`](https://django-environ.readthedocs.io/en/latest/) provides you with a way to do that:

```python
# That's in the beginning of base.py

import os

from config.env import env, environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env.read_env(os.path.join(BASE_DIR, ".env"))
```

Now you can have a `.env` (but it's not required) file in your project root & place values for your settings there.

There are 2 things worth mentioning here:

1. Don't put `.env` in your source control, since this will leak credentials.
2. Rather put an `.env.example` with empty values for everything, so new developers can figure out what's being used.
