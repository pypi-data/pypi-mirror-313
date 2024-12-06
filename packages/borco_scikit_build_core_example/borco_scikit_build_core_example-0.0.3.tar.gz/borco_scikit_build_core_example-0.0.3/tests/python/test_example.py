import pytest

import borco_scikit_build_core_example


@pytest.mark.parametrize(
    "arg, result",
    [
        [0, 0.0],
        [1, 1.0],
        [2, 4.0],
        [-2, 4.0],
    ]
)
def test_square(arg: float, result: float) -> None:
    """Tests `example.square` defined in C++."""
    assert borco_scikit_build_core_example.square(arg) == result
