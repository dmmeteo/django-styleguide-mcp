### How exception handling works (in the context of DRF)

DRF has an excellent guide on how exceptions are being handled, so make sure to read it first - <https://www.django-rest-framework.org/api-guide/exceptions/>

Additionally, here's a neat diagram with an overview of the process:

![Exception handler (1)](https://user-images.githubusercontent.com/387867/142426205-2c0356e6-ce20-425e-a811-072c3334edb0.png)

Basically, if the exception handler cannot handle the given exception & returns `None`, this will result in an unhandled exception & a `500 Server Error`. This is often good, because you won't be silencing errors, that you need to pay attention to.

**Now, there are some quirks, that we need to pay attention to.**

#### DRF's `ValidationError`

For example, if we simply raise a `rest_framework.exceptions.ValidationError` like that:

```python
from rest_framework import exceptions


def some_service():
    raise ValidationError("Error message here.")
```

The response payload is going to look like this:

```json
["Some message"]
```

This looks strange, because if we do it like this:

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.ValidationError({"error": "Some message"})
```

The response payload is going to look like this:

```json
{
  "error": "Some message"
}
```

That's basically what we passed as the `detail` of the `ValidationError`. But it's a different data structure from the initial array.

Now, if we decide to raise another of the DRF's built-in exceptions:

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.NotFound()
```

The response payload is going to look like this:

```json
{
  "detail": "Not found."
}
```

That's entirely different from what we saw as behavior from the `ValidationError` and this might cause problems.

So far, the default DRF behavior can get us:

- An array.
- A dictionary.
- A specific `{"detail": "something"}` result.

**So if we need to use the default DRF behavior, we need to take care of this inconsistency.**

#### Django's `ValidationError`

Now, DRF's default exception handling is not playing nice with Django's `ValidationError`.

This piece of code:

```python
from django.core.exceptions import ValidationError as DjangoValidationError


def some_service():
    raise DjangoValidationError("Some error message")
```

Will result in an unhandled exception, causing `500 Server Error`.

This will also happen if this `ValidationError` comes from model validation, for example:

```python
def some_service():
    user = BaseUser()
    user.full_clean()  # Throws ValidationError
    user.save()
```

This will also result in `500 Server Error`.

If we want to start handling this, as if it was `rest_framework.exceptions.ValidationError`, we need to roll-out our own [custom exception handler](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling):

```python
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework.serializers import as_serializer_error
from rest_framework import exceptions


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    return response
```

This is basically the default implementation, with the addition of this piece of code:

```python
if isinstance(exc, DjangoValidationError):
    exc = exceptions.ValidationError(as_serializer_error(exc))
```

Since we need to map between `django.core.exceptions.ValidationError` and `rest_framework.exceptions.ValidationError`, we are using DRF's `as_serializer_error`, which is used internally in the serializers, just for that.

With that, we can now have Django's `ValidationError` playing nice with DRF's exception handler.