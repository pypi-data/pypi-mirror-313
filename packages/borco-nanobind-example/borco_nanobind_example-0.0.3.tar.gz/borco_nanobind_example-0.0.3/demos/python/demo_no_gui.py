"""Demo script showing how to access exported non-GUI items."""

import borco_nanobind_example as dut  # pylint: disable=wrong-import-position # noqa: E402


if __name__ == "__main__":
    SEPARATOR = "\n" + "-" * 20 + "\n"

    # -------------
    # module help
    # -------------

    help(dut)

    # -------------------
    # exported function
    # -------------------

    print(SEPARATOR)

    print(f"add(2, 3) = {dut.add(2, 3)}")
    print(f"add(a=2, b=3) = {dut.add(a=2, b=3)}")  # use argument names
    print(f"add(a=2) = {dut.add(a=2)}")  # use default value for `b`

    # ----------------
    # exported value
    # ----------------

    print(SEPARATOR)

    # print the initial value
    print(f"the_answer = {dut.the_answer}")

    # set the exported value
    dut.the_answer = -1
    print(f"the_answer = {dut.the_answer}")

    # ----------------
    # exported class
    # ----------------

    print(SEPARATOR)

    dog = dut.Dog()
    print(f"{dog}.bark(): {dog.bark()}")

    dog = dut.Dog(name="Max")
    print(f"{dog}.bark(): {dog.bark()}")

    dog.name = "Charlie"
    print(f"{dog}.bark(): {dog.bark()}")

    # ------------------
    # module docstring
    # ------------------

    print(SEPARATOR)

    print(f"{dut.__name__}.__doc__: {dut.__doc__}")
