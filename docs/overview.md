### Overview

Testing is an interesting & vast topic.

As an overview, you can listen to [Radoslav Georgiev's talk at DjangoCon Europe 2022](https://www.youtube.com/watch?v=PChaEAIsQls):

[![Quality Assurance in Django - Testing what matters](https://img.youtube.com/vi/PChaEAIsQls/0.jpg)](https://www.youtube.com/watch?v=PChaEAIsQls)

In our Django projects, we split our tests depending on the type of code they represent.

Meaning, we generally have tests for models, services, selectors & APIs / views.

The file structure usually looks like this:

```
project_name
├── app_name
│   ├── __init__.py
│   └── tests
│       ├── __init__.py
│       ├── factories.py
│       ├── models
│       │   └── __init__.py
│       │   └── test_some_model_name.py
│       ├── selectors
│       │   └── __init__.py
│       │   └── test_some_selector_name.py
│       └── services
│           ├── __init__.py
│           └── test_some_service_name.py
└── __init__.py
```