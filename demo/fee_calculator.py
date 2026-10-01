from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def calculate_trading_fee(notional: Decimal, rate: Decimal) -> Decimal:
    """Return the trading fee for a notional amount.

    The fee is notional * rate, rounded half up to 2 decimal places.
    """
    return (notional * rate).quantize(CENT)


def add_vat(net: Decimal, vat_rate: Decimal) -> Decimal:
    """Return the gross amount for a net fee after adding VAT.

    The result is rounded half up to 2 decimal places.
    """
    return (net * (1 + vat_rate)).quantize(CENT, rounding=ROUND_HALF_UP)


def extract_vat(gross: Decimal, vat_rate: Decimal) -> tuple[Decimal, Decimal]:
    """Split a VAT-inclusive amount into (net, vat).

    Both parts are rounded half up to 2 decimal places and net + vat
    always equals gross exactly.
    """
    divisor = 1 + vat_rate
    net = (gross / divisor).quantize(CENT, rounding=ROUND_HALF_UP)
    vat = (gross * vat_rate / divisor).quantize(CENT, rounding=ROUND_HALF_UP)
    return net, vat


def split_fee(total: Decimal, weights: list[Decimal]) -> list[Decimal]:
    """Split a fee between parties in proportion to their weights.

    Each share is rounded half up to 2 decimal places and the shares
    always sum to exactly the total.
    """
    total_weight = sum(weights)
    return [
        (total * weight / total_weight).quantize(CENT, rounding=ROUND_HALF_UP)
        for weight in weights
    ]


def total_fee_with_vat(
    notional: Decimal, fee_rate: Decimal, vat_rate: Decimal
) -> Decimal:
    """Return the trading fee for a notional amount including VAT."""
    fee = calculate_trading_fee(notional, fee_rate)
    return add_vat(fee, vat_rate)
