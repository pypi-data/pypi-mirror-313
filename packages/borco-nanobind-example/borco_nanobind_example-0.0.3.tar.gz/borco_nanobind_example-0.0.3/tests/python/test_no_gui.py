import pytest

import borco_nanobind_example as dut


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (1, 2, 3),
        (1, -1, 0),
        (1, None, 2),
        (2, None, 3),
    ]
)
def test_add(a: int, b: int | None, expected_result: int) -> None:
    """Test `add` function exported by `borco_nanobind_example` works."""
    if b is not None:
        assert dut.add(a, b) == expected_result
    else:
        assert dut.add(a) == expected_result


def test_the_answer() -> None:
    """Test exported constant `the_answer` works."""
    assert dut.the_answer == 42


def test_default_dog() -> None:
    """Test creating a dog with no name."""
    dog = dut.Dog()
    assert dog.name == ""


def test_dog_with_name() -> None:
    """Test creating a dog with an initial name."""
    dog = dut.Dog("Max")
    assert dog.name == "Max"


@pytest.mark.parametrize(
    "initial_name",
    (
        None, "Max"
    )
)
def test_set_dog_name(initial_name: str) -> None:
    """Test setting the dog name works."""
    d = dut.Dog(initial_name) if initial_name is not None else dut.Dog()

    # set the name
    d.name = "Charlie"

    # read the name and verify it was set correctly
    assert d.name == "Charlie"
