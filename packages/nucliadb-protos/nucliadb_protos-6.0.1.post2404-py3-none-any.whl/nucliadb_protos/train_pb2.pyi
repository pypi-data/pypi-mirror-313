"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import nucliadb_protos.knowledgebox_pb2
import nucliadb_protos.resources_pb2
import typing
from nucliadb_protos.knowledgebox_pb2 import (
    AWS_EU_WEST_1 as AWS_EU_WEST_1,
    AWS_US_EAST_1 as AWS_US_EAST_1,
    AWS_US_WEST_2 as AWS_US_WEST_2,
    AZURE_EASTUS2 as AZURE_EASTUS2,
    CONFLICT as CONFLICT,
    CreateExternalIndexProviderMetadata as CreateExternalIndexProviderMetadata,
    CreatePineconeConfig as CreatePineconeConfig,
    DeleteKnowledgeBoxResponse as DeleteKnowledgeBoxResponse,
    DeletedEntitiesGroups as DeletedEntitiesGroups,
    ERROR as ERROR,
    EXTERNAL_INDEX_PROVIDER_ERROR as EXTERNAL_INDEX_PROVIDER_ERROR,
    EntitiesGroup as EntitiesGroup,
    EntitiesGroupSummary as EntitiesGroupSummary,
    EntitiesGroups as EntitiesGroups,
    Entity as Entity,
    EntityGroupDuplicateIndex as EntityGroupDuplicateIndex,
    ExternalIndexProviderType as ExternalIndexProviderType,
    GCP_US_CENTRAL1 as GCP_US_CENTRAL1,
    KBConfiguration as KBConfiguration,
    KnowledgeBoxConfig as KnowledgeBoxConfig,
    KnowledgeBoxID as KnowledgeBoxID,
    KnowledgeBoxResponseStatus as KnowledgeBoxResponseStatus,
    KnowledgeBoxUpdate as KnowledgeBoxUpdate,
    KnowledgeBoxVectorSetsConfig as KnowledgeBoxVectorSetsConfig,
    Label as Label,
    LabelSet as LabelSet,
    Labels as Labels,
    NOTFOUND as NOTFOUND,
    OK as OK,
    PINECONE as PINECONE,
    PINECONE_UNSET as PINECONE_UNSET,
    PineconeIndexMetadata as PineconeIndexMetadata,
    PineconeServerlessCloud as PineconeServerlessCloud,
    SemanticModelMetadata as SemanticModelMetadata,
    StoredExternalIndexProviderMetadata as StoredExternalIndexProviderMetadata,
    StoredPineconeConfig as StoredPineconeConfig,
    Synonyms as Synonyms,
    TermSynonyms as TermSynonyms,
    UNSET as UNSET,
    UpdateKnowledgeBoxResponse as UpdateKnowledgeBoxResponse,
    VectorSet as VectorSet,
    VectorSetConfig as VectorSetConfig,
    VectorSets as VectorSets,
)
from nucliadb_protos.resources_pb2 import (
    AllFieldIDs as AllFieldIDs,
    Answers as Answers,
    Basic as Basic,
    Block as Block,
    CONVERSATION as CONVERSATION,
    Classification as Classification,
    CloudFile as CloudFile,
    ComputedMetadata as ComputedMetadata,
    Conversation as Conversation,
    Entity as Entity,
    Extra as Extra,
    ExtractedTextWrapper as ExtractedTextWrapper,
    ExtractedVectorsWrapper as ExtractedVectorsWrapper,
    FILE as FILE,
    FieldClassifications as FieldClassifications,
    FieldComputedMetadata as FieldComputedMetadata,
    FieldComputedMetadataWrapper as FieldComputedMetadataWrapper,
    FieldConversation as FieldConversation,
    FieldEntities as FieldEntities,
    FieldEntity as FieldEntity,
    FieldFile as FieldFile,
    FieldID as FieldID,
    FieldLargeMetadata as FieldLargeMetadata,
    FieldLink as FieldLink,
    FieldMetadata as FieldMetadata,
    FieldQuestionAnswerWrapper as FieldQuestionAnswerWrapper,
    FieldQuestionAnswers as FieldQuestionAnswers,
    FieldRef as FieldRef,
    FieldText as FieldText,
    FieldType as FieldType,
    FileExtractedData as FileExtractedData,
    FilePages as FilePages,
    GENERIC as GENERIC,
    LINK as LINK,
    LargeComputedMetadata as LargeComputedMetadata,
    LargeComputedMetadataWrapper as LargeComputedMetadataWrapper,
    LinkExtractedData as LinkExtractedData,
    Message as Message,
    MessageContent as MessageContent,
    Metadata as Metadata,
    NestedListPosition as NestedListPosition,
    NestedPosition as NestedPosition,
    Origin as Origin,
    PageInformation as PageInformation,
    PagePositions as PagePositions,
    PageSelections as PageSelections,
    PageStructure as PageStructure,
    PageStructurePage as PageStructurePage,
    PageStructureToken as PageStructureToken,
    Paragraph as Paragraph,
    ParagraphAnnotation as ParagraphAnnotation,
    ParagraphRelations as ParagraphRelations,
    Position as Position,
    Positions as Positions,
    Question as Question,
    QuestionAnswer as QuestionAnswer,
    QuestionAnswerAnnotation as QuestionAnswerAnnotation,
    QuestionAnswers as QuestionAnswers,
    Relations as Relations,
    Representation as Representation,
    RowsPreview as RowsPreview,
    Sentence as Sentence,
    TEXT as TEXT,
    TokenSplit as TokenSplit,
    UserFieldMetadata as UserFieldMetadata,
    UserMetadata as UserMetadata,
    UserVectorsWrapper as UserVectorsWrapper,
    VisualSelection as VisualSelection,
)
from nucliadb_protos.writer_pb2 import (
    Audit as Audit,
    BrokerMessage as BrokerMessage,
    BrokerMessageBlobReference as BrokerMessageBlobReference,
    DelEntitiesRequest as DelEntitiesRequest,
    DelVectorSetRequest as DelVectorSetRequest,
    DelVectorSetResponse as DelVectorSetResponse,
    Error as Error,
    GetEntitiesGroupRequest as GetEntitiesGroupRequest,
    GetEntitiesGroupResponse as GetEntitiesGroupResponse,
    GetEntitiesRequest as GetEntitiesRequest,
    GetEntitiesResponse as GetEntitiesResponse,
    GetLabelsRequest as GetLabelsRequest,
    GetLabelsResponse as GetLabelsResponse,
    GetVectorSetsRequest as GetVectorSetsRequest,
    GetVectorSetsResponse as GetVectorSetsResponse,
    IndexResource as IndexResource,
    IndexStatus as IndexStatus,
    ListEntitiesGroupsRequest as ListEntitiesGroupsRequest,
    ListEntitiesGroupsResponse as ListEntitiesGroupsResponse,
    ListMembersRequest as ListMembersRequest,
    ListMembersResponse as ListMembersResponse,
    Member as Member,
    MergeEntitiesRequest as MergeEntitiesRequest,
    NewEntitiesGroupRequest as NewEntitiesGroupRequest,
    NewEntitiesGroupResponse as NewEntitiesGroupResponse,
    NewKnowledgeBoxV2Request as NewKnowledgeBoxV2Request,
    NewKnowledgeBoxV2Response as NewKnowledgeBoxV2Response,
    NewVectorSetRequest as NewVectorSetRequest,
    NewVectorSetResponse as NewVectorSetResponse,
    Notification as Notification,
    NotificationSource as NotificationSource,
    OpStatusWriter as OpStatusWriter,
    PROCESSOR as PROCESSOR,
    SetEntitiesRequest as SetEntitiesRequest,
    ShardObject as ShardObject,
    ShardReplica as ShardReplica,
    Shards as Shards,
    SynonymsRequest as SynonymsRequest,
    UNSET as UNSET,
    UpdateEntitiesGroupRequest as UpdateEntitiesGroupRequest,
    UpdateEntitiesGroupResponse as UpdateEntitiesGroupResponse,
    WRITER as WRITER,
    WriterStatusRequest as WriterStatusRequest,
    WriterStatusResponse as WriterStatusResponse,
)

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class EnabledMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TEXT_FIELD_NUMBER: builtins.int
    ENTITIES_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    VECTOR_FIELD_NUMBER: builtins.int
    text: builtins.bool
    entities: builtins.bool
    labels: builtins.bool
    vector: builtins.bool
    def __init__(
        self,
        *,
        text: builtins.bool = ...,
        entities: builtins.bool = ...,
        labels: builtins.bool = ...,
        vector: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["entities", b"entities", "labels", b"labels", "text", b"text", "vector", b"vector"]) -> None: ...

