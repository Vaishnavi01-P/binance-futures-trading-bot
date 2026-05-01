# Binance Futures Testnet Trading Bot

A CLI-based Python trading bot for placing `MARKET` and `LIMIT` orders on Binance USDT-M Futures Testnet. The project uses `python-binance`, structured validation, file logging, and a small client wrapper to keep exchange access separate from CLI concerns.

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── cli.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Add Binance Futures Testnet API credentials as environment variables.

```bash
set BINANCE_API_KEY=your_testnet_api_key
set BINANCE_API_SECRET=your_testnet_api_secret
```

PowerShell:

```powershell
$env:BINANCE_API_KEY="your_testnet_api_key"
$env:BINANCE_API_SECRET="your_testnet_api_secret"
```

## Usage

Run commands from the `trading_bot` directory.

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

## Logging

The app writes API requests, responses, validation failures, and errors to:

```text
trading.log
```

## Assumptions

- Orders are submitted to Binance USDT-M Futures Testnet at `https://testnet.binancefuture.com`.
- `LIMIT` orders use `GTC` time-in-force.
- API keys must be Futures Testnet keys, not production Binance keys.
- Symbol precision, lot size, min notional, and exchange-specific filters are enforced by Binance. This CLI validates only basic user input before submitting the order.

