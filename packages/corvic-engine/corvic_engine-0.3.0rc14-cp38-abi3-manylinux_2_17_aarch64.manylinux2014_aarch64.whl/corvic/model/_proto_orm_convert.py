import dataclasses
from typing import Generic, TypeVar, cast

import sqlalchemy.orm as sa_orm
from google.protobuf import json_format, struct_pb2, timestamp_pb2
from more_itertools import flatten
from typing_extensions import overload

from corvic import orm
from corvic.result import InvalidArgumentError, Ok
from corvic_generated.model.v1alpha import models_pb2
from corvic_generated.orm.v1 import common_pb2

UNCOMMITTED_ID_PREFIX = "__uncommitted_object-"

_Proto = (
    models_pb2.Resource
    | models_pb2.Source
    | models_pb2.FeatureView
    | models_pb2.Space
    | models_pb2.FeatureViewSource
    | models_pb2.Agent
    | models_pb2.Pipeline
)
_Orm = (
    orm.Resource
    | orm.Source
    | orm.FeatureView
    | orm.Space
    | orm.FeatureViewSource
    | orm.Agent
    | orm.Pipeline
)
_ID = TypeVar(
    "_ID",
    orm.ResourceID,
    orm.SourceID,
    orm.FeatureViewID,
    orm.SpaceID,
    orm.FeatureViewSourceID,
    orm.AgentID,
    orm.PipelineID,
)
OrmID = (
    orm.ResourceID
    | orm.SourceID
    | orm.FeatureViewID
    | orm.SpaceID
    | orm.FeatureViewSourceID
    | orm.AgentID
    | orm.PipelineID
)


@overload
def id_class_for(val: models_pb2.Resource) -> type[orm.ResourceID]: ...


@overload
def id_class_for(val: models_pb2.Source) -> type[orm.SourceID]: ...


@overload
def id_class_for(val: models_pb2.FeatureView) -> type[orm.FeatureViewID]: ...


@overload
def id_class_for(val: models_pb2.Space) -> type[orm.SpaceID]: ...


@overload
def id_class_for(
    val: models_pb2.FeatureViewSource,
) -> type[orm.FeatureViewSourceID]: ...


@overload
def id_class_for(val: models_pb2.Agent) -> type[orm.AgentID]: ...


@overload
def id_class_for(val: models_pb2.Pipeline) -> type[orm.PipelineID]: ...


def id_class_for(val: _Proto) -> type[OrmID]:
    match val:
        case models_pb2.Resource():
            return orm.ResourceID
        case models_pb2.Source():
            return orm.SourceID
        case models_pb2.FeatureView():
            return orm.FeatureViewID
        case models_pb2.Space():
            return orm.SpaceID
        case models_pb2.FeatureViewSource():
            return orm.FeatureViewSourceID
        case models_pb2.Agent():
            return orm.AgentID
        case models_pb2.Pipeline():
            return orm.PipelineID


@overload
def orm_class_for(val: orm.ResourceID) -> type[orm.Resource]: ...


@overload
def orm_class_for(val: orm.SourceID) -> type[orm.Source]: ...


@overload
def orm_class_for(val: orm.FeatureViewID) -> type[orm.FeatureView]: ...


@overload
def orm_class_for(val: orm.SpaceID) -> type[orm.Space]: ...


@overload
def orm_class_for(val: orm.FeatureViewSourceID) -> type[orm.FeatureViewSource]: ...


@overload
def orm_class_for(val: orm.AgentID) -> type[orm.Agent]: ...


@overload
def orm_class_for(val: orm.PipelineID) -> type[orm.Pipeline]: ...


@overload
def orm_class_for(val: models_pb2.Resource) -> type[orm.Resource]: ...


@overload
def orm_class_for(val: models_pb2.Source) -> type[orm.Source]: ...


@overload
def orm_class_for(val: models_pb2.FeatureView) -> type[orm.FeatureView]: ...


@overload
def orm_class_for(val: models_pb2.Space) -> type[orm.Space]: ...


@overload
def orm_class_for(val: models_pb2.FeatureViewSource) -> type[orm.FeatureViewSource]: ...


@overload
def orm_class_for(val: models_pb2.Agent) -> type[orm.Agent]: ...


