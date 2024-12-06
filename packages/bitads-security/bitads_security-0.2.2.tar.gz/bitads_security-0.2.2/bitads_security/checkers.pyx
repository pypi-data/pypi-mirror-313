# sensitive_module.pyx

import base64
import hmac
import json
import os
from hashlib import sha256

# Secret key for HMAC
SECRET_KEY = bytes(
    os.environ.get(
        "SECRET_KEY", "super_secret_key_change_this_to_something_random_and_secure"
    )
)
NUM_ITERATIONS = int(os.environ.get("NUM_ITERATION", 777))


def check_hash(
    x_unique_id: str = "",
    x_signature: str = None,
    campaign_id: str = "",
    body: dict = None,
    sep: str = "",
) -> bool:
    if body:
        body = dict(sorted(body.items()))
    data = (
        base64.b64encode(json.dumps(body, separators=(",", ":")).encode())
        if body
        else b""
    )

    data_string = sep.join([x_unique_id, campaign_id, data.decode()])

    # Extract hash and salt from the signature
    if x_signature:
        try:
            provided_hash, salt = x_signature.split(":")
        except ValueError:
            return False
    else:
        return False

    # Recompute the hash using the provided salt
    hmac_hash = hmac.new(SECRET_KEY, (data_string + salt).encode(), sha256).hexdigest()
    final_hash = hmac_hash
    for _ in range(NUM_ITERATIONS):
        final_hash = sha256(final_hash.encode()).hexdigest()

    return provided_hash == final_hash
