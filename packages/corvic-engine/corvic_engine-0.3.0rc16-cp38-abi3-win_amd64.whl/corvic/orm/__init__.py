"""Data model definitions; backed by an RDBMS."""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.orm.collections import attribute_mapped_collection

from corvic.orm.base import Base, OrgBase
from corvic.orm.errors import (
    DeletedObjectError,
    InvalidORMIdentifierError,
    RequestedObjectsForNobodyError,
)
from corvic.orm.ids import (
    AgentID,
    AgentMessageID,
    FeatureViewID,
    FeatureViewSourceID,
    MessageEntryID,
    OrgID,
    PipelineID,
    ResourceID,
    RoomID,
    SourceID,
    SpaceID,
    SpaceParametersID,
    SpaceRunID,
    UserMessageID,
)
from corvic.orm.keys import (
    INT_PK_TYPE,
    ForeignKey,
    primary_key_foreign_column,
    primary_key_identity_column,
)
from corvic.orm.mixins import (
    BelongsToOrgMixin,
    Session,
    SoftDeleteMixin,
    live_unique_constraint,
)
from corvic_generated.orm.v1 import (
    agent_pb2,
    common_pb2,
    feature_view_pb2,
    pipeline_pb2,
    space_pb2,
    table_pb2,
)


class Org(SoftDeleteMixin, OrgBase):
    """An organization it a top level grouping of resources."""

    rooms: sa_orm.Mapped[dict[str, Room]] = sa_orm.relationship(
        collection_class=attribute_mapped_collection("room_key"),
        cascade="all",
        init=False,
        default_factory=dict,
    )
    sources: sa_orm.Mapped[list[Source]] = sa_orm.relationship(
        collection_class=list, cascade="all", init=True, default_factory=list
    )


class Room(BelongsToOrgMixin, SoftDeleteMixin, Base):
    """A Room is a logical collection of Documents."""

    __tablename__ = "room"
    __table_args__ = (live_unique_constraint("name", "org_id"),)

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    id: sa_orm.Mapped[RoomID | None] = primary_key_identity_column()
    org: sa_orm.Mapped[Org] = sa_orm.relationship(back_populates="rooms", init=False)

    feature_views: sa_orm.Mapped[dict[str, FeatureView]] = sa_orm.relationship(
        collection_class=attribute_mapped_collection("feature_view_key"),
        cascade="all",
        init=False,
        default_factory=dict,
    )
    sources: sa_orm.Mapped[dict[str, Source]] = sa_orm.relationship(
        collection_class=attribute_mapped_collection("source_key"),
        cascade="all",
        init=False,
        default_factory=dict,
    )
    spaces: sa_orm.Mapped[dict[str, Space]] = sa_orm.relationship(
        collection_class=attribute_mapped_collection("space_key"),
        cascade="all",
        init=False,
        default_factory=dict,
    )

    @property
    def room_key(self):
        return self.name


class DefaultObjects(Base):
    """Holds the identifiers for default objects."""

    __tablename__ = "default_objects"
    default_org: sa_orm.Mapped[OrgID] = sa_orm.mapped_column(
        ForeignKey(Org).make(ondelete="CASCADE")
    )
    default_room: sa_orm.Mapped[RoomID | None] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"), nullable=True, default=None
    )
    version: sa_orm.Mapped[int | None] = primary_key_identity_column(type_=INT_PK_TYPE)


class Resource(BelongsToOrgMixin, Base):
    """A Resource is a reference to some durably stored file.

    E.g., a document could be a PDF file, an image, or a text transcript of a
    conversation
    """

    __tablename__ = "resource"

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    mime_type: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    url: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    room_id: sa_orm.Mapped[RoomID] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"), name="room_id"
    )
    md5: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.CHAR(32), nullable=True)
    size: sa_orm.Mapped[int] = sa_orm.mapped_column(nullable=True)
    original_path: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    id: sa_orm.Mapped[ResourceID | None] = primary_key_identity_column()

    source_associations: sa_orm.Mapped[list[SourceResourceAssociation]] = (
        sa_orm.relationship(
            back_populates="resource",
            cascade="save-update, merge, delete, delete-orphan",
            default_factory=list,
        )
    )
    pipeline_input_refs: sa_orm.Mapped[list[PipelineInput]] = sa_orm.relationship(
        viewonly=True,
        back_populates="resource",
        default_factory=list,
        cascade="save-update, merge, delete, delete-orphan",
    )