@overload
def orm_class_for(val: models_pb2.Pipeline) -> type[orm.Pipeline]: ...


def orm_class_for(val: OrmID | _Proto) -> type[_Orm]:
    if isinstance(val, _Proto):
        id_val: OrmID = id_class_for(val)()
    else:
        id_val = val
    match id_val:
        case orm.ResourceID():
            return orm.Resource
        case orm.SourceID():
            return orm.Source
        case orm.FeatureViewID():
            return orm.FeatureView
        case orm.SpaceID():
            return orm.Space
        case orm.FeatureViewSourceID():
            return orm.FeatureViewSource
        case orm.AgentID():
            return orm.Agent
        case orm.PipelineID():
            return orm.Pipeline


@dataclasses.dataclass
class _OrmIDs(Generic[_ID]):
    obj_id: _ID | None
    room_id: orm.RoomID | None


def _translate_orm_ids(
    proto_obj: _Proto, obj_id_class: type[_ID]
) -> Ok[_OrmIDs[_ID]] | orm.InvalidORMIdentifierError:
    if proto_obj.id.startswith(UNCOMMITTED_ID_PREFIX):
        obj_id = None
    else:
        obj_id = obj_id_class(proto_obj.id)
        match obj_id.to_db():
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok():
                pass

    match proto_obj:
        case (
            models_pb2.Resource()
            | models_pb2.Source()
            | models_pb2.FeatureView()
            | models_pb2.Space()
            | models_pb2.Agent()
            | models_pb2.Pipeline()
        ):
            room_id = orm.RoomID(proto_obj.room_id)
            match room_id.to_db():
                case orm.InvalidORMIdentifierError() as err:
                    return err
                case Ok():
                    pass
        case models_pb2.FeatureViewSource():
            room_id = None

    return Ok(_OrmIDs(obj_id, room_id))


@overload
def orm_to_proto(orm_obj: orm.Resource) -> models_pb2.Resource: ...


@overload
def orm_to_proto(orm_obj: orm.Source) -> models_pb2.Source: ...


@overload
def orm_to_proto(orm_obj: orm.FeatureView) -> models_pb2.FeatureView: ...


@overload
def orm_to_proto(orm_obj: orm.Space) -> models_pb2.Space: ...


@overload
def orm_to_proto(orm_obj: orm.FeatureViewSource) -> models_pb2.FeatureViewSource: ...


@overload
def orm_to_proto(orm_obj: orm.Agent) -> models_pb2.Agent: ...


@overload
def orm_to_proto(orm_obj: orm.Pipeline) -> models_pb2.Pipeline: ...


def _agent_orm_to_proto(orm_obj: orm.Agent, created_at: timestamp_pb2.Timestamp | None):
    messages: list[models_pb2.MessageEntry] = []
    for raw_message in orm_obj.messages.values():
        agent_message = None
        user_message = None
        if (
            raw_message.agent_message is not None
            and raw_message.user_message is not None
        ):
            raise ValueError("both agent message and user message are not None")
        if raw_message.agent_message is not None:
            match raw_message.agent_message.message_metadata:
                case common_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED
                case common_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_DOWN:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_DOWN
                case common_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_UP:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_UP
                case _:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED

            struct = struct_pb2.Struct()
            json_format.Parse(
                raw_message.agent_message.policy
                if raw_message.agent_message.policy is not None
                else "{}",
                struct,
            )
            agent_message = models_pb2.AgentMessage(
                id=str(raw_message.agent_message_id),
                message=raw_message.agent_message.message,
                policy=struct,
                context=raw_message.agent_message.context,
                message_reaction=reaction,
                user_message_id=str(raw_message.agent_message.user_message_id),
                retrieved_entities=raw_message.agent_message.retrieved_entities,
            )
        elif raw_message.user_message is not None:
            user_message = models_pb2.UserMessage(
                id=str(raw_message.user_message_id),
                message=raw_message.user_message.message,
            )
        else:
            raise ValueError("no user message nor agent message retrieved")

        if raw_message.created_at is not None:
            msg_created_at = timestamp_pb2.Timestamp()
            msg_created_at.FromDatetime(raw_message.created_at)
        else:
            msg_created_at = None

        message = models_pb2.MessageEntry(
            id=str(raw_message.id),
            user_message=user_message,
            agent_message=agent_message,
            created_at=msg_created_at,
        )
        messages.append(message)

    return models_pb2.Agent(
        id=str(orm_obj.id),
        name=orm_obj.name,
        room_id=str(orm_obj.room_id),
        agent_parameters=orm_obj.parameters,
        org_id=str(orm_obj.org_id),
        messages=messages,
        created_at=created_at,
    )


