"""Final return type for chunk objects."""

from typing import Any
from uuid import UUID


class Chunk:
    """Class for storing a piece of text and associated metadata.

    Fields:
        - chunk_num: The number of chunk inside the page.
        - content: Text of chunk.
        - metadata: {
                page : Number of page to which it belongs,
                file_name: Name of file,
                positions: Positions of all SubChunks inside the Chunk,
                bbox: Coordinates of the minimal bounding box for the Chunk, only exists if computed with dedicated function,
            },
        - embedding: Embedding of chunk text (not handled by unichunking package).
        - chunk_uid: Unique identifier of the chunk.
        - file_hash: File unique reference.
        - num_tokens: Number of tokens.
    """

    def __init__(
        self: "Chunk",
        chunk_num: int,
        content: str,
        metadata: dict[str, Any],
        embedding: list[float],
        chunk_uid: UUID,
        file_hash: str,
        num_tokens: int,
    ) -> None:
        """Create a Chunk object."""
        self.chunk_num = chunk_num
        self.content = content
        self.metadata = metadata
        self.embedding = embedding
        self.chunk_uid = chunk_uid
        self.file_hash = file_hash
        self.num_tokens = num_tokens

    def to_dict(
        self: "Chunk",
        as_subchunk: bool = False,
    ) -> dict[str, str | int | dict[str, dict[str, float] | list[dict[str, float]]]]:
        """Converts a Chunk object to a dictionary."""
        output_dict = {
            "content": self.content,
            "size": self.num_tokens,
            "page": self.metadata["page"],
        }

        if as_subchunk:
            output_dict["position"] = self.metadata["positions"][0]

        else:
            output_dict["position"] = {
                "bbox": self.metadata["bbox"],
                "subchunks": self.metadata["positions"],
            }
        return output_dict
