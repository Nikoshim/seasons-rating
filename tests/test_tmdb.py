from __future__ import annotations

from seasons_rating.integrations.tmdb import fetch_show, fetch_season
from seasons_rating import models


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def test_fetch_show(monkeypatch):
    data = {
        "id": 1399,
        "name": "Game of Thrones",
        "overview": "Seven noble families fight...",
    }

    def fake_get(url, params=None):
        assert url.endswith("/tv/1399")
        return DummyResponse(data)

    monkeypatch.setattr("seasons_rating.integrations.tmdb.requests.get", fake_get)
    models.SHOWS.clear()
    show = fetch_show(1399)
    assert show.tmdb_id == 1399
    assert show.name == "Game of Thrones"
    assert models.SHOWS[1399] == show


def test_fetch_season(monkeypatch):
    show_data = {
        "id": 1399,
        "name": "Game of Thrones",
    }
    season_data = {
        "id": 3627,
        "name": "Season 1",
        "season_number": 1,
        "overview": "The first season.",
    }

    def fake_get_show(url, params=None):
        return DummyResponse(show_data)

    models.SHOWS.clear()
    models.SEASONS.clear()
    monkeypatch.setattr("seasons_rating.integrations.tmdb.requests.get", fake_get_show)
    fetch_show(1399)

    def fake_get_season(url, params=None):
        assert url.endswith("/tv/1399/season/1")
        return DummyResponse(season_data)

    monkeypatch.setattr("seasons_rating.integrations.tmdb.requests.get", fake_get_season)
    season = fetch_season(1399, 1)
    assert season.tmdb_id == 3627
    assert season.name == "Season 1"
    assert models.SEASONS[(1399, 1)] == season
    assert models.SHOWS[1399].seasons[0] == season
