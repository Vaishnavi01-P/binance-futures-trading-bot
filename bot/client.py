"""Binance Futures Testnet client wrapper."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any


logger = logging.getLogger(__name__)


class BinanceClientError(RuntimeError):
    """Raised when Binance client operations fail."""


class BinanceFuturesClient:
    """Small wrapper around python-binance for USDT-M Futures Testnet."""

    TESTNET_FUTURES_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str) -> None:
        try:
            from binance.client import Client
        except ImportError as exc:
            raise BinanceClientError(
                "Missing dependency: install python-binance with `pip install -r requirements.txt`."
            ) from exc

        if not api_key or not api_secret:
            raise BinanceClientError(
                "Missing Binance API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET."
            )

        self.client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
        self.client.FUTURES_URL = self.TESTNET_FUTURES_URL
        logger.info("Initialized Binance Futures Testnet client")

    def place_market_order(
        self,
        *,
        symbol: str,
        side: str,
        quantity: float,
    ) -> dict[str, Any]:
        payload = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": self._format_decimal(quantity),
        }
        return self._create_order(payload)

    def place_limit_order(
        self,
        *,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
    ) -> dict[str, Any]:
        payload = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": self._format_decimal(quantity),
            "price": self._format_decimal(price),
        }
        return self._create_order(payload)

    def _create_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        from binance.exceptions import BinanceAPIException, BinanceRequestException
        from requests.exceptions import RequestException

        logger.info("Submitting futures order request: %s", self._redact_payload(payload))
        try:
            response = self.client.futures_create_order(**payload)
            logger.info("Received futures order response: %s", response)
            return response
        except BinanceAPIException as exc:
            logger.exception("Binance API error while placing order")
            raise BinanceClientError(
                f"Binance API error: {getattr(exc, 'message', str(exc))}"
            ) from exc
        except BinanceRequestException as exc:
            logger.exception("Binance request error while placing order")
            raise BinanceClientError(
                f"Binance request error: {getattr(exc, 'message', str(exc))}"
            ) from exc
        except RequestException as exc:
            logger.exception("Network error while placing order")
            raise BinanceClientError("Network error while connecting to Binance.") from exc
        except Exception as exc:
            logger.exception("Unexpected error while placing order")
            raise BinanceClientError("Unexpected error while placing order.") from exc

    @staticmethod
    def _format_decimal(value: float) -> str:
        return format(Decimal(str(value)).normalize(), "f")

    @staticmethod
    def _redact_payload(payload: dict[str, Any]) -> dict[str, Any]:
        return dict(payload)
