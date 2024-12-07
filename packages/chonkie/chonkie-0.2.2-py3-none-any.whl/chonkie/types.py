"""Dataclasses for Chonkie."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    import numpy as np


@dataclass
class Context:
    """A dataclass representing contextual information for chunk refinement.

    This class stores text and token count information that can be used to add
    context to chunks during the refinement process. It can represent context
    that comes before or after a chunk.

    Attributes:
        text (str): The context text
        token_count (int): Number of tokens in the context text
        start_index (Optional[int]): Starting position of context in original text
        end_index (Optional[int]): Ending position of context in original text

    Example:
        context = Context(
            text="This is some context.",
            token_count=5,
            start_index=0,
            end_index=20
        )

    """

    text: str
    token_count: int
    start_index: Optional[int] = None
    end_index: Optional[int] = None

    def __post_init__(self):
        """Validate the Context attributes after initialization."""
        if not isinstance(self.text, str):
            raise ValueError("text must be a string")
        if not isinstance(self.token_count, int):
            raise ValueError("token_count must be an integer")
        if self.token_count < 0:
            raise ValueError("token_count must be non-negative")
        if (
            self.start_index is not None
            and self.end_index is not None
            and self.start_index > self.end_index
        ):
            raise ValueError("start_index must be less than or equal to end_index")

    def __len__(self) -> int:
        """Return the length of the context text."""
        return len(self.text)

    def __str__(self) -> str:
        """Return a string representation of the Context."""
        return self.text

    def __repr__(self) -> str:
        """Return a detailed string representation of the Context."""
        return (
            f"Context(text='{self.text}', token_count={self.token_count}, "
            f"start_index={self.start_index}, end_index={self.end_index})"
        )


@dataclass
class Chunk:
    """Dataclass representing a text chunk with metadata.

    All attributes are read-only via slots for performance reasons.

    Attributes:
        text: The text content of the chunk
        start_index: The starting index of the chunk in the original text
        end_index: The ending index of the chunk in the original text
        token_count: The number of tokens in the chunk
        context: The context of the chunk, useful for refinery classes

    """

    text: str
    start_index: int
    end_index: int
    token_count: int
    context: Optional[Context] = None

    def __str__(self) -> str:
        """Return string representation of the chunk."""
        return self.text

    def __len__(self) -> int:
        """Return the length of the chunk."""
        return len(self.text)

    def __repr__(self) -> str:
        """Return string representation of the chunk."""
        if self.context is not None:
            return (
                f"Chunk(text={self.text}, start_index={self.start_index}, "
                f"end_index={self.end_index}, token_count={self.token_count})"
            )
        else:
            return (
                f"Chunk(text={self.text}, start_index={self.start_index}, "
                f"end_index={self.end_index}, token_count={self.token_count}, "
                f"context={self.context})"
            )

    def __iter__(self):
        """Return an iterator over the chunk."""
        return iter(self.text)

    def __getitem__(self, index: int):
        """Return the item at the given index."""
        return self.text[index]

    def copy(self) -> "Chunk":
        """Return a deep copy of the chunk."""
        return Chunk(
            text=self.text,
            start_index=self.start_index,
            end_index=self.end_index,
            token_count=self.token_count,
        )


@dataclass
class Sentence:
    """Dataclass representing a sentence with metadata.

    All attributes are read-only via slots for performance reasons.

    Attributes:
        text: The text content of the sentence
        start_index: The starting index of the sentence in the original text
        end_index: The ending index of the sentence in the original text
        token_count: The number of tokens in the sentence

    """

    text: str
    start_index: int
    end_index: int
    token_count: int


@dataclass
class SentenceChunk(Chunk):
    """Dataclass representing a sentence chunk with metadata.

    All attributes are read-only via slots for performance reasons.

    Attributes:
        text: The text content of the chunk
        start_index: The starting index of the chunk in the original text
        end_index: The ending index of the chunk in the original text
        token_count: The number of tokens in the chunk
        sentences: List of Sentence objects in the chunk

    """

    # Don't redeclare inherited fields
    sentences: List[Sentence] = field(default_factory=list)


@dataclass
class SemanticSentence(Sentence):
    """Dataclass representing a semantic sentence with metadata.

    All attributes are read-only via slots for performance reasons.

    Attributes:
        text: The text content of the sentence
        start_index: The starting index of the sentence in the original text
        end_index: The ending index of the sentence in the original text
        token_count: The number of tokens in the sentence
        embedding: The sentence embedding

    """

    embedding: Optional["np.ndarray"] = field(default=None)


@dataclass
class SemanticChunk(SentenceChunk):
    """SemanticChunk dataclass representing a semantic chunk with metadata.

    All attributes are read-only via slots for performance reasons.

    Attributes:
        text: The text content of the chunk
        start_index: The starting index of the chunk in the original text
        end_index: The ending index of the chunk in the original text
        token_count: The number of tokens in the chunk
        sentences: List of SemanticSentence objects in the chunk

    """

    sentences: List[SemanticSentence] = field(default_factory=list)
