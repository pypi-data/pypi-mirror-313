"""Useful functions for handling SubChunks and Chunks."""

from uuid import uuid4

from llmax import tokens

from unichunking.types import Chunk, SubChunk


def subchunks_to_chunks(
    subchunks: list[SubChunk],
    file_hash: str = "",
) -> list[Chunk]:
    """Convert a SubChunk object to a Chunk object with the same content."""
    return [
        Chunk(
            chunk_num=i + 1,
            content=subchunks[i].content,
            metadata={
                "page": subchunks[i].page,
                "file_name": subchunks[i].file_name,
                "positions": [subchunks[i].position.to_dict()],
            },
            embedding=[0] * 1536,
            chunk_uid=uuid4(),
            file_hash=file_hash,
            num_tokens=tokens.count(subchunks[i].content),
        )
        for i in range(len(subchunks))
    ]


def compute_bbox(
    chunks: list[Chunk],
) -> dict[str, float]:
    """Compute the coordinates of the minimal bounding box for a list of chunks."""
    min_x0, min_y0, max_x1, max_y1 = 1, 1, 0, 0

    for chunk in chunks:
        positions = [chunk.metadata.get("bbox", [])]
        if not positions[0]:
            positions = chunk.metadata["positions"]
        for chunk_position in positions:
            min_x0 = max(0, min(min_x0, chunk_position["x0"]))
            min_y0 = max(0, min(min_y0, chunk_position["y0"]))
            max_x1 = min(1, max(max_x1, chunk_position["x1"]))
            max_y1 = min(1, max(max_y1, chunk_position["y1"]))

    return {
        "x0": min_x0,
        "y0": min_y0,
        "x1": max_x1,
        "y1": max_y1,
    }
