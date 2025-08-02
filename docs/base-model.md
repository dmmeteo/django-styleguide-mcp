### Base model

It's a good idea to define a `BaseModel`, that you can inherit.

Usually, fields like `created_at` and `updated_at` are perfect candidates to go into a `BaseModel`.

Here's an example `BaseModel`:

```python
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

Then, whenever you need a new model, just inherit `BaseModel`:

```python
class SomeModel(BaseModel):
    pass
```