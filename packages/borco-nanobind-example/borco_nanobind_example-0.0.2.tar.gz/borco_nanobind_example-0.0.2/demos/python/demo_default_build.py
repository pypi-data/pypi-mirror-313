"""Demo script showing how to access exported items from the implementation (*.pyd)
library.
"""

import sys
from os.path import dirname

# add the build directory where _borco_nanobind_example_impl.*.pyd
# is located to the path
sys.path.append(
    dirname(__file__) + "/../../build/default/src/_borco_nanobind_example_impl"
)

# import should work after changing the path
import _borco_nanobind_example_impl as _impl


if __name__ == "__main__":
    separator = "\n" + "-" * 20 + "\n"

    # -------------------
    # exported function
    # -------------------

    print(f"add(2, 3) = {_impl.add(2, 3)}")
    print(f"add(a=2, b=3) = {_impl.add(a=2, b=3)}")  # use argument names
    print(f"add(a=2) = {_impl.add(a=2)}")  # use default value for `b`

    print(separator)

    # ----------------
    # exported value
    # ----------------

    # print the initial value
    print(f"_impl.the_answer = {_impl.the_answer}")

    # set the exported value
    _impl.the_answer = -1
    print(f"_impl.the_answer = {_impl.the_answer}")

    print(separator)

    # ----------------
    # exported class
    # ----------------

    dog = _impl.Dog()
    print(f"{dog}.bark(): {dog.bark()}")

    dog = _impl.Dog(name="Max")
    print(f"{dog}.bark(): {dog.bark()}")

    dog.name = "Charlie"
    print(f"{dog}.bark(): {dog.bark()}")

    print(separator)

    # ------------------
    # module docstring
    # ------------------

    print(f"my_ext.__doc__: {_impl.__doc__}")

    print(separator)

    # -------------
    # module help
    # -------------

    help(_impl)
