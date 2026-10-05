"""Currency exchange rate tool using Frankfurter public API (public-apis directory)."""

import json
import urllib.request
from typing import Any


def get_currency_exchange_rates(
    base_currency: str = "USD",
    target_currencies: list[str] | None = None
) -> dict[str, Any]:
    """Fetches real-time foreign exchange conversion rates for budget travel planning.

    Args:
        base_currency: Three-letter ISO code for base currency (default 'USD').
        target_currencies: Optional list of target currency ISO codes (e.g. ['JPY', 'EUR', 'MXN']).

    Returns:
        Dictionary containing base currency, date, and conversion rates.
    """
    try:
        base = base_currency.upper().strip()
        default_targets = ["EUR", "JPY", "MXN", "GBP", "CAD"]
        targets = [t.upper().strip() for t in (target_currencies or default_targets)]
        symbols = ",".join(targets)

        url = f"https://api.frankfurter.app/latest?from={base}&to={symbols}"
        req = urllib.request.Request(url, headers={"User-Agent": "TravelConciergeAgent/1.0"})

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        return {
            "base_currency": data.get("base", base),
            "date": data.get("date"),
            "rates": data.get("rates", {}),
            "note": f"Live exchange rates relative to 1 {base}"
        }
    except Exception as e:
        return {"error": f"Failed to fetch currency exchange rates for '{base_currency}': {e!s}"}
