from typing import Optional

from pydantic import BaseModel, Field


class NotificationWebhook(BaseModel):
    url: str
    per_order: bool = Field(default=False, description="If \'true\', webhook will be called when order completes.")


class OrderNotifications(BaseModel):
    webhook: Optional[NotificationWebhook] = Field(default=None,
        description="Details for calling your webhook. An OrderComponent will be POST\'ed to endpoint.")
    email: bool = Field(default=False, description='Send email to address associated with submitter account.')
