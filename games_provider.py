"""
games_provider.py — launch integration scaffold.

WHAT THIS FILE DOES ONCE WIRED UP:
  Calling launch_game(slug, player) will call your aggregator's real launch
  API and return a signed URL to the actual licensed game client (Aviator,
  Sweet Bonanza, whatever the provider maps 'slug' to). app.py embeds that
  URL in an iframe (see templates/game_play.html) or redirects to it.

WHAT'S MISSING:
  Everything inside launch_game() below is a placeholder. I need your
  aggregator's actual docs to fill in:
    - PROVIDER_BASE_URL          (their API host)
    - the exact launch endpoint path
    - the auth scheme (API key header? HMAC signature? JWT?)
    - the request payload shape (game code, currency, player id, return_url...)
    - the response shape (do they give back a full URL, or pieces to build one?)
    - how they map YOUR slugs (e.g. 'aviator') to THEIR internal game codes
      (e.g. 'spb_aviator' or a numeric id) — this mapping table below is a guess

Until real credentials/docs are provided, launch_game() raises
ProviderNotConfigured so the Flask route can fall back to the demo UI
instead of silently failing.
"""

import os
import time
import hmac
import hashlib
import requests

PROVIDER_BASE_URL = os.environ.get("PROVIDER_BASE_URL", "")
PROVIDER_API_KEY = os.environ.get("PROVIDER_API_KEY", "")
PROVIDER_API_SECRET = os.environ.get("PROVIDER_API_SECRET", "")
PROVIDER_OPERATOR_ID = os.environ.get("PROVIDER_OPERATOR_ID", "")

# TODO: replace with the real mapping the aggregator gives you between your
# slugs and their internal game identifiers. Left blank/guessed for now.
GAME_CODE_MAP = {
    "aviator": "TODO_PROVIDER_CODE",
    "jetx": "TODO_PROVIDER_CODE",
    "sweet-bonanza": "TODO_PROVIDER_CODE",
    "aviabet": "TODO_PROVIDER_CODE",
    # ... rest of GAMES catalog goes here once you have the provider's list
}


class ProviderNotConfigured(Exception):
    pass


class ProviderError(Exception):
    pass


def _sign_request(payload: dict) -> str:
    """
    PLACEHOLDER signature scheme — HMAC-SHA256 over a sorted query string is
    a common pattern (Pragmatic-style aggregators do this) but every provider
    differs. Replace with whatever their docs specify once you have them.
    """
    msg = "&".join(f"{k}={payload[k]}" for k in sorted(payload))
    return hmac.new(PROVIDER_API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()


def launch_game(slug: str, player_id: str, player_currency: str = "KES", return_url: str = ""):
    """
    Returns a dict: {"game_url": "<signed url to the real game client>"}

    Raises ProviderNotConfigured if credentials aren't set yet, so callers
    can fall back to the demo UI gracefully instead of crashing.
    """
    if not (PROVIDER_BASE_URL and PROVIDER_API_KEY and PROVIDER_API_SECRET):
        raise ProviderNotConfigured(
            "Provider credentials not set — PROVIDER_BASE_URL / PROVIDER_API_KEY / "
            "PROVIDER_API_SECRET env vars are empty. Fill these in once you have "
            "the aggregator's real credentials."
        )

    game_code = GAME_CODE_MAP.get(slug)
    if not game_code or game_code.startswith("TODO"):
        raise ProviderNotConfigured(f"No provider game code mapped for slug '{slug}' yet.")

    timestamp = int(time.time())
    payload = {
        "operator_id": PROVIDER_OPERATOR_ID,
        "api_key": PROVIDER_API_KEY,
        "game_code": game_code,
        "player_id": player_id,
        "currency": player_currency,
        "return_url": return_url,
        "timestamp": timestamp,
    }
    payload["signature"] = _sign_request(payload)

    # TODO: replace this path with the real launch endpoint from the docs.
    endpoint = f"{PROVIDER_BASE_URL}/api/v1/game/launch"

    try:
        resp = requests.post(endpoint, json=payload, timeout=8)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ProviderError(f"Launch request failed: {e}") from e

    data = resp.json()
    # TODO: adjust this to match the real response shape.
    game_url = data.get("game_url") or data.get("url")
    if not game_url:
        raise ProviderError(f"Launch response missing game_url: {data}")

    return {"game_url": game_url}