global___EnabledMetadata = EnabledMetadata

@typing.final
class TrainLabels(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCE_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    PARAGRAPH_FIELD_NUMBER: builtins.int
    @property
    def resource(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[nucliadb_protos.resources_pb2.Classification]: ...
    @property
    def field(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[nucliadb_protos.resources_pb2.Classification]: ...
    @property
    def paragraph(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[nucliadb_protos.resources_pb2.Classification]: ...
    def __init__(
        self,
        *,
        resource: collections.abc.Iterable[nucliadb_protos.resources_pb2.Classification] | None = ...,
        field: collections.abc.Iterable[nucliadb_protos.resources_pb2.Classification] | None = ...,
        paragraph: collections.abc.Iterable[nucliadb_protos.resources_pb2.Classification] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "paragraph", b"paragraph", "resource", b"resource"]) -> None: ...

global___TrainLabels = TrainLabels

@typing.final
class Position(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    START_FIELD_NUMBER: builtins.int
    END_FIELD_NUMBER: builtins.int
    start: builtins.int
    end: builtins.int
    def __init__(
        self,
        *,
        start: builtins.int = ...,
        end: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["end", b"end", "start", b"start"]) -> None: ...

global___Position = Position

@typing.final
class EntityPositions(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENTITY_FIELD_NUMBER: builtins.int
    POSITIONS_FIELD_NUMBER: builtins.int
    entity: builtins.str
    @property
    def positions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Position]: ...
    def __init__(
        self,
        *,
        entity: builtins.str = ...,
        positions: collections.abc.Iterable[global___Position] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["entity", b"entity", "positions", b"positions"]) -> None: ...

global___EntityPositions = EntityPositions

@typing.final
class TrainMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class EntitiesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing.final
    class EntityPositionsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___EntityPositions: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___EntityPositions | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    TEXT_FIELD_NUMBER: builtins.int
    ENTITIES_FIELD_NUMBER: builtins.int
    ENTITY_POSITIONS_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    VECTOR_FIELD_NUMBER: builtins.int
    text: builtins.str
    @property
    def entities(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    @property
    def entity_positions(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___EntityPositions]: ...
    @property
    def labels(self) -> global___TrainLabels: ...
    @property
    def vector(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        text: builtins.str = ...,
        entities: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        entity_positions: collections.abc.Mapping[builtins.str, global___EntityPositions] | None = ...,
        labels: global___TrainLabels | None = ...,
        vector: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["labels", b"labels"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["entities", b"entities", "entity_positions", b"entity_positions", "labels", b"labels", "text", b"text", "vector", b"vector"]) -> None: ...

global___TrainMetadata = TrainMetadata

@typing.final
class GetInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KB_FIELD_NUMBER: builtins.int
    @property
    def kb(self) -> nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID: ...
    def __init__(
        self,
        *,
        kb: nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["kb", b"kb"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["kb", b"kb"]) -> None: ...

global___GetInfoRequest = GetInfoRequest

@typing.final
class GetLabelsetsCountRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KB_FIELD_NUMBER: builtins.int
    PARAGRAPH_LABELSETS_FIELD_NUMBER: builtins.int
    RESOURCE_LABELSETS_FIELD_NUMBER: builtins.int
    @property
    def kb(self) -> nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID: ...
    @property
    def paragraph_labelsets(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def resource_labelsets(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        kb: nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID | None = ...,
        paragraph_labelsets: collections.abc.Iterable[builtins.str] | None = ...,
        resource_labelsets: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["kb", b"kb"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["kb", b"kb", "paragraph_labelsets", b"paragraph_labelsets", "resource_labelsets", b"resource_labelsets"]) -> None: ...

global___GetLabelsetsCountRequest = GetLabelsetsCountRequest

@typing.final
class GetResourcesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KB_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    RANDOM_FIELD_NUMBER: builtins.int
    size: builtins.int
    random: builtins.bool
    @property
    def kb(self) -> nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID: ...
    @property
    def metadata(self) -> global___EnabledMetadata: ...
    def __init__(
        self,
        *,
        kb: nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID | None = ...,
        metadata: global___EnabledMetadata | None = ...,
        size: builtins.int = ...,
        random: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["kb", b"kb", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["kb", b"kb", "metadata", b"metadata", "random", b"random", "size", b"size"]) -> None: ...

global___GetResourcesRequest = GetResourcesRequest

@typing.final
class GetParagraphsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KB_FIELD_NUMBER: builtins.int
    UUID_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    RANDOM_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    size: builtins.int
    random: builtins.bool
    @property
    def kb(self) -> nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID: ...
    @property
    def field(self) -> nucliadb_protos.resources_pb2.FieldID: ...
    @property
    def metadata(self) -> global___EnabledMetadata: ...
    def __init__(
        self,
        *,
        kb: nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID | None = ...,
        uuid: builtins.str = ...,
        field: nucliadb_protos.resources_pb2.FieldID | None = ...,
        metadata: global___EnabledMetadata | None = ...,
        size: builtins.int = ...,
        random: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["field", b"field", "kb", b"kb", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "kb", b"kb", "metadata", b"metadata", "random", b"random", "size", b"size", "uuid", b"uuid"]) -> None: ...

global___GetParagraphsRequest = GetParagraphsRequest

@typing.final
class GetSentencesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KB_FIELD_NUMBER: builtins.int
    UUID_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    RANDOM_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    size: builtins.int
    random: builtins.bool
    @property
    def kb(self) -> nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID: ...
    @property
    def field(self) -> nucliadb_protos.resources_pb2.FieldID: ...
    @property
    def metadata(self) -> global___EnabledMetadata: ...
    def __init__(
        self,
        *,
        kb: nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID | None = ...,
        uuid: builtins.str = ...,
        field: nucliadb_protos.resources_pb2.FieldID | None = ...,
        metadata: global___EnabledMetadata | None = ...,
        size: builtins.int = ...,
        random: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["field", b"field", "kb", b"kb", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "kb", b"kb", "metadata", b"metadata", "random", b"random", "size", b"size", "uuid", b"uuid"]) -> None: ...

global___GetSentencesRequest = GetSentencesRequest

@typing.final
class GetFieldsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KB_FIELD_NUMBER: builtins.int
    UUID_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    RANDOM_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    size: builtins.int
    random: builtins.bool
    @property
    def kb(self) -> nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID: ...
    @property
    def field(self) -> nucliadb_protos.resources_pb2.FieldID: ...
    @property
    def metadata(self) -> global___EnabledMetadata: ...
    def __init__(
        self,
        *,
        kb: nucliadb_protos.knowledgebox_pb2.KnowledgeBoxID | None = ...,
        uuid: builtins.str = ...,
        field: nucliadb_protos.resources_pb2.FieldID | None = ...,
        metadata: global___EnabledMetadata | None = ...,
        size: builtins.int = ...,
        random: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["field", b"field", "kb", b"kb", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "kb", b"kb", "metadata", b"metadata", "random", b"random", "size", b"size", "uuid", b"uuid"]) -> None: ...

global___GetFieldsRequest = GetFieldsRequest

@typing.final
class TrainInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESOURCES_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    PARAGRAPHS_FIELD_NUMBER: builtins.int
    SENTENCES_FIELD_NUMBER: builtins.int
    resources: builtins.int
    fields: builtins.int
    paragraphs: builtins.int
    sentences: builtins.int
    def __init__(
        self,
        *,
        resources: builtins.int = ...,
        fields: builtins.int = ...,
        paragraphs: builtins.int = ...,
        sentences: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["fields", b"fields", "paragraphs", b"paragraphs", "resources", b"resources", "sentences", b"sentences"]) -> None: ...

global___TrainInfo = TrainInfo

@typing.final
class TrainSentence(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UUID_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    PARAGRAPH_FIELD_NUMBER: builtins.int
    SENTENCE_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    paragraph: builtins.str
    sentence: builtins.str
    @property
    def field(self) -> nucliadb_protos.resources_pb2.FieldID: ...
    @property
    def metadata(self) -> global___TrainMetadata: ...
    def __init__(
        self,
        *,
        uuid: builtins.str = ...,
        field: nucliadb_protos.resources_pb2.FieldID | None = ...,
        paragraph: builtins.str = ...,
        sentence: builtins.str = ...,
        metadata: global___TrainMetadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["field", b"field", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "metadata", b"metadata", "paragraph", b"paragraph", "sentence", b"sentence", "uuid", b"uuid"]) -> None: ...

global___TrainSentence = TrainSentence

@typing.final
class TrainParagraph(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UUID_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    PARAGRAPH_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    paragraph: builtins.str
    @property
    def field(self) -> nucliadb_protos.resources_pb2.FieldID: ...
    @property
    def metadata(self) -> global___TrainMetadata: ...
    def __init__(
        self,
        *,
        uuid: builtins.str = ...,
        field: nucliadb_protos.resources_pb2.FieldID | None = ...,
        paragraph: builtins.str = ...,
        metadata: global___TrainMetadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["field", b"field", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "metadata", b"metadata", "paragraph", b"paragraph", "uuid", b"uuid"]) -> None: ...

global___TrainParagraph = TrainParagraph

@typing.final
class TrainField(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UUID_FIELD_NUMBER: builtins.int
    FIELD_FIELD_NUMBER: builtins.int
    SUBFIELD_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    subfield: builtins.str
    @property
    def field(self) -> nucliadb_protos.resources_pb2.FieldID: ...
    @property
    def metadata(self) -> global___TrainMetadata: ...
    def __init__(
        self,
        *,
        uuid: builtins.str = ...,
        field: nucliadb_protos.resources_pb2.FieldID | None = ...,
        subfield: builtins.str = ...,
        metadata: global___TrainMetadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["field", b"field", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["field", b"field", "metadata", b"metadata", "subfield", b"subfield", "uuid", b"uuid"]) -> None: ...

global___TrainField = TrainField

@typing.final
class TrainResource(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UUID_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    ICON_FIELD_NUMBER: builtins.int
    SLUG_FIELD_NUMBER: builtins.int
    CREATED_FIELD_NUMBER: builtins.int
    MODIFIED_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    title: builtins.str
    icon: builtins.str
    slug: builtins.str
    @property
    def created(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def modified(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def metadata(self) -> global___TrainMetadata: ...
    def __init__(
        self,
        *,
        uuid: builtins.str = ...,
        title: builtins.str = ...,
        icon: builtins.str = ...,
        slug: builtins.str = ...,
        created: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        modified: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        metadata: global___TrainMetadata | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["created", b"created", "metadata", b"metadata", "modified", b"modified"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["created", b"created", "icon", b"icon", "metadata", b"metadata", "modified", b"modified", "slug", b"slug", "title", b"title", "uuid", b"uuid"]) -> None: ...

global___TrainResource = TrainResource

@typing.final
class LabelsetCount(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class ParagraphsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.int
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing.final
    class ResourcesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.int
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    PARAGRAPHS_FIELD_NUMBER: builtins.int
    RESOURCES_FIELD_NUMBER: builtins.int
    @property
    def paragraphs(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.int]: ...
    @property
    def resources(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.int]: ...
    def __init__(
        self,
        *,
        paragraphs: collections.abc.Mapping[builtins.str, builtins.int] | None = ...,
        resources: collections.abc.Mapping[builtins.str, builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["paragraphs", b"paragraphs", "resources", b"resources"]) -> None: ...

global___LabelsetCount = LabelsetCount

@typing.final
class LabelsetsCount(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class LabelsetsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___LabelsetCount: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___LabelsetCount | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    LABELSETS_FIELD_NUMBER: builtins.int
    @property
    def labelsets(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___LabelsetCount]: ...
    def __init__(
        self,
        *,
        labelsets: collections.abc.Mapping[builtins.str, global___LabelsetCount] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["labelsets", b"labelsets"]) -> None: ...

global___LabelsetsCount = LabelsetsCount
