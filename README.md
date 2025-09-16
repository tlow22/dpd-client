# dpd-client

Python client and CLI for Health Canada Drug Product Database (DPD) API.

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
