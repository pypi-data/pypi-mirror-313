# scikit-build-code example

A simple project to build a python module using
[scikit-build-core](https://scikit-build-core.readthedocs.io/en/latest/) and Qt6.

## Code Organization

Folder | Notes
---|---
src/cpp/_core_lib | main code (as a library)
src/cpp/_core | pybind11 bindings
src/example | wrapps the pybind11 bindings adds typing info and docstrings to it
tests/cpp/catch | C++ tests using [Catch2](https://github.com/catchorg/Catch2)
tests/cpp/google | C++ tests using [Google Test](https://google.github.io/googletest/)
tests/cpp/qtest | C++ tests using [QtTest](https://doc.qt.io/qt-6/qttest-index.html)
tests/python | Python tests

## C++ development

* load the main `CMakeLists.txt` in `QtCreator` or open the code folder in `VSCode`

## C++ tests

* load the main `CMakeLists.txt` in `QtCreator`
* run all test with `Tools > Tests > Run All Tests` (`Alt+Shift+T, Alt+A`)
* check the results in the `Test Results` dock (`Alt+9`)

### Catch2

Disabled [Catch2](https://github.com/catchorg/Catch2) tests by default because they:

* add a lot of files to the build, increasing the build time
* don't integrate very well with the VSCode test explorer

## Python pybind11 bindings

* the binding library is located in `src/cpp/_core`
* the `src/cpp/example` contains a wrapper for the binding library that adds some typing
  info and some docstrings
* the `tests/python` folder has some `pytest` tests using the `example` package

### Building pybind11 bindings

The `_core_lib` library that provides the main functionality is built with Qt6. For this
reason, `cmake` must find it. The easiest way to solve this is to:

* install Qt6
* define `Qt6_DIR` environment variable

This example defines the `Qt6_DIR` in the `.vscode/settings.json` file where local
`VSCode` workspace configuration is defined.

```js
{
    "cmake.buildDirectory": "${workspaceFolder}/build/vscode",
    "cmake.generator": "Ninja",
    "terminal.integrated.env.windows": {
        "Qt6_DIR": "C:/Qt/6.8.1/msvc2022_64",
    }
}
```

Once Qt6 is installed and `Qt6_DIR` is set, open the project in `VSCode` and run this
command:

```bash
uv sync
```

After the initial sync, the tests can be run with:

```bash
uv run pytest
```