class Source(BelongsToOrgMixin, Base):
    """A source."""

    __tablename__ = "source"
    __table_args__ = (sa.UniqueConstraint("name", "room_id"),)

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    room_id: sa_orm.Mapped[RoomID] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"),
    )
    # protobuf describing the operations required to construct a table
    table_op_graph: sa_orm.Mapped[table_pb2.TableComputeOp] = sa_orm.mapped_column()
    id: sa_orm.Mapped[SourceID | None] = primary_key_identity_column()

    resource_associations: sa_orm.Mapped[list[SourceResourceAssociation]] = (
        sa_orm.relationship(
            back_populates="source",
            cascade="save-update, merge, delete, delete-orphan",
            default_factory=list,
        )
    )
    org: sa_orm.Mapped[Org] = sa_orm.relationship(back_populates="sources", init=False)
    room: sa_orm.Mapped[Room] = sa_orm.relationship(
        back_populates="sources", init=False
    )
    source_files: sa_orm.Mapped[common_pb2.BlobUrlList | None] = sa_orm.mapped_column(
        default=None
    )
    pipeline_output_refs: sa_orm.Mapped[list[PipelineOutput]] = sa_orm.relationship(
        viewonly=True,
        back_populates="source",
        default_factory=list,
        cascade="save-update, merge, delete, delete-orphan",
    )

    @property
    def source_key(self):
        return self.name


class Pipeline(BelongsToOrgMixin, Base):
    """A resource to source pipeline."""

    __tablename__ = "pipeline"
    __table_args__ = (sa.UniqueConstraint("name", "room_id"),)

    transformation: sa_orm.Mapped[pipeline_pb2.PipelineTransformation] = (
        sa_orm.mapped_column()
    )
    room_id: sa_orm.Mapped[RoomID] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE")
    )
    name: sa_orm.Mapped[str] = sa_orm.mapped_column()
    description: sa_orm.Mapped[str | None] = sa_orm.mapped_column()
    id: sa_orm.Mapped[PipelineID | None] = primary_key_identity_column()

    inputs: sa_orm.Mapped[list[PipelineInput]] = sa_orm.relationship(
        back_populates="pipeline",
        cascade="save-update, merge, delete, delete-orphan",
        default_factory=list,
    )

    outputs: sa_orm.Mapped[list[PipelineOutput]] = sa_orm.relationship(
        back_populates="pipeline",
        cascade="save-update, merge, delete, delete-orphan",
        default_factory=list,
    )


class PipelineInput(BelongsToOrgMixin, Base):
    """Pipeline input resources."""

    __tablename__ = "pipeline_input"
    __table_args__ = (sa.UniqueConstraint("name", "pipeline_id"),)

    pipeline: sa_orm.Mapped[Pipeline] = sa_orm.relationship(
        back_populates="inputs",
    )
    resource: sa_orm.Mapped[Resource] = sa_orm.relationship(
        back_populates="pipeline_input_refs",
    )
    name: sa_orm.Mapped[str]
    """A name the pipeline uses to refer to this input."""

    _pipeline_id: sa_orm.Mapped[PipelineID] = primary_key_foreign_column(
        ForeignKey(Pipeline).make(), name="pipeline_id", init=False
    )
    _resource_id: sa_orm.Mapped[ResourceID] = primary_key_foreign_column(
        ForeignKey(Resource).make(), name="resource_id", init=False
    )


