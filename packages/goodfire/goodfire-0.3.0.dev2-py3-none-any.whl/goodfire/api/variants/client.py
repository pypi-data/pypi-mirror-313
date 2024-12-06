from typing import Any, Optional

from pydantic import BaseModel

from ...api.constants import PRODUCTION_BASE_URL
from ...api.utils import AsyncHTTPWrapper
from ...features.features import Feature
from ...utils.asyncio import run_async_safely
from ...variants.fast import Variant


class VariantMetaData(BaseModel):
    name: str
    base_model: str
    id: str


class AsyncVariantsAPI:
    """Client for interacting with the Goodfire Variants API."""

    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.base_url = base_url
        self.api_key = api_key

        self._http = AsyncHTTPWrapper()

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def get(self, variant_id: str):
        """Get a model variant by ID."""
        url = f"{self.base_url}/api/inference/v1/model-variants/{variant_id}"
        headers = self._get_headers()
        response = await self._http.get(url, headers=headers)

        response_json = response.json()

        variant = Variant(
            response_json["base_model"],
        )

        if config := response_json.get("fastmodel_config"):
            for edit in config:
                variant.set(
                    Feature(
                        uuid=edit["feature_id"],
                        label=edit["feature_label"],
                        max_activation_strength=edit["max_activation_strength"],
                        index_in_sae=edit["index_in_sae"],
                    ),
                    edit["value"],
                    edit["mode"],
                )

        return variant

    async def list(self):
        """List all model variants."""
        url = f"{self.base_url}/api/inference/v1/model-variants/"
        headers = self._get_headers()
        response = await self._http.get(url, headers=headers)

        response_json = response.json()

        return [
            VariantMetaData(
                name=variant["name"],
                base_model=variant["base_model"],
                id=variant["id"],
            )
            for variant in response_json["model_variants"]
        ]

    async def create(self, variant: Variant, name: str):
        """Create a new model variant with the specified name."""
        payload: dict[str, Any] = {
            "tokens": [],
            "base_model": variant.base_model,
            "name": name,
        }

        payload["fastmodel_config"] = variant.json()["fastmodel_config"]

        url = f"{self.base_url}/api/inference/v1/model-variants/"
        headers = self._get_headers()
        response = await self._http.post(
            url,
            headers=headers,
            json=payload,
        )

        response_json = response.json()

        return response_json["id"]

    async def update(self, id: str, variant: Variant, new_name: Optional[str] = None):
        """Update an existing model variant."""
        payload: dict[str, Any] = {
            "tokens": [],
            "base_model": variant.base_model,
        }

        payload["fastmodel_config"] = variant.json()["fastmodel_config"]

        if new_name:
            payload["name"] = new_name

        url = f"{self.base_url}/api/inference/v1/model-variants/{id}"
        headers = self._get_headers()
        await self._http.put(
            url,
            headers=headers,
            json=payload,
        )

    async def delete(self, id: str):
        """Delete a model variant by ID."""
        url = f"{self.base_url}/api/inference/v1/model-variants/{id}"
        headers = self._get_headers()
        await self._http.delete(url, headers=headers)


class VariantsAPI:
    """Client for interacting with the Goodfire Variants API."""

    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self._async_client = AsyncVariantsAPI(api_key, base_url=base_url)

    def get(self, variant_id: str):
        return run_async_safely(self._async_client.get(variant_id))

    def list(self):
        return run_async_safely(self._async_client.list())

    def create(self, variant: Variant, name: str):
        return run_async_safely(self._async_client.create(variant, name))

    def update(self, id: str, variant: Variant, new_name: Optional[str] = None):
        return run_async_safely(self._async_client.update(id, variant, new_name))

    def delete(self, id: str):
        return run_async_safely(self._async_client.delete(id))
