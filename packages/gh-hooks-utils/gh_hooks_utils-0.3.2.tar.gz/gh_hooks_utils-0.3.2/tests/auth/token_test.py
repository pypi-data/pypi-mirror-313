from pathlib import Path

import pytest

from gh_hooks_utils.auth import token


def test_get_auth_token_should_generate_jwt_if_a_cert_bytes_is_passed():
    cert_path = Path(__file__).resolve().parent / Path("key.pem")
    with open(cert_path, "rb") as f:
        cert = f.read()

    jwt = token.get_auth_jwt(101101, cert=cert)

    assert jwt is not None
    assert isinstance(jwt, str)
    assert len(jwt.split(".")) == 3


def test_get_auth_token_should_generate_jwt_if_a_cert_path_is_passed():
    cert_path = Path(__file__).resolve().parent / Path("key.pem")
    jwt = token.get_auth_jwt(101101, cert_path=cert_path)

    assert jwt is not None
    assert isinstance(jwt, str)
    assert len(jwt.split(".")) == 3


def test_get_auth_token_should_raise_value_error_if_installation_id_is_none():
    with pytest.raises(ValueError, match=token._INSTALL_ID_VALUE_ERR_MSG):
        token.get_auth_jwt(None)


def test_get_auth_token_should_raise_value_error_if_exp_is_lower_than_1_or_greater_than_600():
    with pytest.raises(ValueError, match=token._EXP_ERR_MSG):
        token.get_auth_jwt(101010, exp=-1)

    with pytest.raises(ValueError, match=token._EXP_ERR_MSG):
        token.get_auth_jwt(101010, exp=999)


def test_get_auth_token_should_raise_value_error_if_no_cert_or_cert_path_is_provided():
    with pytest.raises(ValueError, match=token._CERT_REQUIRED_ERR_MSG):
        token.get_auth_jwt(101010, exp=100)
