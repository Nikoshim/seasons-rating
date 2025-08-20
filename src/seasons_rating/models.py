from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class Episode:
    tmdb_id: int
    name: str
    episode_number: int
    overview: str | None = None

@dataclass
class Season:
    tmdb_id: int
    show_tmdb_id: int
    name: str
    season_number: int
    overview: str | None = None
    episodes: List[Episode] = field(default_factory=list)

@dataclass
class Show:
    tmdb_id: int
    name: str
    overview: str | None = None
    seasons: List[Season] = field(default_factory=list)

SHOWS: Dict[int, Show] = {}
SEASONS: Dict[Tuple[int, int], Season] = {}


def save_show(show: Show) -> Show:
    """Save a show in the in-memory store."""
    SHOWS[show.tmdb_id] = show
    return show


def save_season(season: Season) -> Season:
    """Save a season in the in-memory store and attach to its show."""
    SEASONS[(season.show_tmdb_id, season.season_number)] = season
    show = SHOWS.setdefault(season.show_tmdb_id, Show(tmdb_id=season.show_tmdb_id, name=""))
    show.seasons.append(season)
    return season
