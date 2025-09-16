import httpx
import respx

from dpd_client import DPDClient


@respx.mock
def test_route_active_flag_maps_to_yes():
    base = "https://health-products.canada.ca/api/drug/"
    route = respx.get(f"{base}route/").mock(
        return_value=httpx.Response(200, json=[
            {"drug_code": 3, "route_of_administration_code": 49, "route_of_administration_name": "Intravenous"}
        ])
    )
    client = DPDClient()
    try:
        items = client.route(id=3, active=True)
        assert len(items) == 1
        assert items[0].route_of_administration_name == "Intravenous"
        assert route.called
        # verify query includes active=yes
        last_call = route.calls.last
        assert "active=yes" in str(last_call.request.url)
    finally:
        client.close()


@respx.mock
def test_packaging_returns_list():
    base = "https://health-products.canada.ca/api/drug/"
    r = respx.get(f"{base}packaging/").mock(
        return_value=httpx.Response(200, json={
            "drug_code": 11685,
            "upc": "055599047240",
            "package_size_unit": "24",
            "package_type": "Blister Pack",
            "package_size": "Ea",
            "product_information": "",
        })
    )
    client = DPDClient()
    try:
        items = client.packaging(id=11685)
        assert len(items) == 1
        assert items[0].package_type == "Blister Pack"
        assert r.called
    finally:
        client.close()
