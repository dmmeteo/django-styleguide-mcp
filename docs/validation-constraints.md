### Validation - constraints

As proposed in [this issue](https://github.com/HackSoftware/Django-Styleguide/issues/22), if you can do validation using [Django's constraints](https://docs.djangoproject.com/en/dev/ref/models/constraints/), then you should aim for that.

Less code to write, less code to maintain, the database will take care of the data even if it's being inserted from a different place.

Lets look at an example!

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```

Now, if we try to create new object via `course.save()` or via `Course.objects.create(...)`, we are going to get an `IntegrityError`, rather than a `ValidationError`.

This can actually be a downside (_this is not the case, starting from Django 4.1. Check the extra section below._) to the approach, because now, we have to deal with the `IntegrityError`, which does not always have the best error message.

> 👀 ⚠️ 👀 Since Django 4.1, calling `.full_clean` will also check model constraints!
>
> This actually removes the downside, mentioned above, since you'll get a nice `ValidationError`, if your model constraints fail the check (if you go thru `Model.objects.create(...)` the downside still holds)
>
> More on this, here - <https://docs.djangoproject.com/en/4.1/ref/models/instances/#validating-objects>
>
> For an example test case, check the Styleguide-Example repo - <https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/tests/models/test_random_model.py#L12>

The Django's documentation on constraints is quite lean, so you can check the following articles by Adam Johnson, for examples of how to use them:

1. [Using Django Check Constraints to Ensure Only One Field Is Set](https://adamj.eu/tech/2020/03/25/django-check-constraints-one-field-set/)
1. [Django's Field Choices Don't Constrain Your Data](https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/)
1. [Using Django Check Constraints to Prevent Self-Following](https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/)