from pathlib import Path

TARGET_HTTPX = "gh_hooks_utils.auth.app_auth.httpx.post"


def cert_bytes():
    with open(cert_path(), "rb") as f:
        return f.read()


def cert_path():
    return Path(__file__).resolve().parent / Path("key.pem")


def mock_post(url, headers):
    return MockResponse()


class MockResponse:
    def json(self):
        return {
            "token": "ghs_vKp4LOYGaq0JoiYTrEQiatBlJdyMzA1CaLPf",
            "expires_at": "2024-11-27T12:33:02Z",
            "permissions": {
                "contents": "read",
                "discussions": "read",
                "pull_requests": "read",
            },
            "repository_selection": "all",
        }
