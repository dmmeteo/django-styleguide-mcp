### More ideas

As you can see, we can mold exception handling to our needs.

You can start handling more stuff - for example - translating `django.core.exceptions.ObjectDoesNotExist` to `rest_framework.exceptions.NotFound`.

You can even handle all exceptions, but then, you should be sure those exceptions are being logged properly, otherwise you might silence something that's important.