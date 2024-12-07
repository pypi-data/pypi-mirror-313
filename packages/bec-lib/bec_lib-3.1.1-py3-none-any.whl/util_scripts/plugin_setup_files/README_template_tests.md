# Getting Started with Testing using pytest

BEC is using the [pytest](https://docs.pytest.org/en/8.0.x/) framework. 
It can be install via 
``` bash
pip install pytest
```
in your *python environment*. 
We note that pytest is part of the optional-dependencies `[dev]` of the plugin package.

## Introduction

Tests in this package should be stored in the `tests` directory.
We suggest to sort tests of different submodules, i.e. `scans` or `devices` in the respective folder structure, and to folow a naming convention of `<test_module_name.py>`.

To run all tests, navigate to the directory of the plugin from the command line, and run the command 

``` bash
pytest -v --random-order ./tests
```
Note, the python environment needs to be active.
The additional arg `-v` allows pytest to run in verbose mode which provides more detailed information about the tests being run.
The argument `--random-order` instructs pytest to run the tests in random order, which is the default in the CI pipelines. 

## Test examples

Writing tests can be quite specific for the given function. 
We recommend writing tests as isolated as possible, i.e. try to test single functions instead of full classes.
A very useful class to enable isolated testing is [MagicMock](https://docs.python.org/3/library/unittest.mock.html).
In addition, we also recommend to take a look at the [How-to guides from pytest](https://docs.pytest.org/en/8.0.x/how-to/index.html).