def orm_to_proto(orm_obj: _Orm) -> _Proto:
    if orm_obj.created_at is not None:
        created_at = timestamp_pb2.Timestamp()
        created_at.FromDatetime(orm_obj.created_at)
    else:
        created_at = None
    match orm_obj:
        case orm.Resource():
            return models_pb2.Resource(
                id=str(orm_obj.id),
                name=orm_obj.name,
                description=orm_obj.description,
                mime_type=orm_obj.mime_type,
                url=orm_obj.url,
                md5=orm_obj.md5,
                size=orm_obj.size,
                original_path=orm_obj.original_path,
                room_id=str(orm_obj.room_id),
                source_ids=[str(val.source_id) for val in orm_obj.source_associations],
                org_id=str(orm_obj.org_id),
                pipeline_id=str(orm_obj.pipeline_input_refs[-1].pipeline.id)
                if orm_obj.pipeline_input_refs
                else None,
                created_at=created_at,
            )
        case orm.Source():
            return models_pb2.Source(
                id=str(orm_obj.id),
                name=orm_obj.name,
                table_op_graph=orm_obj.table_op_graph,
                room_id=str(orm_obj.room_id),
                resource_id=str(orm_obj.resource_associations[0].resource_id)
                if orm_obj.resource_associations
                else "",
                org_id=str(orm_obj.org_id),
                pipeline_id=str(orm_obj.pipeline_output_refs[-1].pipeline.id)
                if orm_obj.pipeline_output_refs
                else None,
                created_at=created_at,
            )
        case orm.Pipeline():
            return models_pb2.Pipeline(
                id=str(orm_obj.id),
                name=orm_obj.name,
                room_id=str(orm_obj.room_id),
                resource_inputs={
                    input_obj.name: orm_to_proto(input_obj.resource)
                    for input_obj in orm_obj.inputs
                },
                source_outputs={
                    output_obj.name: orm_to_proto(output_obj.source)
                    for output_obj in orm_obj.outputs
                },
                pipeline_transformation=orm_obj.transformation,
                org_id=str(orm_obj.org_id),
                created_at=created_at,
                description=orm_obj.description,
            )
        case orm.FeatureView():
            return models_pb2.FeatureView(
                id=str(orm_obj.id),
                name=orm_obj.name,
                description=orm_obj.description,
                room_id=str(orm_obj.room_id),
                feature_view_output=orm_obj.feature_view_output,
                feature_view_sources=[
                    orm_to_proto(fvs) for fvs in orm_obj.feature_view_sources
                ],
                org_id=str(orm_obj.org_id),
                created_at=created_at,
            )
        case orm.Space():
            raise NotImplementedError()
        case orm.FeatureViewSource():
            return models_pb2.FeatureViewSource(
                id=str(orm_obj.id),
                source=orm_to_proto(orm_obj.source),
                table_op_graph=orm_obj.table_op_graph,
                drop_disconnected=orm_obj.drop_disconnected,
                org_id=str(orm_obj.org_id),
                created_at=created_at,
            )
        case orm.Agent():
            return _agent_orm_to_proto(orm_obj=orm_obj, created_at=created_at)


@overload
def proto_to_orm(
    proto_obj: models_pb2.Resource, session: sa_orm.Session
) -> Ok[orm.Resource] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Source, session: sa_orm.Session
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Pipeline, session: sa_orm.Session
) -> Ok[orm.Pipeline] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.FeatureView, session: sa_orm.Session
) -> Ok[orm.FeatureView] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Space, session: sa_orm.Session
) -> Ok[orm.Space] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.FeatureViewSource, session: sa_orm.Session
) -> Ok[orm.FeatureViewSource] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Agent, session: sa_orm.Session
) -> Ok[orm.Agent] | orm.InvalidORMIdentifierError: ...


