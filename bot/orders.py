"""Order orchestration and response formatting."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from bot.client import BinanceFuturesClient


def create_market_order(
    client: BinanceFuturesClient,
    *,
    symbol: str,
    side: str,
    quantity: float,
) -> dict[str, Any]:
    response = client.place_market_order(symbol=symbol, side=side, quantity=quantity)
    return format_order_response(response)


def create_limit_order(
    client: BinanceFuturesClient,
    *,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> dict[str, Any]:
    response = client.place_limit_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
    )
    return format_order_response(response)


def format_order_response(response: dict[str, Any]) -> dict[str, Any]:
    """Return a compact response shape for CLI output."""

    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice"),
    }
