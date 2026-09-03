# Crypto Price Alert CLI

A small terminal utility for checking cryptocurrency prices and triggering simple above/below price alerts using CoinGecko's public API.

## Features

- Fetches spot prices by CoinGecko coin ID
- Supports any quote currency available from the API
- Above/below thresholds
- One-shot checks or continuous watch mode
- Configurable polling interval
- JSON output for scripts
- No exchange account or API key required
- Standard-library only

## Requirements

- Python 3.10+

## Quick start

```bash
git clone https://github.com/SamAlpha1/CryptoPriceAlertCLI.git
cd CryptoPriceAlertCLI
python price_alert.py --coin bitcoin
```

Alert when Bitcoin reaches or exceeds a target:

```bash
python price_alert.py --coin bitcoin --above 100000 --watch
```

Alert when Ethereum falls to or below a target:

```bash
python price_alert.py --coin ethereum --below 2500 --watch --interval 30
```

Use another quote currency:

```bash
python price_alert.py --coin solana --currency eur
```

JSON output:

```bash
python price_alert.py --coin bitcoin --json
```

You can also set defaults through environment variables shown in `.env.example`.

## Notes

Use CoinGecko coin IDs such as `bitcoin`, `ethereum`, `solana`, and `ripple`, not ticker symbols. Public APIs can rate-limit heavy polling, so use a reasonable interval.

Maintained by **SamAlpha1** · X: **@samalpha_**
