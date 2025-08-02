### Fetching objects

When our APIs receive an `object_id`, the question that arises is: **Where should we fetch that object?**

We have several options:

1. We can pass that object to a serializer, which has a [`PrimaryKeyRelatedField`](https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield) (or a [`SlugRelatedField`](https://www.django-rest-framework.org/api-guide/relations/#slugrelatedfield) for that matter)
1. We can do some kind of object fetching in the API & pass the object to a service or a selector.
1. We can pass the id to the service / selector and do the object fetching there.

What approach we take is a matter of project context & preference.

What we usually do is to fetch objects on the API level, using a special `get_object` util:

```python
def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
```

This is a very basic utility, that handles the exception and returns `None` instead.

Whatever you do, make sure to keep it consistent.