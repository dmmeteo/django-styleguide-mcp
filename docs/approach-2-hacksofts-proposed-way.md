### Approach 2 - HackSoft's proposed way

We are going to propose an approach, that can be easily extended into something that works well for you.

**Here are the key ideas:**

1. **Your application will have its own hierarchy of exceptions**, that are going to be thrown by the business logic.
1. Lets say, for simplicity, that we are going to have only 1 error - `ApplicationError`.
   - This is going to be defined in a special `core` app, within `exceptions` module. Basically, having `project.core.exceptions.ApplicationError`.
1. We want to let DRF handle everything else, by default.
1. `ValidationError` is now special and it's going to be handled differently.
   - `ValidationError` should only come from either serializer or a model validation.

---

**We are going to define the following structure for our errors:**

```json
{
  "message": "The error message here",
  "extra": {}
}
```

The `extra` key can hold arbitrary data, for the purposes of passing information to the frontend.

For example, whenever we have a `ValidationError` (usually coming from a Serializer or a Model), we are going to present the error like that:

```json
{
  "message": "Validation error.",
  "extra": {
    "fields": {
      "password": ["This field cannot be blank."],
      "email": ["This field cannot be blank."]
    }
  }
}
```

This can be communicated with the frontend, so they can look for `extra.fields`, to present those specific errors to the user.

In order to achieve that, the custom exception handler is going to look like this:

```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response

from styleguide_example.core.exceptions import ApplicationError


def hacksoft_proposed_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=400)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
```

Take a look at that code & try to understand what's going on. **The strategy is - reuse as much as possible from DRF & then adjust.**

Now, we are going to have the following behavior:

Code:

```python
from styleguide_example.core.exceptions import ApplicationError


def trigger_application_error():
    raise ApplicationError(message="Something is not correct", extra={"type": "RANDOM"})
```

Response:

```json
{
  "message": "Something is not correct",
  "extra": {
    "type": "RANDOM"
  }
}
```

---

Code:

```python
def some_service():
    raise DjangoValidationError("Some error message")
```

Response:

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "non_field_errors": ["Some error message"]
    }
  }
}
```

---

Code:

```python
from django.core.exceptions import PermissionDenied

def some_service():
    raise PermissionDenied()
```

Response:

```json
{
  "message": "You do not have permission to perform this action.",
  "extra": {}
}
```

---

Code:

```python
from django.http import Http404

def some_service():
    raise Http404()
```

Response:

```json
{
  "message": "Not found.",
  "extra": {}
}
```

---

Code:

```python
def some_service():
    raise RestValidationError("Some error message")
```

Response:

```json
{
  "message": "Validation error",
  "extra": {
    "fields": ["Some error message"]
  }
}
```

---

Code:

```python
def some_service():
    raise RestValidationError(detail={"error": "Some error message"})
```

Response:

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "error": "Some error message"
    }
  }
}
```

---

Code:

```python
class NestedSerializer(serializers.Serializer):
    bar = serializers.CharField()


class PlainSerializer(serializers.Serializer):
    foo = serializers.CharField()
    email = serializers.EmailField(min_length=200)

    nested = NestedSerializer()


def some_service():
    serializer = PlainSerializer(data={
        "email": "foo",
        "nested": {}
    })
    serializer.is_valid(raise_exception=True)

```

Response:

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "foo": ["This field is required."],
      "email": [
        "Ensure this field has at least 200 characters.",
        "Enter a valid email address."
      ],
      "nested": {
        "bar": ["This field is required."]
      }
    }
  }
}
```

---

Code:

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.Throttled()
```

Response:

```json
{
  "message": "Request was throttled.",
  "extra": {}
}
```

---

Code:

```python
def some_service():
    user = BaseUser()
    user.full_clean()
```

Response:

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "password": ["This field cannot be blank."],
      "email": ["This field cannot be blank."]
    }
  }
}
```

---

Now, this can be extended & made to better suit your needs:

1. You can have `ApplicationValidationError` and `ApplicationPermissionError`, as an additional hierarchy.
1. You can reimplement DRF's default exception handler, instead of reusing it (copy-paste it & adjust to your needs).

**The general idea is - figure out what kind of error handling you need and then implement it accordingly.**
