from typing import Any

import httpx

from gh_hooks_utils.logger import logger

from .token import get_auth_jwt

_url = (
    "https://api.github.com/app/installations/{installation_id}/access_tokens"
)

_headers = {
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json",
}


def authenticate(
    installation_id: int,
    *,
    app_client_id: int | None = None,
    token: str | None = None,
    cert: bytes | None = None,
    cert_path: str | None = None,
    exp: int = 300,
) -> dict[str, Any]:
    """Authenticates on Github with the installation id.

    Args:
        installation_id (int): The installation id. It's the identification of
            the instalation in the organization or account.
        app_client_id (int, optional): The app id. It's the fixed id generated
            for the app itself. It's only needed if you don't provide a signed
            token. Defaults to `None`.
        token (str, optional): A signed token with the github app client id.
            It's only required if the app client id is not provided. Defaults
                to `None`.
        cert (bytes, optional): The certificate in bytes. Defaults to
            `None`.
        cert_path (str, optional): The app certificate path. If both `cert` and
            `cert_path` are informed, the `cert_path` will be ignored. Defaults
                to `None`.
        exp (int, optional): The expiration of the github token. Needs to be
            greater than `1` and lower or equal to `600`. Defaults to `300`.

    Examples:
        1. You can call authenticate with the installation_id and and token:

        >>> token = "eyJlbW.bXTzIgo1Nz1zMTQxNn0.RtB8Yjui1Q"
        >>> authenticate(11111111, token=token, exp=100)
        {'token': 'ghs_l71cF2fpzwQ', 'expires_at': '2024-11-26T11:50:13Z', 'permissions': {'contents': 'read'}, 'repository_selection': 'all'}

        2. You can call authenticate with the installation_id, app_client_id and
        cert:

        >>> with open('mycert.pem', 'rb') as f:
        >>>     cert = f.read()
        >>> authenticate(11111111, app_client_id=11111111, cert=cert)
        {'token': 'ghs_l71cF2fpzwQ', 'expires_at': '2024-11-26T11:50:13Z', 'permissions': {'contents': 'read'}, 'repository_selection': 'all'}

        3. You can call authenticate with the installation_id, app_client_id and
        the cert's path:

        >>> authenticate(11111111, app_client_id=11111111, cert_path='mycert.pem')
        {'token': 'ghs_l71cF2fpzwQ', 'expires_at': '2024-11-26T11:50:13Z', 'permissions': {'contents': 'read'}, 'repository_selection': 'all'}

    Returns:
        dict[str, Any]: A `dict` containing the authenticated `JWT`.
    """
    logger.debug(f"Authenticating with installation {installation_id}")
    url = _url.format(installation_id=installation_id)

    _token = _get_token(app_client_id, token, cert, cert_path, exp)

    headers = {**_headers, "Authorization": f"Bearer {_token}"}

    r = httpx.post(url, headers=headers)

    return r.json()


def _get_token(
    app_client_id: int | None = None,
    token: str | None = None,
    cert: bytes | None = None,
    cert_path: str | None = None,
    exp: int = 300,
) -> str:
    if token:
        return token

    logger.debug("No jwt was provided. Creating token with the provided cert")

    if app_client_id and isinstance(app_client_id, int):
        return get_auth_jwt(
            app_client_id, cert=cert, cert_path=cert_path, exp=exp
        )

    raise ValueError("Either token or app_client_id are required")
