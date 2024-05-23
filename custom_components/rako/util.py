"""Utilities for Rako."""
from __future__ import annotations


def create_unique_id(
    bridge_id: str, device_type: str, device_id: int
) -> str:
    """Create Unique ID for devices."""
    return f"b:{bridge_id}t:{device_type}d:{device_id}"
