"""Chunking settings."""

from pydantic_settings import BaseSettings


class ChunkingSettings(BaseSettings):
    """Default values for specific chunking tasks."""

    DEFAULT_K_MIN: int = 220
    DEFAULT_K_MAX: int = 1000
    DEFAULT_MIN_MAX_GAP: int = 100
    DEFAULT_OVERLAP: int = 0
    DEFAULT_PAGES_OVERLAP: int = 100

    FAKE_PAGES_LENGTH: int = 1000
    MIN_INTERSECTION_LENGTH: int = 3
