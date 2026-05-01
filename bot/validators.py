"""CLI input validation helpers."""

from __future__ import annotations


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(ValueError):
    """Raised when user-provided order input is invalid."""


def validate_symbol(symbol: str) -> str:
    cleaned = (symbol or "").strip().upper()
    if not cleaned:
        raise ValidationError("Symbol must not be empty.")
    return cleaned


def validate_side(side: str) -> str:
    cleaned = (side or "").strip().upper()
    if cleaned not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    return cleaned


def validate_order_type(order_type: str) -> str:
    cleaned = (order_type or "").strip().upper()
    if cleaned not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return cleaned


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValidationError("Quantity must be positive.")
    return quantity


def validate_price(order_type: str, price: float | None) -> float | None:
    if order_type == "LIMIT" and price is None:
        raise ValidationError("Price is required for LIMIT orders.")
    if price is not None and price <= 0:
        raise ValidationError("Price must be positive.")
    return price


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> dict[str, str | float | None]:
    """Validate and normalize all order inputs."""

    normalized_type = validate_order_type(order_type)
    return {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "type": normalized_type,
        "quantity": validate_quantity(quantity),
        "price": validate_price(normalized_type, price),
    }

