import json
import httpx
import respx

from dpd_client import DPDClient, DPDInvalidParam


@respx.mock
def test_drugproduct_by_din_normalizes_to_list():
    base = "https://health-products.canada.ca/api/drug/"
    route = respx.get(f"{base}drugproduct/").mock(
        return_value=httpx.Response(200, json={
            "drug_code": 2049,
            "drug_identification_number": "00326925",
            "brand_name": "SINEQUAN",
        })
    )
    client = DPDClient()
    try:
        items = client.drugproduct(din="00326925")
        assert len(items) == 1
        assert items[0].brand_name == "SINEQUAN"
        assert route.called
    finally:
        client.close()


def test_drugproduct_requires_a_filter():
    client = DPDClient()
    try:
        try:
            client.drugproduct()
        except DPDInvalidParam:
            pass
        else:
            raise AssertionError("Expected DPDInvalidParam")
    finally:
        client.close()

