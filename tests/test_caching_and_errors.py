import httpx
import pytest
import respx

from dpd_client import DPDClient, AsyncDPDClient, DPDHTTPError, DPDDecodeError


@respx.mock
def test_sync_caching_prevents_second_request():
    base = "https://health-products.canada.ca/api/drug/"
    route = respx.get(f"{base}drugproduct/").mock(
        return_value=httpx.Response(200, json={
            "drug_code": 1,
            "drug_identification_number": "00000000",
            "brand_name": "X",
        })
    )
    client = DPDClient(cache_ttl=60)
    try:
        a = client.drugproduct(din="00000000")
        b = client.drugproduct(din="00000000")
        assert len(a) == len(b) == 1
        assert route.call_count == 1
    finally:
        client.close()


@respx.mock
def test_sync_404_raises_http_error():
    base = "https://health-products.canada.ca/api/drug/"
    respx.get(f"{base}drugproduct/").mock(return_value=httpx.Response(404, text="not found"))
    client = DPDClient()
    try:
        with pytest.raises(DPDHTTPError):
            client.drugproduct(din="doesnotexist")
    finally:
        client.close()


@respx.mock
def test_sync_decode_error():
    base = "https://health-products.canada.ca/api/drug/"
    respx.get(f"{base}drugproduct/").mock(return_value=httpx.Response(200, text="not json"))
    client = DPDClient()
    try:
        with pytest.raises(DPDDecodeError):
            client.drugproduct(din="00326925")
    finally:
        client.close()


@respx.mock
def test_sync_retries_on_5xx_then_succeeds():
    base = "https://health-products.canada.ca/api/drug/"
    seq = [
        httpx.Response(500, text="err1"),
        httpx.Response(502, text="err2"),
        httpx.Response(200, json=[{"drug_code": 2, "drug_identification_number": "11111111"}]),
    ]
    r = respx.get(f"{base}drugproduct/").mock(side_effect=seq)
    client = DPDClient(retries=3)
    try:
        items = client.drugproduct(din="11111111")
        assert len(items) == 1
        assert r.call_count == 3
    finally:
        client.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_client_basic_call():
    base = "https://health-products.canada.ca/api/drug/"
    respx.get(f"{base}company/").mock(return_value=httpx.Response(200, json=[{"company_code": 1, "company_name": "ACME"}]))
    client = AsyncDPDClient()
    try:
        items = await client.company(id=1)
        assert len(items) == 1
        assert items[0].company_name == "ACME"
    finally:
        await client.aclose()

