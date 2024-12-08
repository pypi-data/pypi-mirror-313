# nanobind example

Example creating a Python binding for C++ with
[nanobind](https://github.com/wjakob/nanobind). Based on the
[nanobind docs](https://nanobind.readthedocs.io/en/latest/index.html).

## Using the bindings

```bash
$ uv venv --python 3.12
$ uv pip install borco-nanobind-example
$ uv run python
>>> import borco_nanobind_example as ex
>>> ex.Dog("Max").bark()
'Max: woof!'
>>> ex.the_answer
42
>>> ex.add(3)
4
>>> ex.add(3, 4)
7
```
