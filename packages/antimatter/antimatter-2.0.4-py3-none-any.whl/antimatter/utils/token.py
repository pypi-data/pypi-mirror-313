import base64
import cbor2
from datetime import datetime, timezone


def decode_token(t):
    """
    Decode a domain identity token and return the NotValidBefore and NotValidAfter timestamps.
    """
    if not t:
        return None, None
    try:
        decoded_bytes = base64.b64decode(t)
        if decoded_bytes[:7] == b"apikey:":
            # It is an API key, not a token, and we should invoke the refresh call.
            return None, None
        decoded_token = cbor2.loads(decoded_bytes)
        not_before = datetime.fromtimestamp(decoded_token.get("NotValidBefore"), timezone.utc)
        not_after = datetime.fromtimestamp(decoded_token.get("NotValidAfter"), timezone.utc)
    except:
        return None, None
    return not_before, not_after


def is_token_valid(not_before, not_after):
    """
    Check if the token is valid based on the NotValidBefore and NotValidAfter timestamps.
    """
    now_time = datetime.now(timezone.utc)
    return not_before and not_after and (not_before <= now_time <= not_after)