class PipelineOutput(BelongsToOrgMixin, Base):
    """Objects for tracking pipeline output sources."""

    __tablename__ = "pipeline_output"
    __table_args__ = (sa.UniqueConstraint("name", "pipeline_id"),)

    pipeline: sa_orm.Mapped[Pipeline] = sa_orm.relationship(
        back_populates="outputs",
    )
    source: sa_orm.Mapped[Source] = sa_orm.relationship(
        back_populates="pipeline_output_refs",
    )
    name: sa_orm.Mapped[str]
    """A name the pipeline uses to refer to this output."""

    _pipeline_id: sa_orm.Mapped[PipelineID] = primary_key_foreign_column(
        ForeignKey(Pipeline).make(ondelete="CASCADE"), name="pipeline_id", init=False
    )
    _source_id: sa_orm.Mapped[SourceID] = primary_key_foreign_column(
        ForeignKey(Source).make(ondelete="CASCADE"), name="source_id", init=False
    )


class SourceResourceAssociation(BelongsToOrgMixin, Base):
    __tablename__ = "source_resource_association"

    source_id: sa_orm.Mapped[SourceID | None] = (
        # this should be legal but pyright complains that it makes Source depend
        # on itself
        primary_key_foreign_column(ForeignKey(Source).make())
    )
    resource_id: sa_orm.Mapped[ResourceID | None] = (
        # this should be legal but pyright complains that it makes Resource depend
        # on itself
        primary_key_foreign_column(ForeignKey(Resource).make())
    )
    source: sa_orm.Mapped[Source] = sa_orm.relationship(
        back_populates="resource_associations", init=False
    )
    resource: sa_orm.Mapped[Resource] = sa_orm.relationship(
        back_populates="source_associations", init=False
    )


class FeatureView(SoftDeleteMixin, BelongsToOrgMixin, Base):
    """A FeatureView is a logical collection of sources used by various spaces."""

    __tablename__ = "feature_view"
    __table_args__ = (live_unique_constraint("name", "room_id"),)

    id: sa_orm.Mapped[FeatureViewID | None] = primary_key_identity_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default="")

    room_id: sa_orm.Mapped[RoomID | None] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"),
        nullable=True,
        init=True,
        default=None,
    )
    room: sa_orm.Mapped[Room] = sa_orm.relationship(
        back_populates="feature_views", init=False
    )

    feature_view_output: sa_orm.Mapped[feature_view_pb2.FeatureViewOutput | None] = (
        sa_orm.mapped_column(default_factory=feature_view_pb2.FeatureViewOutput)
    )

    @property
    def feature_view_key(self):
        return self.name

    feature_view_sources: sa_orm.Mapped[list[FeatureViewSource]] = sa_orm.relationship(
        init=True,
        default_factory=list,
        back_populates="feature_view",
    )

    spaces: sa_orm.Mapped[list[Space]] = sa_orm.relationship(
        init=False, default_factory=list
    )


class FeatureViewSource(BelongsToOrgMixin, Base):
    """A source inside of a feature view."""

    __tablename__ = "feature_view_source"
    table_op_graph: sa_orm.Mapped[table_pb2.TableComputeOp] = sa_orm.mapped_column()
    id: sa_orm.Mapped[FeatureViewSourceID | None] = primary_key_identity_column()
    drop_disconnected: sa_orm.Mapped[bool] = sa_orm.mapped_column(default=False)
    feature_view_id: sa_orm.Mapped[FeatureViewID] = sa_orm.mapped_column(
        ForeignKey(FeatureView).make(ondelete="CASCADE"), nullable=False, default=None
    )
    # this should be legal but pyright complains that it makes Source depend
    # on itself
    source_id: sa_orm.Mapped[SourceID] = sa_orm.mapped_column(
        ForeignKey(Source).make(ondelete="CASCADE"),
        nullable=False,
        default=None,
    )
    source: sa_orm.Mapped[Source] = sa_orm.relationship(init=True, default=None)
    feature_view: sa_orm.Mapped[FeatureView] = sa_orm.relationship(
        init=True, default=None
    )


