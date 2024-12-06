import math
from datetime import datetime, timezone

import pytest

from crypto_connector.base.exchange import Exchange

exc = Exchange()


@pytest.mark.parametrize(
    argnames="f,decimal_places,expected",
    argvalues=[
        (10.123, 2, 10.12),
        (0.2999999999999997637, 2, 0.29),
        (10.0, 1, 10),
        (10.0, 1, 10),
        (10.0, 1, 10.0),
        (10.12323, 0, 10),
        (0.3, 1, 0.3),
        (0.3, 2, 0.3),
        (10e3, 1, 10000),
    ],
)
def test_truncate_float(f, decimal_places, expected) -> None:
    assert math.isclose(a=exc.truncate_float(f, decimal_places), b=expected, abs_tol=0)


@pytest.mark.parametrize(
    argnames="n,expected",
    argvalues=[
        (0.1, 1),
        (0.01, 2),
        (0.001, 3),
        (0.000001, 6),
        (0.0000001, 7),
        (0, 0),
        (1, 0),
        (1.0, 1),
        (-1, 0),
        (-0.01, 2),
    ],
)
def test_decimal_places(n, expected) -> None:
    assert exc.decimal_places(n) == expected


def test_decimal_places_wrong_input_type() -> None:
    with pytest.raises(ValueError):
        exc.decimal_places("0.01")  # type: ignore


@pytest.mark.parametrize(
    argnames="string,format,expected",
    argvalues=[
        (
            "2019-05-18T15:17:08Z",
            "%Y-%m-%dT%H:%M:%SZ",
            datetime(2019, 5, 18, 15, 17, 8, tzinfo=timezone.utc),
        ),
        (
            "2019-05-18T15:17:00+00:00",
            "%Y-%m-%dT%H:%M:%S%z",
            datetime(2019, 5, 18, 15, 17, tzinfo=timezone.utc),
        ),
    ],
)
def test_str_to_dt(string, format, expected) -> None:
    assert exc.str_to_dt(string=string, format=format) == expected


if __name__ == "__main__":
    pytest.main([__file__])
