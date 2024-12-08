from unittest import mock

from gh_hooks_utils.auth import app_auth

from .app_auth_mock import TARGET_HTTPX, cert_bytes, cert_path, mock_post


@mock.patch(TARGET_HTTPX, mock_post)
def test_authenticate_with_cert_bytes_should_return_jwt():
    token = app_auth.authenticate(1019212, app_client_id=102030, cert=cert_bytes())

    assert token is not None
    assert isinstance(token, dict)
    assert "token" in token


@mock.patch(TARGET_HTTPX, mock_post)
def test_authenticate_with_cert_path_should_return_jwt():
    token = app_auth.authenticate(1019212, app_client_id=102030, cert_path=cert_path())

    assert token is not None
    assert isinstance(token, dict)
    assert "token" in token


@mock.patch(TARGET_HTTPX, mock_post)
def test_authenticate_with_token_should_return_jwt():
    token = app_auth.authenticate(1019212, token="6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwib.SflKx_adQssw5c", exp=500)

    assert token is not None
    assert isinstance(token, dict)
    assert "token" in token
