"""Primary types used during subchunks extraction."""

import re
from typing import Literal


class ChunkPosition:
    """Class for handling positioning information during subchunks/chunks extraction."""

    x0: float
    y0: float
    x1: float
    y1: float

    def __init__(
        self: "ChunkPosition",
        x0: float,
        y0: float,
        x1: float,
        y1: float,
    ) -> None:
        """Create a ChunkPosition object."""
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def __add__(
        self: "ChunkPosition",
        other: "ChunkPosition",
    ) -> "ChunkPosition":
        """Adds two items' positions."""
        return ChunkPosition(
            x0=min(self.x0, other.x0),
            y0=min(self.y0, other.y0),
            x1=max(self.x1, other.x1),
            y1=max(self.y1, other.y1),
        )

    def to_dict(self: "ChunkPosition") -> dict[str, float]:
        """Convert ChunkPosition to a dictionary."""
        return {
            "x0": self.x0,
            "y0": self.y0,
            "x1": self.x1,
            "y1": self.y1,
        }


class SubChunk:
    """Class for handling subchunks extraction when reading different file formats."""

    subchunk_id: int
    content: str
    page: int
    position: ChunkPosition
    file_name: str
    content_type: Literal["text", "table", "image"]

    def __init__(
        self: "SubChunk",
        subchunk_id: int,
        content: str,
        page: int,
        position: ChunkPosition,
        file_name: str,
        content_type: Literal["text", "table", "image"] = "text",
    ) -> None:
        """Create a SubChunk object."""
        self.subchunk_id = subchunk_id
        self.content = content
        self.page = page
        self.position = position
        self.file_name = file_name
        self.content_type = content_type

    def __add__(self: "SubChunk", other: "SubChunk") -> "SubChunk":
        """Adds two SubChunk objects together."""
        content = self.content + " " + other.content
        re.sub(r"\s{2,}", " ", content)
        return SubChunk(
            subchunk_id=self.subchunk_id,
            content=content,
            page=min(self.page, other.page),
            position=self.position + other.position,
            file_name=self.file_name,
            content_type=self.content_type,
        )

    def __str__(self: "SubChunk") -> str:
        """Str representation of the object."""
        return self.content

    def __repr__(self: "SubChunk") -> str:
        """Str representation of the object."""
        return self.content + " " + self.content_type
