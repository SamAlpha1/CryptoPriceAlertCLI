#!/usr/bin/env python3
"""Simple cryptocurrency price checker and threshold alert CLI."""

from __future__ import annotations

import argparse
import json
import os
import time
from urllib import parse, request

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_price(coin: str, currency: str, timeout: float) -> float:
    query = parse.urlencode({"ids": coin, "vs_currencies": currency})
    req = request.Request(f"{API_URL}?{query}", headers={"User-Agent": "CryptoPriceAlertCLI/1.0"})
    with request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode())
    try:
        return float(body[coin][currency])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Price unavailable for coin={coin!r}, currency={currency!r}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check crypto prices and trigger simple threshold alerts.")
    parser.add_argument("--coin", default=os.getenv("COIN_ID", "bitcoin"), help="CoinGecko coin ID.")
    parser.add_argument("--currency", default=os.getenv("QUOTE_CURRENCY", "usd"), help="Quote currency.")
    parser.add_argument("--above", type=float, default=float(os.getenv("ALERT_ABOVE", "nan")))
    parser.add_argument("--below", type=float, default=float(os.getenv("ALERT_BELOW", "nan")))
    parser.add_argument("--interval", type=float, default=float(os.getenv("POLL_INTERVAL", "60")))
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--watch", action="store_true", help="Keep polling until a configured threshold is reached.")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def is_number(value: float) -> bool:
    return value == value


def evaluate(price: float, above: float, below: float) -> tuple[bool, str]:
    reasons: list[str] = []
    if is_number(above) and price >= above:
        reasons.append(f"price >= {above}")
    if is_number(below) and price <= below:
        reasons.append(f"price <= {below}")
    return bool(reasons), ", ".join(reasons)


def main() -> int:
    args = parse_args()
    if args.interval < 1:
        raise SystemExit("--interval must be at least 1 second.")

    while True:
        price = fetch_price(args.coin, args.currency, args.timeout)
        triggered, reason = evaluate(price, args.above, args.below)
        payload = {
            "coin": args.coin,
            "currency": args.currency,
            "price": price,
            "triggered": triggered,
            "reason": reason or None,
        }
        if args.json:
            print(json.dumps(payload))
        else:
            marker = "ALERT" if triggered else "PRICE"
            print(f"[{marker}] {args.coin} = {price:g} {args.currency.upper()}" + (f" ({reason})" if reason else ""))

        if triggered or not args.watch:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
