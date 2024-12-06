"""Data classes for PetKit API"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Any


@dataclass
class PetKitData:
    """Dataclass for all PetKit Data."""

    user_id: str
    feeders: dict[int, Any] | None = None
    litter_boxes: dict[int, Any] | None = None
    water_fountains: dict[int, Fountain] | None = None
    pets: dict[int, Pet] | None = None
    purifiers: dict[int, Purifier] | None = None


@dataclass
class Feeder:
    """Dataclass for PetKit Feeders."""

    id: int
    data: dict[str, Any]
    device_record: dict[str, Any]
    type: str
    sound_list: dict[int, str] | None = None
    last_manual_feed_id: str | None = None


@dataclass
class LitterBox:
    """Dataclass for PetKit Litter Boxes."""

    id: int
    device_detail: dict[str, Any]
    device_record: dict[str, Any]
    statistics: dict[str, Any]
    type: str
    manually_paused: bool
    manual_pause_end: datetime | None = None


@dataclass
class Purifier:
    """Dataclass for PetKit Purifiers."""

    id: int
    device_detail: dict[str, Any]
    type: str


@dataclass
class Fountain:
    """Dataclass for Water Fountain."""

    id: int
    data: dict[str, Any]
    type: str
    group_relay: bool
    ble_relay: int | None = None


@dataclass
class Pet:
    """Dataclass for registered pets."""

    id: int
    data: dict[str, Any]
    type: str
