import time

import jwt

from gh_hooks_utils.logger import logger

_CERT_REQUIRED_ERR_MSG = "cert or cert_path must be provided"

_EXP_ERR_MSG = (
    "Expiration must be greater than 0 and lower than or equal to 600"
)

_INSTALL_ID_VALUE_ERR_MSG = "Github App installation id is required"


def get_auth_jwt(
    app_client_id: int,
    *,
    cert: bytes | None = None,
    cert_path: str | None = None,
    exp: int = 600,
) -> str:
    """Creates a jwt token for github app installations.

    You should either pass cert or cert_path. If none is provided, an ValueError will
    be raised.

    Args:
        app_client_id (int): The installation id for the github app
        cert (bytes, optional): The pem file of the github app. Defaults to None.
        cert_path (str, optional): The path of the pem file. Defaults to None.
        exp (int, optional): Token expiration. Must be less than 600. Defaults to 600.

    Raises:
        ValueError: Will raise a `ValueError` if:
            * If cert is not provided, neither the cert path
            * If installation id is `None`
            * If exp is lower than 1 or greater than 600

    Returns:
        str: The jwt signed with the cert, to be used in the authentication process.
    """
    logger.debug(f"Generating jwt for installation {app_client_id}")
    _raise_for_invalid_args(app_client_id, cert, cert_path, exp)

    signing_key = _get_cert(cert, cert_path)

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + exp,
        "iss": app_client_id,
    }

    return jwt.encode(payload, signing_key, algorithm="RS256")


def _raise_for_invalid_args(
    app_client_id: int,
    cert: bytes | None = None,
    cert_path: str | None = None,
    exp: int = 600,
) -> None:
    if not app_client_id:
        logger.error("No installation id was provided")
        raise ValueError(_INSTALL_ID_VALUE_ERR_MSG)

    if exp < 1 or exp > 600:
        logger.error("Expiration time is lower than 1 or greater than 600")
        raise ValueError(_EXP_ERR_MSG)

    if not cert and not cert_path:
        logger.error("Neither cert nor cert_path were provided")
        raise ValueError(_CERT_REQUIRED_ERR_MSG)


def _get_cert(cert: bytes | None, cert_path: str | None) -> bytes:
    if cert:
        logger.debug("Will use the cert provided")
        return cert

    logger.debug(
        f"No cert was provided. Will try to open cert from the cert path {cert_path}"
    )
    with open(str(cert_path), mode="rb") as f:
        return f.read()
