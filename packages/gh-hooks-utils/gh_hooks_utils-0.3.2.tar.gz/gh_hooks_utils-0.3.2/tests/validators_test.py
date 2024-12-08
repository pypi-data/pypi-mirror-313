from gh_hooks_utils import validators


def test_is_signature_valid_should_validate_incoming_raw_body_as_bytes():
    secret = "It's a Secret to Everybody"
    payload = b"Hello, World!"
    signature = "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"

    assert validators.is_signature_valid(payload, secret, signature)
