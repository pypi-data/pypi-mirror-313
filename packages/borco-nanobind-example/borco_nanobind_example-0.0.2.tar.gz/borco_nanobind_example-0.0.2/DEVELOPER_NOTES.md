# Developer notes

## Code organization

Folder | Notes
---|---
`src/_core_lib` | the C++ code for the `_core_lib` static lib with main functionality
`src/_my_ext_impl` | the C++ code for the `_my_ext_impl` Python binding that exposes `_core_lib`
`src/my_ext` | small Python wrapper that imports `_my_ext_impl` and exposes relevant functionality
`demos/python` | some demo python scripts

## Windows

To build on Windows, you will need:

* *Visual Studio 2022* C++ compiler, `cmake` and `ninja`
* *Python*

The `CMakePresets.json` has a `default` preset that uses the current *Python* version
installed with [scoop](https://scoop.sh/).

### vcvarsall

In order to compile the project with *Visual Studio 2022* C++ compiler you should load
the `vcvarsall` before running `cmake` or `ninja`.

### "Git Bash + vcvarsall" VSCode terminal profile

If you use *VSCode*, the workspace is configured to use a custom terminal that loads
the `vcvarsall.bat` and then launches *git bash*, named `Git Bash + vcvarsall`.

Check `.vscode\settings.json` and `.vscode\vcvarsall.bat` if you need to customize it
further.

### Compiling

The `CMakePresets.json` file contains some presets for *Windows*.

First time compiling:

```bash
cmake --workflow --preset default
```

Recompiling:

```bash
cmake --build --preset default
```

### Removing old artifacts

```bash
rm -rf build
```

### Publishing

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
