### Nested serializers

In case you need to use a nested serializer, you can do the following thing:

```python
class Serializer(serializers.Serializer):
    weeks = inline_serializer(many=True, fields={
        'id': serializers.IntegerField(),
        'number': serializers.IntegerField(),
    })
```

The implementation of `inline_serializer` can be found [here](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/api/utils.py), in the [Styleguide-Example](https://github.com/HackSoftware/Styleguide-Example) repo.