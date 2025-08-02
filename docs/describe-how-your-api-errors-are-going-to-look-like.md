### Describe how your API errors are going to look like.

This is very important and should be done as early as possible in any given project.

This is basically agreeing upon what the interface of your API errors - **How an error is going to look like as an API response?**

This is very project specific, you can use some of the popular APIs for inspiration:

- Stripe - <https://stripe.com/docs/api/errors>

As an example, we might decide that our errors are going to look like this:

1. `4**` and `5**` status codes for different types of errors.
1. Each error will be a dictionary with a single `message` key, containing the error message.

```json
{
  "message": "Some error message here"
}
```

That's simple enough:

- `400` will be used for validation errors.
- `401` for auth errors.
- `403` for permission errors.
- `404` for not found errors.
- `429` for throttling errors.
- `500` for server errors (we need to be careful not to silence an exception causing 500 and always report that in services like Sentry)

Again, this is up to you & it's specific to the project. **We'll propose something similiar for one of the specific approaches.**
