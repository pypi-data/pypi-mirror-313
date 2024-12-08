import pytest
from pydantic import ValidationError

from gh_hooks_utils.headers.headers import (
    _INVALID_EVENT_MSG,
    _INVALID_USER_AGENT_MSG,
    _USER_AGENT_PREFIX,
    WebhookHeaders,
)


def test_user_agent_should_start_with_github_hookshot():
    with pytest.raises(ValidationError, match=_INVALID_USER_AGENT_MSG):
        WebhookHeaders(
            x_github_hook_id="321",
            x_github_event="pull_request",
            x_github_delivery="4321",
            x_hub_signature="sig",
            x_hub_signature_256="sig",
            user_agent="requests/",
            x_github_hook_installation_target_type="type",
            x_github_hook_installation_target_id="id",
        )


def test_x_github_event_must_be_a_known_event():
    with pytest.raises(ValidationError, match=_INVALID_EVENT_MSG):
        WebhookHeaders(
            x_github_hook_id="321",
            x_github_event="beer_opened",
            x_github_delivery="4321",
            x_hub_signature="sig",
            x_hub_signature_256="sig",
            user_agent=_USER_AGENT_PREFIX,
            x_github_hook_installation_target_type="type",
            x_github_hook_installation_target_id="id",
        )
