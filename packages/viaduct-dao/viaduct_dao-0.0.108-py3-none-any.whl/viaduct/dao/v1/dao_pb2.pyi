from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_DIRECTION_UNSPECIFIED: _ClassVar[OrderDirection]
    ORDER_DIRECTION_ASC: _ClassVar[OrderDirection]
    ORDER_DIRECTION_DESC: _ClassVar[OrderDirection]

class BinaryOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BINARY_OP_UNSPECIFIED: _ClassVar[BinaryOp]
    BINARY_OP_ADD: _ClassVar[BinaryOp]
    BINARY_OP_AND: _ClassVar[BinaryOp]
    BINARY_OP_DIV: _ClassVar[BinaryOp]
    BINARY_OP_EQ: _ClassVar[BinaryOp]
    BINARY_OP_GT: _ClassVar[BinaryOp]
    BINARY_OP_GTE: _ClassVar[BinaryOp]
    BINARY_OP_IN: _ClassVar[BinaryOp]
    BINARY_OP_LT: _ClassVar[BinaryOp]
    BINARY_OP_LTE: _ClassVar[BinaryOp]
    BINARY_OP_MOD: _ClassVar[BinaryOp]
    BINARY_OP_MUL: _ClassVar[BinaryOp]
    BINARY_OP_NE: _ClassVar[BinaryOp]
    BINARY_OP_OR: _ClassVar[BinaryOp]
    BINARY_OP_SUB: _ClassVar[BinaryOp]
    BINARY_OP_REGEXP: _ClassVar[BinaryOp]

class UnaryOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNARY_OP_UNSPECIFIED: _ClassVar[UnaryOp]
    UNARY_OP_NOT: _ClassVar[UnaryOp]
    UNARY_OP_NEG: _ClassVar[UnaryOp]
    UNARY_OP_IS_NULL: _ClassVar[UnaryOp]

class AggOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGG_OP_UNSPECIFIED: _ClassVar[AggOp]
    AGG_OP_AVG: _ClassVar[AggOp]
    AGG_OP_MAX: _ClassVar[AggOp]
    AGG_OP_MIN: _ClassVar[AggOp]
    AGG_OP_SUM: _ClassVar[AggOp]
    AGG_OP_COUNT: _ClassVar[AggOp]
    AGG_OP_ASSET_COUNT: _ClassVar[AggOp]

class DType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    D_TYPE_UNSPECIFIED: _ClassVar[DType]
    D_TYPE_STRING: _ClassVar[DType]
    D_TYPE_FLOAT: _ClassVar[DType]
    D_TYPE_TIMESTAMP: _ClassVar[DType]
    D_TYPE_BOOLEAN: _ClassVar[DType]

class DataSourceKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_SOURCE_KIND_UNSPECIFIED: _ClassVar[DataSourceKind]
    DATA_SOURCE_KIND_ASSET: _ClassVar[DataSourceKind]
    DATA_SOURCE_KIND_EVENT: _ClassVar[DataSourceKind]
ORDER_DIRECTION_UNSPECIFIED: OrderDirection
ORDER_DIRECTION_ASC: OrderDirection
ORDER_DIRECTION_DESC: OrderDirection
BINARY_OP_UNSPECIFIED: BinaryOp
BINARY_OP_ADD: BinaryOp
BINARY_OP_AND: BinaryOp
BINARY_OP_DIV: BinaryOp
BINARY_OP_EQ: BinaryOp
BINARY_OP_GT: BinaryOp
BINARY_OP_GTE: BinaryOp
BINARY_OP_IN: BinaryOp
BINARY_OP_LT: BinaryOp
BINARY_OP_LTE: BinaryOp
BINARY_OP_MOD: BinaryOp
BINARY_OP_MUL: BinaryOp
BINARY_OP_NE: BinaryOp
BINARY_OP_OR: BinaryOp
BINARY_OP_SUB: BinaryOp
BINARY_OP_REGEXP: BinaryOp
UNARY_OP_UNSPECIFIED: UnaryOp
UNARY_OP_NOT: UnaryOp
UNARY_OP_NEG: UnaryOp
UNARY_OP_IS_NULL: UnaryOp
AGG_OP_UNSPECIFIED: AggOp
AGG_OP_AVG: AggOp
AGG_OP_MAX: AggOp
AGG_OP_MIN: AggOp
AGG_OP_SUM: AggOp
AGG_OP_COUNT: AggOp
AGG_OP_ASSET_COUNT: AggOp
D_TYPE_UNSPECIFIED: DType
D_TYPE_STRING: DType
D_TYPE_FLOAT: DType
D_TYPE_TIMESTAMP: DType
D_TYPE_BOOLEAN: DType
DATA_SOURCE_KIND_UNSPECIFIED: DataSourceKind
DATA_SOURCE_KIND_ASSET: DataSourceKind
DATA_SOURCE_KIND_EVENT: DataSourceKind

