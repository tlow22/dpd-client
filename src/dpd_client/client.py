from __future__ import annotations

from typing import Any, Dict, List

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
from .params import (
    base_params as _base_params,
    params_with_id_lang as _params_with_id_lang,
    params_with_id_lang_active as _params_with_id_lang_active,
    params_packaging as _params_packaging,
    params_pharmaceuticalstd as _params_pharmaceuticalstd,
    params_drugproduct as _params_drugproduct,
    params_activeingredient as _params_activeingredient,
)


BASE_URL = "https://health-products.canada.ca/api/drug/"


def _normalize_list(data: Any) -> List[Dict[str, Any]]:
    if data is None:
        return []
    if isinstance(data, List):
        return [x for x in data if isinstance(x, Dict)]
    if isinstance(data, Dict):
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
        cache_ttl: float | int | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.default_lang = lang
        self._http = HTTPClient(
            self.base_url,
            timeout=timeout,
            max_retries=retries,
            user_agent=user_agent,
            cache_ttl=cache_ttl,
        )

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
    ) -> List[DrugProduct]:
        params = _params_drugproduct(
            self.default_lang, id=id, din=din, brandname=brandname, status=status, lang=lang
        )
        data = self._http.get_json("drugproduct/", params)
        return [DrugProduct.model_validate(obj) for obj in _normalize_list(data)]

    def company(self, *, id: int, lang: str | None = None) -> List[Company]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = self._http.get_json("company/", params)
        return [Company.model_validate(obj) for obj in _normalize_list(data)]

    def activeingredient(
        self,
        *,
        id: int | None = None,
        ingredientname: str | None = None,
        lang: str | None = None,
    ) -> List[ActiveIngredient]:
        params = _params_activeingredient(
            self.default_lang, id=id, ingredientname=ingredientname, lang=lang
        )
        data = self._http.get_json("activeingredient/", params)
        return [ActiveIngredient.model_validate(obj) for obj in _normalize_list(data)]

    def form(self, *, id: int, active: bool | None = None, lang: str | None = None) -> List[DosageForm]:
        params = _params_with_id_lang_active(self.default_lang, id=id, active=active, lang=lang)
        data = self._http.get_json("form/", params)
        return [DosageForm.model_validate(obj) for obj in _normalize_list(data)]

    def packaging(self, *, id: int) -> List[Packaging]:
        params = _params_packaging(id)
        data = self._http.get_json("packaging/", params)
        return [Packaging.model_validate(obj) for obj in _normalize_list(data)]

    def pharmaceuticalstd(self, *, id: int) -> List[PharmaceuticalStandard]:
        params = _params_pharmaceuticalstd(id)
        data = self._http.get_json("pharmaceuticalstd/", params)
        return [PharmaceuticalStandard.model_validate(obj) for obj in _normalize_list(data)]

    def route(self, *, id: int, active: bool | None = None, lang: str | None = None) -> List[RouteOfAdministration]:
        params = _params_with_id_lang_active(self.default_lang, id=id, active=active, lang=lang)
        data = self._http.get_json("route/", params)
        return [RouteOfAdministration.model_validate(obj) for obj in _normalize_list(data)]

    def schedule(self, *, id: int, active: bool | None = None, lang: str | None = None) -> List[Schedule]:
        params = _params_with_id_lang_active(self.default_lang, id=id, active=active, lang=lang)
        data = self._http.get_json("schedule/", params)
        return [Schedule.model_validate(obj) for obj in _normalize_list(data)]

    def status(self, *, id: int, lang: str | None = None) -> List[ProductStatus]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = self._http.get_json("status/", params)
        return [ProductStatus.model_validate(obj) for obj in _normalize_list(data)]

    def therapeuticclass(self, *, id: int, lang: str | None = None) -> List[TherapeuticClass]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = self._http.get_json("therapeuticclass/", params)
        return [TherapeuticClass.model_validate(obj) for obj in _normalize_list(data)]

    def veterinaryspecies(self, *, id: int, lang: str | None = None) -> List[VeterinarySpecies]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
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
        cache_ttl: float | int | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.default_lang = lang
        self._http = AsyncHTTPClient(
            self.base_url,
            timeout=timeout,
            max_retries=retries,
            user_agent=user_agent,
            cache_ttl=cache_ttl,
        )

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
    ) -> List[DrugProduct]:
        params = _params_drugproduct(
            self.default_lang, id=id, din=din, brandname=brandname, status=status, lang=lang
        )
        data = await self._http.get_json("drugproduct/", params)
        return [DrugProduct.model_validate(obj) for obj in _normalize_list(data)]

    async def company(self, *, id: int, lang: str | None = None) -> List[Company]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = await self._http.get_json("company/", params)
        return [Company.model_validate(obj) for obj in _normalize_list(data)]

    async def activeingredient(
        self,
        *,
        id: int | None = None,
        ingredientname: str | None = None,
        lang: str | None = None,
    ) -> List[ActiveIngredient]:
        params = _params_activeingredient(
            self.default_lang, id=id, ingredientname=ingredientname, lang=lang
        )
        data = await self._http.get_json("activeingredient/", params)
        return [ActiveIngredient.model_validate(obj) for obj in _normalize_list(data)]

    async def form(self, *, id: int, active: bool | None = None, lang: str | None = None) -> List[DosageForm]:
        params = _params_with_id_lang_active(self.default_lang, id=id, active=active, lang=lang)
        data = await self._http.get_json("form/", params)
        return [DosageForm.model_validate(obj) for obj in _normalize_list(data)]

    async def packaging(self, *, id: int) -> List[Packaging]:
        params = _params_packaging(id)
        data = await self._http.get_json("packaging/", params)
        return [Packaging.model_validate(obj) for obj in _normalize_list(data)]

    async def pharmaceuticalstd(self, *, id: int) -> List[PharmaceuticalStandard]:
        params = _params_pharmaceuticalstd(id)
        data = await self._http.get_json("pharmaceuticalstd/", params)
        return [PharmaceuticalStandard.model_validate(obj) for obj in _normalize_list(data)]

    async def route(self, *, id: int, active: bool | None = None, lang: str | None = None) -> List[RouteOfAdministration]:
        params = _params_with_id_lang_active(self.default_lang, id=id, active=active, lang=lang)
        data = await self._http.get_json("route/", params)
        return [RouteOfAdministration.model_validate(obj) for obj in _normalize_list(data)]

    async def schedule(self, *, id: int, active: bool | None = None, lang: str | None = None) -> List[Schedule]:
        params = _params_with_id_lang_active(self.default_lang, id=id, active=active, lang=lang)
        data = await self._http.get_json("schedule/", params)
        return [Schedule.model_validate(obj) for obj in _normalize_list(data)]

    async def status(self, *, id: int, lang: str | None = None) -> List[ProductStatus]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = await self._http.get_json("status/", params)
        return [ProductStatus.model_validate(obj) for obj in _normalize_list(data)]

    async def therapeuticclass(self, *, id: int, lang: str | None = None) -> List[TherapeuticClass]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = await self._http.get_json("therapeuticclass/", params)
        return [TherapeuticClass.model_validate(obj) for obj in _normalize_list(data)]

    async def veterinaryspecies(self, *, id: int, lang: str | None = None) -> List[VeterinarySpecies]:
        params = _params_with_id_lang(self.default_lang, id=id, lang=lang)
        data = await self._http.get_json("veterinaryspecies/", params)
        return [VeterinarySpecies.model_validate(obj) for obj in _normalize_list(data)]
