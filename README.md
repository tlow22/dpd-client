# dpd-client

Python client and CLI for Health Canada Drug Product Database (DPD) API.
Docs: https://health-products.canada.ca/api/documentation/dpd-documentation-en.html

This README is split into a User Guide and a Developer Guide.

**User Guide**

- Install with `uv` and use the client/CLI.
- Understand retries, caching, endpoints, and examples.

**Developer Guide**

- Project layout, internal helpers, testing, and workflows.

**User Guide**

- Install dependencies (creates `.venv`):
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

**CLI**

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

**Caching and Retries**

- Caching: pass `cache_ttl` (seconds) to `DPDClient` or `AsyncDPDClient` to enable in-memory caching per request URL + params.
  - Example: `DPDClient(cache_ttl=60)` caches results for 60 seconds.
- Retries: automatic retries with exponential backoff for `429` and `5xx` responses.
  - `4xx` (client errors) raise `DPDHTTPError` without retry.
  - Invalid/malformed JSON raises `DPDDecodeError`.

**Status**

- Implemented endpoints: `drugproduct`, `company`, `activeingredient`, `form`, `route`, `schedule`, `status`, `packaging`, `pharmaceuticalstd`, `therapeuticclass`, `veterinaryspecies`.
- Do not publish yet; more testing and validation are planned.

**Developer Guide**

**Tests**

- Run test suite:
  - `uv run pytest -q`
- What’s covered:
  - Parameter validation, list normalization, and error mapping.
  - Retry logic for transient `5xx` responses.
  - Caching prevents redundant requests for identical calls.
  - Async client parity using `pytest-asyncio`.
- How tests work:
  - HTTP calls are mocked with `respx` over `httpx`; no live network calls.
  - Add new tests under `tests/` following existing patterns.

**Project Layout**

```
.
├── AGENTS.md                  # Agent conventions (tooling, testing, release policy)
├── CHANGELOG.md               # Notable changes and versions
├── LICENSE                    # MIT license
├── README.md                  # This document (User & Developer guides)
├── pyproject.toml             # Project metadata, deps, scripts, tool configs
├── src/
│   └── dpd_client/
│       ├── __init__.py        # Public exports (clients, models, errors)
│       ├── cli.py             # Typer CLI entry (subcommands per endpoint)
│       ├── client.py          # Sync & async clients (use shared param helpers)
│       ├── errors.py          # Exception types (DPDError, DPDHTTPError, ...)
│       ├── http.py            # HTTP helpers (httpx, retries, caching)
│       ├── models.py          # Pydantic models per resource
│       ├── params.py          # Internal helpers to build/validate query params
│       └── py.typed           # PEP 561 typing marker
└── tests/
    ├── test_client.py                 # Core client behavior
    ├── test_more_endpoints.py         # Additional endpoints & params
    └── test_caching_and_errors.py     # Caching, retries, errors, async basic
```

**File Notes**

- `src/dpd_client/http.py`: wraps `httpx` with retries/backoff, JSON parsing, and optional TTL cache.
- `src/dpd_client/models.py`: Pydantic v2 models for each API object, extra fields allowed.
- `src/dpd_client/client.py`: `DPDClient` and `AsyncDPDClient`; methods return lists of models.
- `src/dpd_client/params.py`: shared param builders; keeps sync/async signatures DRY and validated.
- `src/dpd_client/cli.py`: Typer commands that mirror client methods; pretty JSON output.
- `src/dpd_client/errors.py`: exceptions (`DPDError`, `DPDHTTPError`, `DPDDecodeError`, `DPDInvalidParam`).

**Tooling & Workflows**

- Manage dependencies and commands with `uv`.
- Lint/type (optional):
  - `uv run ruff check .`
  - `uv run mypy .`
- See `CHANGELOG.md` for notable changes; version is tracked in `pyproject.toml`.
- Do not publish yet; additional testing will be performed first.