class QueryRequest(_message.Message):
    __slots__ = ("query", "daoql", "limit", "debug_options")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    DAOQL_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    DEBUG_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    query: Query
    daoql: str
    limit: int
    debug_options: QueryDebugOptions
    def __init__(self, query: _Optional[_Union[Query, _Mapping]] = ..., daoql: _Optional[str] = ..., limit: _Optional[int] = ..., debug_options: _Optional[_Union[QueryDebugOptions, _Mapping]] = ...) -> None: ...

class QueryDebugOptions(_message.Message):
    __slots__ = ("drop_asset_filter",)
    DROP_ASSET_FILTER_FIELD_NUMBER: _ClassVar[int]
    drop_asset_filter: bool
    def __init__(self, drop_asset_filter: bool = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("row", "debug_info")
    ROW_FIELD_NUMBER: _ClassVar[int]
    DEBUG_INFO_FIELD_NUMBER: _ClassVar[int]
    row: Row
    debug_info: QueryDebugInfo
    def __init__(self, row: _Optional[_Union[Row, _Mapping]] = ..., debug_info: _Optional[_Union[QueryDebugInfo, _Mapping]] = ...) -> None: ...

class QueryDebugInfo(_message.Message):
    __slots__ = ("query", "sql")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    SQL_FIELD_NUMBER: _ClassVar[int]
    query: Query
    sql: str
    def __init__(self, query: _Optional[_Union[Query, _Mapping]] = ..., sql: _Optional[str] = ...) -> None: ...

class Row(_message.Message):
    __slots__ = ("attributes",)
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AttributeValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AttributeValue, _Mapping]] = ...) -> None: ...
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.MessageMap[str, AttributeValue]
    def __init__(self, attributes: _Optional[_Mapping[str, AttributeValue]] = ...) -> None: ...

