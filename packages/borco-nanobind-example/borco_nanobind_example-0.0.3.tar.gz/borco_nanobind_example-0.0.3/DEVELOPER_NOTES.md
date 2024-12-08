# Developer notes

## Code organization

Folder | Notes
---|---
`src/_core_lib` | C++ code for the `_core_lib` static lib with main functionality
`src/_my_ext_impl` | C++ code for the `_my_ext_impl` Python binding that exposes `_core_lib`
`src/my_ext` | Python wrapper that imports `_my_ext_impl` and exposes relevant functionality
`demos/python` | Python demo scripts
`tests/cpp/catch` | C++ tests using [catch2](https://github.com/catchorg/Catch2)
`tests/cpp/google` | C++  tests using [google test & google mock](https://github.com/google/googletest)
`tests/python` | Python tests

## Windows

To build on Windows, you will need to install *Visual Studio 2022* with:

* C++ compiler (check **Workload &rarr; Desktop development with C++**)
* `cmake` and `ninja` (check **Installation Details &rarr; Desktop development with C++ &rarr; C++ CMake tools for Windows**)

You will have to load the `vcvarsall.bat` before being able to run the `cmake` or `ninja`
installed by *Visual Studio 2022*.

## uv

### Compile and sync

```bash
uv sync
```

### Publish to pypi

```bash
rm -rf .venv/ build/ dist/
```

```bash
uv sync
```

```bash
uv build
```

```bash
uv publish
```

## Run the tests

```bash
pytest
```

or

```bash
uv run pytest
```

## Run the demo

```bash
python demos/python/demo_no_gui.py
```

or

```bash
uv run python demos/python/demo_no_gui.py
```

## Qt Creator

Open the top `CMakeLists.txt` in *Qt Creator*.

The `CMakePresets.json` file contains some presets for *Windows*.

## VS Code

### "Git Bash + vcvarsall" VSCode terminal profile

If you use *VSCode*, the workspace is configured to use a custom terminal that loads
the `vcvarsall.bat` and then launches *git bash*, named `Git Bash + vcvarsall`.

Check `.vscode\settings.json` and `.vscode\vcvarsall.bat` if you need to customize it
further.

### CMake presets

The `venv` presets from `CMakePresets.json` can be used to build on the command line with
the *Python* version installed in `.venv` with `uv sync`.

First time compiling:

```bash
uv sync
```

```bash
cmake --workflow --preset venv
```

Only recompiling:

```bash
cmake --build --preset venv
```

Only running the tests:

```bash
ctest --preset venv
```

**NOTE:** The build artifacts are stored under `build/venv`.

## Removing old artifacts

```bash
rm -rf .venv/ build/ dist/
```
