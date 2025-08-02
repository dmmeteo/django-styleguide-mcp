### Example - function-based service

An example service that creates a user:

```python
def user_create(
    *,
    email: str,
    name: str
) -> User:
    user = User(email=email)
    user.full_clean()
    user.save()

    profile_create(user=user, name=name)
    confirmation_email_send(user=user)

    return user
```

As you can see, this service calls 2 other services - `profile_create` and `confirmation_email_send`.

In this example, everything related to the user creation is in one place and can be traced.