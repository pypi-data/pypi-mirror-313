"""Main package for Chonkie."""

from .chunker import (
    BaseChunker,
    SDPMChunker,
    SemanticChunker,
    SentenceChunker,
    TokenChunker,
    WordChunker,
)
from .embeddings import (
    AutoEmbeddings,
    BaseEmbeddings,
    Model2VecEmbeddings,
    OpenAIEmbeddings,
    SentenceTransformerEmbeddings,
)
from .refinery import (
    BaseRefinery,
    OverlapRefinery,
)
from .types import (
    Chunk,
    Context,
    SemanticChunk,
    SemanticSentence,
    Sentence,
    SentenceChunk,
)

__version__ = "0.2.2"
__name__ = "chonkie"
__author__ = "Bhavnick Minhas"

# Add basic package metadata to __all__
__all__ = [
    "__name__",
    "__version__",
    "__author__",
]

# Add all data classes to __all__
__all__ += [
    "Context",
    "Chunk",
    "SentenceChunk",
    "SemanticChunk",
    "Sentence",
    "SemanticSentence",
]

# Add all chunker classes to __all__
__all__ += [
    "BaseChunker",
    "TokenChunker",
    "WordChunker",
    "SentenceChunker",
    "SemanticChunker",
    "SDPMChunker",
]

# Add all embeddings classes to __all__
__all__ += [
    "BaseEmbeddings",
    "Model2VecEmbeddings",
    "SentenceTransformerEmbeddings",
    "OpenAIEmbeddings",
    "AutoEmbeddings",
]

# Add all refinery classes to __all__
__all__ += [
    "BaseRefinery",
    "OverlapRefinery",
]
