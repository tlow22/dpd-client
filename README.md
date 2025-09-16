# dpd-client

Python client and CLI for Health Canada Drug Product Database (DPD) (API)[https://health-products.canada.ca/api/documentation/dpd-documentation-en.html].

## Quickstart

- Install dependencies with `uv` (created `.venv`):

  - `uv sync`

- Example (sync client):

```
from dpd_client import DPDClient

client = DPDClient()
try:
    products = client.drugproduct(din="00326925")
    for p in products:
        print(p.brand_name, p.drug_identification_number)
finally:
    client.close()
```

- Example (async client):

```
import asyncio
from dpd_client import AsyncDPDClient


async def main() -> None:
    client = AsyncDPDClient()
    try:
        products = await client.drugproduct(din="00326925")
        for p in products:
            print(p.brand_name, p.drug_identification_number)
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
```

## CLI

After `uv run` or activating the venv, run:

- `dpd drugproduct --din 00326925`
- `dpd company --id 10825`
- `dpd activeingredient --id 48905`
- `dpd form --id 10846`
- `dpd route --id 3`
- `dpd schedule --id 10687`
- `dpd status --id 2049`
- `dpd packaging --id 11685`
- `dpd pharmaceuticalstd --id 11534`
- `dpd therapeuticclass --id 10564`
- `dpd veterinaryspecies --id 13755`

Use `--lang fr` for French.

## Caching and Retries

- Caching: pass `cache_ttl` (seconds) to `DPDClient` or `AsyncDPDClient` to enable in-memory caching per request URL + params.
  - Example: `DPDClient(cache_ttl=60)` caches results for 60 seconds.
- Retries: automatic retries with exponential backoff for `429` and `5xx` responses.
  - `4xx` (client errors) raise `DPDHTTPError` without retry.
  - Invalid/malformed JSON raises `DPDDecodeError`.

## Tests

- Run test suite:
  - `uv run pytest -q`
- What’s covered:
  - Core client behavior: parameter validation, list normalization, error mapping.
  - Retry logic on transient `5xx` responses.
  - Caching prevents redundant requests for identical calls.
  - Async client parity using `pytest-asyncio`.
- How tests work:
  - HTTP calls are mocked with `respx` over `httpx`; no live network calls.
  - Add new tests under `tests/` following existing patterns.

## Status

- Implemented endpoints: `drugproduct`, `company`, `activeingredient`, `form`, `route`, `schedule`, `status`, `packaging`, `pharmaceuticalstd`, `therapeuticclass`, `veterinaryspecies`.
- Do not publish yet; more testing and validation are planned.

## Development

- Manage dependencies and workflows with `uv`.
- See `CHANGELOG.md` for notable changes; version is in `pyproject.toml`.
- Lint/type: `ruff`, `mypy`. Run `uv run ruff check .` and `uv run mypy .` if desired.