class AttributeValue(_message.Message):
    __slots__ = ("boolean_value", "string_value", "float_value", "timestamp_value")
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_VALUE_FIELD_NUMBER: _ClassVar[int]
    boolean_value: bool
    string_value: str
    float_value: float
    timestamp_value: _timestamp_pb2.Timestamp
    def __init__(self, boolean_value: bool = ..., string_value: _Optional[str] = ..., float_value: _Optional[float] = ..., timestamp_value: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Query(_message.Message):
    __slots__ = ("filter", "from_assets", "from_events", "columns", "aggregations", "group_by", "order_by", "drill")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    FROM_ASSETS_FIELD_NUMBER: _ClassVar[int]
    FROM_EVENTS_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    DRILL_FIELD_NUMBER: _ClassVar[int]
    filter: Node
    from_assets: QueryFromAssets
    from_events: QueryFromEvents
    columns: _containers.RepeatedCompositeFieldContainer[QueryColumn]
    aggregations: _containers.RepeatedCompositeFieldContainer[QueryAggregation]
    group_by: _containers.RepeatedCompositeFieldContainer[IdentifierNode]
    order_by: _containers.RepeatedCompositeFieldContainer[QueryOrderBy]
    drill: QueryDrill
    def __init__(self, filter: _Optional[_Union[Node, _Mapping]] = ..., from_assets: _Optional[_Union[QueryFromAssets, _Mapping]] = ..., from_events: _Optional[_Union[QueryFromEvents, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[QueryColumn, _Mapping]]] = ..., aggregations: _Optional[_Iterable[_Union[QueryAggregation, _Mapping]]] = ..., group_by: _Optional[_Iterable[_Union[IdentifierNode, _Mapping]]] = ..., order_by: _Optional[_Iterable[_Union[QueryOrderBy, _Mapping]]] = ..., drill: _Optional[_Union[QueryDrill, _Mapping]] = ...) -> None: ...

class QueryFromAssets(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryFromEvents(_message.Message):
    __slots__ = ("asset_filter",)
    ASSET_FILTER_FIELD_NUMBER: _ClassVar[int]
    asset_filter: Node
    def __init__(self, asset_filter: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class QueryColumn(_message.Message):
    __slots__ = ("name", "expr")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    name: str
    expr: Node
    def __init__(self, name: _Optional[str] = ..., expr: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class QueryAggregation(_message.Message):
    __slots__ = ("name", "expr", "op", "normalized")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    NORMALIZED_FIELD_NUMBER: _ClassVar[int]
    name: str
    expr: Node
    op: AggOp
    normalized: bool
    def __init__(self, name: _Optional[str] = ..., expr: _Optional[_Union[Node, _Mapping]] = ..., op: _Optional[_Union[AggOp, str]] = ..., normalized: bool = ...) -> None: ...

class QueryOrderBy(_message.Message):
    __slots__ = ("column", "direction")
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    column: IdentifierNode
    direction: OrderDirection
    def __init__(self, column: _Optional[_Union[IdentifierNode, _Mapping]] = ..., direction: _Optional[_Union[OrderDirection, str]] = ...) -> None: ...

class QueryDrill(_message.Message):
    __slots__ = ("columns", "max_depth", "exclude_columns")
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[IdentifierNode]
    max_depth: int
    exclude_columns: bool
    def __init__(self, columns: _Optional[_Iterable[_Union[IdentifierNode, _Mapping]]] = ..., max_depth: _Optional[int] = ..., exclude_columns: bool = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ("binary_op", "identifier", "literal", "unary_op", "window_agg")
    BINARY_OP_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    UNARY_OP_FIELD_NUMBER: _ClassVar[int]
    WINDOW_AGG_FIELD_NUMBER: _ClassVar[int]
    binary_op: BinaryOpNode
    identifier: IdentifierNode
    literal: LiteralNode
    unary_op: UnaryOpNode
    window_agg: WindowAggNode
    def __init__(self, binary_op: _Optional[_Union[BinaryOpNode, _Mapping]] = ..., identifier: _Optional[_Union[IdentifierNode, _Mapping]] = ..., literal: _Optional[_Union[LiteralNode, _Mapping]] = ..., unary_op: _Optional[_Union[UnaryOpNode, _Mapping]] = ..., window_agg: _Optional[_Union[WindowAggNode, _Mapping]] = ...) -> None: ...

class BinaryOpNode(_message.Message):
    __slots__ = ("op", "lhs", "rhs")
    OP_FIELD_NUMBER: _ClassVar[int]
    LHS_FIELD_NUMBER: _ClassVar[int]
    RHS_FIELD_NUMBER: _ClassVar[int]
    op: BinaryOp
    lhs: Node
    rhs: Node
    def __init__(self, op: _Optional[_Union[BinaryOp, str]] = ..., lhs: _Optional[_Union[Node, _Mapping]] = ..., rhs: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class IdentifierNode(_message.Message):
    __slots__ = ("identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, identifier: _Optional[_Iterable[str]] = ...) -> None: ...

class LiteralNode(_message.Message):
    __slots__ = ("string_value", "float_value", "boolean_value")
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_VALUE_FIELD_NUMBER: _ClassVar[int]
    string_value: str
    float_value: float
    boolean_value: bool
    def __init__(self, string_value: _Optional[str] = ..., float_value: _Optional[float] = ..., boolean_value: bool = ...) -> None: ...

class UnaryOpNode(_message.Message):
    __slots__ = ("op", "node")
    OP_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    op: UnaryOp
    node: Node
    def __init__(self, op: _Optional[_Union[UnaryOp, str]] = ..., node: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class WindowAggNode(_message.Message):
    __slots__ = ("query", "start", "end", "op", "agg_node")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    AGG_NODE_FIELD_NUMBER: _ClassVar[int]
    query: Node
    start: int
    end: int
    op: AggOp
    agg_node: Node
    def __init__(self, query: _Optional[_Union[Node, _Mapping]] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., op: _Optional[_Union[AggOp, str]] = ..., agg_node: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class AttributeSpec(_message.Message):
    __slots__ = ("name", "dtype")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    dtype: DType
    def __init__(self, name: _Optional[str] = ..., dtype: _Optional[_Union[DType, str]] = ...) -> None: ...

class Connection(_message.Message):
    __slots__ = ("name", "dsn")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DSN_FIELD_NUMBER: _ClassVar[int]
    name: str
    dsn: str
    def __init__(self, name: _Optional[str] = ..., dsn: _Optional[str] = ...) -> None: ...

class CreateConnectionRequest(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: Connection
    def __init__(self, connection: _Optional[_Union[Connection, _Mapping]] = ...) -> None: ...

class CreateConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListConnectionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListConnectionsResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[Connection]
    def __init__(self, connections: _Optional[_Iterable[_Union[Connection, _Mapping]]] = ...) -> None: ...

class DeleteConnectionRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteConnectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteQueryEngineRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteQueryEngineResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteDataSourceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteDataSourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryEngine(_message.Message):
    __slots__ = ("name", "connection")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    connection: str
    def __init__(self, name: _Optional[str] = ..., connection: _Optional[str] = ...) -> None: ...

class CreateQueryEngineRequest(_message.Message):
    __slots__ = ("query_engine",)
    QUERY_ENGINE_FIELD_NUMBER: _ClassVar[int]
    query_engine: QueryEngine
    def __init__(self, query_engine: _Optional[_Union[QueryEngine, _Mapping]] = ...) -> None: ...

class CreateQueryEngineResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetDefaultQueryEngineRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SetDefaultQueryEngineResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListQueryEnginesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListQueryEnginesResponse(_message.Message):
    __slots__ = ("query_engines",)
    QUERY_ENGINES_FIELD_NUMBER: _ClassVar[int]
    query_engines: _containers.RepeatedCompositeFieldContainer[QueryEngine]
    def __init__(self, query_engines: _Optional[_Iterable[_Union[QueryEngine, _Mapping]]] = ...) -> None: ...

class DataSourceConnectionDetails(_message.Message):
    __slots__ = ("connection", "database", "table", "schema")
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    connection: str
    database: str
    table: str
    schema: str
    def __init__(self, connection: _Optional[str] = ..., database: _Optional[str] = ..., table: _Optional[str] = ..., schema: _Optional[str] = ...) -> None: ...

class AttributeMapping(_message.Message):
    __slots__ = ("asset_name", "event_timestamp")
    ASSET_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    asset_name: str
    event_timestamp: str
    def __init__(self, asset_name: _Optional[str] = ..., event_timestamp: _Optional[str] = ...) -> None: ...

class DataSource(_message.Message):
    __slots__ = ("name", "kind", "connection_details", "attributes", "attribute_mapping")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: DataSourceKind
    connection_details: DataSourceConnectionDetails
    attributes: _containers.RepeatedCompositeFieldContainer[AttributeSpec]
    attribute_mapping: AttributeMapping
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[_Union[DataSourceKind, str]] = ..., connection_details: _Optional[_Union[DataSourceConnectionDetails, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[AttributeSpec, _Mapping]]] = ..., attribute_mapping: _Optional[_Union[AttributeMapping, _Mapping]] = ...) -> None: ...

class CreateDataSourceRequest(_message.Message):
    __slots__ = ("datasource",)
    DATASOURCE_FIELD_NUMBER: _ClassVar[int]
    datasource: DataSource
    def __init__(self, datasource: _Optional[_Union[DataSource, _Mapping]] = ...) -> None: ...

class CreateDataSourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDataSourcesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDataSourcesResponse(_message.Message):
    __slots__ = ("datasources",)
    DATASOURCES_FIELD_NUMBER: _ClassVar[int]
    datasources: _containers.RepeatedCompositeFieldContainer[DataSource]
    def __init__(self, datasources: _Optional[_Iterable[_Union[DataSource, _Mapping]]] = ...) -> None: ...

class CreateOrganizationRequest(_message.Message):
    __slots__ = ("org_id", "display_name")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    display_name: str
    def __init__(self, org_id: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class CreateOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class GetOrganizationRequest(_message.Message):
    __slots__ = ("org_id",)
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    def __init__(self, org_id: _Optional[str] = ...) -> None: ...

class GetOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class ListOrganizationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOrganizationsResponse(_message.Message):
    __slots__ = ("organizations",)
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    organizations: _containers.RepeatedCompositeFieldContainer[Organization]
    def __init__(self, organizations: _Optional[_Iterable[_Union[Organization, _Mapping]]] = ...) -> None: ...

class Organization(_message.Message):
    __slots__ = ("org_id", "display_name")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    display_name: str
    def __init__(self, org_id: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...
