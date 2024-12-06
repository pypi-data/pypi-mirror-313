
from viaduct.dao.v1 import dao_pb2, dao_pb2_grpc

import logging

def load_examples(client: dao_pb2_grpc.DaoServiceStub) -> None:
    """Load example datasets into DAO."""
    
    # Create connection to ClickHouse
    client.CreateConnection(dao_pb2.CreateConnectionRequest(
        connection=dao_pb2.Connection(
            name="examples",
            dsn="clickhouse://default@localhost:9000/examples"
        )
    ))

    # Create and set default query engine
    client.CreateQueryEngine(dao_pb2.CreateQueryEngineRequest(
        query_engine=dao_pb2.QueryEngine(
            name="examples_engine",
            connection="examples"
        )
    ))
    client.SetDefaultQueryEngine(dao_pb2.SetDefaultQueryEngineRequest(
        name="examples_engine"
    ))

    # Create vehicle asset data source
    client.CreateDataSource(dao_pb2.CreateDataSourceRequest(
        datasource=dao_pb2.DataSource(
            name="vehicles",
            kind=dao_pb2.DataSourceKind.DATA_SOURCE_KIND_ASSET,
            connection_details=dao_pb2.DataSourceConnectionDetails(
                connection="examples",
                database="examples",
                schema="",
                table="vehicles"
            ),
            attributes=[
                dao_pb2.AttributeSpec(name="dealer_code", dtype=dao_pb2.DType.D_TYPE_STRING),
                dao_pb2.AttributeSpec(name="model", dtype=dao_pb2.DType.D_TYPE_STRING),
                dao_pb2.AttributeSpec(name="manufacture_date", dtype=dao_pb2.DType.D_TYPE_TIMESTAMP),
            ],
            attribute_mapping=dao_pb2.AttributeMapping(
                asset_name="vin"
            )
        )
    ))

    # Create claims event data source
    client.CreateDataSource(dao_pb2.CreateDataSourceRequest(
        datasource=dao_pb2.DataSource(
            name="claims",
            kind=dao_pb2.DataSourceKind.DATA_SOURCE_KIND_EVENT,
            connection_details=dao_pb2.DataSourceConnectionDetails(
                connection="examples",
                database="examples",
                schema="",
                table="claims"
            ),
            attributes=[
                dao_pb2.AttributeSpec(name="repair_description", dtype=dao_pb2.DType.D_TYPE_STRING),
                dao_pb2.AttributeSpec(name="total_amount", dtype=dao_pb2.DType.D_TYPE_FLOAT),
                dao_pb2.AttributeSpec(name="failure_location", dtype=dao_pb2.DType.D_TYPE_STRING),
            ],
            attribute_mapping=dao_pb2.AttributeMapping(
                asset_name="vin",
                event_timestamp="claim_date"
            )
        )
    ))

    # Create faults event data source
    client.CreateDataSource(dao_pb2.CreateDataSourceRequest(
        datasource=dao_pb2.DataSource(
            name="faults",
            kind=dao_pb2.DataSourceKind.DATA_SOURCE_KIND_EVENT,
            connection_details=dao_pb2.DataSourceConnectionDetails(
                connection="examples",
                database="examples",
                schema="",
                table="faults"
            ),
            attributes=[
                dao_pb2.AttributeSpec(name="fault_code", dtype=dao_pb2.DType.D_TYPE_STRING),
                dao_pb2.AttributeSpec(name="description", dtype=dao_pb2.DType.D_TYPE_STRING),
                dao_pb2.AttributeSpec(name="severity", dtype=dao_pb2.DType.D_TYPE_STRING),
            ],
            attribute_mapping=dao_pb2.AttributeMapping(
                asset_name="vin",
                event_timestamp="fault_date"
            )
        )
    ))