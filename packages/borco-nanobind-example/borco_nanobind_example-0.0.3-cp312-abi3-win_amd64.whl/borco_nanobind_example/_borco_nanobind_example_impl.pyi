from typing import overload


class Dog:
    @overload
    def __init__(self) -> None:
        """Create a dog with no name."""

    @overload
    def __init__(self, name: str) -> None:
        """Create a dog with a name."""

    def bark(self) -> str:
        """Make the dog bark."""

    @property
    def name(self) -> str:
        """The name of the dog."""

    @name.setter
    def name(self, arg: str, /) -> None: ...

    def __repr__(self) -> str: ...

def add(a: int, b: int = 1) -> int:
    """This function adds two numbers and increments if only one is provided."""

the_answer: int = 42
