import pytest
from pipes_and_filters.utils import identity


@pytest.mark.parametrize('x, expected', [
    (1, 1),
    (-2, -2),
    ('abc', 'abc'),
    (None, None),
    (True, True),
    (False, False),
    (1.0, 1.0),
    (-2.0, -2.0),
    ([1, 2, 3], [1, 2, 3]),
    ({'a': 1, 'b': 2}, {'a': 1, 'b': 2}),
])
def test_identity(x, expected):
    assert identity(x) == expected