class Space(BelongsToOrgMixin, Base):
    """A space is a named evaluation of space parameters."""

    __tablename__ = "space"
    __table_args__ = (sa.UniqueConstraint("name", "room_id"),)

    room_id: sa_orm.Mapped[RoomID] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"),
        nullable=True,
        init=True,
        default=None,
    )
    room: sa_orm.Mapped[Room] = sa_orm.relationship(
        back_populates="spaces", init=True, default=None
    )

    id: sa_orm.Mapped[SpaceID | None] = primary_key_identity_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default="")

    feature_view_id: sa_orm.Mapped[FeatureViewID] = sa_orm.mapped_column(
        ForeignKey(FeatureView).make(ondelete="CASCADE"),
        nullable=False,
        default=None,
    )
    parameters: sa_orm.Mapped[space_pb2.SpaceParameters | None] = sa_orm.mapped_column(
        default=None
    )
    auto_sync: sa_orm.Mapped[bool | None] = sa_orm.mapped_column(default=None)
    feature_view: sa_orm.Mapped[FeatureView] = sa_orm.relationship(
        init=True,
        default=None,
        back_populates="spaces",
    )

    @property
    def space_key(self):
        return self.name


class SpaceRun(BelongsToOrgMixin, Base):
    """A Space run."""

    __tablename__ = "space_run"

    id: sa_orm.Mapped[SpaceRunID | None] = primary_key_identity_column()
    table_op_graph: sa_orm.Mapped[table_pb2.TableComputeOp] = sa_orm.mapped_column(
        default_factory=table_pb2.TableComputeOp
    )
    space_id: sa_orm.Mapped[SpaceID] = sa_orm.mapped_column(
        ForeignKey(Space).make(ondelete="CASCADE"), nullable=False, default=None
    )
    space: sa_orm.Mapped[Space] = sa_orm.relationship(init=True, default=None)
    result_url: sa_orm.Mapped[str | None] = sa_orm.mapped_column(sa.Text, default=None)
    coordinates_urls: sa_orm.Mapped[common_pb2.BlobUrlList | None] = (
        sa_orm.mapped_column(default=None)
    )
    is_running: sa_orm.Mapped[bool | None] = sa_orm.mapped_column(default=None)
    vector_urls: sa_orm.Mapped[common_pb2.BlobUrlList | None] = sa_orm.mapped_column(
        default=None
    )

    embedding_metrics: sa_orm.Mapped[common_pb2.EmbeddingMetrics | None] = (
        sa_orm.mapped_column(default=None)
    )
    insight_tools: sa_orm.Mapped[table_pb2.NamedTables | None] = sa_orm.mapped_column(
        default=None
    )


class Agent(SoftDeleteMixin, BelongsToOrgMixin, Base):
    """An Agent."""

    __tablename__ = "agent"
    __table_args__ = (live_unique_constraint("name", "room_id"),)

    room_id: sa_orm.Mapped[RoomID | None] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"),
        nullable=True,
        init=True,
        default=None,
    )
    id: sa_orm.Mapped[AgentID | None] = primary_key_identity_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)

    @property
    def agent_key(self):
        return self.name

    parameters: sa_orm.Mapped[agent_pb2.AgentParameters | None] = sa_orm.mapped_column(
        default=None
    )
    messages: sa_orm.Mapped[dict[str, MessageEntry]] = sa_orm.relationship(
        collection_class=attribute_mapped_collection("entry_id"),
        cascade="all",
        init=False,
        default_factory=dict,
        viewonly=True,
    )


class UserMessage(SoftDeleteMixin, BelongsToOrgMixin, Base):
    """A message sent by an user."""

    __tablename__ = "user_message"

    message_entry: sa_orm.Mapped[MessageEntry] = sa_orm.relationship(
        init=True, default=None
    )

    id: sa_orm.Mapped[UserMessageID | None] = primary_key_identity_column()

    message: sa_orm.Mapped[str | None] = sa_orm.mapped_column(sa.Text, default=None)


