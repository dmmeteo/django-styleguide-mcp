### `mypy` / type annotations

When it comes to [`mypy`](https://mypy.readthedocs.io/en/stable/index.html), we have the following philosophy:

> Use it, if it makes sense for you & helps you produce better software.

In HackSoft, we have:

- Projects where we enforce `mypy` and are very strict about it.
- Projects where types are more loose and `mypy` is not used at all.

Context is king here.

In the [`Django-Styleguide-Example`](https://github.com/HackSoftware/Django-Styleguide-Example), we've configured `mypy`, using both <https://github.com/typeddjango/django-stubs> and <https://github.com/typeddjango/djangorestframework-stubs/>. You can check it as an example.

Additionally, this particular project - <https://github.com/wemake-services/wemake-django-template> - also has `mypy` configuration.

Figure out what is going to work best for you.
