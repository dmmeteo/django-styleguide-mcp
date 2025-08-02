### Class-based vs. Function-based

> This is mostly up to personal preferences, since you can achieve the same results with both approaches.

We have the following preferences:

1. Pick class-based APIS / views by default.
1. If everyone else preferes & are comfortable with functions, use function-based APIs / views.

For us, the added benefits of using classes for APIs / views are the following:

1. You can inherit a `BaseApi` or add mixins.
   - If you are using function-based APIs / views, you'll need to do the same, but with decorators.
2. The class creates a namespace where you can nest things (attributes, methods, etc.).
   - Additional API configuration can be done via class attributes.
   - In the case of function-based APIs / views, you need to stack decorators.

Here's an example with a class, inheriting a `BaseApi`:

```python
class SomeApi(BaseApi):
    def get(self, request):
        data = something()

        return Response(data)
```

Here's an example with a function, using a `base_api` decorator (implementation is based on your needs)

```python
@base_api(["GET"])
def some_api(request):
    data = something()
    return Response(data)
```