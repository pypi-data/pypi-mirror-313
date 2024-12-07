import importlib
from typing import TYPE_CHECKING, List, Union

from chonkie.embeddings.base import BaseEmbeddings

if TYPE_CHECKING:
    import numpy as np
    from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddings(BaseEmbeddings):
    """Class for SentenceTransformer embeddings.

    This class provides an interface for the SentenceTransformer library, which
    provides a variety of pre-trained models for sentence embeddings. This is also
    the recommended way to use sentence-transformers in Chonkie.

    Args:
        model (str): Name of the SentenceTransformer model to load

    """

    def __init__(
        self, model: Union[str, "SentenceTransformer"] = "all-MiniLM-L6-v2", **kwargs
    ) -> None:
        """Initialize SentenceTransformerEmbeddings with a sentence-transformers model.

        Args:
            model (str): Name of the SentenceTransformer model to load
            **kwargs: Additional keyword arguments to pass to the SentenceTransformer constructor

        Raises:
            ImportError: If sentence-transformers is not available
            ValueError: If the model is not a string or SentenceTransformer instance

        """
        super().__init__()

        if not self.is_available():
            raise ImportError(
                "SentenceTransformer is not available. Please install it via pip."
            )
        else:
            global SentenceTransformer
            from sentence_transformers import SentenceTransformer

        if isinstance(model, str):
            self.model_name_or_path = model
            self.model = SentenceTransformer(self.model_name_or_path, **kwargs)
        elif isinstance(model, SentenceTransformer):
            self.model = model
            self.model_name_or_path = self.model.model_card_data.base_model
        else:
            raise ValueError("model must be a string or SentenceTransformer instance")

        self._dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> "np.ndarray":
        """Embed a single text using the sentence-transformers model."""
        return self.model.encode(text, convert_to_numpy=True)

    def embed_batch(self, texts: List[str]) -> List["np.ndarray"]:
        """Embed multiple texts using the sentence-transformers model."""
        return self.model.encode(texts, convert_to_numpy=True)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using the model's tokenizer."""
        return len(self.model.tokenizer.encode(text))

    def count_tokens_batch(self, texts: List[str]) -> List[int]:
        """Count tokens in multiple texts using the model's tokenizer."""
        encodings = self.model.tokenizer(texts)
        return [len(enc) for enc in encodings["input_ids"]]

    def similarity(self, u: "np.ndarray", v: "np.ndarray") -> float:
        """Compute cosine similarity between two embeddings."""
        return self.model.similarity(u, v).item()

    def get_tokenizer_or_token_counter(self):
        """Return the tokenizer or token counter object."""
        return self.model.tokenizer

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        return self._dimension

    @classmethod
    def is_available(cls) -> bool:
        """Check if sentence-transformers is available."""
        return importlib.util.find_spec("sentence_transformers") is not None

    def __repr__(self):
        """Representation of the SentenceTransformerEmbeddings instance."""
        return f"SentenceTransformerEmbeddings(model={self.model_name_or_path})"
