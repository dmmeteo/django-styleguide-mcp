### Naming conventions

We follow 2 general naming conventions:

- The test file names should be `test_the_name_of_the_thing_that_is_tested.py`
- The test case should be `class TheNameOfTheThingThatIsTestedTests(TestCase):`

For example, if we have:

```python
def a_very_neat_service(*args, **kwargs):
    pass
```

We are going to have the following for file name:

```
project_name/app_name/tests/services/test_a_very_neat_service.py
```

And the following for test case:

```python
class AVeryNeatServiceTests(TestCase):
    pass
```

For tests of utility functions, we follow a similar pattern.

For example, if we have `project_name/common/utils.py`, then we are going to have `project_name/common/tests/test_utils.py` and place different test cases in that file.

If we are to split the `utils.py` module into submodules, the same will happen for the tests:

- `project_name/common/utils/files.py`
- `project_name/common/tests/utils/test_files.py`

We try to match the structure of our modules with the structure of their respective tests.