def _resource_proto_to_orm(
    proto_obj: models_pb2.Resource,
) -> Ok[orm.Resource] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.ResourceID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")

    source_ids = list[orm.SourceID]()
    for source_id in proto_obj.source_ids:
        orm_id = orm.SourceID(source_id)
        match orm_id.to_db():
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok():
                source_ids.append(orm_id)
    orm_obj = orm.Resource(
        id=ids.obj_id,
        name=proto_obj.name,
        description=proto_obj.description,
        mime_type=proto_obj.mime_type,
        md5=proto_obj.md5,
        url=proto_obj.url,
        size=proto_obj.size,
        original_path=proto_obj.original_path,
        room_id=ids.room_id,
        source_associations=[
            orm.SourceResourceAssociation(source_id=src_id, resource_id=ids.obj_id)
            for src_id in source_ids
        ],
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
        for assn in orm_obj.source_associations:
            assn.org_id = orm_obj.org_id
    return Ok(orm_obj)


def _pipeline_proto_to_orm(  # noqa: C901
    proto_obj: models_pb2.Pipeline, session: sa_orm.Session
) -> Ok[orm.Pipeline] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.PipelineID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit pipeline")

    orm_obj = orm.Pipeline(
        id=ids.obj_id,
        name=proto_obj.name,
        room_id=ids.room_id,
        transformation=proto_obj.pipeline_transformation,
        description=proto_obj.description,
    )

    for name, val in proto_obj.resource_inputs.items():
        match _resource_proto_to_orm(val):
            case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
                return err
            case Ok(resource_orm):
                if resource_orm.id:
                    resource_orm = session.merge(resource_orm)
                else:
                    session.add(resource_orm)
                orm_obj.inputs.append(
                    orm.PipelineInput(
                        pipeline=orm_obj, resource=resource_orm, name=name
                    )
                )

    for name, val in proto_obj.source_outputs.items():
        match _source_proto_to_orm(val):
            case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
                return err
            case Ok(source_orm):
                if source_orm.id:
                    source_orm = session.merge(source_orm)
                else:
                    session.add(source_orm)
                orm_obj.outputs.append(
                    orm.PipelineOutput(pipeline=orm_obj, source=source_orm, name=name)
                )
    if proto_obj.org_id:
        org_id = orm.OrgID(proto_obj.org_id)
        orm_obj.org_id = org_id
        for obj in flatten((orm_obj.inputs, orm_obj.outputs)):
            obj.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def _source_proto_to_orm(
    proto_obj: models_pb2.Source,
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.SourceID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")
    resource_id = orm.ResourceID(proto_obj.resource_id)
    if resource_id:
        associations = [
            orm.SourceResourceAssociation(source_id=ids.obj_id, resource_id=resource_id)
        ]
    else:
        associations = list[orm.SourceResourceAssociation]()

    orm_obj = orm.Source(
        id=ids.obj_id,
        name=proto_obj.name,
        table_op_graph=proto_obj.table_op_graph,
        room_id=ids.room_id,
        resource_associations=associations,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
        for assn in orm_obj.resource_associations:
            assn.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def _agent_proto_to_orm(
    proto_obj: models_pb2.Agent,
) -> Ok[orm.Agent] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.AgentID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")

    orm_obj = orm.Agent(
        id=ids.obj_id,
        name=proto_obj.name,
        parameters=proto_obj.agent_parameters,
        room_id=ids.room_id,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def _feature_view_proto_to_orm(
    proto_obj: models_pb2.FeatureView, session: sa_orm.Session
) -> Ok[orm.FeatureView] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.FeatureViewID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")

    feature_view_sources = list[orm.FeatureViewSource]()
    for fvs in proto_obj.feature_view_sources:
        match proto_to_orm(fvs, session):
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok(orm_fvs):
                if orm_fvs.id:
                    orm_fvs = session.merge(orm_fvs)
                else:
                    session.add(orm_fvs)
                feature_view_sources.append(orm_fvs)

    orm_obj = orm.FeatureView(
        id=ids.obj_id,
        name=proto_obj.name,
        description=proto_obj.description,
        room_id=ids.room_id,
        feature_view_output=proto_obj.feature_view_output,
        feature_view_sources=feature_view_sources,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def _feature_view_source_proto_to_orm(
    proto_obj: models_pb2.FeatureViewSource, session: sa_orm.Session
) -> Ok[orm.FeatureViewSource] | orm.InvalidORMIdentifierError:
    match proto_to_orm(proto_obj.source, session):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(source):
            pass

    if source.id:
        source = session.merge(source)
    else:
        session.add(source)
    orm_obj = orm.FeatureViewSource(
        table_op_graph=proto_obj.table_op_graph,
        drop_disconnected=proto_obj.drop_disconnected,
        source=source,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def proto_to_orm(
    proto_obj: _Proto, session: sa_orm.Session
) -> Ok[_Orm] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match proto_obj:
        case models_pb2.Resource():
            return _resource_proto_to_orm(proto_obj)
        case models_pb2.Source():
            return _source_proto_to_orm(proto_obj)
        case models_pb2.FeatureView():
            return _feature_view_proto_to_orm(proto_obj, session)
        case models_pb2.Space():
            raise NotImplementedError()
        case models_pb2.FeatureViewSource():
            return _feature_view_source_proto_to_orm(proto_obj, session)
        case models_pb2.Agent():
            return _agent_proto_to_orm(proto_obj)
        case models_pb2.Pipeline():
            return _pipeline_proto_to_orm(proto_obj, session)


def _pipeline_merge_old_orm(
    new_orm: orm.Pipeline, old_orm: orm.Pipeline, session: sa_orm.Session
):
    output_names = {val.name for val in new_orm.outputs}
    for output in old_orm.outputs:
        if output.name not in output_names:
            new_orm.outputs.append(output)

    input_names = {val.name for val in new_orm.inputs}
    for input in old_orm.inputs:
        if input.name not in input_names:
            new_orm.inputs.append(input)


def merge_old_orm(new_orm: _Orm, old_orm: _Orm | None, session: sa_orm.Session) -> None:
    if old_orm is None:
        return

    match new_orm:
        case orm.Resource():
            return
        case orm.Source():
            return
        case orm.FeatureView():
            return
        case orm.Space():
            raise NotImplementedError()
        case orm.FeatureViewSource():
            raise NotImplementedError()
        case orm.Agent():
            return
        case orm.Pipeline():
            _pipeline_merge_old_orm(new_orm, cast(orm.Pipeline, old_orm), session)


def _source_delete_related_objects(
    orm_obj: orm.Source, session: sa_orm.Session
) -> Ok[None] | InvalidArgumentError:
    feat_view_refs = list(
        session.scalars(
            session.query(orm.FeatureViewSource)
            .where(orm.FeatureViewSource.source_id == orm_obj.id)
            .limit(1)
        )
    )

    if feat_view_refs:
        return InvalidArgumentError(
            "cannot delete a source that still has feature views"
        )
    return Ok(None)


def _pipeline_delete_related_objects(
    orm_obj: orm.Pipeline, session: sa_orm.Session
) -> Ok[None] | InvalidArgumentError:
    for input in orm_obj.inputs:
        match delete_related_orm(input.resource, session):
            case InvalidArgumentError() as err:
                return err
            case Ok():
                pass
        session.delete(input.resource)
    for output in orm_obj.outputs:
        match delete_related_orm(output.source, session):
            case InvalidArgumentError() as err:
                return err
            case Ok():
                pass
        session.delete(output.source)
    return Ok(None)


def delete_related_orm(
    orm_obj: _Orm, session: sa_orm.Session
) -> Ok[None] | InvalidArgumentError:
    match orm_obj:
        case orm.Resource():
            return Ok(None)
        case orm.Source():
            return _source_delete_related_objects(orm_obj, session)
        case orm.FeatureView():
            return Ok(None)
        case orm.Space():
            return Ok(None)
        case orm.FeatureViewSource():
            return Ok(None)
        case orm.Agent():
            return Ok(None)
        case orm.Pipeline():
            return _pipeline_delete_related_objects(orm_obj, session)
