from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence

from .errors import DPDInvalidParam
from .http import HTTPClient, AsyncHTTPClient
from .models import (
    ActiveIngredient,
    Company,
    DrugProduct,
    DosageForm,
    Packaging,
    PharmaceuticalStandard,
    RouteOfAdministration,
    Schedule,
    ProductStatus,
    TherapeuticClass,
    VeterinarySpecies,
)


BASE_URL = "https://health-products.canada.ca/api/drug/"


def _normalize_list(data: Any) -> list[dict[str, Any]]:
    if data is None:
        return []
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        # Some endpoints may return a single object
        return [data]
    return []


class DPDClient:
    """Synchronous client for Health Canada DPD API.

    Parameters
    - base_url: override API base URL (default: official endpoint)
    - lang: default language ('en' or 'fr')
    - timeout: request timeout in seconds
    - retries: max retry attempts for transient failures
    - user_agent: custom User-Agent header
    """

    def __init__(
        self,
        *,
        base_url: str = BASE_URL,
        lang: str = "en",
        timeout: float = 15.0,
        retries: int = 3,
        user_agent: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.default_lang = lang
        self._http = HTTPClient(self.base_url, timeout=timeout, max_retries=retries, user_agent=user_agent)

    def close(self) -> None:
        self._http.close()

    # ---------- Resource methods ----------
    def drugproduct(
        self,
        *,
        id: int | None = None,
        din: str | None = None,
        brandname: str | None = None,
        status: str | None = None,
        lang: str | None = None,
    ) -> list[DrugProduct]:
        if not any([id, din, brandname, status]):
            # API supports listing all, but that can be huge; require at least one filter
            raise DPDInvalidParam("Provide at least one of id, din, brandname, or status")
        params: dict[str, Any] = {"type": "json", "lang": lang or self.default_lang}
        if id is not None:
            params["id"] = id
        if din is not None:
            params["din"] = din
        if brandname is not None:
            params["brandname"] = brandname
        if status is not None:
            params["status"] = status
        data = self._http.get_json("drugproduct/", params)
        return [DrugProduct.model_validate(obj) for obj in _normalize_list(data)]

    def company(self, *, id: int, lang: str | None = None) -> list[Company]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = self._http.get_json("company/", params)
        return [Company.model_validate(obj) for obj in _normalize_list(data)]

    def activeingredient(
        self,
        *,
        id: int | None = None,
        ingredientname: str | None = None,
        lang: str | None = None,
    ) -> list[ActiveIngredient]:
        if id is None and ingredientname is None:
            raise DPDInvalidParam("Provide id or ingredientname for activeingredient")
        params: dict[str, Any] = {"type": "json", "lang": lang or self.default_lang}
        if id is not None:
            params["id"] = id
        if ingredientname is not None:
            params["ingredientname"] = ingredientname
        data = self._http.get_json("activeingredient/", params)
        return [ActiveIngredient.model_validate(obj) for obj in _normalize_list(data)]

    def form(self, *, id: int, active: bool | None = None, lang: str | None = None) -> list[DosageForm]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        if active:
            params["active"] = "yes"
        data = self._http.get_json("form/", params)
        return [DosageForm.model_validate(obj) for obj in _normalize_list(data)]

    def packaging(self, *, id: int) -> list[Packaging]:
        params: dict[str, Any] = {"id": id, "type": "json"}
        data = self._http.get_json("packaging/", params)
        return [Packaging.model_validate(obj) for obj in _normalize_list(data)]

    def pharmaceuticalstd(self, *, id: int) -> list[PharmaceuticalStandard]:
        params: dict[str, Any] = {"id": id, "type": "json"}
        data = self._http.get_json("pharmaceuticalstd/", params)
        return [PharmaceuticalStandard.model_validate(obj) for obj in _normalize_list(data)]

    def route(self, *, id: int, active: bool | None = None, lang: str | None = None) -> list[RouteOfAdministration]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        if active:
            params["active"] = "yes"
        data = self._http.get_json("route/", params)
        return [RouteOfAdministration.model_validate(obj) for obj in _normalize_list(data)]

    def schedule(self, *, id: int, active: bool | None = None, lang: str | None = None) -> list[Schedule]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        if active:
            params["active"] = "yes"
        data = self._http.get_json("schedule/", params)
        return [Schedule.model_validate(obj) for obj in _normalize_list(data)]

    def status(self, *, id: int, lang: str | None = None) -> list[ProductStatus]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = self._http.get_json("status/", params)
        return [ProductStatus.model_validate(obj) for obj in _normalize_list(data)]

    def therapeuticclass(self, *, id: int, lang: str | None = None) -> list[TherapeuticClass]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = self._http.get_json("therapeuticclass/", params)
        return [TherapeuticClass.model_validate(obj) for obj in _normalize_list(data)]

    def veterinaryspecies(self, *, id: int, lang: str | None = None) -> list[VeterinarySpecies]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = self._http.get_json("veterinaryspecies/", params)
        return [VeterinarySpecies.model_validate(obj) for obj in _normalize_list(data)]


class AsyncDPDClient:
    """Async client for Health Canada DPD API (httpx.AsyncClient based)."""

    def __init__(
        self,
        *,
        base_url: str = BASE_URL,
        lang: str = "en",
        timeout: float = 15.0,
        retries: int = 3,
        user_agent: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.default_lang = lang
        self._http = AsyncHTTPClient(self.base_url, timeout=timeout, max_retries=retries, user_agent=user_agent)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def drugproduct(
        self,
        *,
        id: int | None = None,
        din: str | None = None,
        brandname: str | None = None,
        status: str | None = None,
        lang: str | None = None,
    ) -> list[DrugProduct]:
        if not any([id, din, brandname, status]):
            raise DPDInvalidParam("Provide at least one of id, din, brandname, or status")
        params: dict[str, Any] = {"type": "json", "lang": lang or self.default_lang}
        if id is not None:
            params["id"] = id
        if din is not None:
            params["din"] = din
        if brandname is not None:
            params["brandname"] = brandname
        if status is not None:
            params["status"] = status
        data = await self._http.get_json("drugproduct/", params)
        return [DrugProduct.model_validate(obj) for obj in _normalize_list(data)]

    async def company(self, *, id: int, lang: str | None = None) -> list[Company]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = await self._http.get_json("company/", params)
        return [Company.model_validate(obj) for obj in _normalize_list(data)]

    async def activeingredient(
        self,
        *,
        id: int | None = None,
        ingredientname: str | None = None,
        lang: str | None = None,
    ) -> list[ActiveIngredient]:
        if id is None and ingredientname is None:
            raise DPDInvalidParam("Provide id or ingredientname for activeingredient")
        params: dict[str, Any] = {"type": "json", "lang": lang or self.default_lang}
        if id is not None:
            params["id"] = id
        if ingredientname is not None:
            params["ingredientname"] = ingredientname
        data = await self._http.get_json("activeingredient/", params)
        return [ActiveIngredient.model_validate(obj) for obj in _normalize_list(data)]

    async def form(self, *, id: int, active: bool | None = None, lang: str | None = None) -> list[DosageForm]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        if active:
            params["active"] = "yes"
        data = await self._http.get_json("form/", params)
        return [DosageForm.model_validate(obj) for obj in _normalize_list(data)]

    async def packaging(self, *, id: int) -> list[Packaging]:
        params: dict[str, Any] = {"id": id, "type": "json"}
        data = await self._http.get_json("packaging/", params)
        return [Packaging.model_validate(obj) for obj in _normalize_list(data)]

    async def pharmaceuticalstd(self, *, id: int) -> list[PharmaceuticalStandard]:
        params: dict[str, Any] = {"id": id, "type": "json"}
        data = await self._http.get_json("pharmaceuticalstd/", params)
        return [PharmaceuticalStandard.model_validate(obj) for obj in _normalize_list(data)]

    async def route(self, *, id: int, active: bool | None = None, lang: str | None = None) -> list[RouteOfAdministration]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        if active:
            params["active"] = "yes"
        data = await self._http.get_json("route/", params)
        return [RouteOfAdministration.model_validate(obj) for obj in _normalize_list(data)]

    async def schedule(self, *, id: int, active: bool | None = None, lang: str | None = None) -> list[Schedule]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        if active:
            params["active"] = "yes"
        data = await self._http.get_json("schedule/", params)
        return [Schedule.model_validate(obj) for obj in _normalize_list(data)]

    async def status(self, *, id: int, lang: str | None = None) -> list[ProductStatus]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = await self._http.get_json("status/", params)
        return [ProductStatus.model_validate(obj) for obj in _normalize_list(data)]

    async def therapeuticclass(self, *, id: int, lang: str | None = None) -> list[TherapeuticClass]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = await self._http.get_json("therapeuticclass/", params)
        return [TherapeuticClass.model_validate(obj) for obj in _normalize_list(data)]

    async def veterinaryspecies(self, *, id: int, lang: str | None = None) -> list[VeterinarySpecies]:
        params: dict[str, Any] = {"id": id, "type": "json", "lang": lang or self.default_lang}
        data = await self._http.get_json("veterinaryspecies/", params)
        return [VeterinarySpecies.model_validate(obj) for obj in _normalize_list(data)]
