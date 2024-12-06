from __future__ import annotations

from typing import Sequence, Type

import numpy as np
import pyarrow as pa

from chalk.features._embedding.embedding_provider import EmbeddingProvider
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import cohere
except ImportError:
    cohere = None

supported_models = [
    "embed-english-v3.0",
    "embed-multilingual-v3.0",
    "embed-english-light-v3.0",
    "embed-multilingual-light-v3.0",
]


class CohereProvider(EmbeddingProvider):
    def __init__(self, model: str) -> None:
        super().__init__()
        self.model = model
        if not cohere:
            raise missing_dependency_exception("chalkpy[cohere]")

        supported_models_str = ", ".join(f"'{model}'" for model in supported_models)
        assert (
            self.model in supported_models
        ), f"Unsupported model '{self.model}' for Cohere. The supported models are [{supported_models_str}]."

    def get_provider_name(self) -> str:
        return "Cohere"

    def get_model_name(self) -> str:
        return self.model

    def validate_input_schema(self, input_schema: Sequence[pa.DataType]) -> str | None:
        # Cohere requires two columns -- the data and the input type
        # For now not validating but will do so later
        return

    def generate_embedding(self, input: pa.Table) -> pa.FixedSizeListArray:
        assert cohere
        co = cohere.Client()
        text_input: list[str] = input.column(0).to_pylist()
        response = co.embed(texts=text_input, model=self.model, input_type="search_document")
        vectors = np.array(
            response.embeddings, dtype=np.dtype(self.get_vector_class().precision.replace("fp", "float"))
        )
        return pa.FixedSizeListArray.from_arrays(vectors.reshape(-1), self.get_vector_class().num_dimensions)

    def get_vector_class(self) -> Type[Vector]:
        if self.model in ["embed-english-v3.0", "embed-multilingual-v3.0"]:
            return Vector[1024]
        else:  # if self.model in ["embed-english-light-v3.0", "embed-multilingual-light-v3.0"]
            return Vector[384]
