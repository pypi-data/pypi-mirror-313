from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
)

from .events import KNOWN_EVENTS

_INVALID_USER_AGENT_MSG = "An invalid user agent was received."

_INVALID_EVENT_MSG = "An invalid event was received."

_USER_AGENT_PREFIX = "GitHub-Hookshot/"

_X_HUB_SIGNATURE_DESCRIPTION = """This header is sent if the webhook
is configured with a secret. This is the HMAC hex digest of the request
body, and is generated  using the SHA-1 hash function and the secret as
the HMAC key. X-Hub-Signature is provided for compatibility with existing
integrations. We recommend that you use the more secure X-Hub-Signature-256
instead.
"""

_X_HUB_SIGNATURE_256_DESCRIPTION = """This header is sent if the webhook is
configured with a secret. This is the HMAC hex digest of the request body,
and is generated using the SHA-256 hash function and the secret as the HMAC key.
"""


class WebhookHeaders(BaseModel):
    """Headers sent by Github Webhooks.

    For more information, see `Webhook events and payloads`_

    .. _Webhook events and payloads:
       https://docs.github.com/en/webhooks/webhook-events-and-payloads
    """

    x_github_hook_id: str = Field(
        ..., description="The unique identifier of the webhook."
    )
    x_github_event: str = Field(
        ..., description="The name of the event that triggered the delivery."
    )
    x_github_delivery: str = Field(
        ...,
        description="A globally unique identifier (GUID) to identify the event.",
    )
    x_hub_signature: str | None = Field(
        None, description=_X_HUB_SIGNATURE_DESCRIPTION
    )
    x_hub_signature_256: str | None = Field(
        None, description=_X_HUB_SIGNATURE_256_DESCRIPTION
    )
    user_agent: str = Field(
        ...,
        description="This header will always have the prefix GitHub-Hookshot/",
    )
    x_github_hook_installation_target_type: str = Field(
        ..., description=" The type of resource where the webhook was created."
    )
    x_github_hook_installation_target_id: str = Field(
        ...,
        description="The unique identifier of the resource where the webhook was created.",
    )

    @field_validator("user_agent")
    def validate_user_agent(cls, v: str, _: ValidationInfo) -> str:
        if not v.startswith(_USER_AGENT_PREFIX):
            raise ValueError(_INVALID_USER_AGENT_MSG)

        return v

    @field_validator("x_github_event")
    def validate_known_event(cls, v: str, _: ValidationInfo) -> str:
        if v not in KNOWN_EVENTS:
            raise ValueError(_INVALID_EVENT_MSG)

        return v
