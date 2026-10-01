from decimal import Decimal

from demo.fee_calculator import (
    add_vat,
    calculate_trading_fee,
    extract_vat,
    split_fee,
    total_fee_with_vat,
)

D = Decimal


def test_calculate_trading_fee():
    assert calculate_trading_fee(D("10000.00"), D("0.001")) == D("10.00")
    assert calculate_trading_fee(D("2500.00"), D("0.0015")) == D("3.75")


def test_add_vat():
    assert add_vat(D("10.00"), D("0.07")) == D("10.70")


def test_extract_vat():
    assert extract_vat(D("107.00"), D("0.07")) == (D("100.00"), D("7.00"))


def test_split_fee():
    assert split_fee(D("100.00"), [D(1), D(1)]) == [D("50.00"), D("50.00")]
    assert split_fee(D("100.00"), [D(3), D(1)]) == [D("75.00"), D("25.00")]


def test_total_fee_with_vat():
    assert total_fee_with_vat(D("10000.00"), D("0.001"), D("0.07")) == D("10.70")
