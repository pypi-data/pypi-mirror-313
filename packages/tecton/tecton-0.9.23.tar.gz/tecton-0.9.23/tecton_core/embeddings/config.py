from __future__ import annotations

from enum import Enum

import attrs


class TextEmbeddingModel(str, Enum):
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"


@attrs.frozen
class TextEmbeddingInferenceConfig:
    input_column: str
    output_column: str
    model: TextEmbeddingModel
