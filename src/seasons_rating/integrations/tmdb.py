"""Simple integration with The Movie Database (TMDb) API."""
from __future__ import annotations

import os
from typing import Any

import requests

from seasons_rating import models

TMDB_API_URL = "https://api.themoviedb.org/3"


def _params() -> dict[str, Any]:
    """Build query parameters including the optional API key."""
    api_key = os.getenv("TMDB_API_KEY")
    return {"api_key": api_key} if api_key else {}


def fetch_show(tmdb_id: int) -> models.Show:
    """Fetch show information from TMDb and store it in models."""
    url = f"{TMDB_API_URL}/tv/{tmdb_id}"
    response = requests.get(url, params=_params())
    data = response.json()
    show = models.Show(
        tmdb_id=data["id"],
        name=data.get("name", ""),
        overview=data.get("overview"),
    )
    return models.save_show(show)


def fetch_season(tmdb_show_id: int, season_number: int) -> models.Season:
    """Fetch season information for a show from TMDb and store it."""
    url = f"{TMDB_API_URL}/tv/{tmdb_show_id}/season/{season_number}"
    response = requests.get(url, params=_params())
    data = response.json()
    season = models.Season(
        tmdb_id=data["id"],
        show_tmdb_id=tmdb_show_id,
        name=data.get("name", ""),
        season_number=data.get("season_number", season_number),
        overview=data.get("overview"),
    )
    return models.save_season(season)
