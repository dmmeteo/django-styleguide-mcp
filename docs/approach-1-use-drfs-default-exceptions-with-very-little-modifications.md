### Approach 1 - Use DRF's default exceptions, with very little modifications.

DRF's error handling is good. It'd be great, if the end result was always consistent. Those are the little modifications that we are going to do.

We want to end up with errors, always looking like that:

```json
{
  "detail": "Some error"
}
```

or

```json
{
  "detail": ["Some error", "Another error"]
}
```

or

```json
{
  "detail": { "key": "... some arbitrary nested structure ..." }
}
```

Basically, make sure we always have a dictionary with a `detail` key.

Additonally, we want to handle Django's `ValidationError` as well.

In order to achieve that, this is how our custom exception handler is going to look like:

```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error


def drf_default_with_modifications_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    return response
```

We kind-of replicate the original exception handler, so we can deal with an `APIException` after that (looking for `detail`).

Now, lets run a set of tests:

Code:

```python
def some_service():
    raise DjangoValidationError("Some error message")
```

Response:

```json
{
  "detail": {
    "non_field_errors": ["Some error message"]
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
  "detail": "You do not have permission to perform this action."
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
  "detail": "Not found."
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
  "detail": ["Some error message"]
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
  "detail": {
    "error": "Some error message"
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
  "detail": {
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
  "detail": "Request was throttled."
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
  "detail": {
    "password": ["This field cannot be blank."],
    "email": ["This field cannot be blank."]
  }
}
```
