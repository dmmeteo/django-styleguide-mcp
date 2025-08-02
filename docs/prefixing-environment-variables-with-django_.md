### Prefixing environment variables with `DJANGO_`

In a lot of examples, you'll see that environment variables are usually prefixed with `DJANGO_`. This is very helpful when there are other applications alongside your Django app that run on the same environment. In that case, prefixing the environment variables with `DJANGO_` helps you to differ which are the environment variables specific to your Django app.

In HackSoft we do not ususally have several apps running on the same environment. So, we tend to prefix with `DJANGO_` only the Django specific environments & anything else.

For example, we would have `DJANGO_SETTINGS_MODULE`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CORS_ORIGIN_WHITELIST` prefixed. We would have `AWS_SECRET_KEY`, `CELERY_BROKER_URL`, `EMAILS_ENABLED` not prefixed.

This is mostly up to personal preference. **Just make sure you are consistent with that.**