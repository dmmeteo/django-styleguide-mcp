## Errors & Exception Handling

> 👀 If you want the code, hop to the `Styleguide-Example` project - <https://github.com/HackSoftware/Styleguide-Example/blob/master/styleguide_example/api/exception_handlers.py>

Errors & exception handling is a big topic & quite often - the details are specific for a given project.

That's why we'll split things into two - **general guidelines**, followed by some **specific approaches** for error handling.

**Our general guidelines are:**

1. Know how exception handling works (we'll give context for Django Rest Framework).
1. Describe how your API errors are going to look like.
1. Know how to change the default exception handling behavior.

**Followed by some specific approaches:**

1. Use DRF's default exceptions, with very little modifications.
1. HackSoft's proposed approach.

If you are looking for a standard way to structure your error responses, **check RFC7807** - <https://datatracker.ietf.org/doc/html/rfc7807> (as proposed here - <https://github.com/HackSoftware/Django-Styleguide/issues/133>)