class AgentMessage(SoftDeleteMixin, BelongsToOrgMixin, Base):
    """A message sent by an agent."""

    __tablename__ = "agent_message"
    message_metadata: sa_orm.Mapped[common_pb2.AgentMessageMetadata | None] = (
        sa_orm.mapped_column(
            default_factory=lambda: common_pb2.AgentMessageMetadata(
                message_reaction=common_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED
            )
        )
    )
    id: sa_orm.Mapped[AgentMessageID | None] = primary_key_identity_column()

    message_entry: sa_orm.Mapped[MessageEntry] = sa_orm.relationship(
        init=True, default=None
    )

    user_message_id: sa_orm.Mapped[UserMessageID | None] = sa_orm.mapped_column(
        ForeignKey(UserMessage).make(ondelete="CASCADE"), init=True, default=None
    )
    message: sa_orm.Mapped[str | None] = sa_orm.mapped_column(sa.Text, default=None)
    policy: sa_orm.Mapped[str | None] = sa_orm.mapped_column(sa.Text, default=None)
    context: sa_orm.Mapped[str | None] = sa_orm.mapped_column(sa.Text, default=None)
    retrieved_entities: sa_orm.Mapped[common_pb2.RetrievedEntities | None] = (
        sa_orm.mapped_column(default=None)
    )


class MessageEntry(SoftDeleteMixin, BelongsToOrgMixin, Base):
    """A message either sent by an Agent or an User."""

    __tablename__ = "message_entry"

    id: sa_orm.Mapped[MessageEntryID | None] = primary_key_identity_column()

    agent_id: sa_orm.Mapped[AgentID] = sa_orm.mapped_column(
        ForeignKey(Agent).make(ondelete="CASCADE"),
        nullable=True,
        init=True,
        default=None,
    )

    agent_message_id: sa_orm.Mapped[AgentMessageID | None] = sa_orm.mapped_column(
        ForeignKey(AgentMessage).make(ondelete="CASCADE"), default=None
    )
    user_message_id: sa_orm.Mapped[UserMessageID | None] = sa_orm.mapped_column(
        ForeignKey(UserMessage).make(ondelete="CASCADE"), default=None
    )

    agent_message: sa_orm.Mapped[AgentMessage | None] = sa_orm.relationship(
        back_populates="message_entry", init=True, default=None
    )

    user_message: sa_orm.Mapped[UserMessage | None] = sa_orm.relationship(
        back_populates="message_entry", init=True, default=None
    )

    @property
    def entry_id(self):
        return self.id


ID = (
    AgentID
    | AgentMessageID
    | FeatureViewID
    | FeatureViewSourceID
    | MessageEntryID
    | OrgID
    | PipelineID
    | ResourceID
    | RoomID
    | SourceID
    | SpaceID
    | SpaceParametersID
    | SpaceRunID
    | UserMessageID
)


__all__ = [
    "Agent",
    "AgentID",
    "AgentMessage",
    "AgentMessageID",
    "Base",
    "DefaultObjects",
    "DeletedObjectError",
    "FeatureView",
    "FeatureViewID",
    "FeatureViewSource",
    "FeatureViewSourceID",
    "ID",
    "InvalidORMIdentifierError",
    "MessageEntry",
    "MessageEntryID",
    "Org",
    "OrgID",
    "PipelineID",
    "PipelineInput",
    "PipelineOutput",
    "RequestedObjectsForNobodyError",
    "Resource",
    "ResourceID",
    "Room",
    "RoomID",
    "Session",
    "Source",
    "SourceID",
    "Space",
    "SpaceID",
    "SpaceParametersID",
    "SpaceRun",
    "SpaceRunID",
    "UserMessage",
    "UserMessageID",
]
