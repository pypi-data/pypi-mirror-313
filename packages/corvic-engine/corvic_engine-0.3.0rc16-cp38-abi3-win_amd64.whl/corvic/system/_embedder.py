import dataclasses
from collections.abc import Sequence
from typing import Any, Literal

import numpy as np
import polars as pl
from typing_extensions import Protocol

from corvic.result import InternalError, InvalidArgumentError, Ok


@dataclasses.dataclass
class EmbedTextContext:
    """Data to be embedded and arguments to describe how to embed them."""

    inputs: Sequence[str] | pl.Series
    model_name: str
    tokenizer_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: Literal[32, 64]


@dataclasses.dataclass
class EmbedTextResult:
    """The result of running text embedding on an EmbedTextContext."""

    context: EmbedTextContext
    embeddings: pl.Series


class TextEmbedder(Protocol):
    """Use a model to embed text."""

    def embed(
        self, context: EmbedTextContext
    ) -> Ok[EmbedTextResult] | InvalidArgumentError | InternalError: ...


@dataclasses.dataclass
class EmbedImageContext:
    """Data to be embedded and arguments to describe how to embed them."""

    inputs: Sequence[bytes] | pl.Series
    model_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: Literal[32, 64]


@dataclasses.dataclass
class EmbedImageResult:
    """The result of running Image embedding on an EmbedImageContext."""

    context: EmbedImageContext
    embeddings: pl.Series


class ImageEmbedder(Protocol):
    """Use a model to embed text."""

    def embed(
        self, context: EmbedImageContext
    ) -> Ok[EmbedImageResult] | InvalidArgumentError | InternalError: ...


class ClipText(TextEmbedder):
    """Clip Text embedder.

    CLIP (Contrastive Language-Image Pre-Training) is a neural network trained
    on a variety of (image, text) pairs. It can be instructed in natural language
    to predict the most relevant text snippet, given an image, without
    directly optimizing for the task, similarly to the zero-shot capabilities of
    GPT-2 and 3. We found CLIP matches the performance of the original ResNet50
    on ImageNet "zero-shot" without using any of the original 1.28M labeled examples,
    overcoming several major challenges in computer vision.
    """

    def embed(
        self, context: EmbedTextContext
    ) -> Ok[EmbedTextResult] | InvalidArgumentError | InternalError:
        import torch
        from transformers import (
            CLIPModel,
            CLIPProcessor,
        )

        model: CLIPModel = CLIPModel.from_pretrained(  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
            "openai/clip-vit-base-patch32"
        )
        processor: CLIPProcessor = CLIPProcessor.from_pretrained(  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
            "openai/clip-vit-base-patch32"
        )
        model.eval()
        match context.expected_coordinate_bitwidth:
            case 64:
                coord_dtype = pl.Float64()
            case 32:
                coord_dtype = pl.Float32()

        with torch.no_grad():
            inputs: dict[str, torch.Tensor] = processor(  # pyright: ignore[reportAssignmentType]
                text=context.inputs,
                return_tensors="pt",
                padding=True,
            )
            text_features = model.get_text_features(input_ids=inputs["input_ids"])

        text_features_numpy: np.ndarray[Any, Any] = text_features.numpy()  #  pyright: ignore[reportUnknownMemberType]

        return Ok(
            EmbedTextResult(
                context=context,
                embeddings=pl.Series(
                    values=text_features_numpy[:, : context.expected_vector_length],
                    dtype=pl.List(
                        coord_dtype,
                    ),
                ),
            )
        )
