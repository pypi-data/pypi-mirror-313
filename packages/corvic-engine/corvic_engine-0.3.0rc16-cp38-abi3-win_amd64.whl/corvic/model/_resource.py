"""Resources."""

from __future__ import annotations

import dataclasses
import datetime
import uuid
from collections.abc import Iterable
from typing import TypeAlias

import polars as pl
import structlog
from typing_extensions import Self

from corvic import orm, result, system
from corvic.model._defaults import get_default_client, get_default_room_id
from corvic.model._wrapped_proto import WrappedProto
from corvic_generated.model.v1alpha import models_pb2

SourceID: TypeAlias = orm.SourceID
ResourceID: TypeAlias = orm.ResourceID
RoomID: TypeAlias = orm.RoomID
PipelineID: TypeAlias = orm.PipelineID

_logger = structlog.get_logger()


@dataclasses.dataclass(frozen=True)
class Resource(WrappedProto[ResourceID, models_pb2.Resource]):
    """Resources represent import data."""

    @property
    def url(self) -> str:
        return self.proto_self.url

    @property
    def name(self) -> str:
        return self.proto_self.name

    @property
    def room_id(self) -> RoomID:
        return RoomID(self.proto_self.room_id)

    @property
    def pipeline_id(self) -> PipelineID | None:
        return PipelineID(self.proto_self.pipeline_id) or None

    @property
    def mime_type(self) -> str:
        return self.proto_self.mime_type

    @property
    def md5(self) -> str:
        return self.proto_self.md5

    @property
    def size(self) -> int:
        return self.proto_self.size

    @property
    def original_path(self) -> str:
        return self.proto_self.original_path

    @property
    def description(self) -> str:
        return self.proto_self.description

    @property
    def source_ids(self) -> list[SourceID]:
        return [SourceID(val) for val in self.proto_self.source_ids]

    @classmethod
    def list(
        cls,
        room_id: RoomID | None = None,
        limit: int | None = None,
        created_before: datetime.datetime | None = None,
        client: system.Client | None = None,
    ) -> (
        result.Ok[Iterable[Resource]]
        | result.NotFoundError
        | result.InvalidArgumentError
    ):
        """List resources."""
        client = client or get_default_client()
        match cls.list_as_proto(
            orm.Resource,
            client,
            limit=limit,
            room_id=room_id,
            created_before=created_before,
        ):
            case result.NotFoundError() | result.InvalidArgumentError() as err:
                return err
            case result.Ok(protos):
                pass
        resources = list[Resource]()
        for proto in protos:
            match cls.from_proto(proto, client):
                case result.InvalidArgumentError() as err:
                    _logger.warning("error when listing resources", exc_info=err)
                case result.Ok(resource):
                    resources.append(resource)
        return result.Ok(resources)

    @classmethod
    def from_proto(
        cls, proto: models_pb2.Resource, client: system.Client | None = None
    ) -> result.Ok[Resource] | result.InvalidArgumentError:
        client = client or get_default_client()
        return result.Ok(cls(client, proto))

    @classmethod
    def from_id(
        cls, resource_id: ResourceID, client: system.Client | None = None
    ) -> result.Ok[Resource] | result.NotFoundError | result.InvalidArgumentError:
        client = client or get_default_client()
        return cls.load_proto_for(resource_id, client).and_then(
            lambda proto_self: cls.from_proto(proto_self, client)
        )

    @classmethod
    def from_blob(
        cls,
        name: str,
        blob: system.Blob,
        client: system.Client | None,
        original_path: str = "",
        description: str = "",
        room_id: orm.RoomID | None = None,
    ) -> Self:
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        blob.reload()
        md5 = blob.md5_hash
        size = blob.size

        if not md5 or not size:
            raise result.Error("failed to get metadata from blob store")

        proto_resource = models_pb2.Resource(
            name=name,
            mime_type=blob.content_type,
            url=blob.url,
            md5=md5,
            size=size,
            original_path=original_path,
            description=description,
            room_id=str(room_id),
        )
        return cls(client, proto_resource)

    @classmethod
    def from_polars(
        cls,
        data_frame: pl.DataFrame,
        client: system.Client | None = None,
        room_id: orm.RoomID | None = None,
    ) -> Self:
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        blob = client.storage_manager.tabular.blob(f"polars_dataframe/{uuid.uuid4()}")

        with blob.open(mode="wb") as stream:
            data_frame.write_parquet(stream)

        blob.content_type = "application/octet-stream"
        blob.patch()
        return cls.from_blob(blob.url, blob, client, room_id=room_id)
