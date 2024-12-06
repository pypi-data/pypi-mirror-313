"""Data modeling objects for creating corvic pipelines."""

import corvic.model._feature_type as feature_type
from corvic.model._agent import Agent, AgentID
from corvic.model._feature_view import (
    Column,
    DeepGnnCsvUrlMetadata,
    FeatureView,
    FeatureViewEdgeTableMetadata,
    FeatureViewRelationshipsMetadata,
)
from corvic.model._pipeline import (
    ChunkPdfsPipeline,
    OcrPdfsPipeline,
    Pipeline,
    PipelineID,
    SanitizeParquetPipeline,
    SpecificPipeline,
)
from corvic.model._resource import (
    Resource,
    ResourceID,
)
from corvic.model._source import Source, SourceID, SourceType
from corvic.model._space import (
    ConcatAndEmbedParameters,
    EmbedAndConcatParameters,
    EmbedImageParameters,
    ImageSpace,
    Node2VecParameters,
    RelationalSpace,
    SemanticSpace,
    Space,
    TabularSpace,
)

FeatureType = feature_type.FeatureType

__all__ = [
    "Agent",
    "AgentID",
    "ChunkPdfsPipeline",
    "Column",
    "ConcatAndEmbedParameters",
    "DeepGnnCsvUrlMetadata",
    "EmbedAndConcatParameters",
    "EmbedImageParameters",
    "FeatureType",
    "FeatureView",
    "FeatureViewEdgeTableMetadata",
    "FeatureViewRelationshipsMetadata",
    "ImageSpace",
    "Node2VecParameters",
    "OcrPdfsPipeline",
    "Pipeline",
    "PipelineID",
    "RelationalSpace",
    "Resource",
    "ResourceID",
    "SanitizeParquetPipeline",
    "SemanticSpace",
    "Source",
    "SourceID",
    "SourceType",
    "Space",
    "SpecificPipeline",
    "TabularSpace",
    "feature_type",
]
