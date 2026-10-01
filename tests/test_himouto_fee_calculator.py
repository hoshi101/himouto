from decimal import ROUND_HALF_UP, Decimal

from hypothesis import example, given
from hypothesis import strategies as st

from demo.fee_calculator import (
    CENT,
    add_vat,
    calculate_trading_fee,
    extract_vat,
    split_fee,
)

D = Decimal

amounts = st.decimals(min_value=0, max_value=D("1e9"), places=2)
rates = st.decimals(min_value=0, max_value=1, places=4)
vat_rates = st.decimals(min_value=0, max_value=D("0.5"), places=2)
weights = st.lists(st.integers(min_value=1, max_value=1000).map(D), min_size=1, max_size=10)


@example(notional=D("0.50"), rate=D("0.0100"))
@given(notional=amounts, rate=rates)
def test_trading_fee_rounds_half_up(notional, rate):
    expected = (notional * rate).quantize(CENT, rounding=ROUND_HALF_UP)
    assert calculate_trading_fee(notional, rate) == expected


@example(gross=D("0.03"), vat_rate=D("0.20"))
@given(gross=amounts, vat_rate=vat_rates)
def test_extract_vat_parts_sum_to_gross(gross, vat_rate):
    net, vat = extract_vat(gross, vat_rate)
    assert net + vat == gross


@example(total=D("0.01"), weights=[D(1), D(1)])
@given(total=amounts, weights=weights)
def test_split_fee_sums_to_total(total, weights):
    assert sum(split_fee(total, weights)) == total


@given(net=amounts, vat_rate=vat_rates)
def test_add_vat_matches_oracle(net, vat_rate):
    expected = (net * (1 + vat_rate)).quantize(CENT, rounding=ROUND_HALF_UP)
    assert add_vat(net, vat_rate) == expected
