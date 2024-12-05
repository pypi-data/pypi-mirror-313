from typing import Any, Dict, Optional

from huntflow_api_client.entities.base import (
    BaseEntity,
    CreateEntityMixin,
    DeleteEntityMixin,
    ListEntityMixin,
)
from huntflow_api_client.models.consts import WebhookType
from huntflow_api_client.models.request.webhooks import WebhookRequest
from huntflow_api_client.models.response.webhooks import WebhookResponse, WebhooksListResponse


class Webhook(BaseEntity, ListEntityMixin, CreateEntityMixin, DeleteEntityMixin):
    async def list(
        self,
        account_id: int,
        webhook_type: Optional[WebhookType] = None,
    ) -> WebhooksListResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/hooks

        :param account_id: Organization ID
        :param webhook_type: Webhook type. If no value provided, webhooks of all types will be
            returned.
        :return: List of webhooks
        """
        path = f"/accounts/{account_id}/hooks"
        params: Dict[str, Any] = {}
        if webhook_type:
            params["webhook_type"] = webhook_type.value
        response = await self._api.request("GET", path, params=params)
        return WebhooksListResponse.model_validate(response.json())

    async def create(self, account_id: int, data: WebhookRequest) -> WebhookResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/hooks

        :param account_id: Organization ID
        :param data: Dictionary with secret, url, active and webhook_events fields
        :return: Information about the webhook
        """
        path = f"/accounts/{account_id}/hooks"
        response = await self._api.request("POST", path, json=data.jsonable_dict(exclude_none=True))
        return WebhookResponse.model_validate(response.json())

    async def delete(self, account_id: int, webhook_id: int) -> None:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#delete-/accounts/-account_id-/hooks/-webhook_id-

        :param account_id: Organization ID
        :param webhook_id: Webhook ID
        """
        path = f"/accounts/{account_id}/hooks/{webhook_id}"
        await self._api.request("DELETE", path)
