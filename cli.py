"""CLI entry point for Binance Futures Testnet orders."""

from __future__ import annotations

import argparse
import logging
import os
import sys

from bot.logging_config import setup_logging
from bot.validators import ValidationError, validate_order_inputs


logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Place MARKET and LIMIT orders on Binance Futures Testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Required for LIMIT orders")
    return parser.parse_args()


def print_order_summary(order: dict[str, str | float | None]) -> None:
    print("Order Request Summary")
    print("---------------------")
    print(f"Symbol:   {order['symbol']}")
    print(f"Side:     {order['side']}")
    print(f"Type:     {order['type']}")
    print(f"Quantity: {order['quantity']}")
    if order["type"] == "LIMIT":
        print(f"Price:    {order['price']}")
    print()


def print_order_response(response: dict[str, object]) -> None:
    print("Order Response")
    print("--------------")
    print(f"orderId:     {response.get('orderId')}")
    print(f"status:      {response.get('status')}")
    print(f"executedQty: {response.get('executedQty')}")
    avg_price = response.get("avgPrice")
    if avg_price not in (None, ""):
        print(f"avgPrice:    {avg_price}")
    print()


def main() -> int:
    setup_logging()
    args = parse_args()

    try:
        order = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )
        logger.info("Validated order inputs: %s", order)
        print_order_summary(order)

        from bot.client import BinanceClientError, BinanceFuturesClient
        from bot.orders import create_limit_order, create_market_order

        client = BinanceFuturesClient(
            api_key=os.getenv("BINANCE_API_KEY", ""),
            api_secret=os.getenv("BINANCE_API_SECRET", ""),
        )

        if order["type"] == "MARKET":
            response = create_market_order(
                client,
                symbol=str(order["symbol"]),
                side=str(order["side"]),
                quantity=float(order["quantity"]),
            )
        else:
            response = create_limit_order(
                client,
                symbol=str(order["symbol"]),
                side=str(order["side"]),
                quantity=float(order["quantity"]),
                price=float(order["price"]),
            )

        print_order_response(response)
        print("Success: order submitted.")
        return 0
    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"Failure: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        from bot.client import BinanceClientError

        if not isinstance(exc, BinanceClientError):
            logger.exception("Unexpected application error")
            print("Failure: Unexpected application error.", file=sys.stderr)
            return 1
        logger.error("Binance client error: %s", exc)
        print(f"Failure: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
